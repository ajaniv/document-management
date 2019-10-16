"""
.. module:: ondalear.backend.docmgmt.models.derived_document
   :synopsis: derived document model unit test module.


"""
import os
import logging

from django.conf import settings
from django.core.files import File
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError


from ondalear.backend.core.python.utils import file_exists, module_directory, remove
from ondalear.backend.tests.base_models import AbstractModelTestCase
from . import factories

_logger = logging.getLogger(__name__)


def test_data_file_path(file_name):
    """build test data file path"""
    data_dir = os.path.join(module_directory(__file__), "data")
    return os.path.join(data_dir, file_name)

# pylint: disable=too-many-locals,no-member,missing-docstring,no-self-use,too-many-ancestors

class DerivedDocumentCRUDMixin:
    """Derived document crud mixing class"""

    def assert_crud(self):
        """Verify document crud operations"""

        document_factory = self.document_factory_class
        derived_factory = self.derived_document_factory_class

        document_model = document_factory.model_class()
        derived_model = derived_factory.model_class()

        # create document instance
        name = "document_one"
        document = document_factory(name=name)

        # verify it was created and saved
        self.assertIsNotNone(document.id)
        self.assertEqual(document.name, name)

        # create the derived document
        derived_document = derived_factory(document=document, content="sample content")

        # verify it was created and saved
        self.assertIsNotNone(derived_document.document_id)

        new_content = 'new content'
        derived_document.content = new_content
        derived_document.save()

        # verify update
        assert derived_model.objects.get(pk=derived_document.document_id).content == new_content

        # delete the document instance
        deleted = document.delete()

        # verify deletion of document and associated tags and derived document
        self.assertEqual(deleted[0], 2)
        try:
            document_model.objects.get(pk=document.id)
        except document_model.DoesNotExist:
            pass
        try:
            derived_model.objects.get(pk=derived_document.document_id)
        except derived_document.DoesNotExist:
            pass


class FileUploadAssertMixin:
    """File upload mixin class"""

    def assert_uploaded_instance(self, dir_path=None):
        """verify creation of  uploaded file instance"""
        # upload file
        file_name = self.file_name
        test_file = File(open(test_data_file_path(file_name)))
        name = file_name
        document = factories.DocumentModelFactory(name=name)
        derived_document = self.derived_document_factory_class(
            content="",
            document=document,
            upload=test_file,
            dir_path=dir_path)
        # verify it was saved
        assert derived_document.document_id
        if dir_path:
            uploaded_file_path = os.path.join(
                settings.MEDIA_ROOT,
                derived_document.document.client.client_id,
                derived_document.document.effective_user.username,
                dir_path,
                file_name)
        else:
            uploaded_file_path = os.path.join(
                settings.MEDIA_ROOT,
                derived_document.document.client.client_id,
                derived_document.document.effective_user.username,
                file_name)
        assert file_exists(uploaded_file_path)
        with(open(uploaded_file_path)) as test_file:
            lines = test_file.readlines()
            assert lines

        return document, derived_document, uploaded_file_path, test_file

    def assert_upload(self):
        """Expect to upload a file to the system designated location"""

        uploaded_file_path = test_file = None
        try:
            (document, _,
             uploaded_file_path,
             test_file) = self.assert_uploaded_instance(dir_path='test_dir/sub_dir')
            # delete the instance
            deleted = document.delete()
            # verify deletion (document and derived document are deleted)
            assert deleted[0] == 2
        finally:
            # cleanup
            if test_file:
                test_file.close()
            if uploaded_file_path and file_exists(uploaded_file_path):
                remove(uploaded_file_path)

    def assert_no_data(self):
        """expect to fail to save as both content and upload are not set"""
        with self.assertRaises(ValidationError):
            self.derived_document_factory_class(content=None, upload=None)

    def assert_content_upload_set(self):
        """ expect to fail to save as both content and upload are not set"""
        with self.assertRaises(ValidationError):
            file_name = self.file_name
            test_file = File(open(test_data_file_path(file_name)))
            self.derived_document_factory_class(content='value', upload=test_file)

    def assert_duplicate_upload(self):
        """expect to fail to save as upload(file path) exists"""
        uploaded_file_path = test_file = None
        try:
            document, _, uploaded_file_path, test_file = self.assert_uploaded_instance()
            try:
                with transaction.atomic():
                    file_name = self.file_name
                    test_file = File(open(test_data_file_path(file_name)))
                    self.derived_document_factory_class(content=None, upload=test_file)
                    assert False, 'no integrity error'
            except IntegrityError:
                pass

            # delete the instance
            deleted = document.delete()
            # verify deletion (document and derived document are deleted)
            assert deleted[0] == 2
        finally:
            # cleanup
            if test_file:
                test_file.close()
            if uploaded_file_path and file_exists(uploaded_file_path):
                remove(uploaded_file_path)

class DerivedDocumentModelTestMixin:
    """Derived document model mixin class"""
    def test_crud(self):
        # Expect to create, update, fetch, and delete client
        self.assert_crud()

    def test_upload(self):
        # Expect to upload a file to the system designated location
        self.assert_upload()

    def test_no_data(self):
        # expect to fail to save as both content and upload are not set
        self.assert_no_data()

    def test_content_upload_set(self):
        # expect to fail to save as both content and upload are not set
        self.assert_content_upload_set()


class AbstractDerivedDocumentModelTest(DerivedDocumentCRUDMixin,
                                       FileUploadAssertMixin,
                                       AbstractModelTestCase):
    """Base class for derived document tests"""
    file_name = 'data.txt'
