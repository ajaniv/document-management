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
from ondalear.backend.docmgmt.models.constants import DOCUMENT_ASSOCIATION_PURPOSE_QUESTION
from ondalear.backend.tests.docmgmt.models import factories
from ondalear.backend.tests.api.base import AbstractAPITestCase

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,no-self-use,too-many-ancestors

class AssertMixin:
    """Assert mixin class"""

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

        # verify status
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

class AssociatedDocumenteMixin:
    """Assoricate document  mixin class

    Used for handling saved resourc test cases
    """
    def analysis_data(self):
        """return analysis data"""
        return dict(model_input=dict(resource_id=self.doc_association.id),
                    model_descriptor=self.model_descriptor())

    def do_setup(self):
        """test case setup"""
        self.doc_association, _, _ = self.create_linked_documents(text_reference=TEXT_REFERENCE,
                                                                  text_auxiliary=TEXT_AUXILIARY)

    def do_teardown(self):
        """test case teardown"""
        # delete the two documents; the association will be automatically deleted.
        self.doc_association.from_document.delete()
        self.doc_association.to_document.delete()

    def create_linked_documents(self, text_reference, text_auxiliary):
        """create linked documents"""
        # obtain critical elements for object creation
        defaults = self.create_defaults()

        # create reference document
        from_document = factories.DocumentModelFactory(name='ref_doc',
                                                       title='ref_doc title',
                                                       description='ref_doc description',
                                                       **defaults)
        ref_document = factories.ReferenceDocumentModelFactory(
            content=text_reference, document=from_document)

        # create auxiliary document
        to_document = factories.DocumentModelFactory(name='aux_doc',
                                                     title='aux_doc title',
                                                     description='aux_doc description',
                                                     **defaults)
        aux_document = factories.AuxiliaryDocumentModelFactory(
            content=text_auxiliary, document=to_document)

        linked_doc = factories.DocumentAssociationModelFactory(
            from_document=from_document, to_document=to_document,
            purpose=DOCUMENT_ASSOCIATION_PURPOSE_QUESTION,
            **defaults)

        return linked_doc, ref_document, aux_document


class AbstractAnalyticsTest(AssertMixin, AbstractAPITestCase):
    """Text analytics base test case class"""
    model_class = DocumentAssociation
    url_name = 'analyze'

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

class AbstractReadingComphrensionBDAFTest(AbstractAnalyticsTest):
    """Base class BDAF reading comprehension"""
    def expected_response(self):
        """return expected response"""
        keys = ['passage_question_attention', 'span_start_logits',
                'span_start_probs', 'span_end_logits', 'span_end_probs',
                'best_span', 'best_span_str', 'question_tokens', 'passage_tokens']
        data = {key: None for key in keys}
        data[MODEL_PRIMARY_OUTPUT_KEY] = 'Two'

        return data

    def model_descriptor(self):
        """return model descriptor"""
        return dict(model_family=ALLENNLP_MODEL_FAMILY,
                    model_name=ALLENNLP_MODEL_BDAF)

class ReadingComprenhensionBDAFByValueTest(AbstractReadingComphrensionBDAFTest):
    """Reading comprehension content by value test case.

    BDAF text data for analysis is passed by value
    """

    def analysis_data(self):
        """return analysis data"""
        return dict(model_input=dict(text_reference=TEXT_REFERENCE,
                                     text_auxiliary=TEXT_AUXILIARY),
                    model_descriptor=self.model_descriptor())

    def test_by_value(self):
        # Expect to execute reading comprehension analysis.
        self.assert_analysis()

    def test_by_value_with_caching(self):
        # Expect to execute reading comprehension analysis and cache the results
        request_data = self.analysis_data()
        request_data['processing_instructions'] = dict(use_cache=True,
                                                       analysis_name='reading_comprehension')
        self.assert_analysis(request_data=request_data)

class ReadingComprenhensionBDAFByReferenceTest(AssociatedDocumenteMixin,
                                               AbstractReadingComphrensionBDAFTest):
    """Reading comprehension content by reference test case.

    BDAF text data for analysis is passed by reference via resource id stored in db
    """

    def setUp(self):
        """setup the test case"""
        super().setUp()
        self.do_setup()

    def tearDown(self):
        """test case down"""
        self.do_teardown()
        super().tearDown()

    def test_by_reference(self):
        # Expect to execute reading comprehension analysis.
        self.assert_analysis()

class AbstractReadingComprehensionBDAFNAQNAETTest(AbstractAnalyticsTest):
    """Base class BDAF NAQNAET reading comprehension test case"""

    def expected_response(self):
        """return expected response"""
        keys = ['loss', 'question_id', 'answer', 'passage_question_attention',
                'question_tokens', 'passage_tokens']
        data = {key: None for key in keys}
        data[MODEL_PRIMARY_OUTPUT_KEY] = {'answer_type': 'count', 'count': 2}

        return data

    def model_descriptor(self):
        """return model descriptor"""
        return dict(model_family=ALLENNLP_MODEL_FAMILY,
                    model_name=ALLENNLP_MODEL_BDAF_NAQNAET)

class ReadingComprenhensionBDAFNAQNAETByValueTest(AbstractReadingComprehensionBDAFNAQNAETTest):
    """Reading comprehension content by value test case.

    BDAF NAQNAET text data for analysis is passed by value
    """
    def analysis_data(self):
        """return analysis data"""
        return dict(model_input=dict(text_reference=TEXT_REFERENCE,
                                     text_auxiliary=TEXT_AUXILIARY),
                    model_descriptor=self.model_descriptor())

    def test_by_value(self):
        # Expect to execute reading comprehension analysis.
        self.assert_analysis()


class ReadingComprenhensionBDAFNAETByReferenceTest(AssociatedDocumenteMixin,
                                                   AbstractReadingComprehensionBDAFNAQNAETTest):
    """Reading comprehension content by reference test case.

    BDAF NAQNAET text data for analysis is passed by reference via resource id stored in db
    """

    def setUp(self):
        """setup the test case"""
        super().setUp()
        self.do_setup()

    def tearDown(self):
        """test case down"""
        self.do_teardown()
        super().tearDown()

    def test_by_reference(self):
        # Expect to execute reading comprehension analysis.
        self.assert_analysis()
