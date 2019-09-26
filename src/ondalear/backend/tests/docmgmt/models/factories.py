"""
.. module::  ondalear.backend.docmgmt.models.factories
   :synopsis:  Models factory module.


Note: Factory Meta inheritance does not appear to work consistently
"""

import factory

from ondalear.backend.docmgmt.models import constants
from ondalear.backend.docmgmt.models import (Annotation,
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


from ondalear.backend.tests.base_factories import (AbstractModelFactory,
                                                   FactoryMixin,
                                                   UserFactory)


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
