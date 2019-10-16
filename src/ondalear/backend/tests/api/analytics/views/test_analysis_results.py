"""
.. module:: ondalear.backend.tests.api.analytics.views.test_analysis_results
   :synopsis: Analysis results view unit test  module.


"""
import logging

from ondalear.backend.analytics.models import AnalysisResults
from ondalear.backend.tests.analytics.models import factories
from ondalear.backend.tests.docmgmt.models.factories import DocumentAssociationModelFactory
from ondalear.backend.tests.api.model_viewset  import AbstractModelViewsetTestCase



_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors


class AbstractAnalysisResultsApiTest(AbstractModelViewsetTestCase):
    """Base analysis results  api test"""
    create_url_name = 'analysis-results-crud-list'
    factory_class = factories.AnalysisResultsModelFactory
    model_class = AnalysisResults

    create_request_data = {
        'name': 'analysis_results_1',
        'description': 'analysis results description',
        'input': dict(input1='input1'),
        'output': dict(output1='output1')
    }

    response_no_values = tuple()

    def setUp(self):
        """test case setup"""
        super().setUp()
        defaults = self.create_defaults()
        document_association = DocumentAssociationModelFactory(**defaults)
        self.created_models.extend([document_association.from_document,
                                    document_association.to_document])
        self.create_request_data['documents'] = document_association.id

class AnalysisResultsAPIPostTest(AbstractAnalysisResultsApiTest):
    """Analysis results post test case"""

    url_name = 'analysis-results-crud-list'

    def test_post(self):
        # expect to create analysis results through api
        self.assert_create()


class AnalysisResultsAPIListTest(AbstractAnalysisResultsApiTest):
    """Analysis results  list test case"""

    url_name = 'analysis-results-crud-list'

    def test_list(self):
        # expect to fetch analysis results list
        self.assert_list()


class AnalysisResultsAPIRetrieveTest(AbstractAnalysisResultsApiTest):
    """Analysis results  retrieve test case"""

    url_name = 'analysis-results-crud-detail'

    def test_retrieve(self):
        # expect to retrive the analysis results instance
        self.assert_retrieve()


class AnalysisResultsAPIPutTest(AbstractAnalysisResultsApiTest):
    """Analysis results  put test case"""

    url_name = 'analysis-results-crud-detail'

    def test_put(self):
        # expect to update the analysis results instance
        self.assert_put()


class AnalysisResultsAPIPatchTest(AbstractAnalysisResultsApiTest):
    """Analysis results  patch test case"""

    url_name = 'analysis-results-crud-detail'

    def test_patch(self):
        # expect to patch the analysis results instance
        self.assert_patch()


class AnalysisResultsAPIDeleteTest(AbstractAnalysisResultsApiTest):
    """Analysis results delete test case"""

    url_name = 'analysis-results-crud-detail'

    def test_delete(self):
        # expect to delete the analysis results instance
        self.assert_delete()


class AnalysisResultsAPIFilterTest(AbstractAnalysisResultsApiTest):
    """Analysis results filter test case"""
    url_name = 'analysis-results-crud-list'

    def test_name_exact(self):
        # expect to fetch analysis results list
        self.assert_list(query_str='name=analysis_results_1')

    def test_name_exact_missing(self):
        # expect to fail to fetch analysis results list
        self.assert_list(query_str='name=analysis_results_2', expected_count=0)

    def test_name_starts_with(self):
        # expect to fetch analysis results list
        self.assert_list(query_str='name__startswith=analysis_')

    def test_name_in(self):
        # expect to fetch analysis results list
        self.assert_list(query_str='name__in=analysis_results_1,analysis_results_2')
