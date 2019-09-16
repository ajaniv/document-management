"""
.. module:: ondalear.backend.api.analytics.views.test_reading_comprehension
   :synopsis: analytics  views  reading comprehension unit test  module.


"""
import logging

from django.urls import reverse
from rest_framework import status

from ondalear.analytics import (ALLENNLP_MODEL_FAMILY,
                                ALLENNLP_MODEL_BDAF,
                                ALLENNLP_MODEL_BDAF_NAQNAET,
                                MODEL_PRIMARY_OUTPUT_KEY)
from ondalear.backend.docmgmt.models import DocumentAssociation
from ondalear.backend.tests.api.base import AbstractAPITestCase

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,no-self-use,too-many-ancestors

class AbstractAnalyticsTest(AbstractAPITestCase):
    def assert_response_detail(self, data, expected=None):
        """verify response detail"""
        expected = expected or self.expected_response()
        self.assertEqual(sorted(data.keys()), sorted(expected.keys()))
        if MODEL_PRIMARY_OUTPUT_KEY in expected:
            self.assertEqual(data[MODEL_PRIMARY_OUTPUT_KEY], expected[MODEL_PRIMARY_OUTPUT_KEY])


    def assert_analysis(self, expected_status=None, request_data=None, fmt=None):
        """verify analysis request"""
        expected_status = expected_status or status.HTTP_200_OK
        request_data = request_data or self.analysis_data().copy()
        fmt = fmt or 'json'

        url = reverse(self.url_name)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.post(url, request_data, format=fmt)
        self.assertEqual(response.status_code, expected_status, f'{response.data}')
        if expected_status != status.HTTP_200_OK:
            return response
        response_data = response.data

        # verify the header
        self.assert_response_header(
            data=response_data['header'],
            msg='Analysis request successfully processed.')

        # verify the detail
        detail = response_data['detail']
        self.assert_response_detail(detail)

        return response

    @classmethod
    def setUpClass(cls):
        """Class setup"""
        super(AbstractAnalyticsTest, cls).setUpClass()
        cls.create_essential_objects()

    def setUp(self):
        """test case level setup"""
        super(AbstractAnalyticsTest, self).setUp()

        # configure user group and permissions relationships
        self.configure_group(model_class=self.model_class)

        # login
        self.login()

    def tearDown(self):
        """test case level tear down"""
        self.logout()
        super(AbstractAnalyticsTest, self).tearDown()


TEXT_REFERENCE = """
A reusable launch system (RLS, or reusable launch vehicle, RLV) is a launch system which is capable of launching a 
payload into space more than once. This contrasts with expendable launch systems, where each launch vehicle is 
launched once and then discarded. No completely reusable orbital launch system has ever been created. 
Two partially reusable launch systems were developed, the Space Shuttle and Falcon 9. The Space Shuttle was partially 
reusable: the orbiter (which included the Space Shuttle main engines and the Orbital Maneuvering System engines), 
and the two solid rocket boosters were reused after several months of refitting work for each launch. 
The external tank was discarded after each flight. 

"""
TEXT_AUXILIARY = 'How many partially reusable launch systems were developed?'

class ReadingComprenhensionBDAFTextByValueTest(AbstractAnalyticsTest):
    """Reading comprehension test case.

    Text data for analysis is passed by value
    """

    url_name = 'analyze'
    model_class = DocumentAssociation

    def expected_response(self):
        """return expected response"""
        keys = ['passage_question_attention', 'span_start_logits', 
                'span_start_probs', 'span_end_logits', 'span_end_probs', 
                'best_span', 'best_span_str', 'question_tokens', 'passage_tokens']
        data = {key: None for key in keys}
        data[MODEL_PRIMARY_OUTPUT_KEY] =  'Two'

        return data

    def analysis_data(self):
        """return analysis data"""
        return dict(model_input=dict(text_reference=TEXT_REFERENCE,
                                     text_auxiliary=TEXT_AUXILIARY),
                    model_descriptor=dict(model_family=ALLENNLP_MODEL_FAMILY,
                                          model_name=ALLENNLP_MODEL_BDAF))

    def test_by_value(self):
        # Expect to execute reading comprehension analysis.
        self.assert_analysis()
