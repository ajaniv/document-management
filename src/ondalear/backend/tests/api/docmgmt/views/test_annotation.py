"""
.. module:: ondalear.backend.tests.api.docmgmt.views.test_annotation
   :synopsis: Annotation view unit test  module.


"""
import logging

from ondalear.backend.docmgmt.models import Annotation
from ondalear.backend.tests.docmgmt.models import factories
from ondalear.backend.tests.api.docmgmt.views.base import AbstractDocMgmtAPITestCase



_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors


class AnnotationApiTest(AbstractDocMgmtAPITestCase):
    """Base annotation  api test"""
    create_url_name = 'annotation-list'
    factory_class = factories.AnnotationModelFactory
    model_class = Annotation

    create_request_data = {
        'annotation': 'some annotation',
        'name': 'annotation name'
    }

    response_no_values = tuple()

class AnnotationAPIPostTest(AnnotationApiTest):
    """Annotation post test case"""

    url_name = 'annotation-list'

    def test_post(self):
        # expect to create annotation through api
        self.assert_create()


class AnnotationAPIListTest(AnnotationApiTest):
    """Annotation list test case"""

    url_name = 'annotation-list'

    def test_list(self):
        # expect to fetch annotation list
        self.assert_list()


class AnnotationAPIRetrieveTest(AnnotationApiTest):
    """Annotation retrieve test case"""

    url_name = 'annotation-detail'

    def test_retrieve(self):
        # expect to retrive the annotation instance
        self.assert_retrieve()


class AnnotationPIPutTest(AnnotationApiTest):
    """Annotation put test case"""

    url_name = 'annotation-detail'

    def test_put(self):
        # expect to update the annotation instance
        self.assert_put()


class AnnotationAPIPatchTest(AnnotationApiTest):
    """Annotation patch test case"""

    url_name = 'annotation-detail'

    def test_patch(self):
        # expect to patch the annotation instance
        self.assert_patch()


class AnnotationAPIDeleteTest(AnnotationApiTest):
    """Annotation delete test case"""

    url_name = 'annotation-detail'

    def test_delete(self):
        # expect to delete the annotation instance
        self.assert_delete()