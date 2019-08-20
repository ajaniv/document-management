"""
.. module:: ondalear.backend.docmgmt.models.test_document
   :synopsis: AuxiliaryDocument model unit test module.

"""
import logging

from ondalear.backend.docmgmt.models import constants
from . import factories
from .base import AbstractModelTestCase

_logger = logging.getLogger(__name__)

# pylint: disable=missing-docstring,no-self-use,no-member

class DocumentCRUDMixin:
    """document crud mixing class"""

    def assert_create(self, **kwargs):
        """verify creation"""
        # create document instance
        defaults = dict(name='document_one')
        defaults.update(kwargs)
        document = self.document_factory(**defaults)

        # verify it was created and saved
        self.assertIsNotNone(document.id)
        for key, value in defaults.items():
            self.assertEqual(getattr(document, key), value)
        return document

    def assert_fetch(self, document):
        """verify fetch"""
        # fetch the instance
        fetched = document.__class__.objects.get(pk=document.id)
        assert fetched
        # verify the category
        assert fetched.category.name
        return fetched

    def assert_update(self, document):
        """verify update"""
        # update the instance
        new_name = 'New Name'
        document.name = new_name
        document.save()

        # verify update
        assert document.__class__.objects.get(pk=document.id).name == new_name
        return document

    def assert_tag(self, document):
        # create document tag association
        tag_name = 'tag_one'
        tag = self.tag_factory(name=tag_name)
        tag_association = self.document_tag_factory(document=document, tag=tag)
        assert tag_association

        # verify document tag association
        fetched = document.__class__.objects.prefetch_related('tags').get(pk=document.id)
        self.assertEqual(fetched.tags.count(), 1)
        for fetched_tag in fetched.tags.all():
            self.assertEqual(fetched_tag.name, tag_name)

        return fetched, tag

    def assert_annotation(self, document):
        """verify annotation"""
        # create document annotation association
        annotation_name = 'annotation_one'
        annotation = self.annotation_factory(name=annotation_name, annotation='some annotation')
        annotation_association = self.document_annotation_factory(document=document,
                                                                  annotation=annotation)
        assert annotation_association

        # verify document annotation association
        fetched = document.__class__.objects.prefetch_related('annotations').get(pk=document.id)
        self.assertEqual(fetched.annotations.count(), 1)
        for fetched_annotation in fetched.annotations.all():
            self.assertEqual(fetched_annotation.name, annotation_name)

        return fetched, annotation

    def assert_doc_to_doc_association(self, from_document):
        """verify document to document association"""
        # create document  association
        to_document_name = 'to_document'
        to_document = self.assert_create(name=to_document_name)
        document_association = self.doc_to_doc_association_factory(
            from_document=from_document,
            to_document=to_document,
            purpose=constants.DOCUMENT_ASSOCIATION_PURPOSE_QUESTION)
        assert document_association

        # verify document association
        fetched = from_document.__class__.objects.prefetch_related('documents').get(
            pk=from_document.id)
        self.assertEqual(fetched.documents.count(), 1)
        for fetched_document in fetched.documents.all():
            self.assertEqual(fetched_document.name, to_document_name)

        return fetched, to_document

    def assert_delete_document(self, document, to_document):
        """verify document deletion"""
        # delete the document instance
        deleted = document.delete()

        # verify deletion of document and associated tags, annotations, document association
        self.assertEqual(deleted[0], 4)
        try:
            document.__class__.objects.get(pk=document.id)
        except document.__class__.DoesNotExist:
            pass

        deleted = to_document.delete()
        self.assertEqual(deleted[0], 1)

    def assert_delete_tag(self, document, tag):
        """verify tag deletion"""
        # verify that the tag has not been deleted
        tag_instance = tag.__class__.objects.get(pk=tag.id)
        assert tag_instance

        # delete all tag document associations
        document_tag_model = self.document_tag_factory.model_class()
        deleted = document_tag_model.objects.filter(document=document,
                                                    tag=tag).delete()
        self.assertEqual(deleted[0], 0)

        # delete the tag
        deleted = tag_instance.delete()
        self.assertEqual(deleted[0], 1)

    def assert_delete_annotation(self, document, annotation):
        """verify annotation deletion"""

        # verify that the annotation has not been deleted
        annotation_instance = annotation.__class__.objects.get(pk=annotation.id)
        assert annotation_instance

        # delete all annotation document associations
        document_annotation_model = self.document_annotation_factory.model_class()
        deleted = document_annotation_model.objects.filter(document=document,
                                                           annotation=annotation).delete()
        self.assertEqual(deleted[0], 0)

        # delete the annotation
        deleted = annotation_instance.delete()
        self.assertEqual(deleted[0], 1)


class DocumentModelCRUDTests(DocumentCRUDMixin, AbstractModelTestCase):
    """Auxiliary document  model basic lifecycle test case"""
    document_factory = factories.DocumentModelFactory
    tag_factory = factories.TagModelFactory
    document_tag_factory = factories.DocumentTagModelFactory
    annotation_factory = factories.AnnotationModelFactory
    document_annotation_factory = factories.DocumentAnnotationModelFactory
    doc_to_doc_association_factory = factories.DocumentAssociationModelFactory


    def test_create(self):
        # expect to create instance
        document = self.assert_create()
        document.delete()

    def test_fetch(self):
        # expect to fetch instance
        document = self.assert_create()
        self.assert_fetch(document)
        document.delete()

    def test_update(self):
        # expect to update instance
        document = self.assert_create()
        self.assert_update(document)
        document.delete()

    def test_document_tag(self):
        # expect to create document tag association
        document = self.assert_create()
        fetched, tag = self.assert_tag(document)
        deleted = fetched.delete()
        self.assertEqual(deleted[0], 2) # document and the tag association
        self.assert_delete_tag(document, tag)

    def test_document_annotation(self):
        # expect to create document annotation association
        document = self.assert_create()
        fetched, annotation = self.assert_annotation(document)
        deleted = fetched.delete()
        self.assertEqual(deleted[0], 2) # document and the tag annotation
        self.assert_delete_annotation(document, annotation)

    def test_doc_to_doc_association(self):
        # expect to create document -> document association
        document = self.assert_create()
        fetched, to_document = self.assert_doc_to_doc_association(document)
        deleted = fetched.delete()
        self.assertEqual(deleted[0], 2) # document and the doc association
        deleted = to_document.delete()
        self.assertEqual(deleted[0], 1)
    