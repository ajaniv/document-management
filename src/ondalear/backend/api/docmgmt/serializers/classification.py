"""
.. module::  ondalear.backend.api.docmgmt.serializers.classification
   :synopsis:  classification serializers module.

"""
import logging
from rest_framework.serializers import PrimaryKeyRelatedField
from ondalear.backend.docmgmt.models import (Category,
                                             DocumentTag,
                                             Tag)
from ondalear.backend.api.base_serializers import AbstratModelSerializer

logger = logging.getLogger(__name__)

# pylint: disable=too-many-ancestors

base_classification_fields = ('client', 'description', 'domain', 'name', 'parent', 'target')

class AbstractClassificationModelSerializer(AbstratModelSerializer):
    """Base classification serializer class.
    """

    class Meta(AbstratModelSerializer.Meta):
        """Meta class"""
        fields = AbstratModelSerializer.Meta.fields + base_classification_fields
        read_only_fields = AbstratModelSerializer.Meta.fields + ('client',)

class TagSerializer(AbstractClassificationModelSerializer):
    """Tag serializer class"""

    parent = PrimaryKeyRelatedField(
        allow_null=True,
        queryset=Tag.objects.all(),
        required=False)

    class Meta(AbstractClassificationModelSerializer.Meta):
        """Meta class"""
        model = Tag


document_tag_fields = ('client', 'document', 'tag')

class DocumentTagSerializer(AbstratModelSerializer):
    """Document  tag association serializer class"""

    class Meta(AbstratModelSerializer.Meta):
        """Meta class"""
        fields = AbstratModelSerializer.Meta.fields + document_tag_fields
        read_only_fields = AbstratModelSerializer.Meta.fields + ('client',)
        model = DocumentTag

class CategorySerializer(AbstractClassificationModelSerializer):
    """Category serializer class"""

    parent = PrimaryKeyRelatedField(
        allow_null=True,
        queryset=Category.objects.all(),
        required=False)

    class Meta(AbstractClassificationModelSerializer.Meta):
        """Meta class"""
        model = Category
