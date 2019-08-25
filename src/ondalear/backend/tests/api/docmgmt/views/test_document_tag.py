"""
.. module:: ondalear.backend.tests.api.docmgmt.views.test_document_tag
   :synopsis: Document tag view unit test module.


"""
import logging
from rest_framework import status

from ondalear.backend.docmgmt.models import constants
from ondalear.backend.api.constants import ANALYSIS_REQUIRED

from ondalear.backend.tests.docmgmt.models import factories
from .base import AbstractDocMgmtAPITestCase

logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors
_factory_class = factories.DocumentTagModelFactory

class AbstractDocumentTagApiTest(AbstractDocMgmtAPITestCase):
    """Base document tag  api test"""
    create_url_name = 'document-tag-list'

    factory_class = _factory_class
    model_class = factories.model_class(_factory_class)
    create_request_data = []
    response_no_values = tuple()

    def setUp(self):
        """Setup testcase"""
        super().setUp()

        target = constants.CLASSIFICATION_TARGET_REFERENCE_DOCUMENT
        defaults = self.create_defaults()
        tag1 = factories.TagModelFactory(
            name='tag_1', parent=None, target=target, **defaults)
        doc1 = factories.DocumentModelFactory(
            name='document_1', **defaults)

        self.created_models.extend([tag1, doc1])
        self.tag1 = tag1
        self.doc1 = doc1
        self.create_request_data = [dict(document=doc1.id, tag=tag1.id)]


class DocumentTagAPIPostTest(AbstractDocumentTagApiTest):
    """Document tag post test case"""

    url_name = 'document-tag-list'

    def test_post(self):
        # expect to create instance through api
        self.assert_create()

    def test_post_client_disabled(self):
        # expect to fail to create instance
        self.assert_post_client_disabled()

class DocumentTagAPIListTest(AbstractDocumentTagApiTest):
    """Document tag list test case"""

    url_name = 'document-tag-list'

    def test_list(self):
        # expect to fetch document tag list through api
        self.assert_list()

class DocumentTagAPIRetrieveTest(AbstractDocumentTagApiTest):
    """Document tag retrieve  test case"""

    url_name = 'document-tag-detail'

    def test_retrieve(self):
        # expect to retrive the document tag instance
        self.assert_retrieve()

class DocumentTagAPIPutTest(AbstractDocumentTagApiTest):
    """Document tag put test case"""

    url_name = 'document-tag-detail'

    def test_put(self):
        # expect to fail to update the document tag  instance - update not supported
        response = self.assert_put(attr_name='document',
                                   attr_value=self.doc1.id,
                                   expected_status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.assertEqual(response.data['detail'], ANALYSIS_REQUIRED)

class DocumentTagAPIPatchTest(AbstractDocumentTagApiTest):
    """Document tag patch test case"""

    url_name = 'document-tag-detail'

    def test_patch(self):
        # expect to fail to update the document tag  instance - update not supported
        response = self.assert_patch(attr_name='document',
                                     attr_value=self.doc1.id,
                                     expected_status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.assertEqual(response.data['detail'], ANALYSIS_REQUIRED)

class DocumentTagAPIDeleteTest(AbstractDocumentTagApiTest):
    """Document tag delete test case"""

    url_name = 'document-tag-detail'

    def test_delete(self):
        # expect to delete the instance
        self.assert_delete()


class DocumentTagAPIDeleteManyTest(AbstractDocumentTagApiTest):
    """Document tag delete many test case"""

    url_name = 'document-tag-delete-many'

    def test_delete_many(self):
        # expect to delete many instances
        self.assert_delete_many()
