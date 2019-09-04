"""
.. module:: ondalear.backend.docmgmt.models.document_tab
   :synopsis: document  tag module.

The *document tag* module contains *Document tag* model abstractions.

"""
import logging
from inflection import humanize, pluralize, underscore

from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _

from ondalear.backend.core.django.models import db_table
from ondalear.backend.core.django import fields
from ondalear.backend.docmgmt.models.client import Client
from ondalear.backend.docmgmt.models.document import Document
from ondalear.backend.docmgmt.models.classification import Tag
from ondalear.backend.docmgmt.models.base import AbstractDocumentManagementModel, app_label

_logger = logging.getLogger(__name__)


_document_tag = "DocumentTag"
_document_tag_verbose = humanize(underscore(_document_tag))

class DocumentTag(AbstractDocumentManagementModel):
    """Document tag association model class.

    A document  may be associated with 0 or more tags:
    Document(1)  -------> Tag(0..*)
    """
    document = fields.foreign_key_field(Document, on_delete=CASCADE)
    tag = fields.foreign_key_field(Tag, on_delete=CASCADE)
    client = fields.foreign_key_field(Client, on_delete=CASCADE)

    class Meta(AbstractDocumentManagementModel.Meta):
        """Model meta class definition"""
        db_table = db_table(app_label, _document_tag)
        verbose_name = _(_document_tag_verbose)
        verbose_name_plural = _(pluralize(_document_tag_verbose))
        unique_together = ('document', 'tag')

    def __str__(self):
        """pretty format instance as string"""
        return '({},{})'.format(str(self.document), str(self.tag))
