"""
.. module::  ondalear.backend.api.docmgmt.serializers.document
   :synopsis:  ondalear docmgmt document serializers module.

"""
import logging
from ondalear.backend.docmgmt.models import Document
from ondalear.backend.api.base_serializers import AbstratModelSerializer


_logger = logging.getLogger(__name__)

# pylint: disable=too-many-ancestors


document_fields = (
    'client', 'category', 'description', 'documents', 'document_type',
    'language', 'mime_type', 'name', 'tags', 'title')


class DocumentSerializer(AbstratModelSerializer):
    """Document serializer class.
    """
    class Meta(AbstratModelSerializer.Meta):
        """Meta class"""
        model = Document
        fields = AbstratModelSerializer.Meta.fields + document_fields
        read_only_fields = AbstratModelSerializer.Meta.fields + ('client', 'mime_type',)


class DocumentSummarySerializer(AbstratModelSerializer):
    """Document summary serializer class"""

    class Meta(AbstratModelSerializer.Meta):
        """Meta class"""
        model = Document
        fields = AbstratModelSerializer.Meta.fields + ('category', 'client', 'description',
                                                       'name', 'tags', 'title')
