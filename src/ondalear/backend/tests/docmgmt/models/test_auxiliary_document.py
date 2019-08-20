"""
.. module:: ondalear.backend.docmgmt.models.test_auxiliary_document
   :synopsis: AuxiliaryDocument model unit test module.


"""
import logging

from . import factories
from .derived_document import AbstractDerivedDocumentModelTest, DerivedDocumentModelTestMixin

_logger = logging.getLogger(__name__)

# pylint: disable=too-many-ancestors

class AuxiliaryDocumentModelCRUDTests(DerivedDocumentModelTestMixin,
                                      AbstractDerivedDocumentModelTest):
    """Auxiliary document  model basic lifecycle test case"""
    document_factory_class = factories.DocumentModelFactory
    derived_document_factory_class = factories.AuxiliaryDocumentModelFactory
