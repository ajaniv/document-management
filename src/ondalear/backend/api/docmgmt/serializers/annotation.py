"""
.. module::  ondalear.backend.api.docmgmt.serializers.annotation
   :synopsis:  annotation serializers module.

"""
import logging

from ondalear.backend.docmgmt.models import (Annotation,
                                             DocumentAnnotation)
from ondalear.backend.api.base_serializers import AbstratModelSerializer

logger = logging.getLogger(__name__)

# pylint: disable=too-many-ancestors

annotation_fields = ('annotation', 'client', 'name')

class AnnotationSerializer(AbstratModelSerializer):
    """Annotation serializer class.
    """

    class Meta(AbstratModelSerializer.Meta):
        """Meta class"""
        fields = AbstratModelSerializer.Meta.fields + annotation_fields
        read_only_fields = AbstratModelSerializer.Meta.fields + ('client',)
        model = Annotation


document_annotation_fields = ('client', 'document', 'annotation')

class DocumentAnnotationSerializer(AbstratModelSerializer):
    """Document annotation association serializer class"""

    class Meta(AbstratModelSerializer.Meta):
        """Meta class"""
        fields = AbstratModelSerializer.Meta.fields + document_annotation_fields
        read_only_fields = AbstratModelSerializer.Meta.fields + ('client',)
        model = DocumentAnnotation
