"""
.. module::  ondalear.backend.api.analytics.views
   :synopsis:  analytics  api views module.

"""
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from ondalear.backend.services import find, TEXT_ANALYTICS_SERVICE
from ondalear.backend.api import constants
from ondalear.backend.api.base_views import response_header, DRFMixin, PermissionsMixin
from ondalear.backend.api.docmgmt.views.queries import DocumentAssociationQueryMixin
from ondalear.backend.api.analytics.serializers import NLPAnalysisSerializer

_logger = logging.getLogger(__name__)


class NLPAnalysisView(PermissionsMixin, DRFMixin, 
                      DocumentAssociationQueryMixin, GenericAPIView):
    """ NLP Analysis view class
    """
    serializer_class = NLPAnalysisSerializer

    def _build_response_data(self, detail, msg=None, api_status=None): # pylint: disable=unused-argument,no-self-use
        """build response data"""
        msg = msg or 'Analysis request successfully processed.'
        api_status = api_status or constants.STATUS_OK
        header = response_header(msg=msg,
                                 username=self.request.user.username,
                                 api_status=api_status)
        data = {
            'header': header,
            'detail': detail
        }
        return data

    def post(self, request, *args, **kwargs): # pylint: disable=unused-argument
        """Handle analysis post request"""
        # If  a valid token has been defined, the user will be authenticated
        # before this methodd is calldd
        serializer = self.get_serializer(data=self.request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        return self.analyze(serializer.data)


    def analyze(self, request_data):  # pylint: disable=no-self-use
        """Handle analysis"""

        # prepare model parameters
        # prepare model input
        # perform data model permission check on document association if required
        # perform the analysis if required (results change time earlier than documents)
        # save the results if required

        default_processing_instructions = dict(use_cache=False, save_results=False)
        default_model_params = dict()
        model_descriptor = request_data['model_descriptor']
        model_input = request_data['model_input']
        model_params = request_data.get('model_params', default_model_params)
        processing_instructions = request_data.get('processing_instructions', 
                                                   default_processing_instructions)
        service = find(TEXT_ANALYTICS_SERVICE)
        detail = service.analyze(model_descriptor=model_descriptor,
                                 model_params=model_params,
                                 model_input=model_input,
                                 processing_instructions=processing_instructions)
        response = Response(data=self._build_response_data(detail),
                            status=status.HTTP_200_OK)

        return response
