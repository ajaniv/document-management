"""
.. module:: ondalear.backend.tests.api.docmgmt.views.test_reference_document
   :synopsis: Reference document view unit test  module.

"""
import logging

from ondalear.backend.docmgmt.models import constants, ReferenceDocument
from ondalear.backend.api.docmgmt.views.document import summary_response_fields
from ondalear.backend.tests.docmgmt.models import factories
from ondalear.backend.tests.api.docmgmt.views.base_document import (AbstractDocumentApiTest,
                                                                    DocumentAnnotationMixin,
                                                                    DocumentFilterTestMixin,
                                                                    DocumentTagFilterTestMixin,
                                                                    FileUploadMixin,
                                                                    FileUploadAssertMixin)
from .base_document import LinkedDocumentsMixin

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors


class AbstractReferenceDocumentApiTest(AbstractDocumentApiTest):
    """Base reference document api test"""
    create_url_name = 'reference-document-list'
    model_class = ReferenceDocument

    category_target = constants.CLASSIFICATION_TARGET_REFERENCE_DOCUMENT



class ReferenceDocumentAPIPostTest(AbstractReferenceDocumentApiTest):
    """Reference document post test case"""

    url_name = 'reference-document-list'

    def test_post(self):
        # expect to create document
        self.assert_create()

    def test_post_client_disabled(self):
        # expect to fail to create document
        self.assert_post_client_disabled()

class ReferenceDocumentAPIListTest(AbstractReferenceDocumentApiTest):
    """Reference document list test case"""
    url_name = 'reference-document-list'

    def test_list(self):
        # expect to list documents through api
        self.assert_list()

class ReferenceDocumentAPIRetrieveTest(AbstractReferenceDocumentApiTest):
    """Reference document retrieve test case"""

    url_name = 'reference-document-detail'

    def test_retrieve(self):
        # Expect to retrive the document instance
        self.assert_retrieve()

class ReferenceDocumentAPIPutTest(AbstractReferenceDocumentApiTest):
    """Reference document put test case"""

    url_name = 'reference-document-detail'

    def test_put(self):
        # Expect to update the document instance
        self.assert_put(attr_name='content', attr_value='new content')

class ReferenceDocumentAPIPatchTest(AbstractReferenceDocumentApiTest):
    """Reference document patch test case"""

    url_name = 'reference-document-detail'

    def test_patch(self):
        # Expect to patch the document instance
        self.assert_patch(attr_name='name', attr_value='new_name')

class ReferenceDocumentAPIDeleteTest(AbstractReferenceDocumentApiTest):
    """Reference document delete test case"""

    url_name = 'reference-document-detail'

    def test_delete(self):
        # Expect to destroy the document instance
        self.assert_delete()

class AbstractReferenceDocumnetUploadTest(FileUploadMixin,
                                          FileUploadAssertMixin,
                                          AbstractReferenceDocumentApiTest):
    """Base reference document file upload test case"""

class ReferenceDocumentFileUploadAPIPostTest(AbstractReferenceDocumnetUploadTest):
    """Post file upload test"""
    url_name = 'reference-document-list'

    def test_post_file_upload(self):
        # expect to load the document
        self.assert_post_file_upload()

class ReferenceDocumentFileUploadAPIPutTest(AbstractReferenceDocumnetUploadTest):
    """Put file upload test"""
    url_name = 'reference-document-detail'
    def test_put_file_upload(self):
        # expect to update the file
        self.assert_put_file_upload()

class ReferenceDocumentFileUploadAPIDeleteTest(AbstractReferenceDocumnetUploadTest):
    """Delete file upload test"""
    url_name = 'reference-document-detail'
    def test_delete_file_upload(self):
        # expect to delete the document and associated file
        self.assert_delete_file_upload()

class ReferenceDocumentSummaryAPIListTest(AbstractReferenceDocumentApiTest):
    """Reference document summary list test case"""
    url_name = 'reference-document-summary-list'

    def assert_list_item(self, data):
        """assert list item"""
        self.assert_is_set(data, summary_response_fields)

    def test_list(self):
        # expect to list documents through api
        self.assert_list()

class ReferenceDocumentAPIFilterTest(DocumentFilterTestMixin, AbstractReferenceDocumentApiTest):
    """Reference document list filter test case"""
    url_name = 'reference-document-list'

class ReferenceDocumentAPITagFilterTest(DocumentTagFilterTestMixin,
                                        AbstractReferenceDocumentApiTest):
    """Reference document tag list filter test case"""
    url_name = 'reference-document-list'
    tag_target = constants.CLASSIFICATION_TARGET_REFERENCE_DOCUMENT
    document_type = constants.DOCUMENT_TYPE_REFERENCE
    document_factory = factories.ReferenceDocumentModelFactory


    def setUp(self):
        """Setup test case

        Setting document tag association for tag related queries
        """
        super().setUp()
        self.prepare()

class DocumentAssociationListTest(LinkedDocumentsMixin, AbstractReferenceDocumentApiTest):
    """Document association list test with linked documents"""
    url_name = 'reference-document-list'

    def setUp(self):
        """Setup test case"""
        super().setUp()
        self.prepare()


    def test_list(self):
        # expect to list documents through api

        response = self.assert_list(documents=self.ref_doc)
        # verify that the linked document is returned and has the expected id
        self.assertEqual(response.data['detail'][0]['documents'], [self.aux_doc.document.id])


class DocumentAnnotationListTest(DocumentAnnotationMixin, AbstractReferenceDocumentApiTest):
    """Document annotation list test"""
    url_name = 'reference-document-list'
    document_factory = factories.ReferenceDocumentModelFactory

    def setUp(self):
        """Setup test case"""
        super().setUp()
        self.prepare()
