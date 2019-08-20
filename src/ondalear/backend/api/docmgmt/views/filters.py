"""
.. module::  ondalear.backend.api.docmgmt.views.filters
   :synopsis:  docmgmt views filters module.

"""
import logging
import rest_framework_filters as filters
from ondalear.backend.docmgmt.models import (AuxiliaryDocument,
                                             Category,
                                             Document,
                                             ReferenceDocument,
                                             DocumentTag)

_logger = logging.getLogger(__name__)

class DocumentTagFilter(filters.FilterSet):
    """Document tag filter class"""
    class Meta:
        """Meta class"""
        model = DocumentTag
        fields = {
            'tag': ['exact', 'in'],
        }

# @TODO: use a filter for document tag queries -- did not get it to work
class CategoryFilter(filters.FilterSet):
    """Category filter class"""
    class Meta:
        """Meta class"""
        model = Category
        fields = {
            'name': ['exact', 'in', 'startswith']
        }

class DocumentFilter(filters.FilterSet):
    """Document filter class"""
    category = filters.RelatedFilter(
        CategoryFilter,
        field_name='category', queryset=Category.objects.all())

    class Meta:
        """Meta class"""
        model = Document
        fields = {
            'name': ['exact', 'in', 'startswith'],
            'update_time': ['exact', 'lte', 'gte'],
            'document_type': ['exact'],
            'category__name': ['exact', 'in']
        }

class DerivedDocumentFilter(filters.FilterSet):
    """Derived document filter class"""
    document = filters.RelatedFilter(
        DocumentFilter,
        field_name='document', queryset=Document.objects.all())

    class Meta:
        """Meta class"""
        fields = {}

class AuxiliaryDocumentFilter(DerivedDocumentFilter):
    """Auxiliary document filter class"""
    class Meta(DerivedDocumentFilter.Meta):
        """Meta class"""
        model = AuxiliaryDocument
        fields = {}

class ReferenceDocumentFilter(DerivedDocumentFilter):
    """Reference document filter class"""
    class Meta(DerivedDocumentFilter.Meta):
        """Meta class"""
        model = ReferenceDocument
