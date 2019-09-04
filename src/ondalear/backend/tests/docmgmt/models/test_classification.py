"""
.. module:: ondalear.backend.tests.docmgmt.models.test_classification
   :synopsis: Classification model unit test  module.


"""
import logging
from django.core.exceptions import ValidationError

from .base import ClassCRUDMixin
from . import factories
from .base  import AbstractModelTestCase

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,no-self-use,missing-docstring,too-many-ancestors

class AbstractClassificationModelCRUDTests(ClassCRUDMixin, AbstractModelTestCase):
    """Abstract classification model basic lifecycle test case"""


    def assert_persisted_parent(self):
        """verify that parent foreign key can be handled"""
        factory_class = self.factory_class
        instance = factory_class(name=self.name)
        # verify that invalid parent is not allowed
        parent = factory_class(name='root')
        instance.parent = parent
        instance.save()
        assert instance.parent.id == parent.id

    def assert_shallow_chain(self):
        """verify that chain is valid"""
        factory_class = self.factory_class
        instance = factory_class(name=self.name)
        root = factory_class(name='root')
        intermediate = factory_class(name='intermediate')
        intermediate.parent = root
        intermediate.save()
        instance.parent = intermediate
        instance.save()

    def assert_not_persisted_parent(self):
        """verify that a parent has to be persisted"""
        factory_class = self.factory_class
        instance = factory_class(name=self.name)
        # verify that invalid parent is not allowed
        parent = factory_class(name='root')
        parent.delete()
        with self.assertRaises(ValidationError):
            instance.parent = parent
            instance.save()

    def assert_circular_reference(self):
        """verify no circular references exist"""
        factory_class = self.factory_class
        instance = factory_class(name=self.name)
        with self.assertRaises(ValidationError):
            instance.parent = instance
            instance.save()

    def assert_duplicate_parent_name(self):
        """verify that a parent and child have unique names"""
        factory_class = self.factory_class

        instance = factory_class(name=self.name)
        # verify that invalid parent is not allowed
        parent = factory_class(name=self.name)

        with self.assertRaises(ValidationError):
            instance.parent = parent
            instance.save()


class ClassificationModelTestMixin:
    """classification model test mixin class"""
    def test_crud(self):
        # expect crud operations to succeed
        self.assert_crud(update_field_name='name', update_field_value=self.new_name, name=self.name)

    def test_pesisted_parent(self):
        # expect save operation to succeed
        self.assert_persisted_parent()

    def test_shallow_chain(self):
        # expect save operation to succeed
        self.assert_shallow_chain()

    def test_not_persistend_parent(self):
        # expect save operation to fail
        self.assert_not_persisted_parent()

    def test_circular_reference(self):
        # expect save operation to fail
        self.assert_circular_reference()

    def test_duplicate_parent_name(self):
        # expect save operation to fail
        self.assert_duplicate_parent_name()


class TagModelCRUDTests(ClassificationModelTestMixin, AbstractClassificationModelCRUDTests):
    """Tag model basic lifecycle test case"""

    factory_class = factories.TagModelFactory
    name = 'tag_one'
    new_name = 'new_tag_one'


class CategoryModelCRUDTests(ClassificationModelTestMixin, AbstractClassificationModelCRUDTests):
    """Category document tag model basic lifecycle test case"""

    factory_class = factories.CategoryModelFactory
    name = 'category_one'
    new_name = 'new_category_one'

class TestMixedHierarchy(AbstractModelTestCase):
    """Invalid class tree test case"""
    def test_invalid_parent_class(self):
        # expect to fail
        category = tag = None
        try:
            category = factories.CategoryModelFactory(name='category')
            tag = factories.TagModelFactory(name='tag')
            with self.assertRaises(ValueError):
                category.parent = tag
                category.save()
        finally:
            for item in (category, tag):
                if item:
                    item.delete()
