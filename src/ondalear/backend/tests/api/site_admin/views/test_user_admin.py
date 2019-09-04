"""
.. module:: ondalear.backend.api.site_admin.views.test_user_admin
   :synopsis: site admin  user view unit test module.


"""
import logging
from django.contrib.auth.models import User
from .base import AssertMixin, AbstractSiteAdminTests, NonStaffMixin

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors

class UserMixinClass:
    """User unit test mixin class"""
    detail_url = 'user-detail'
    list_url = 'user-list'

    def assert_response_detail(self, data):
        """verify response detail"""
        for attr in ('id', 'username', 'email'):
            self.assertEqual(data[attr], getattr(self.staff_user, attr))

class AbstractUserAdminTestCase(UserMixinClass, AssertMixin, AbstractSiteAdminTests):
    """Base User admin test case class"""
    model_class = User

    def object_id(self):
        """return default object id for detail urls"""
        return self.staff_user.id

class UserCreateAdminTestCase(AbstractUserAdminTestCase):
    """User post test case"""

    def test_create(self):
        # Expect to fail - create user not supported at this time
        self.login()
        self.assert_create(self.list_url)
        self.logout()

class UserUpdateAdminTestCase(AbstractUserAdminTestCase):
    """User put test case"""

    def test_update(self):
        # Expect to fail - update user not supported at this time
        self.login()
        self.assert_update(self.detail_url, self.object_id())
        self.logout()

class UserPartialUpdateAdminTestCase(AbstractUserAdminTestCase):
    """User patch test case"""

    def test_patch(self):
        # Expect to fail - patch user not supported at this time
        self.login()
        self.assert_patch(self.detail_url, self.object_id())
        self.logout()

class UserDestroyAdminTestCase(AbstractUserAdminTestCase):
    """User delete test case"""
    def test_delete(self):
        # Expect to fail - delete user not supported at this time
        self.login()
        self.assert_delete(self.detail_url, self.object_id())
        self.logout()

class UserRetrieveAdminTestCase(AbstractUserAdminTestCase):
    """User retrieve test case"""
    def test_retrieve(self):
        # Expect to fetch user instance
        self.login()
        self.assert_retrieve(self.detail_url, self.object_id())
        self.logout()

class UserListAdminTestCase(AbstractUserAdminTestCase):
    """User list test case"""

    def test_list(self):
        # Expect to fetch user list
        self.login()
        # admin user is created as part of db setup, results ordered by update_time
        self.assert_list(self.list_url, expected_count=2, result_index=0)
        self.logout()


class NonStaffUserRetrieveAdminTestCase(NonStaffMixin, AbstractUserAdminTestCase):
    """User retrieve test case as non staff
    Designed to prove that non staff users have access to user
    """

    def object_id(self):
        """return object id for designated user"""
        return self.user.id

    def test_retrieve(self):
        # Expect to fetch user instance
        self.login()
        self.assert_retrieve(self.detail_url, self.object_id())
        self.logout()
