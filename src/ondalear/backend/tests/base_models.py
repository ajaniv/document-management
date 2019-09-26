"""
.. module:: ondalear.backend.docmgmt.models.base
   :synopsis: base  model unit test module.


"""
import logging
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site

from . import base_factories as factories

_logger = logging.getLogger(__name__)

# pylint: disable=no-member

class AbstractModelTestCase(TestCase):
    """Base class model test case"""
    @classmethod
    def tearDownClass(cls):
        """tear down test class"""
        # @TODO: review implementation approach.  TestCase inheritance
        #   is expected to roll back database changes.
        #   It was implemented because could not explain some instances
        #   when running a large number of tests
        try:
            instance = User.objects.get(username=factories.User.username)
            instance.delete()
        except User.DoesNotExist:
            pass
        try:
            instance = Group.objects.get(name=factories.Group.name)
            instance.delete()
        except Group.DoesNotExist:
            pass
        try:
            instance = Site.objects.get(domain=factories.Site.domain)
            instance.delete()
        except Site.DoesNotExist:
            pass

        super(AbstractModelTestCase, cls).tearDownClass()

class ClassCRUDMixin:
    """CRUD mixin class"""
    def assert_crud(self, update_field_name, update_field_value, **kwargs):
        """
        verify create, update, fetch, and delete
        """
        factory_class = self.factory_class
        model_class = factory_class.model_class()

        # create instance
        instance = factory_class(**kwargs)
        # verify it was saved
        assert instance.id

        # fetch the instance
        fetched = model_class.objects.get(pk=instance.id)
        assert fetched

        # update the instance
        new_name = self.new_name
        instance.name = new_name
        setattr(instance, update_field_name, update_field_value)
        instance.save()

        # verify update
        updated = model_class.objects.get(pk=instance.id)
        self.assertEqual(getattr(updated, update_field_name), update_field_value)

        # delete the instance
        deleted = instance.delete()
        # verify deletion
        assert deleted[0] == 1
        try:
            model_class.objects.get(pk=instance.id)
        except model_class.DoesNotExist:
            pass
