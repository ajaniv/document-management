"""
.. module:: ondalear.backend.tests.api.docmgmt.views.test_auxiliary_document
   :synopsis: Auxiliary document view unit test  module.

"""
import logging

from ondalear.backend.docmgmt.models import constants, AuxiliaryDocument
from ondalear.backend.api.docmgmt.views.document import summary_response_fields

from ondalear.backend.tests.docmgmt.models import factories
from ondalear.backend.tests.api.docmgmt.views.base_document import (
    AbstractDocumentApiTest, DocumentAnnotationMixin,
    DocumentFilterTestMixin, DocumentTagFilterTestMixin,
    FileUploadAssertMixin, FileUploadMixin)



_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors

class AbstractAuxiliaryDocumentApiTest(AbstractDocumentApiTest):
    """Base auxiliary document api test"""
    create_url_name = 'auxiliary-document-crud-list'
    model_class = AuxiliaryDocument
    tag_target = constants.CLASSIFICATION_TARGET_AUXILIARY_DOCUMENT
    category_target = constants.CLASSIFICATION_TARGET_AUXILIARY_DOCUMENT


class AuxiliaryDocumentAPIPostTest(AbstractAuxiliaryDocumentApiTest):
    """Auxiliary document post test case"""

    url_name = 'auxiliary-document-crud-list'

    def test_post(self):
        # expect to create instance through api
        self.assert_create()

    def test_post_client_disabled(self):
        # expect to fail to create instance
        self.assert_post_client_disabled()

class AuxiliaryDocumentAPIListTest(AbstractAuxiliaryDocumentApiTest):
    """Auxiliary document list test case"""
    url_name = 'auxiliary-document-crud-list'

    def test_list(self):
        # expect to fetch document list
        self.assert_list()

class AuxiliaryDocumentAPIRetrieveTest(AbstractAuxiliaryDocumentApiTest):
    """Auxiliary document retrieve test case"""

    url_name = 'auxiliary-document-crud-detail'

    def test_retrieve(self):
        # expect to retrive the document instance
        self.assert_retrieve()

class AuxiliaryDocumentAPIPutTest(AbstractAuxiliaryDocumentApiTest):
    """Auxiliary document put test case"""

    url_name = 'auxiliary-document-crud-detail'

    def test_put(self):
        # expect to update the document instance
        self.assert_put(attr_name='content', attr_value='new content')

class AuxiliaryDocumentAPIPatchTest(AbstractAuxiliaryDocumentApiTest):
    """CrAuxiliaryiteria document patch test case"""

    url_name = 'auxiliary-document-crud-detail'

    def test_patch(self):
        # expect to patch the document instance
        self.assert_patch(attr_name='name', attr_value='new_name')

class AuxiliaryDocumentAPIDeleteTest(AbstractAuxiliaryDocumentApiTest):
    """Auxiliary document delete test case"""

    url_name = 'auxiliary-document-crud-detail'

    def test_delete(self):
        # expect to delete the document instance
        self.assert_delete()


class AbstractAuxiliaryDocumnetUploadTest(FileUploadMixin,
                                          FileUploadAssertMixin,
                                          AbstractAuxiliaryDocumentApiTest):
    """Base auxiliary document file upload test case"""

class AuxiliaryDocumentFileUploadAPIPostTest(AbstractAuxiliaryDocumnetUploadTest):
    """Post file upload test"""
    url_name = 'auxiliary-document-crud-list'

    def test_post_file_upload(self):
        # expect to load the document
        self.assert_post_file_upload()

class AuxiliaryDocumentFileUploadAPIPutTest(AbstractAuxiliaryDocumnetUploadTest):
    """Put file upload test"""
    url_name = 'auxiliary-document-crud-detail'

    def test_put_file_upload(self):
        # expect to update the file
        self.assert_put_file_upload()

class AuxiliaryDocumentFileUploadAPIDeleteTest(AbstractAuxiliaryDocumnetUploadTest):
    """Delete file upload test"""
    url_name = 'auxiliary-document-crud-detail'

    def test_delete_file_upload(self):
        # expect to delete the document and associated file
        self.assert_delete_file_upload()

class AuxiliaryDocumentSummaryAPIListTest(AbstractAuxiliaryDocumentApiTest):
    """Auxiliary document summary list test case"""
    url_name = 'auxiliary-document-summary-list'

    def assert_list_item(self, data):
        """assert list item"""
        self.assert_is_set(data, summary_response_fields)

    def test_list(self):
        # expect to list documents through api
        self.assert_list()

class AuxiliaryDocumentAPIFilterTest(DocumentFilterTestMixin,
                                     AbstractAuxiliaryDocumentApiTest):
    """Auxiliary document list filter test case"""
    url_name = 'auxiliary-document-crud-list'

class AuxiliaryDocumentAPITagFilterTest(DocumentTagFilterTestMixin,
                                        AbstractAuxiliaryDocumentApiTest):
    """Auxiliary document tag list filter test case"""
    url_name = 'auxiliary-document-crud-list'
    tag_target = constants.CLASSIFICATION_TARGET_AUXILIARY_DOCUMENT
    document_type = constants.DOCUMENT_TYPE_AUXILIARY
    document_factory = factories.AuxiliaryDocumentModelFactory

    def setUp(self):
        """Setup test case

        Setting document tag association for tag related queries
        """
        super().setUp()
        self.prepare()

class DocumentAnnotationListTest(DocumentAnnotationMixin, AbstractAuxiliaryDocumentApiTest):
    """Document annotation list test"""
    url_name = 'auxiliary-document-crud-list'
    document_factory = factories.AuxiliaryDocumentModelFactory

    def setUp(self):
        """Setup test case"""
        super().setUp()
        self.prepare()
