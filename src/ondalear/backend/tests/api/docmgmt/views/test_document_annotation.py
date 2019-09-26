"""
.. module:: ondalear.backend.tests.api.docmgmt.views.test_document_annotation
   :synopsis: Document annotation view unit test module.


"""
import logging
from rest_framework import status
from ondalear.backend.api.constants import ANALYSIS_REQUIRED
from ondalear.backend.tests.base_factories import model_class
from ondalear.backend.tests.docmgmt.models import factories
from .base import AbstractDocMgmtAPITestCase

logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors
_factory_class = factories.DocumentAnnotationModelFactory

class AbstractDocumentAnnotationApiTest(AbstractDocMgmtAPITestCase):
    """Base document annotation  api test"""
    create_url_name = 'document-annotation-crud-list'
    factory_class = _factory_class
    model_class = model_class(_factory_class)

    create_request_data = []

    response_no_values = tuple()

    def setUp(self):
        """Setup testcase"""
        super().setUp()
        defaults = self.create_defaults()
        annotation1 = factories.AnnotationModelFactory(name='annotation_1', **defaults)
        doc1 = factories.DocumentModelFactory(name='document_1', **defaults)

        self.created_models.extend([annotation1, doc1])
        self.annotation1 = annotation1
        self.doc1 = doc1
        self.create_request_data = [dict(document=doc1.id, annotation=annotation1.id)]


class DocumentAnnotationAPIPostTest(AbstractDocumentAnnotationApiTest):
    """Document annotation post test case"""

    url_name = 'document-annotation-crud-list'

    def test_post(self):
        # expect to create instance through api
        self.assert_create()

    def test_post_client_disabled(self):
        # expect to fail to create instance
        self.assert_post_client_disabled()

class DocumentAnnotationAPIListTest(AbstractDocumentAnnotationApiTest):
    """Document annotation list test case"""

    url_name = 'document-annotation-crud-list'

    def test_list(self):
        # expect to fetch instance list through api
        self.assert_list()

class DocumentAnnotationAPIRetrieveTest(AbstractDocumentAnnotationApiTest):
    """Document annotation retrieve  test case"""

    url_name = 'document-annotation-crud-detail'

    def test_retrieve(self):
        # expect to retrive the  instance
        self.assert_retrieve()

class DocumentAnnotationAPIPutTest(AbstractDocumentAnnotationApiTest):
    """Document annotation put test case"""

    url_name = 'document-annotation-crud-detail'

    def test_put(self):
        # expect to fail to update the  instance - update not supported
        response = self.assert_put(
            attr_name='document', attr_value=self.doc1.id,
            expected_status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.assertEqual(response.data['detail'], ANALYSIS_REQUIRED)

class DocumentAnnotationAPIPatchTest(AbstractDocumentAnnotationApiTest):
    """Document annotation patch test case"""

    url_name = 'document-annotation-crud-detail'

    def test_patch(self):
        # expect to fail to update the instance - update not supported
        response = self.assert_patch(
            attr_name='document', attr_value=self.doc1.id,
            expected_status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.assertEqual(response.data['detail'], ANALYSIS_REQUIRED)

class DocumentAnnotationAPIDeleteTest(AbstractDocumentAnnotationApiTest):
    """Document annotation delete test case"""

    url_name = 'document-annotation-crud-detail'

    def test_delete(self):
        # expect to delete the instance
        self.assert_delete()


class DocumentAnnotationAPIDeleteManyTest(AbstractDocumentAnnotationApiTest):
    """Document annotation delete many test case"""

    url_name = 'document-annotation-delete-many-list'

    def test_delete_many(self):
        # expect to delete many instances
        self.assert_delete_many()
