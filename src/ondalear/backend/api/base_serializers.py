"""
.. module::  ondalear.backend.api.base_serializers
   :synopsis:  api base module.

"""
import logging

from rest_framework import serializers

from ondalear.backend.core.django.utils import current_site
from ondalear.backend.docmgmt.models import ClientUser


_logger = logging.getLogger(__name__)


system_fields = (
    'creation_time', 'creation_user',
    'is_deleted', 'is_enabled',
    'effective_user', 'id', 'site',
    'update_user', 'update_time',
    'uuid', 'version')

class RequestContextMixin:
    """Request context mixin class"""

    def build_request_context(self):
        """build the request context"""
        context = dict()
        user = self.context['request'].user
        #@TODO: handle exception if client user is not found
        client_user = ClientUser.objects.get(user=user)
        context['client'] = client_user.client
        for attr in ('creation_user', 'effective_user', 'update_user'):
            context[attr] = user
        context['site'] = current_site()
        return context

class AbstratModelSerializer(RequestContextMixin, serializers.ModelSerializer):
    """Base document serializer class.
    """
    class Meta:
        """Meta class"""
        fields = system_fields
        read_only_fields = system_fields

    def create(self, validated_data):
        """Create request serializer method.
        Need to build the derived data from the request"""
        context = self.build_request_context()
        validated_data.update(context)

        return super(AbstratModelSerializer, self).create(validated_data)


    @classmethod
    def field_names(cls):
        """return field names"""
        return cls.Meta.fields
