"""
.. module::  ondalaer.backend.api.docmgmt.views.document
   :synopsis:  ondalear backend docmgmt document view module.

"""
import logging

from rest_framework import viewsets

from ondalear.backend.docmgmt.models import Document
from ondalear.backend.api.base_views import (DRFMixin,
                                             DRFListModelMixin,
                                             AbstractModelViewSet,
                                             PermissionsMixin)
from ondalear.backend.api.docmgmt.serializers import DocumentSerializer
from ondalear.backend.api.docmgmt.views.queries import (AuxiliaryDocumentSummaryQueryMixin,
                                                        DocumentQueryMixin,
                                                        ReferenceDocumentSummaryQueryMixin)

_logger = logging.getLogger(__name__)

# pylint: disable=too-many-ancestors,attribute-defined-outside-init,no-member

class DocumentViewSet(DocumentQueryMixin, AbstractModelViewSet):
    """Document view set"""

summary_response_fields = (
    'category', 'creation_time', 'creation_user', 'is_deleted', 'is_enabled',
    'effective_user', 'id', 'site', 'update_user', 'update_time',
    'uuid', 'version', 'client', 'description', 'name', 'title'
    )

class AbstractDocumentSummaryViewset(
        DRFMixin,
        PermissionsMixin,
        DRFListModelMixin,
        viewsets.GenericViewSet):
    """
    Base document summary  view set class.
    Only supports list action and returns a limited set of attributes
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    query_fields = summary_response_fields

    def get_queryset(self):  # pylint: disable=arguments-differ
        """
        This view should return a list of all the documents
        for the currently authenticated user.
        """
        qs = super(AbstractDocumentSummaryViewset, self).get_queryset()
        return qs.only(*self.query_fields)

# @TODO: consider using document_type filter instead of custom summary end points
class AuxiliaryDocumentSummaryViewset(
        AuxiliaryDocumentSummaryQueryMixin,
        AbstractDocumentSummaryViewset):
    """Auxiliary document summary view.

    Fetch a list of auxiliary  document with a limited set of fields
    """

class ReferenceDocumentSummaryViewset(
        ReferenceDocumentSummaryQueryMixin,
        AbstractDocumentSummaryViewset):
    """Reference document summary view.

    Fetch a list of reference document with a limited set of fields
    """
