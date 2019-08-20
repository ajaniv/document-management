"""
.. module::  ondalaer.backend.api.docmgmt.views.derived_document
   :synopsis:  ondalear backend docmgmt derived document view module.

"""
import logging

from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser
from rest_framework.mixins import UpdateModelMixin

from ondalear.backend.core.python.utils import file_exists, remove
from ondalear.backend.docmgmt.models import (AuxiliaryDocument,
                                             ReferenceDocument)
from ondalear.backend.api.base_views import AbstractModelViewSet
from ondalear.backend.api.docmgmt.serializers import (AuxiliaryDocumentSerializer,
                                                      ReferenceDocumentSerializer)
from ondalear.backend.api.docmgmt.views.queries import (AuxiliaryDocumentQueryMixin,
                                                        ReferenceDocumentQueryMixin)
_logger = logging.getLogger(__name__)

# pylint: disable=too-many-ancestors,attribute-defined-outside-init,no-member


class DerivedDocumentViewSet(AbstractModelViewSet):
    """Derived document view set"""
    parser_classes = (JSONParser, MultiPartParser, FileUploadParser)

    def perform_destroy(self, instance):
        """actual instance destroy"""
        # delete the underlying document triggering deletion of derived instance
        instance.document.delete()

    def prepare_update(self, request, *args, **kwargs):
        """prepare update hook for subclassing"""
        serializer, instance = super(DerivedDocumentViewSet, self).prepare_update(
            request, *args, **kwargs)
        if instance.upload:
            self.before_save_instance = instance
            self.before_save_path = instance.upload.path
            self.before_save_content = instance.content
        return serializer, instance

    def perform_update(self, serializer):
        """perform update """
        UpdateModelMixin.perform_update(self, serializer)

        # need to remove files if no longer needed
        if hasattr(self, 'before_save_instance'):
            instance = self.before_save_instance
            saved_path = self.before_save_path

            if instance.upload.path != saved_path or instance.content:
                # uploaded file name has changed, or content
                # was defined - need to remove old file if it exists
                if file_exists(saved_path):
                    remove(saved_path)

class AuxiliaryDocumentViewSet(AuxiliaryDocumentQueryMixin,
                               DerivedDocumentViewSet):
    """
    API endpoint that allows *AuxiliaryDocument* instance  to be created, viewed and edited.
    """
    queryset = AuxiliaryDocument.objects.all()
    serializer_class = AuxiliaryDocumentSerializer

class ReferenceDocumentViewSet(ReferenceDocumentQueryMixin,
                               DerivedDocumentViewSet):
    """
    API endpoint that allows *ReferenceDocument* instance to be created, viewed and edited.
    """

    queryset = ReferenceDocument.objects.all()
    serializer_class = ReferenceDocumentSerializer
