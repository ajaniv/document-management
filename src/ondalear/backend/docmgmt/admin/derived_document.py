"""
.. module::  ondalear.backend.docmgmt.admin.derived_document
   :synopsis: document management derived document admin module.

This module contains derived document admin abstractions.

"""
import logging
from django.contrib import admin

from ondalear.backend.docmgmt.admin.base import register
from ondalear.backend.docmgmt.models import  AuxiliaryDocument, Document, ReferenceDocument

_logger = logging.getLogger(__name__)

# pylint: disable=no-self-use
_derived_fields = ('document', 'content', 'upload', 'dir_path')

class AbstractDerivedDocumentAdmin(admin.ModelAdmin):
    """Base derived document admin class"""
    model_class = None
    list_display = ('doc_id',
                    'doc_update_time', 'doc_update_user',
                    'doc_name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """handle foreign key"""
        my_type = self.model_class.my_document_type()
        if db_field.name == 'document':
            kwargs["queryset"] = Document.objects.filter(document_type=my_type)
        ret = super().formfield_for_foreignkey(db_field, request, **kwargs)
        return ret

    def doc_id(self, obj):
        """display document id """
        return str(obj.document.id)

    def doc_update_time(self, obj):
        """display document update """
        return str(obj.document.update_time)

    def doc_update_user(self, obj):
        """display document change_time """
        return str(obj.document.update_user)

    def doc_name(self, obj):
        """display document name """
        return str(obj.document.name)


class AuxiliaryDocumentAdmin(AbstractDerivedDocumentAdmin):
    """Auxiliary document admin class"""
    model_class = AuxiliaryDocument
    fieldsets = (
        ('Auxiliary document',
         {'fields': _derived_fields}),
    )

class ReferenceDocumentAdmin(AbstractDerivedDocumentAdmin):
    """Reference document admin class"""
    model_class = ReferenceDocument
    fieldsets = (
        ('Reference document',
         {'fields': _derived_fields}),
    )

# Register the models and admin classes
model_classes = (AuxiliaryDocument, ReferenceDocument)
admin_classes = (AuxiliaryDocumentAdmin, ReferenceDocumentAdmin)

register(model_classes, admin_classes)
