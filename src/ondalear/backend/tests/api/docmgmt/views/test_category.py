"""
.. module:: ondalear.backend.tests.api.docmgmt.views.test_category
   :synopsis: Category view unit test  module.


"""
import logging

from ondalear.backend.docmgmt.models import Category
from ondalear.backend.tests.docmgmt.models import factories
from ondalear.backend.tests.api.docmgmt.views.classification import (
        ClassificationDeleteTestMixin,
        ClassificationListTestMixin,
        ClassificationPostTestMixin,
        ClassificationPatchTestMixin,
        ClassificationPutTestMixin,
        ClassificationRetrieveTestMixin,
        HierarchyMixin)
from ondalear.backend.tests.api.docmgmt.views.classification import AbstractClassificationApiTest

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors


class CategoryApiTest(AbstractClassificationApiTest):
    """Base category  api test"""
    create_url_name = 'category-list'
    factory_class = factories.CategoryModelFactory
    model_class = Category

    create_request_data = {
        'description': 'category description',
        'name': 'category_1',
    }

    response_no_values = ('parent',)

class CategoryAPIPostTest(ClassificationPostTestMixin, CategoryApiTest):
    """Category post test case"""

    url_name = 'category-list'


class CategoryAPIListTest(ClassificationListTestMixin, CategoryApiTest):
    """Category list test case"""

    url_name = 'category-list'


class CategoryAPIRetrieveTest(ClassificationRetrieveTestMixin, CategoryApiTest):
    """Category retrieve test case"""

    url_name = 'category-detail'


class CategoryAPIPutTest(ClassificationPutTestMixin, CategoryApiTest):
    """Category put test case"""

    url_name = 'category-detail'


class CategoryAPIPatchTest(ClassificationPatchTestMixin, CategoryApiTest):
    """Category patch test case"""

    url_name = 'category-detail'


class CategoryAPIDeleteTest(ClassificationDeleteTestMixin, CategoryApiTest):
    """Category delete test case"""

    url_name = 'category-detail'

class CategoryAPIHierarchyTest(HierarchyMixin, CategoryApiTest):
    """Category hierarchy test case"""

    url_name = 'category-hierarchy'

    def test_hierarchy(self):
        # expect to fetch classification list
        self.assert_hierarchy()
    