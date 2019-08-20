"""
.. module:: ondalear.backend.docmgmt.models.annotation
   :synopsis: ondalear backend  models annotation  module.

The *annotation* module contains *Annotation* model abstractions.

"""
import logging
from inflection import humanize, pluralize, underscore

from django.utils.translation import ugettext_lazy as _
from django.db.models import CASCADE

from ondalear.backend.core.django import fields
from ondalear.backend.core.django.models import db_table

from ondalear.backend.docmgmt.models import constants
from ondalear.backend.docmgmt.models.base import app_label, AbstractDocumentManagementModel
from ondalear.backend.docmgmt.models.client import Client

_logger = logging.getLogger(__name__)

_annotation = 'Annotation'
_annotation_verbose = humanize(underscore(_annotation))

class Annotation(AbstractDocumentManagementModel):
    """Annotation class definition
    Allows to annotate another model instance.
    """
    name = fields.char_field(blank=False, null=False, max_length=constants.NAME_FIELD_MAX_LENGTH)
    annotation = fields.annotation_field(blank=False, null=False,
                                         max_length=constants.ANNOTATION_FIELD_MAX_LENGTH)
    # deletion of client will result in deletion of associated annotations
    client = fields.foreign_key_field(Client, on_delete=CASCADE)

    class Meta(AbstractDocumentManagementModel.Meta):
        """Meta class definition"""
        abstract = False
        db_table = db_table(app_label, _annotation)
        verbose_name = _(_annotation_verbose)
        verbose_name_plural = _(pluralize(_annotation_verbose))
        unique_together = ('client', 'name')

    def __str__(self):
        """generate pretty string representation"""
        return self.name
