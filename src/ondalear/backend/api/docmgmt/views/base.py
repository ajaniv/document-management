"""
.. module::  ondalear.backend.api.docmgmt.views.base
   :synopsis:  base docmgmt module.

"""
import logging
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from ondalear.backend.api.base_views import response_header
from ondalear.backend.api import constants

_logger = logging.getLogger(__name__)

# pylint: disable=no-member

class AssociationViewSet:
    """Association view set mixn.

    A component used where association between documents, documents and tags,
    and documents and annotation is required.
    """
    def update(self, request, *args, **kwargs):
        """Update document association view"""
        raise NotImplementedError(constants.ANALYSIS_REQUIRED)

    @action(detail=False, methods=['post'], url_path='delete-many', name='delete-many')
    def delete_many(self, request):
        """handle delete 1..N document association"""
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
