"""
.. module::  ondalear.backend.api.docmgmt.views.annotation
   :synopsis:  ondalear docmgnt  annotation views module.

"""
import logging

from ondalear.backend.docmgmt.models import Annotation, DocumentAnnotation
from ondalear.backend.api.base_views import AbstractModelViewSet
from ondalear.backend.api.docmgmt.serializers import (AnnotationSerializer,
                                                      DocumentAnnotationSerializer)
from ondalear.backend.api.docmgmt.views.queries import (AnnotationQueryMixin,
                                                        DocumentAnnotationQueryMixin)

# pylint: disable=too-many-ancestors

_logger = logging.getLogger(__name__)


class AnnotationViewSet(AnnotationQueryMixin, AbstractModelViewSet):
    """Annotation  view class"""
    queryset = Annotation.objects.all().order_by('-update_time')
    serializer_class = AnnotationSerializer


class DocumentAnnotationViewSet(DocumentAnnotationQueryMixin, AbstractModelViewSet):
    """Document annotation association view class"""
    queryset = DocumentAnnotation.objects.all().order_by('-update_time')
    serializer_class = DocumentAnnotationSerializer
