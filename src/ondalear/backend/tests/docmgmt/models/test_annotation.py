"""
.. module:: ondalear.backend.tests.docmgmt.models.test_annotation
   :synopsis: Annotation model unit test  module.


"""
import logging

from .base import ClassCRUDMixin
from . import factories
from .base  import AbstractModelTestCase

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,no-self-use,missing-docstring

class AnnotationModelCRUDTests(ClassCRUDMixin, AbstractModelTestCase):
    """Annotation model basic lifecycle test case"""
    factory_class = factories.AnnotationModelFactory
    name = 'annotation_one'
    new_name = 'new_annotation'

    def test_crud(self):
        # expect crud operations to succeed
        self.assert_crud(update_field_name='name',
                         update_field_value=self.new_name,
                         name=self.name,
                         annotation='some annotation')
