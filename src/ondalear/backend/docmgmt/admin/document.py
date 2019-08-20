"""
.. module::  ondalear.backend.docmgmt.admin.document
   :synopsis: document management document  admin module.

This module contains document admin abstractions.

"""
import logging
from django.contrib import admin

from ondalear.backend.core.django.admin import base_model_readonly_fields, AbstractModelAdmin
from ondalear.backend.docmgmt.admin.base import register
from ondalear.backend.docmgmt.models import  (constants,
                                              Document,
                                              DocumentAnnotation,
                                              DocumentAssociation,
                                              DocumentTag)

_logger = logging.getLogger(__name__)

# pylint: disable=no-member

class AbstractTabularInline(admin.TabularInline):
    """Base tabular inline class"""
    exclude = base_model_readonly_fields + ('is_enabled', 'is_deleted', 'client')


class DocumentTagInline(AbstractTabularInline):
    """Document tag inline class"""
    model = DocumentTag
    extra = 2 # how many rows to show
    verbose_name = 'Document Tag'
    verbose_name_plural = 'Document Tags'

class DocumentAnnotationgInline(AbstractTabularInline):
    """Document annotation inline class"""
    model = DocumentAnnotation
    extra = 2 # how many rows to show
    verbose_name = 'Document Annotation'
    verbose_name_plural = 'Document Annotations'

class DocumentAssociationInline(AbstractTabularInline):
    """Document association inline class"""
    model = DocumentAssociation
    extra = 2 # how many rows to show
    verbose_name = 'Document Association'
    verbose_name_plural = 'Document Associations'
    fk_name = 'from_document'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """handle foreign key"""
        if db_field.name == 'to_document':
            kwargs['queryset'] = Document.objects.exclude(
                document_type=constants.DOCUMENT_TYPE_REFERENCE)
            try:
                object_id = request.resolver_match.kwargs['object_id']
                try:
                    document = Document.objects.get(pk=object_id)
                    if document.document_type != constants.DOCUMENT_TYPE_REFERENCE:
                        # not allowing other document references.
                        excluded = (constants.DOCUMENT_TYPE_REFERENCE,
                                    constants.DOCUMENT_TYPE_AUXILIARY)
                        kwargs['queryset'] = Document.objects.exclude(document_type__in=excluded)
                except Document.DoesNotExist:
                    pass
            except KeyError:
                pass
        ret = super().formfield_for_foreignkey(db_field, request, **kwargs)
        return ret

_document_tag_fields = ('document', 'tag')

class DocumentTagAdmin(AbstractModelAdmin):
    """Document tag association admin class"""
    list_display = AbstractModelAdmin.list_display + ('document', 'tag')
    model_class = DocumentTag
    fieldsets = (
        ('Document tag',
         {'fields': _document_tag_fields}),
    ) + AbstractModelAdmin.field_sets()


_document_annotation_fields = ('document', 'annotation')

class DocumentAnnotationAdmin(AbstractModelAdmin):
    """Document annotation association admin class"""
    list_display = AbstractModelAdmin.list_display + ('document', 'annotation')
    model_class = DocumentTag
    fieldsets = (
        ('Document annotation',
         {'fields': _document_annotation_fields}),
    ) + AbstractModelAdmin.field_sets()


_document_association_fields = ('from_document', 'to_document', 'purpose')

class DocumentAssociationAdmin(AbstractModelAdmin):
    """Document  association admin class"""
    list_display = AbstractModelAdmin.list_display + ('from_document', 'to_document', 'purpose')
    model_class = DocumentAssociation
    fieldsets = (
        ('Document association', {'fields': _document_association_fields}),
    ) + AbstractModelAdmin.field_sets()

_document_fields = ('client', 'name', 'language',
                    'mime_type', 'document_type', 'category',
                    'title', 'description')

class DocumentAdmin(AbstractModelAdmin):
    """Base document admin class"""
    list_display = AbstractModelAdmin.list_display + ('name', 'document_type')
    inlines = (DocumentTagInline, DocumentAnnotationgInline, DocumentAssociationInline)
    fieldsets = (
        ('Document',
         {'fields': _document_fields}),
    ) + AbstractModelAdmin.field_sets()

    def parent(self):
        """
        Returns the parent object from the request or None.
        """
        if hasattr(self, '_instance'):
            return self._instance
        return None

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        super(DocumentAdmin, self).save_model(request, obj, form, change)
        # @TODO: explore avoiding this capture of the instance and follow the foreign key link
        self._instance = obj        # pylint: disable=attribute-defined-outside-init

    def save_formset(self, request, form, formset, change):
        """save the underlying inlines"""
        parent = self.parent()
        instances = formset.save(commit=False)
        for instance in instances:
            self.prepare_system_fields(request, instance, instance, change=None)
            instance.client = parent.client
            instance.save()
        super(DocumentAdmin, self).save_formset(request, form, formset, change)

# Register the models and admin classes
model_classes = (Document,
                 DocumentAssociation,
                 DocumentAnnotation,
                 DocumentTag)
admin_classes = (DocumentAdmin,
                 DocumentAssociationAdmin,
                 DocumentAnnotationAdmin,
                 DocumentTagAdmin)

register(model_classes, admin_classes)
