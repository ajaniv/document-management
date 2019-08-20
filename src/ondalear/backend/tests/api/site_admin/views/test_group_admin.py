"""
.. module:: ondalear.backend.api.site_admin.views.test_group_admin
   :synopsis: site admin  group view unit test  module.


"""
import logging
from django.contrib.auth.models import Group
from .base import AssertMixin, AbstractSiteAdminTests, NonStaffMixin

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors


class GroupMixinClass:
    """Group unit test mixin class"""
    detail_url = 'group-detail'
    list_url = 'group-list'

    def assert_response_detail(self, data):
        """verify response detail"""
        for attr in ('id', 'name'):
            self.assertEqual(data[attr], getattr(self.staff_group, attr))

class AbstractGroupAdminTestCase(GroupMixinClass, AssertMixin, AbstractSiteAdminTests):
    """Base group admin test case class"""
    model_class = Group

    def object_id(self):
        """fetch default object id for detail urls"""
        return self.staff_group.id

class GroupCreateAdminTestCase(AbstractGroupAdminTestCase):
    """Group post test case"""

    def test_create(self):
        # Expect to fail - create group not supported at this time
        self.login()
        self.assert_create(self.list_url)
        self.logout()

class GroupUpdateAdminTestCase(AbstractGroupAdminTestCase):
    """Group put test case"""

    def test_update(self):
        # Expect to fail - update group not supported at this time
        self.login()
        self.assert_update(self.detail_url, self.object_id())
        self.logout()

class GroupPartialUpdateAdminTestCase(AbstractGroupAdminTestCase):
    """Group patch test case"""

    def test_patch(self):
        # Expect to fail - patch group not supported at this time
        self.login()
        self.assert_update(self.detail_url, self.object_id())
        self.logout()

class GroupDestroyAdminTestCase(AbstractGroupAdminTestCase):
    """Group delete test case"""

    def test_delete(self):
        # Expect to fail - delete group not supported at this time
        self.login()
        self.assert_update(self.detail_url, self.object_id())
        self.logout()

class GroupRetrieveAdminTestCase(AbstractGroupAdminTestCase):
    """Group retrieve test case"""

    def test_retrieve(self):
        # Expect to fetch group instance
        self.login()
        self.assert_retrieve(self.detail_url, self.object_id())
        self.logout()

class GroupListAdminTestCase(AbstractGroupAdminTestCase):
    """Group list test case"""

    def test_list(self):
        # Expect to fetch group list
        self.login()
        self.assert_list(self.list_url, expected_count=1, result_index=0)
        self.logout()

class NonStaffGroupRetrieveAdminTestCase(NonStaffMixin, AbstractGroupAdminTestCase):
    """Group retrieve test case as non staff
    Designed to prove that non staff users have access to group
    """

    def test_retrieve(self):
        # Expect to fetch user instance
        self.login()
        self.assert_retrieve(self.detail_url, self.object_id())
        self.logout()
        