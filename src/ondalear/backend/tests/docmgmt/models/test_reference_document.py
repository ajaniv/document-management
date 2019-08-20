"""
.. module:: ondalear.backend.docmgmt.models.test_reference_document
   :synopsis: ReferenceDocument model unit test  module.

"""
import logging

from . import factories
from .derived_document import (DerivedDocumentModelTestMixin,
                               AbstractDerivedDocumentModelTest)


_logger = logging.getLogger(__name__)


# pylint: disable=too-many-ancestors

class ReferenceDocumentModelCRUDTests(DerivedDocumentModelTestMixin,
                                      AbstractDerivedDocumentModelTest):
    """Reference document model basic lifecycle test case"""
    document_factory_class = factories.DocumentModelFactory
    derived_document_factory_class = factories.ReferenceDocumentModelFactory
    