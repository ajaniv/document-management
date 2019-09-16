"""
.. module:: ondalear.backend.services.text_analytics
   :synopsis: text analytics service  module

"""
import os
import logging
from overrides import overrides

from ondalear.analytics.allennlp import initialize as init_allennlp
from ondalear.analytics.models.registry import find as find_model
from ondalear.backend.services.base import register, AbstractService

_logger = logging.getLogger(__name__)

TEXT_ANALYTICS_SERVICE = 'text_analytics_service'
ALLENNLP_CONFIG_FILE_PATH = 'ALLENNLP_CONFIG_FILE_PATH'
ALLENNLP_CONFIG_FILE_NAME = 'config_allennlp.json'

class TextAnalyticsService(AbstractService):
    """Text analytics service"""

    @overrides
    def initialize(self):
        if not self.is_initialized():
            _logger.info('initializing allennlp')
            config_file_path = os.environ.get(ALLENNLP_CONFIG_FILE_PATH,
                                              self.config_file_path(ALLENNLP_CONFIG_FILE_NAME))
            init_allennlp(config_file_path)
            self.initialized = True
            _logger.info('initialized allennlp')

    def analyze(self, model_descriptor, model_params, model_input, processing_instructions):    # pylint: disable=unused-argument
        """perform an analysis"""
        if not self.is_initialized():
            self.initialize()

        model = find_model(family=model_descriptor['model_family'],
                           name=model_descriptor['model_name'])
        native_model_input = model.convert_model_input(model_input)
        model_output = model.analyze(model_input=native_model_input, model_params=model_params)
        return model_output

register(TEXT_ANALYTICS_SERVICE, TextAnalyticsService(TEXT_ANALYTICS_SERVICE))
