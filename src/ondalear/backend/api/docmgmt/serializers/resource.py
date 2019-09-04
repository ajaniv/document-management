"""
.. module::  ondalear.backend.api.docmgmt.serializers.resource
   :synopsis:  annotation serializers module.

"""
import logging

from rest_framework import serializers

logger = logging.getLogger(__name__)

# pylint: disable=abstract-method

class ResourceListSerializer(serializers.Serializer):
    """Resource list serializer class"""
    resources = serializers.ListField(min_length=1,
                                      allow_empty=False,
                                      child=serializers.IntegerField())
