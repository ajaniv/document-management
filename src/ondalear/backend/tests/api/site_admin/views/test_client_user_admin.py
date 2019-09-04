"""
.. module:: ondalear.backend.api.site_admin.views.test_client_user
   :synopsis: site admin  client user view unit test  module.


"""
import logging
from ondalear.backend.docmgmt.models import ClientUser
from .base import AssertMixin, AbstractSiteAdminTests, NonStaffMixin

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors


class ClientUserMixinClass:
    """Client user unit test  mixin class"""
    detail_url = 'client-user-detail'
    list_url = 'client-user-list'

    def assert_response_detail(self, data):
        """verify response detail"""
        for attr in ('id',):
            self.assertEqual(data[attr], getattr(self.client_user, attr))
        for attr in ('client', 'user'):
            self.assertEqual(data[attr], getattr(self.client_user, attr+'_id'))


class AbstractClientUserAdminTestCase(ClientUserMixinClass, AssertMixin, AbstractSiteAdminTests):
    """Base client user admin test case class"""
    model_class = ClientUser

    def object_id(self):
        """fetch default object id for detail urls"""
        return self.client_user.id

class ClientUserCreateAdminTestCase(AbstractClientUserAdminTestCase):
    """Client user post test case"""

    def test_create(self):
        # Expect to fail - create client user not supported at this time
        self.login()
        self.assert_create(self.list_url)
        self.logout()

class ClientUserUpdateAdminTestCase(AbstractClientUserAdminTestCase):
    """Client user put test case"""

    def test_update(self):
        # Expect to fail - update client user not supported at this time
        self.login()
        self.assert_update(self.detail_url, self.object_id())
        self.logout()

class ClientUserPartialUpdateAdminTestCase(AbstractClientUserAdminTestCase):
    """Client user patch test case"""

    def test_patch(self):
        # Expect to fail - patch client user not supported at this time
        self.login()
        self.assert_update(self.detail_url, self.object_id())
        self.logout()

class ClientUserDestroyAdminTestCase(AbstractClientUserAdminTestCase):
    """Client user delete test case"""

    def test_delete(self):
        # Expect to fail - delete client user not supported at this time
        self.login()
        self.assert_update(self.detail_url, self.object_id())
        self.logout()

class ClientUserRetrieveAdminTestCase(AbstractClientUserAdminTestCase):
    """Client user retrieve test case"""

    def test_retrieve(self):
        # Expect to fetch client user instance
        self.login()
        self.assert_retrieve(self.detail_url, self.object_id())
        self.logout()

class ClientUserListAdminTestCase(AbstractClientUserAdminTestCase):
    """Client user list test case"""

    def test_list(self):
        # Expect to fetch client user list
        self.login()
        self.assert_list(self.list_url, expected_count=1, result_index=0)
        self.logout()

class NonStaffClientUserRetrieveAdminTestCase(NonStaffMixin, AbstractClientUserAdminTestCase):
    """ClientUser retrieve test case as non staff
    Designed to prove that non staff users have access to client user
    """
    def test_retrieve(self):
        # Expect to fetch user instance
        self.login()
        self.assert_retrieve(self.detail_url, self.object_id())
        self.logout()
