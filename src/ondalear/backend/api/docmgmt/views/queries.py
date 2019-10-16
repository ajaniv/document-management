"""
.. module::  ondalear.backend.api.docmgmt.views.queries
   :synopsis:  ondalear docmgmt queries module.

"""
import logging
from django.db.models import Q

from ondalear.backend.docmgmt.models import constants, DocumentTag
from ondalear.backend.api.base_queries import AbstractQueryMixin
from ondalear.backend.api.docmgmt.views.filters import (AuxiliaryDocumentFilter,
                                                        DocumentFilter,
                                                        ReferenceDocumentFilter)

_logger = logging.getLogger(__name__)



class AnnotationQueryMixin(AbstractQueryMixin):
    """Annotation  query mixin class"""


class ClassificationQueryMixin(AbstractQueryMixin):
    """Classification query mixin class.

    Client and user determine data set population retrieved.
    Group has no bearing.
    """
    def get_queryset(self):
        """
        This query set should return a list of all the tags or categories
        for the currently authenticated user.
        """
        # @TODO: determine if group membership should be included in query execution
        # @TODO: analyze query performance
        model_class, user, client, _ = self.prepare()
        # drf checks for model permissions, at which point client has not beed defined yet
        if not client:
            return model_class.objects.all()

        q_effective = Q(effective_user=user)
        q_client = Q(client=client)

        if not client.is_system:
            # This is a user who belongs to a real client (i.e. Morgan Stanley)
            # Can see all tags managed by the client as well as system tags
            # @TODO: may want to further constrain by group
            q = q_client | Q(client__is_system=True)
        else:
            # this is a user associated with a pseudo client - system type client.
            # can see system client tags and his tags
            q = q_effective | q_client
        result = model_class.objects.filter(q).order_by('-update_time')
        return result

class DocumentTagQueryMixin(AbstractQueryMixin):
    """Document tag queryset mixin class"""

class DocumentAssociationQueryMixin(AbstractQueryMixin):
    """Document association queryset mixin class"""

class DocumentAnnotationQueryMixin(AbstractQueryMixin):
    """Document annotation queryset mixin class"""

class DocumentQueryMixin(AbstractQueryMixin):
    """Document queryset mixin class"""
    filter_class = DocumentFilter

class AbstractDocumentSummaryQueryMixin(DocumentQueryMixin):
    """Document summary queryset mixin class"""
    document_type = None
    def get_queryset(self):
        """
        This query set should return a list of all the documents
        for the currently authenticated user.
        """
        qs = super(AbstractDocumentSummaryQueryMixin, self).get_queryset()
        qs = qs.filter(document_type=constants.DOCUMENT_TYPE_REFERENCE)
        return qs

class ReferenceDocumentSummaryQueryMixin(DocumentQueryMixin):
    """Reference cocument summary queryset mixin class"""
    document_type = constants.DOCUMENT_TYPE_REFERENCE

class AuxiliaryDocumentSummaryQueryMixin(DocumentQueryMixin):
    """Auxiliary cocument summary queryset mixin class"""
    document_type = constants.DOCUMENT_TYPE_AUXILIARY

class DerivedDocumentQueryMixin(AbstractQueryMixin):
    """Derived document query mixin class"""

    def get_queryset(self):
        """
        This query set should return a list of all the documents
        for the currently authenticated user.
        """
        # @TODO: analyze query performance
        model_class, user, client, request = self.prepare()
        # drf checks for model permissions, at which point client has not beed defined yet
        if not client:
            return model_class.objects.all()
        tags = request.query_params.get('document__tags__in')
        if tags:
            # @TODO: have not been able to implement with filter set
            tags = [int(tag) for tag in tags.strip().split(',') if tag]
            qs_docs = DocumentTag.objects.only('document_id').filter(tag_id__in=tags)
            q_doc = Q(document__id__in=qs_docs.values_list('document_id', flat=True))
        else:
            q_doc = Q()
        q_effective = Q(document__effective_user=user)
        q_client = Q(document__client=client)
        if not client.is_system:
            # this is a user who belongs to a real client (i.e. Morgan Stanley)
            # get all the groups associated with the user
            qs_groups = user.groups.all()
            q = (Q(document__effective_user__groups__in=qs_groups) | q_effective) & q_client & q_doc
            # Filter the documents where the document effective_user group is in the user groups
            # As a safety valve, In case user is not in any group,
            #   still search for user owned documents.
        else:
            # this is a user associated with a pseudo client - system type client.
            q = q_effective & q_client &  q_doc
        # fetching document as part of the same query
        # fetching associated tags for all documents as a separate query
        # @TODO: limit the fields returned
        qs = model_class.objects.prefetch_related(
            'document__annotations', 'document__documents', 'document__tags').select_related(
                'document').filter(q).order_by('-document__update_time')
        return qs

class AuxiliaryDocumentQueryMixin(DerivedDocumentQueryMixin):
    """Auxiliary document queryset mixin class"""
    filter_class = AuxiliaryDocumentFilter

class ReferenceDocumentQueryMixin(DerivedDocumentQueryMixin):
    """Reference document queryset mixin class"""
    filter_class = ReferenceDocumentFilter
