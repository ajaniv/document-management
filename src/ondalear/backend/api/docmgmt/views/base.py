"""
.. module::  ondalear.backend.api.docmgmt.views.base
   :synopsis:  base docmgmt module.

"""
import logging

from rest_framework.views import APIView

from ondalear.backend.api.base_views import (delete_response,
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





class AbstractDeleteManyAssociationsView(DRFMixin, PermissionsMixin, APIView):
    """
    Abstract delete many associations base class
    """

    def delete_many(self, request, *args, **kwargs):        # pylint: disable=unused-argument
        """handle delete 1..N document association"""
        serializer = self.request_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        resources = serializer.data['resources']
        qs = self.get_queryset()
        deleted = qs.filter(pk__in=resources).delete()
        count_deleted = deleted[0]
        # @TODO: consider providing a detailed list of object ids not deletted
        #   as part of the response
        if count_deleted != len(resources):
            _logger.warning('Some instances from %s of type %s were not deleted as per %s',
                            resources, self.serializer_class.Meta.model, deleted)

        return delete_response(request, count_deleted)


    def post(self, request, *args, **kwargs): # pylint: disable=unused-argument
        """Handle logout post request"""

        return self.delete_many(request)
