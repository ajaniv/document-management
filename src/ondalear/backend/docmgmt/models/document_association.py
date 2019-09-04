"""
.. module:: ondalear.backend.docmgmt.models.document_association
   :synopsis: document association module.

The *document association* module contains *Document association* model abstractions.

"""
import logging
from inflection import humanize, pluralize, underscore
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _

from ondalear.backend.core.django.models import db_table
from ondalear.backend.core.django import fields
from ondalear.backend.docmgmt.models import constants
from ondalear.backend.docmgmt.models.client import Client
from ondalear.backend.docmgmt.models.document import Document
from ondalear.backend.docmgmt.models.base import app_label, AbstractDocumentManagementModel

_logger = logging.getLogger(__name__)


_document_association = "DocumentAssociation"
_document_association_verbose = humanize(underscore(_document_association))

class DocumentAssociation(AbstractDocumentManagementModel):
    """Document  association model class.

    A document  may be associated with 0 or more other documents
    Document(1)  -------> Document(0..*)
    """
    from_document = fields.foreign_key_field(Document,
                                             related_name='from_document',
                                             on_delete=CASCADE)
    to_document = fields.foreign_key_field(Document, related_name='to_document', on_delete=CASCADE)
    client = fields.foreign_key_field(Client, on_delete=CASCADE)

    # relationship purpose
    purpose = fields.char_field(
        blank=False, null=False, default=constants.DOCUMENT_ASSOCIATION_PURPOSE_UNKNOWN,
        choices=constants.DOCUMENT_ASSOCIATION_PURPOSE_CHOICES)

    class Meta(AbstractDocumentManagementModel.Meta):
        """Model meta class definition"""
        db_table = db_table(app_label, _document_association)
        verbose_name = _(_document_association_verbose)
        verbose_name_plural = _(pluralize(_document_association_verbose))
        unique_together = ('from_document', 'to_document', 'purpose')

    def __str__(self):
        """pretty format instance as string"""
        return '({},{},{})'.format(str(self.from_document), str(self.to_document), self.purpose)
