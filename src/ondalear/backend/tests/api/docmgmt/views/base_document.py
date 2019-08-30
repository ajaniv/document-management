"""
.. module:: ondalear.backend.tests.api.docmgmt.views.base
   :synopsis: docmgmt api views base  unittest module.


"""
import os
import ntpath
import logging
from datetime import timedelta
from copy import deepcopy

from django.conf import settings
from django.core.files import File
from django.urls import reverse
from rest_framework import status

from ondalear.backend.core.python.utils import file_exists, module_directory, remove, utc_now
from ondalear.backend.docmgmt.models import constants
from ondalear.backend.tests.docmgmt.models import factories
from .base import AbstractDocMgmtAPITestCase, AssertMixin

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,too-many-ancestors,attribute-defined-outside-init,missing-docstring

def test_data_file_path(file_name):
    """construct test data file path"""
    data_dir = os.path.join(module_directory(__file__), "data")
    return os.path.join(data_dir, file_name)

def uploaded_file_path(file_name, client_id, username):
    """construct uploaded file path"""
    return os.path.join(settings.MEDIA_ROOT, client_id, username, file_name)

class DocumentAssertMixin(AssertMixin):
    """Assert Mixin class"""
    def extract_object_id(self, data): # pylint: disable=no-self-use
        """extract object id"""
        object_id = data.get('id')
        if not object_id:
            object_id = data['document']['id']
        return object_id

    def assert_is_set(self, data, keys):
        """verify data[key] has value"""
        try:
            new_keys = keys.pop('document')
            new_keys = list(new_keys)
            for key in keys:
                new_keys.append(key)
            keys = new_keys
        except (AttributeError, KeyError):
            pass
        super().assert_is_set(data, keys)

    def assert_response_detail(self, data, expected=None):
        """Assert response detail"""
        # check equality
        expected = expected or self.expected_data()
        try:
            document = expected.pop('document')
            expected.update(document)
            # stripping the purpose which was used for the doc->doc request
            documents = expected.pop('documents')
            expected['documents'] = [documents[0][0]]
        except KeyError:
            pass
        super().assert_response_detail(data, expected)

    def assert_create(self, expected_status=None, request_data=None, fmt=None):
        """verify create  model instance"""
        request_data = request_data or self.create_data().copy()
        try:
            document = request_data.pop('document')
            request_data.update(document)
        except KeyError:
            pass
        return super().assert_create(expected_status, request_data, fmt)

    def assert_update_time_gte(self):
        """expect to fetch document list"""
        now = utc_now() - timedelta(minutes=1)
        date_str = now.strftime(self.datetime_format)
        self.assert_list(query_str=f'document__update_time__gte={date_str}')

    def assert_update_time_lte(self):
        """ expect to fetch document list"""
        # 2019-07-21+00:00:00

        now = utc_now() + timedelta(minutes=1)
        date_str = now.strftime(self.datetime_format)

        self.assert_list(query_str=f'document__update_time__lte={date_str}')

    def assert_update_time_range(self):
        """ expect to fetch document list"""
        # 2019-07-21+00:00:00
        now = utc_now()
        upper = now + timedelta(minutes=1)
        lower = now - timedelta(minutes=1)
        lower_str = lower.strftime(self.datetime_format)
        upper_str = upper.strftime(self.datetime_format)

        lower = f'document__update_time__gte={lower_str}'
        upper = f'document__update_time__lte={upper_str}'
        self.assert_list(query_str=f'{lower}&{upper}')

    def assert_tags_exact(self):
        """expect to fetch document list"""
        tag_id = self.tag.id
        query_str = f'document__tags__in={tag_id}'
        self.assert_list(query_str=query_str, documents=[self.doc1])

    def assert_tags_missing(self):
        """ expect to fail to fetch document list"""
        self.assert_list(query_str='document__tags__in=100',
                         expected_count=0,
                         documents=[self.doc1])

    def assert_tags_in(self):
        """expect to fetch document list"""
        tag_id = self.tag.id
        query_str = f'document__tags__in={tag_id},100,200'
        self.assert_list(query_str=query_str, documents=[self.doc1])


class FileUploadMixin:
    """File upload mixin class"""
    source_file_name = "source_one.txt"
    response_no_values = ('dir_path',)

    def setUp(self):
        """Setup test case"""
        super().setUp()
        has_values = self.response_has_values.copy()
        has_values.update({'upload':True})
        self.response_has_values = has_values

    def expected_data(self):
        """return expected data"""
        data = deepcopy(self.create_request_data)
        del data['content']
        data['document']['name'] = self.source_file_name
        return data

    def create_data(self):
        """create data"""
        data = deepcopy(self.create_request_data)
        del data['content']
        data['upload'] = File(open(test_data_file_path(self.source_file_name)))
        data['document']['name'] = self.source_file_name
        return data

    def remove_files(self, paths):
        """remove files"""
        for file_name in paths:
            file_path = uploaded_file_path(
                file_name,
                self.ondalear_client.client_id,
                self.user.username)
            if file_exists(file_path):
                remove(file_path)

class FileUploadAssertMixin:
    """File upload assert mixin class"""
    def assert_post_file_upload(self):
        """expect to load the document"""
        try:
            response = self.assert_create(fmt='multipart')
            detail = response.data['detail']
            if 'upload' in detail:
                self.assertEqual(
                    ntpath.basename(response.data['detail']['upload']),
                    self.source_file_name)
        finally:
            self.remove_files((self.source_file_name,))

    def assert_put_file_upload(self):
        """expect to update the document"""
        source_file_name = "source_two.txt"
        try:
            # create document
            create_response = self.assert_create(fmt='multipart')
            instance = create_response.data['detail']
            object_id = instance['id']
            url = reverse(self.url_name, args=[object_id])

            # fetching the complete data for instance
            get_response = self.client.get(url)
            put_data = get_response.data['detail']

            # prepare the put request data
            for key in ('content', 'dir_path'):
                del put_data[key]
            put_data['name'] = source_file_name
            put_data['upload'] = File(open(test_data_file_path(source_file_name)))

            # make put api request
            put_response = self.client.put(url, data=put_data, format='multipart')
            self.assertEqual(put_response.status_code, status.HTTP_200_OK, f'{put_response.data}')

            # fetching the updated instance again
            get_response = self.client.get(url)
            get_data = get_response.data['detail']
            self.assertEqual(
                ntpath.basename(get_data['upload']),
                source_file_name)
        finally:
            self.remove_files((self.source_file_name, source_file_name))

    def assert_delete_file_upload(self):
        """expect to delete the document and associated file"""
        try:
            # create document
            create_response = self.assert_create(fmt='multipart')
            instance = create_response.data['detail']
            object_id = instance['id']
            url = reverse(self.url_name, args=[object_id])

            # make delete  api request
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK, f'{response.data}')
            
            self.assertEqual(response.data['detail'], dict(count_deleted=2)) # includes underlying
            file_path = uploaded_file_path(
                self.source_file_name,
                self.ondalear_client.client_id,
                self.user.username)
            self.assertFalse(file_exists(file_path))

        finally:
            self.remove_files((self.source_file_name,))

class AbstractDocumentApiTest(DocumentAssertMixin, AbstractDocMgmtAPITestCase):
    """Base  document api test"""

    datetime_format = '%Y-%m-%d+%H:%M:%S'
    response_has_values = {
        'document': (
            'client', 'creation_time',
            'creation_user', 'effective_user',
            'id', 'site', 'update_time',
            'update_user', 'uuid', 'version',
            'is_deleted', 'is_enabled')
    }
    create_request_data = {
        'document': {
            'description': 'some description',
            'language': 'en-us',
            'name': 'document_1',
            'title': 'Document One title',
        },
        'content': 'document one  content',
    }
    response_no_values = (
        'upload', 'dir_path'
        )

    def setUp(self):
        """testcase setup"""
        super(AbstractDocumentApiTest, self).setUp()
        category = factories.CategoryModelFactory(name='category_1',
                                                  target=self.category_target,
                                                  domain=constants.CLASSIFICATION_DOMAIN_GENERAL)

        self.create_request_data['document']['category'] = category.id

        self.category = category
        self.created_models.extend([category])


class DocumentFilterTestMixin:
    """Document filter test mixin class"""

    def test_name_exact(self):
        # expect to fetch document list
        self.assert_list(query_str='document__name=document_1')

    def test_name_exact_missing(self):
        # expect to fail to fetch document list
        self.assert_list(query_str='document__name=document_2', expected_count=0)

    def test_name_starts_with(self):
        # expect to fetch document list
        self.assert_list(query_str='document__name__startswith=document_')

    def test_name_in(self):
        # expect to fetch document list
        self.assert_list(query_str='document__name__in=document_1,document_2')

    def test_update_time_gte(self):
        # expect to fetch document list
        self.assert_update_time_gte()

    def test_update_time_lte(self):
        # expect to fetch document list
        self.assert_update_time_lte()

    def test_update_time_range(self):
        # expect to fetch document list
        self.assert_update_time_range()

    def test_category_name_exact(self):
        # expect to fetch documents
        self.assert_list(query_str='document__category__name=category_1')

    def test_category_name_exact_missing(self):
        # expect to fail to fetch document list
        self.assert_list(query_str='document__category__name=category_2', expected_count=0)

    def test_category_name_in(self):
        # expect to fetch document list
        self.assert_list(query_str='document__category__name__in=category_1,category_2')

class DocumentTagFilterTestMixin:
    """Document tag filter test mixin class"""

    def create_tags(self, defaults):
        tag = factories.TagModelFactory(name='tag_1',
                                        target=self.tag_target,
                                        domain=constants.CLASSIFICATION_DOMAIN_GENERAL,
                                        **defaults)
        # created to verify multiple tag support
        tag_dummy = factories.TagModelFactory(name='dummy_tag',
                                              target=self.tag_target,
                                              domain=constants.CLASSIFICATION_DOMAIN_GENERAL,
                                              **defaults)
        self.tag = tag
        self.tag_dummy = tag_dummy
        self.created_models.extend([tag, tag_dummy])
        return tag, tag_dummy

    def create_document(self, defaults):
        """create document"""
        # prepare the document data so that response comparison work
        create_request_data = deepcopy(self.create_request_data)
        doc_name = 'document_tag_1'
        document_data = create_request_data['document']
        document_data['name'] = doc_name

        # cannot create with category which is not an instance
        category = document_data.pop('category')
        document = factories.DocumentModelFactory(
            document_type=self.document_type,
            category=self.category,
            **document_data, **defaults)
        document_data['category'] = category
        return document, create_request_data

    def prepare(self):
        """prepare for test case execuition"""
        defaults = self.create_defaults()

        tag, _ = self.create_tags(defaults)

        # create reference document
        document, create_request_data = self.create_document(defaults)

        doc1 = self.document_factory(document=document,
                                     content=create_request_data['content'])

        # create document tag association - will be deleted when document is deleted
        doc_tag = factories.DocumentTagModelFactory(
            document=document, tag=tag,
            **defaults)

        self.doc1 = doc1
        self.doc_tag = doc_tag

        self.create_request_data = create_request_data
        self.created_models.extend([doc1.document])

    def test_tags_exact(self):
        # expect to fetch document list
        self.assert_tags_exact()

    def test_tags_missing(self):
        # expect to fail to fetch document list
        self.assert_tags_missing()

    def test_tags_in(self):
        # expect to fetch document list
        self.assert_tags_in()


class LinkedDocumentsMixin:
    """Linked documents mixin class"""

    def create_linked_documents(self, defaults=None):
        """create linked documents"""

        defaults = defaults or self.create_defaults()
        # populating the ref document with data to ensure that the verification aftr the
        #   request does not fail.
        create_data = self.create_request_data
        if create_data:
            doc_data = self.create_request_data['document']
            content = create_data['content']
        else:
            doc_data = dict(name='ref_doc', title='ref doc title', description='ref doc desc')
            content = 'ref data content'
        doc1 = factories.DocumentModelFactory(name=doc_data['name'],
                                              title=doc_data['title'],
                                              description=doc_data['description'],
                                              **defaults)
        ref_doc = factories.ReferenceDocumentModelFactory(
            content=content, document=doc1)
        doc2 = factories.DocumentModelFactory(name='aux_document_1', **defaults)
        aux_doc = factories.AuxiliaryDocumentModelFactory(
            content='what is your name', document=doc2)

        self.created_models.extend([doc1, doc2])
        self.aux_doc = aux_doc
        self.ref_doc = ref_doc
        return ref_doc, aux_doc

    def prepare(self):
        defaults = self.create_defaults()

        ref_doc, aux_doc = self.create_linked_documents(defaults)

        purpose = constants.DOCUMENT_ASSOCIATION_PURPOSE_QUESTION
        doc_association = factories.DocumentAssociationModelFactory(from_document=ref_doc.document,
                                                                    to_document=aux_doc.document,
                                                                    purpose=purpose,
                                                                    **defaults)
        # association will be deleted when document is deleted
        self.doc_association = doc_association

        return ref_doc, aux_doc, doc_association

class DocumentAnnotationMixin:
    """Document annotation mixin class"""

    def prepare(self):
        """create document annotation test environment"""
        defaults = self.create_defaults()

        create_data = self.create_request_data
        if create_data:
            doc_data = self.create_request_data['document']
            content = create_data['content']
        else:
            doc_data = dict(name='annotation_doc',
                            title='annotation doc title',
                            description='annotation doc desc')
            content = 'annotation data content'
        underlying_doc = factories.DocumentModelFactory(name=doc_data['name'],
                                                        title=doc_data['title'],
                                                        description=doc_data['description'],
                                                        **defaults)
        containing_doc = self.document_factory(content=content, document=underlying_doc)
        annotation = factories.AnnotationModelFactory(name='annotation_1', **defaults)
        document_annotation = factories.DocumentAnnotationModelFactory(document=underlying_doc,
                                                                       annotation=annotation,
                                                                       **defaults)
        # when underlying doc is deleted, the associated containing doc and document
        #   annotation will be deleted
        self.created_models.extend([underlying_doc, annotation])
        self.containing_doc = containing_doc
        self.document_annotation = document_annotation
        return document_annotation

    def test_list(self):
        # expect to list documents through api

        response = self.assert_list(documents=self.containing_doc)
        # verify that the associated annotation is returned and has the expected id

        self.assertEqual(
            response.data['detail'][0]['annotations'],
            [self.document_annotation.annotation.id])
