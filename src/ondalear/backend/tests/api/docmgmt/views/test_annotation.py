"""
.. module:: ondalear.backend.tests.api.docmgmt.views.test_annotation
   :synopsis: Annotation view unit test  module.


"""
import logging

from ondalear.backend.docmgmt.models import Annotation
from ondalear.backend.tests.docmgmt.models import factories
from ondalear.backend.tests.api.model_viewset  import AbstractModelViewsetTestCase



_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors


class AbstractAnnotationApiTest(AbstractModelViewsetTestCase):
    """Base annotation  api test"""
    create_url_name = 'annotation-crud-list'
    factory_class = factories.AnnotationModelFactory
    model_class = Annotation

    create_request_data = {
        'annotation': 'some annotation',
        'name': 'annotation name'
    }

    response_no_values = tuple()

class AnnotationAPIPostTest(AbstractAnnotationApiTest):
    """Annotation post test case"""

    url_name = 'annotation-crud-list'

    def test_post(self):
        # expect to create annotation through api
        self.assert_create()


class AnnotationAPIListTest(AbstractAnnotationApiTest):
    """Annotation list test case"""

    url_name = 'annotation-crud-list'

    def test_list(self):
        # expect to fetch annotation list
        self.assert_list()


class AnnotationAPIRetrieveTest(AbstractAnnotationApiTest):
    """Annotation retrieve test case"""

    url_name = 'annotation-crud-detail'

    def test_retrieve(self):
        # expect to retrive the annotation instance
        self.assert_retrieve()


class AnnotationPIPutTest(AbstractAnnotationApiTest):
    """Annotation put test case"""

    url_name = 'annotation-crud-detail'

    def test_put(self):
        # expect to update the annotation instance
        self.assert_put()


class AnnotationAPIPatchTest(AbstractAnnotationApiTest):
    """Annotation patch test case"""

    url_name = 'annotation-crud-detail'

    def test_patch(self):
        # expect to patch the annotation instance
        self.assert_patch()


class AnnotationAPIDeleteTest(AbstractAnnotationApiTest):
    """Annotation delete test case"""

    url_name = 'annotation-crud-detail'

    def test_delete(self):
        # expect to delete the annotation instance
        self.assert_delete()
