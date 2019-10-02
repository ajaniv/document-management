"""
.. module:: ondalear.backend.services.text_analytics
   :synopsis: text analytics service  module

"""
import os
import logging
from overrides import overrides

from ondalear.backend.docmgmt.models import (AuxiliaryDocument,
                                             DocumentAssociation,
                                             ReferenceDocument)
from ondalear.analytics import initialize_allennlp, find_model, MODEL_FAMILY, MODEL_NAME
from ondalear.backend.services.base import register, AbstractService
from ondalear.backend.services.cache import AnalysisResultsCache

_logger = logging.getLogger(__name__)

TEXT_ANALYTICS_SERVICE = 'text_analytics_service'
ALLENNLP_CONFIG_FILE_PATH = 'ALLENNLP_CONFIG_FILE_PATH'
ALLENNLP_CONFIG_FILE_NAME = 'config_allennlp.json'

# pylint: disable=no-member,no-self-use

class TextAnalyticsService(AbstractService):
    """Text analytics service"""

    def __init__(self, name):
        super().__init__(name)
        self.cache = AnalysisResultsCache()

    @overrides
    def initialize(self):
        if not self.is_initialized():
            _logger.info('initializing allennlp')
            config_file_path = os.environ.get(ALLENNLP_CONFIG_FILE_PATH,
                                              self.config_file_path(ALLENNLP_CONFIG_FILE_NAME))
            initialize_allennlp(config_file_path)
            self.initialized = True
            _logger.info('initialized allennlp')

    def _check_cache(self, processing_instructions, username):
        """check cache settings"""
        use_cache = processing_instructions.get('use_cache')
        force_analysis = processing_instructions.get('force_analysis')
        cache_key = None
        results = None
        if use_cache and not force_analysis:
            cache_key = '{}:{}'.format(username, processing_instructions['analysis_name'])
            results = self.cache.find(cache_key)

        return use_cache, cache_key, results

    def _build_model_input(self, model_input):
        """build model input"""

        resource_id = model_input.get('resource_id')
        if resource_id:
            _logger.info('fetching DocumentAssociation resource %s from db',
                         resource_id)
            doc_assoc = DocumentAssociation.objects.get(pk=resource_id)
            ref_doc = ReferenceDocument.objects.get(pk=doc_assoc.from_document.id)
            aux_doc = AuxiliaryDocument.objects.get(pk=doc_assoc.to_document.id)
            model_input = dict(text_reference=ref_doc.get_text(),
                               text_auxiliary=aux_doc.get_text())
        return model_input

    def analyze(self, request_context):    # pylint: disable=unused-argument
        """perform an analysis"""

        model_descriptor = request_context['model_descriptor']
        model_params = request_context['model_params']
        model_input = request_context['model_input'].copy()
        processing_instructions = request_context['processing_instructions']
        username = request_context['username']

        _logger.info('analysis request; user: %s model_descriptor: %s model_parms: %s',
                     username, model_descriptor, model_params)
        # initialize the service
        if not self.is_initialized():
            self.initialize()

        # check cache processing
        use_cache, cache_key, results = self._check_cache(processing_instructions, username)
        if results:
            return results

        # find the model
        model = find_model(family=model_descriptor[MODEL_FAMILY],
                           name=model_descriptor[MODEL_NAME])

        # fetch the data from the db if required
        model_input = self._build_model_input(model_input)

        # convert the model input to native model format
        native_model_input = model.convert_model_input(model_input)
        # perform the analysis
        model_output = model.analyze(model_input=native_model_input, model_params=model_params)

        # update the cache
        if use_cache:
            self.cache.add(cache_key, model_output)

        return model_output

register(TEXT_ANALYTICS_SERVICE, TextAnalyticsService(TEXT_ANALYTICS_SERVICE))
