"""
.. module::  ondalear.backend.docmgmt.models.factories
   :synopsis:  Models factory module.


Note: Factory Meta inheritance does not appear to work consistently
"""

import uuid as uuid_
import factory
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site

from ondalear.backend.core.python.utils import class_name
from ondalear.backend.core.django.models import AbstractModel
from ondalear.backend.docmgmt.models import constants
from ondalear.backend.docmgmt.models import (AnalysisResults,
                                             Annotation,
                                             Category,
                                             Client,
                                             ClientUser,
                                             Tag)
from ondalear.backend.docmgmt.models import (AuxiliaryDocument,
                                             Document,
                                             DocumentAnnotation,
                                             DocumentAssociation,
                                             DocumentTag,
                                             ReferenceDocument)


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

class ClientModelFactory(AbstractModelFactory):
    """Client model factory class."""
    client_id = 'test_client_id'
    name = 'test client name'
    is_system = False

    class Meta:
        """Model meta class."""
        abstract = False
        model = Client
        django_get_or_create = ('client_id',)

class ClientUserModelFactory(AbstractModelFactory):
    """ClientUser model factory class."""
    client = factory.SubFactory(ClientModelFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        """Model meta class."""
        abstract = False
        model = ClientUser
        django_get_or_create = ('client', 'user')


class AnnotationModelFactory(AbstractModelFactory):
    """Annotation model factory class."""
    name = 'annotation name'
    annotation = 'annotation text'
    client = factory.SubFactory(ClientModelFactory)

    class Meta:
        """Model meta class."""
        abstract = False
        model = Annotation
        django_get_or_create = ('client', 'name', 'annotation')


class AbstractClassificationModelFactory(AbstractModelFactory):
    """Classification model factory class."""
    name = 'classification_one'
    parent = None
    client = factory.SubFactory(ClientModelFactory)

    class Meta:
        """Model meta class."""
        abstract = True


class TagModelFactory(AbstractClassificationModelFactory):
    """Criteria document tag model factory class."""
    name = 'tag_1'
    target = constants.CLASSIFICATION_TARGET_AUXILIARY_DOCUMENT
    domain = constants.CLASSIFICATION_DOMAIN_GENERAL
    class Meta:
        """Model meta class."""
        abstract = False
        model = Tag
        django_get_or_create = ('name', 'parent')


class CategoryModelFactory(AbstractClassificationModelFactory):
    """Category document tag model factory class."""
    name = 'category_1'
    target = constants.CLASSIFICATION_TARGET_AUXILIARY_DOCUMENT
    domain = constants.CLASSIFICATION_DOMAIN_GENERAL
    class Meta:
        """Model meta class."""
        abstract = False
        model = Category
        django_get_or_create = ('name', 'parent')


class AbstractDocumentModelFactory(AbstractModelFactory):
    """Base document model factory class."""
    client = factory.SubFactory(ClientModelFactory)
    category = factory.SubFactory(CategoryModelFactory)
    name = 'document name'

    class Meta:
        """Model meta class."""
        abstract = True

class DocumentModelFactory(AbstractDocumentModelFactory):
    """Document model factory class"""
    class Meta:
        """Model meta class."""
        abstract = False
        model = Document
        django_get_or_create = ('client', 'name')


class AbstractDerivedDocumentModelFactory(FactoryMixin, factory.DjangoModelFactory):
    """Base custom document model factory class."""
    content = 'some content'
    dir_path = None
    upload = None

    class Meta:
        """Model meta class."""
        abstract = True

class AuxiliaryDocumentModelFactory(AbstractDerivedDocumentModelFactory):
    """AuxiliaryDocument model factory class."""
    document = factory.SubFactory(DocumentModelFactory,
                                  document_type=constants.DOCUMENT_TYPE_AUXILIARY)

    class Meta:
        """Model meta class."""
        abstract = False
        model = AuxiliaryDocument

class ReferenceDocumentModelFactory(AbstractDerivedDocumentModelFactory):
    """ReferenceDocument model factory class."""
    document = factory.SubFactory(DocumentModelFactory,
                                  document_type=constants.DOCUMENT_TYPE_REFERENCE)

    class Meta:
        """Model meta class."""
        abstract = False
        model = ReferenceDocument



class DocumentTagModelFactory(AbstractModelFactory):
    """Document tag association model factory class"""
    document = None
    tag = None
    client = factory.SubFactory(ClientModelFactory)
    class Meta:
        """Model meta class."""
        abstract = False
        model = DocumentTag
        django_get_or_create = ('document', 'tag')


class DocumentAnnotationModelFactory(AbstractModelFactory):
    """Document annotation association model factory class"""
    document = None
    annotation = None
    client = factory.SubFactory(ClientModelFactory)
    class Meta:
        """Model meta class."""
        abstract = False
        model = DocumentAnnotation
        django_get_or_create = ('document', 'annotation')

class DocumentAssociationModelFactory(AbstractModelFactory):
    """Document  association model factory class"""
    from_document = None
    to_document = None
    purpose = None
    client = factory.SubFactory(ClientModelFactory)

    class Meta:
        """Model meta class."""
        abstract = False
        model = DocumentAssociation
        django_get_or_create = ('from_document', 'to_document', 'purpose')

class AnalysisResultsModelFactory(AbstractModelFactory):
    """Analysis results model factory class"""
    client = factory.SubFactory(ClientModelFactory)
    name = 'analysis results'
    input = dict()
    output = dict()
    documents = None


    class Meta:
        """Model meta class."""
        abstract = False
        model = AnalysisResults
        django_get_or_create = ('client', 'name')
       