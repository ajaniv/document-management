"""
.. module::  ondalear.backend.docmgmt.admin.classification
   :synopsis: document management classification admin module.

This module contains classification admin abstractions.

"""
import logging

from ondalear.backend.core.django.admin import AbstractModelAdmin
from ondalear.backend.docmgmt.admin.base import register
from ondalear.backend.docmgmt.models import  Tag, Category

_logger = logging.getLogger(__name__)


class AbstractClassificationAdmin(AbstractModelAdmin):
    """Base classification admin class"""
    model_class = None
    list_display = AbstractModelAdmin.list_display + ('name', 'display_hierarchy')

    def display_hierarchy(self, obj):   # pylint: disable=no-self-use
        """display inheritance hierarchy"""
        return str(obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """handle foreign key"""
        if db_field.name == 'parent':
            try:
                object_id = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = self.model_class.objects.exclude(pk=object_id)
            except KeyError:
                kwargs['queryset'] = self.model_class.objects.all()
        ret = super().formfield_for_foreignkey(db_field, request, **kwargs)
        return ret

_classification_fields = ('client', 'name', 'target', 'domain', 'parent', 'description')

class TagAdmin(AbstractClassificationAdmin):
    """Tag admin class"""
    model_class = Tag
    fieldsets = (
        ('Tag',
         {'fields': _classification_fields}),
    ) + AbstractModelAdmin.field_sets()     # pylint: disable=no-member



class CategoryAdmin(AbstractClassificationAdmin):
    """Category document tag admin class"""
    model_class = Category
    fieldsets = (
        ('Category',
         {'fields': _classification_fields}),
    ) + AbstractModelAdmin.field_sets()     # pylint: disable=no-member

# Register the models and admin classes.
model_classes = (Category,
                 Tag)
admin_classes = (CategoryAdmin,
                 TagAdmin)

register(model_classes, admin_classes)
