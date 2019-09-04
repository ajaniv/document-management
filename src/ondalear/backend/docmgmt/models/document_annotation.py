"""
.. module:: ondalear.backend.docmgmt.models.document_annotation
   :synopsis: document annotation module.

The *document annotation* module contains *Document annotation* model abstractions.

"""
import logging
from inflection import humanize, pluralize, underscore
from django.utils.translation import ugettext_lazy as _
from django.db.models import CASCADE

from ondalear.backend.core.django.models import db_table
from ondalear.backend.core.django import fields
from ondalear.backend.docmgmt.models.annotation import Annotation
from ondalear.backend.docmgmt.models.client import Client
from ondalear.backend.docmgmt.models.document import Document
from ondalear.backend.docmgmt.models.base import app_label, AbstractDocumentManagementModel

_logger = logging.getLogger(__name__)


_document_annotation = "DocumentAnnotation"
_document_annotation_verbose = humanize(underscore(_document_annotation))

class DocumentAnnotation(AbstractDocumentManagementModel):
    """Document annotation association model class.

    A document  may be associated with 0 or more annotations:
    Document(1)  -------> Annotation(0..*)
    """
    document = fields.foreign_key_field(Document, on_delete=CASCADE)
    annotation = fields.foreign_key_field(Annotation, on_delete=CASCADE)
    client = fields.foreign_key_field(Client, on_delete=CASCADE)

    class Meta(AbstractDocumentManagementModel.Meta):
        """Model meta class definition"""
        db_table = db_table(app_label, _document_annotation)
        verbose_name = _(_document_annotation_verbose)
        verbose_name_plural = _(pluralize(_document_annotation_verbose))
        unique_together = ('document', 'annotation')

    def __str__(self):
        """pretty format instance as string"""
        return '({},{})'.format(str(self.document), str(self.annotation))
