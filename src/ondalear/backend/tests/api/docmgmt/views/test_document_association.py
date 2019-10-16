"""
.. module:: ondalear.backend.tests.api.docmgmt.views.test_document_association
   :synopsis: Document association view unit test module.


"""
import logging
from rest_framework import status

from ondalear.backend.docmgmt.models import constants
from ondalear.backend.api.constants import ANALYSIS_REQUIRED
from ondalear.backend.tests.base_factories import model_class
from ondalear.backend.tests.docmgmt.models import factories
from ondalear.backend.tests.api.model_viewset  import AbstractModelViewsetTestCase
from .base_document import LinkedDocumentsMixin

logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors

_factory_class = factories.DocumentAssociationModelFactory

class AbstractDocumentAssociationApiTest(LinkedDocumentsMixin, AbstractModelViewsetTestCase):
    """Base document tag  api test"""
    create_url_name = 'document-association-crud-list'

    factory_class = _factory_class
    model_class = model_class(_factory_class)

    create_request_data = []
    response_no_values = tuple()

    def setUp(self):
        """Setup testcase"""
        super().setUp()

        ref_doc, aux_doc = self.create_linked_documents()
        purpose = constants.DOCUMENT_ASSOCIATION_PURPOSE_QUESTION
        self.create_request_data = [dict(from_document=ref_doc.document.id,
                                         to_document=aux_doc.document.id,
                                         purpose=purpose)]

class DocumentAssociationAPIPostTest(AbstractDocumentAssociationApiTest):
    """Document association post test case"""

    url_name = 'document-association-crud-list'

    def test_post(self):
        # expect to create instance through api
        self.assert_create()

    def test_post_client_disabled(self):
        # expect to fail to create instance
        self.assert_post_client_disabled()

class DocumentAssociationAPIListTest(AbstractDocumentAssociationApiTest):
    """Document association list test case"""

    url_name = 'document-association-crud-list'

    def test_list(self):
        # expect to fetch document tag list through api
        self.assert_list()

class DocumentAssociationAPIRetrieveTest(AbstractDocumentAssociationApiTest):
    """Document association retrieve  test case"""

    url_name = 'document-association-crud-detail'

    def test_retrieve(self):
        # expect to retrive the document tag instance
        self.assert_retrieve()

class DocumentAssociationAPIPutTest(AbstractDocumentAssociationApiTest):
    """Document association put test case"""

    url_name = 'document-association-crud-detail'

    def test_put(self):
        # expect to fail to update the document tag  instance - update not supported
        response = self.assert_put(attr_name='document',
                                   attr_value=self.ref_doc.document.id,
                                   expected_status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.assertEqual(response.data['detail'], ANALYSIS_REQUIRED)

class DocumentAssociationAPIPatchTest(AbstractDocumentAssociationApiTest):
    """Document association patch test case"""

    url_name = 'document-association-crud-detail'

    def test_patch(self):
        # expect to fail to update the document tag  instance - update not supported
        response = self.assert_patch(attr_name='document',
                                     attr_value=self.ref_doc.document.id,
                                     expected_status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.assertEqual(response.data['detail'], ANALYSIS_REQUIRED)

class DocumentAssociationAPIDeleteTest(AbstractDocumentAssociationApiTest):
    """Document association delete test case"""

    url_name = 'document-association-crud-detail'

    def test_delete(self):
        # expect to delete the instance
        self.assert_delete()


class DocumentAssociationAPIDeleteManyTest(AbstractDocumentAssociationApiTest):
    """Document association delete many test case"""

    url_name = 'document-association-delete-many-list'

    def test_delete_many(self):
        # expect to delete many instances
        self.assert_delete_many()
