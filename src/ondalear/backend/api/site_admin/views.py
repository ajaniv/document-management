"""
.. module::  ondalaer.backend.api.site_admin.views
   :synopsis:  ondalear site admin views module.

"""
import logging
from django.contrib.auth.models import User, Group
from rest_framework import permissions

from ondalear.backend.docmgmt.models import Client, ClientUser
from ondalear.backend.api.base_views import AbstractModelViewSet
from ondalear.backend.api.constants import ANALYSIS_REQUIRED
from ondalear.backend.api.site_admin.serializers import (UserSerializer, GroupSerializer,
                                                         ClientSerializer, ClientUserSerializer)

_logger = logging.getLogger(__name__)

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Allows access only to admin users or read only.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_staff)


# Note: IsAdminUser checks whether the user is staff, not whether is is admin

# pylint: disable=too-many-ancestors,abstract-method
class AbstractSiteAdminViewSet(AbstractModelViewSet):
    """Base admin view class."""
    permission_classes = (permissions.IsAuthenticated,
                          IsAdminUserOrReadOnly,
                          permissions.DjangoModelPermissions)

    # @TODO: figure out whether create, update, delete are to be supported using API
    def _raise_exception(self):
        """raise exception"""
        raise NotImplementedError(ANALYSIS_REQUIRED)

    def create(self, request, *args, **kwargs):
        """Create an instance.

        Called on POST request for collection endpoint
        """
        self._raise_exception()

    def update(self, request, *args, **kwargs):
        """Update an instance.

        Called on PUT and PATCH requests.
        """
        self._raise_exception()

    def destroy(self, request, *args, **kwargs):
        """Delete an instance.

        Called delete requests.
        """
        self._raise_exception()

class UserViewSet(AbstractSiteAdminViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(AbstractSiteAdminViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer

class ClientViewSet(AbstractSiteAdminViewSet):
    """
    API endpoint that allows client to be viewed or edited.
    """
    queryset = Client.objects.all().order_by('-update_time')
    serializer_class = ClientSerializer

class ClientUserViewSet(AbstractSiteAdminViewSet):
    """
    API endpoint that allows client users to be viewed or edited.
    """
    queryset = ClientUser.objects.all().order_by('-update_time')
    serializer_class = ClientUserSerializer
