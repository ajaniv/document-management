"""
.. module:: ondalear.backend.document.models.documents
   :synopsis: ondalear backend  models documents  module.

The *documents* module contains *Document* model abstractions.

"""
import logging
from inflection import humanize, pluralize, underscore
import ftfy
import magic

from django.conf import settings
from django.dispatch import receiver
from django.db.models import CASCADE, SET_NULL, signals
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Model

from ondalear.backend.core.python.utils import file_exists, remove
from ondalear.backend.core.django import fields
from ondalear.backend.core.django.storage import overwrite_storage, client_directory_path
from ondalear.backend.core.django.models import db_table

from ondalear.backend.docmgmt.models import constants
from ondalear.backend.docmgmt.models.base import AbstractDocumentManagementModel, app_label
from ondalear.backend.docmgmt.models.annotation import Annotation
from ondalear.backend.docmgmt.models.client import Client
from ondalear.backend.docmgmt.models.classification import Category, Tag

_logger = logging.getLogger(__name__)

class AbstractDocumentModel(AbstractDocumentManagementModel):
    """Base document model class
    """
    name = fields.char_field(blank=False, null=False, max_length=constants.NAME_FIELD_MAX_LENGTH)
    language = fields.char_field(blank=False, null=False, default=settings.LANGUAGE_CODE)
    # deletion of client will result in deletion of its associated documents
    client = fields.foreign_key_field(Client, on_delete=CASCADE)
    mime_type = fields.char_field(
        blank=False, null=False, default=constants.MIME_TYPE_UNKNOWN,
        choices=constants.MIME_TYPE_CHOICES)
    document_type = fields.char_field(
        blank=False, null=False, default=constants.DOCUMENT_TYPE_REFERENCE,
        choices=constants.DOCUMENT_TYPE_CHOICES)

    title = fields.char_field(blank=True, null=True, max_length=constants.TITLE_FIELD_MAX_LENGTH)
    description = fields.description_field(blank=True, null=True,
                                           max_length=constants.DESCRIPTION_FIELD_MAX_LENGTH)

    category = fields.foreign_key_field(Category, blank=True, null=True, on_delete=SET_NULL)
    tags = fields.many_to_many_field(
        Tag, related_name='documents',
        through='DocumentTag', through_fields=('document', 'tag'))

    annotations = fields.many_to_many_field(
        Annotation, related_name='documents',
        through='DocumentAnnotation', through_fields=('document', 'annotation'))

    #@ TODO: this is not a symetrical relationship -> it is unidirectional using from_document
    documents = fields.many_to_many_field(
        'self', symmetrical=False, related_name='related_documents',
        through='DocumentAssociation', through_fields=('from_document', 'to_document'))

    class Meta(AbstractDocumentManagementModel.Meta):
        """Meta class definition"""
        abstract = True
        unique_together = ('client', 'name')

    def __str__(self):
        """pretty format instance as string"""
        return self.name


_document = "Document"
_document_verbose = humanize(underscore(_document))

class Document(AbstractDocumentModel):
    """ Document model class
    """
    class Meta(AbstractDocumentModel.Meta):
        """Meta class definition"""
        db_table = db_table(app_label, _document)
        verbose_name = _(_document_verbose)
        verbose_name_plural = _(pluralize(_document_verbose))


class AbstractDerivedDocumentModel(Model):
    """Derived document model base class"""
    document = fields.one_to_one_field(to_class=Document, primary_key=True, on_delete=CASCADE)
    # table specific content for table space future optimization
    content = fields.text_field(blank=True, null=True,
                                max_length=constants.CONTENT_FIELD_MAX_LENGTH)
    # designates system managed files uploaded by end user or on his behalf
    upload = fields.constrained_file_field(blank=True, null=True,
                                           upload_to=client_directory_path,
                                           storage=overwrite_storage,
                                           content_types=constants.MIME_TYPES,
                                           max_upload_size=constants.UPLOAD_FIELD_MAX_FILE_SIZE)
    # server mounted file system path
    dir_path = fields.char_field(blank=True, null=True,
                                 max_length=constants.DIR_PATH_FIELD_MAX_LENGTH)
    class Meta:
        """Meta class definition"""
        app_label = app_label
        abstract = True

    def __str__(self):
        """pretty format instance as string"""
        return self.document.name

    @classmethod
    def my_document_type(cls):
        """return document type"""
        return constants.DOCUMENT_TYPE_UNKNOWN

    def clean(self):
        """model wide validation

        """
        # pylint: disable=no-member,broad-except
        # valdiate that upload, content, dir_path are not  empty
        if not (self.content or self.upload or self.dir_path):
            raise ValidationError(_('Must set "content" or "upload" fields.'))

        # valdiate that upload and content are not both set
        if self.content and self.upload:
            raise ValidationError(_('Can not set both "content" and "upload" fields.'))

        if self.upload:
            self.mime_type = self.upload.field.content_type   # pylint: disable=attribute-defined-outside-init,no-member

        if self.content:
            content = self.content
            try:
                mime_type = magic.from_buffer(content, mime=True)
            except Exception:
                _logger.exception('failed to fetch mime_type for id: %s name: %s',
                                  self.document.id, self.document.name)
                raise ValidationError(_(f'Undetected mime type.'))

            if mime_type not in constants.MIME_TYPES:
                raise ValidationError(_(f'Invalid mime type {mime_type}.'))
            try:
                content = ftfy.fix_text(self.content)
            except Exception:
                _logger.exception('failed to fix text for id: %s name: %s',
                                  self.document.id, self.document.name)
            self.content = content
            self.document.mime_type = mime_type

        if not self.document.mime_type:
            # mime type was not discovered on content or file upload data
            self.document.mime_type = constants.MIME_TYPE_UNKNOWN

        super(AbstractDerivedDocumentModel, self).clean()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """save the instance

        Overriding to ensure instance validity across multiple fields.
        Requires implementation due to different model inheritance
        """
        self.full_clean()

        # @TODO: saving again the underlying model as mime_type has changed,
        #    review the approach

        self.document.save()        # pylint: disable=no-member
        return super(AbstractDerivedDocumentModel, self).save(force_insert, force_update,
                                                              using, update_fields)

    def get_file_contents(self):
        """get file contents if file has been uploaded"""
        # @TODO: not handling file contents if file has not been uploaded
        #   (i.e. dir_path is set and upload is not set)
        data = None
        if self.upload:
            # pylint: disable=no-member
            try:
                with open(self.upload.path) as input_file:
                    data = input_file.read()
            except IOError as ex:
                _logger.error('invalid file %s exc %s', self.upload.path, ex)
        return data

    def get_text(self):
        """get text data"""
        if self.content:
            return self.content
        return self.get_file_contents()

_auxiliary_document = "AuxiliaryDocument"
_auxiliary_document_verbose = humanize(underscore(_auxiliary_document))

class AuxiliaryDocument(AbstractDerivedDocumentModel):
    """AuxiliaryDocument class definition

    An auxiliary document contains any additional information to be associated
    with a reference document during analysis.
    """

    class Meta(AbstractDerivedDocumentModel.Meta):
        """Meta class definition"""
        db_table = db_table(app_label, _auxiliary_document)
        verbose_name = _(_auxiliary_document_verbose)
        verbose_name_plural = _(pluralize(_auxiliary_document_verbose))

    @classmethod
    def my_document_type(cls):
        """return document type"""
        return constants.DOCUMENT_TYPE_AUXILIARY


_reference_document = "ReferenceDocument"
_reference_document_verbose = humanize(underscore(_reference_document))

class ReferenceDocument(AbstractDerivedDocumentModel):
    """ReferenceDocument class definition.

    This is an abstraction of the financial contract, event data, and
    other documents that are used as the input for analysis.
    """


    class Meta(AbstractDerivedDocumentModel.Meta):
        """Meta class definition"""
        db_table = db_table(app_label, _reference_document)
        verbose_name = _(_reference_document_verbose)
        verbose_name_plural = _(pluralize(_reference_document_verbose))

    @classmethod
    def my_document_type(cls):
        """return document type"""
        return constants.DOCUMENT_TYPE_REFERENCE


def _delete_file(file_path):
    """ Deletes file from filesystem. """
    if file_exists(file_path):
        remove(file_path)

@receiver(signals.post_delete, sender=ReferenceDocument)
@receiver(signals.post_delete, sender=AuxiliaryDocument)
def delete_file(sender, instance, *args, **kwargs):  # pylint: disable=unused-argument
    """ Deletes  files on `post_delete` """
    if instance.upload:
        _delete_file(instance.upload.path)
