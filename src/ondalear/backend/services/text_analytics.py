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
            initialize_allennlp(config_file_path)
            self.initialized = True
            _logger.info('initialized allennlp')

    def analyze(self, model_descriptor, model_params, model_input, processing_instructions):    # pylint: disable=unused-argument
        """perform an analysis"""
        request_model_input = model_input
        # initialize the service
        if not self.is_initialized():
            self.initialize()

        # find the model
        model = find_model(family=model_descriptor[MODEL_FAMILY],
                           name=model_descriptor[MODEL_NAME])

        # fetch the data from the db if required
        if 'resource_id' in model_input:
            _logger.info('fetching DocumentAssociation resource %s from db',
                         model_input['resource_id'])
            doc_assoc = DocumentAssociation.objects.get(pk=model_input['resource_id'])
            ref_doc = ReferenceDocument.objects.get(pk=doc_assoc.from_document.id)      # pylint: disable=no-member
            aux_doc = AuxiliaryDocument.objects.get(pk=doc_assoc.to_document.id)        # pylint: disable=no-member
            request_model_input = dict(text_reference=ref_doc.get_text(),
                                       text_auxiliary=aux_doc.get_text())

        # convert the model input to native model format
        native_model_input = model.convert_model_input(request_model_input)
        # perform the analysis
        model_output = model.analyze(model_input=native_model_input, model_params=model_params)
        return model_output

register(TEXT_ANALYTICS_SERVICE, TextAnalyticsService(TEXT_ANALYTICS_SERVICE))
