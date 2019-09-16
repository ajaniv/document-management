"""
.. module::  ondalear.backend.api.analytics.serializers
   :synopsis:  analytics  api  serializers module.

"""
import logging
from rest_framework import serializers

from ondalear.backend.docmgmt.models import DocumentAssociation
from ondalear.analytics import ALLENNLP_MODEL_FAMILY, ALLENNLP_MODEL_BDAF

_logger = logging.getLogger(__name__)

# pylint: disable=abstract-method
class ModelInputSerializer(serializers.Serializer):
    """Model input serializer"""
    text_reference = serializers.CharField(required=False)
    text_auxiliary = serializers.CharField(required=False)
    resource_id = serializers.IntegerField(min_value=1, required=False)

    def validate(self, attrs):
        """
        Check that instance is properly configured.
        """
        if not attrs or len(attrs) == 3:
            raise serializers.ValidationError(
                "text_reference and text_auxiliary or resource_id must be defined")
        if not 'resource_id' in attrs:
            if not 'text_reference' in attrs or not 'text_auxiliary' in attrs:
                raise serializers.ValidationError(
                    "text_reference and text_auxiliary must be defined")
        return attrs

    class Meta:
        """Meta class"""
        fields = ('text_reference', 'text_auxiliary', 'resource_id')

class ModelDescriptorSerializer(serializers.Serializer):
    """Model descriptor serializer"""
    model_family = serializers.CharField(required=True)
    model_name = serializers.CharField(required=True)

    class Meta:
        """Meta class"""
        fields = ('model_family', 'model_name')

class ModelParamsSerializer(serializers.Serializer):
    """Model parameters serializer"""
    params = serializers.DictField(required=False)

    class Meta:
        """Meta class"""
        fields = ('params')

class ProcessingInstructionsSerializer(serializers.Serializer):
    """Processing instructions serializer"""
    use_cache = serializers.BooleanField(default=False)
    save_results = serializers.BooleanField(default=False)

    class Meta:
        """Meta class"""
        fields = ('use_cache', 'save_results')

class NLPAnalysisSerializer(serializers.Serializer):
    """NLP analysis serializer class"""
    model_descriptor = ModelDescriptorSerializer(required=True)
    model_input = ModelInputSerializer(required=True)
    model_params = ModelParamsSerializer(required=False)
    processing_instructions = ProcessingInstructionsSerializer(required=False)

    class Meta:
        """Meta class"""
        model = DocumentAssociation
