"""
.. module:: ondalear.backend.tests.api.docmgmt.views.test_tag
   :synopsis: Tag view unit test  module.


"""
import logging

from ondalear.backend.docmgmt.models import Tag
from ondalear.backend.tests.docmgmt.models import factories
from ondalear.backend.tests.api.docmgmt.views.classification import AbstractClassificationApiTest
from ondalear.backend.tests.api.docmgmt.views.classification import (
        ClassificationDeleteTestMixin,
        ClassificationListTestMixin,
        ClassificationPatchTestMixin,
        ClassificationPostTestMixin,
        ClassificationPutTestMixin,
        ClassificationRetrieveTestMixin,
        HierarchyMixin)


_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors


class TagApiTest(AbstractClassificationApiTest):
    """Base tag  api test"""
    create_url_name = 'tag-list'
    factory_class = factories.TagModelFactory
    model_class = Tag

    create_request_data = {
        'description': 'tag description',
        'name': 'tag_1',
    }

    response_no_values = ('parent',)

class TagAPIPostTest(ClassificationPostTestMixin, TagApiTest):
    """Tag post test case"""

    url_name = 'tag-list'


class TagAPIListTest(ClassificationListTestMixin, TagApiTest):
    """Tag list test case"""

    url_name = 'tag-list'


class TagAPIRetrieveTest(ClassificationRetrieveTestMixin, TagApiTest):
    """Tag retrieve test case"""

    url_name = 'tag-detail'


class TagAPIPutTest(ClassificationPutTestMixin, TagApiTest):
    """Tag put test case"""

    url_name = 'tag-detail'


class TagAPIPatchTest(ClassificationPatchTestMixin, TagApiTest):
    """Tag patch test case"""

    url_name = 'tag-detail'


class TagAPIDeleteTest(ClassificationDeleteTestMixin, TagApiTest):
    """Tag delete test case"""

    url_name = 'tag-detail'


class TagAPIHierarchyTest(HierarchyMixin, TagApiTest):
    """Tag hierarchy test case"""

    url_name = 'tag-hierarchy'

    def test_hierarchy(self):
        # expect to fetch classification list
        self.assert_hierarchy()
