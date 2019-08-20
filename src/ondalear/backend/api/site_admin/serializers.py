"""
.. module::  ondalear.backend.api.site_admin.serializers
   :synopsis:   site admin serializers module.

"""
import logging
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ondalear.backend.docmgmt.models import Client, ClientUser

_logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    """UserSerializer class definition"""
    class Meta:
        """Meta class declaration"""
        model = User
        fields = ('id', 'username', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    """GroupSerializer class definition"""
    class Meta:
        """Meta class declaration"""
        model = Group
        fields = ('id', 'name')

class ClientSerializer(serializers.ModelSerializer):
    """ClientSerializer class"""
    class Meta:
        """Meta class"""
        model = Client
        fields = ('id', 'client_id', 'name', 'email', 'phone', 'description')
        read_only_fields = ('id',)

class ClientUserSerializer(serializers.ModelSerializer):
    """ClientUser class"""
    class Meta:
        """Meta class"""
        model = ClientUser
        fields = ('id', 'client', 'user', 'phone', 'description')
        read_only_fields = ('id',)
