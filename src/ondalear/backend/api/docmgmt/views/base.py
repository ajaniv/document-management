"""
.. module::  ondalear.backend.api.docmgmt.views.base
   :synopsis:  base docmgmt module.

"""
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ondalear.backend.api.base_views import (response_header,
                                             DRFMixin,
                                             PermissionsMixin)
from ondalear.backend.api import constants

_logger = logging.getLogger(__name__)

# pylint: disable=no-member

class AssociationUpdateViewSetMixin:
    """Association view set update mixin mixn.

    """
    def update(self, request, *args, **kwargs):     # pylint: disable=unused-argument
        """Update document association view"""
        raise NotImplementedError(constants.ANALYSIS_REQUIRED)


class AssociationDeleteViewSetMixin:
    """Association view set delete mixn.

    """
    def create(self, request, *args, **kwargs):     # pylint: disable=unused-argument
        """handle delete 1..N document association"""
        # @TODO: handles post request, review naming
        data = request.data
        model_class = self.serializer_class.Meta.model
        deleted = model_class.objects.filter(pk__in=data).delete()
        count_deleted = deleted[0]
        # @TODO: consider providing a detailed list of object ids not deletted
        #   as part of the response
        if count_deleted != len(data):
            _logger.warning('Some instances from %s were not deleted as per %s',
                            data, deleted)
        data = {
            'header': response_header(msg='Delete request successfully processed.',
                                      username=request.user.username,
                                      api_status=constants.STATUS_OK),
            'detail': dict(count_deleted=count_deleted)
            }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class AbstractDeleteManyAssociationsView(DRFMixin, PermissionsMixin, APIView):
    """
    Abstract delete many associations base class
    """

    def delete_many(self, request, *args, **kwargs):        # pylint: disable=unused-argument
        """handle delete 1..N document association"""
        # @TODO: handles post request, review naming
        data = request.data
        qs = self.get_queryset()
        deleted = qs.filter(pk__in=data).delete()
        count_deleted = deleted[0]
        # @TODO: consider providing a detailed list of object ids not deletted
        #   as part of the response
        if count_deleted != len(data):
            _logger.warning('Some instances from %s were not deleted as per %s',
                            data, deleted)
        data = {
            'header': response_header(msg='Delete request successfully processed.',
                                      username=request.user.username,
                                      api_status=constants.STATUS_OK),
            'detail': dict(count_deleted=count_deleted)
            }
        return Response(data=data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs): # pylint: disable=unused-argument
        """Handle logout post request"""

        return self.delete_many(request)
