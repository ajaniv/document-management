"""
.. module::  ondalear.backend.api.analytics.views
   :synopsis:  analytics  api views module.

"""
import logging

import rest_framework_filters as filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from ondalear.backend.core.django.utils import current_site
from ondalear.backend.analytics.models import AnalysisResults
from ondalear.backend.services import find, TEXT_ANALYTICS_SERVICE
from ondalear.backend.api import constants
from ondalear.backend.api.base_queries import AbstractQueryMixin
from ondalear.backend.api.docmgmt.views.queries import DocumentAssociationQueryMixin
from ondalear.backend.api.base_views import (response_header,
                                             AbstractModelViewSet,
                                             DRFMixin,
                                             PermissionsMixin)
from ondalear.backend.api.analytics.serializers import (AnalysisResultsSerializer,
                                                        NLPAnalysisSerializer)

_logger = logging.getLogger(__name__)

# pylint: disable=too-many-ancestors,no-self-use

class NLPAnalysisView(PermissionsMixin, DRFMixin,
                      DocumentAssociationQueryMixin, GenericAPIView):
    """ NLP Analysis view class
    """
    serializer_class = NLPAnalysisSerializer

    def _build_response_data(self, results, saved_results, msg=None, api_status=None): # pylint: disable=unused-argument
        """build response data"""
        msg = msg or 'Analysis request successfully processed.'
        api_status = api_status or constants.STATUS_OK
        header = response_header(msg=msg,
                                 username=self.request.user.username,
                                 api_status=api_status)

        results['analysis_results_id'] = saved_results.id if saved_results else None
        data = {
            'header': header,
            'detail': results
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


    def analyze(self, request_data):
        """Handle analysis"""


        # perform data model permission check on document association if required
        # perform the analysis if required (results change time earlier than documents)

        # prepare the request context
        default_model_params = dict()
        default_processing_instructions = dict(use_cache=False, save_results=False, name=None)
        request_context = dict(
            model_descriptor=request_data['model_descriptor'],
            model_input=request_data['model_input'],
            model_params=request_data.get('model_params', default_model_params),
            processing_instructions=request_data.get('processing_instructions',
                                                     default_processing_instructions),
            user=self.request.user,
            client=self.request.client,
            site=current_site()
        )
        service = find(TEXT_ANALYTICS_SERVICE)
        results, saved_results = service.analyze(request_context)

        # save the results if required and user is allowed to save the results
        response = Response(data=self._build_response_data(results, saved_results),
                            status=status.HTTP_200_OK)

        return response

class AnalysisResultsFilter(filters.FilterSet):
    """AnalysisResults filter class"""
    class Meta:
        """Meta class"""
        model = AnalysisResults
        fields = {
            'name': ['exact', 'in', 'startswith']
        }

class AnalysisResultsQueryMixin(AbstractQueryMixin):
    """Analysis result query mixin class"""
    filter_class = AnalysisResultsFilter

class AnalysisResultsViewSet(AnalysisResultsQueryMixin, AbstractModelViewSet):
    """Analysis result  view set"""
    queryset = AnalysisResults.objects.all()
    serializer_class = AnalysisResultsSerializer
