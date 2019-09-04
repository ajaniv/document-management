"""
.. module::  ondalear.backend.api.user_admin.serializers
   :synopsis:  user admin serializers module.

"""
import logging
from rest_framework import serializers
from rest_auth.models import TokenModel

_logger = logging.getLogger(__name__)

class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        """meta class declaration"""
        model = TokenModel
        fields = ('key',)
