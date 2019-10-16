"""
.. module::  ondalear.backend.docmgmt.admin.annotation
   :synopsis: document management annotation admin module.

This module contains annotation admin abstractions.

"""
import logging

from ondalear.backend.core.django.admin import register, AbstractModelAdmin
from ondalear.backend.docmgmt.models import  Annotation

_logger = logging.getLogger(__name__)



_annotation_fields = ('client', 'name', 'annotation')

class AnnotationAdmin(AbstractModelAdmin):
    """Annotation model admin class.
    """
    list_display = AbstractModelAdmin.list_display + ('client_id', 'name')
    fieldsets = (
        ('Annotation',
         {'fields': _annotation_fields}),
    ) + AbstractModelAdmin.field_sets()     # pylint: disable=no-member


# Register the models and admin classes
model_classes = (Annotation,)
admin_classes = (AnnotationAdmin,)

register(model_classes, admin_classes)
