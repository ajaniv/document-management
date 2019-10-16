"""
.. module::  ondalear.backend.tests.base_factories
   :synopsis:  Base factory module.


Note: Factory Meta inheritance does not appear to work consistently
"""

import uuid as uuid_
import factory
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site

from ondalear.backend.core.python.utils import class_name
from ondalear.backend.core.django.models import AbstractModel


def model_class(factory_class):
    """Return model class name .
    """
    return factory_class._meta.model    # pylint: disable=protected-access


def model_class_name(factory_class):
    """Return model class name for factory class.
    """
    return class_name(model_class(factory_class))


def default_name(cls, number):
    """Return a default name for given class.
    """
    return '{}_{}'.format(class_name(cls), number)


class UserFactory(factory.DjangoModelFactory):
    """User factory class."""

    class Meta:
        """Model meta class."""
        model = User
        django_get_or_create = ('username',)

    username = 'test_user'
    is_active = True

    @staticmethod
    def create_users(count=1, prefix='test_user'):
        """Create users method"""
        users = [UserFactory(username='%s_%d' % (prefix, index))
                 for index in range(1, count + 1)]
        return users


class GroupFactory(factory.DjangoModelFactory):
    """Group factory class."""

    class Meta:
        """Model meta class."""
        model = Group
        django_get_or_create = ('name',)

    name = 'test_group'


class SiteFactory(factory.DjangoModelFactory):
    """Site factory class."""

    class Meta:
        """Model meta class."""
        model = Site
        django_get_or_create = ('domain',)

    domain = 'test_domain'

class FactoryMixin:
    """Factory mixin class"""
    @classmethod
    def model_class(cls):
        """Return model class."""
        return model_class(cls)

    @classmethod
    def model_class_name(cls):
        """Return model class name."""
        return model_class_name(cls)

    @classmethod
    def default_name(cls, number):
        """Return default name.
        """
        return '{}_{}'.format(model_class_name(cls), number)

class AbstractModelFactory(FactoryMixin, factory.DjangoModelFactory):
    """Base model factory class."""

    creation_user = factory.SubFactory(UserFactory)
    update_user = factory.SubFactory(UserFactory)
    effective_user = factory.SubFactory(UserFactory)
    site = factory.SubFactory(SiteFactory)
    is_enabled = True
    is_deleted = False
    uuid = factory.Sequence(lambda _: uuid_.uuid4())

    class Meta:
        """Model meta class."""
        abstract = True
        model = AbstractModel
        django_get_or_create = ('id',)
