"""
.. module:: ondalear.backend.api.site_admin.views.test_client_admin
   :synopsis: site admin  client view unit test  module.


"""
import logging
from ondalear.backend.docmgmt.models import Client
from .base import AssertMixin, AbstractSiteAdminTests, NonStaffMixin

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors


class ClientMixinClass:
    """Client unit test  mixin class"""
    detail_url = 'client-detail'
    list_url = 'client-list'

    def assert_response_detail(self, data):
        """verify response detail"""
        for attr in ('id', 'name'):
            self.assertEqual(data[attr], getattr(self.ondalear_client, attr))

class AbstractClientAdminTestCase(ClientMixinClass, AssertMixin, AbstractSiteAdminTests):
    """Base client admin test case class"""
    model_class = Client

    def object_id(self):
        """fetch default object id for detail urls"""
        return self.ondalear_client.id

class ClientCreateAdminTestCase(AbstractClientAdminTestCase):
    """Client post test case"""

    def test_create(self):
        # Expect to fail - create client not supported at this time
        self.login()
        self.assert_create(self.list_url)
        self.logout()

class ClientUpdateAdminTestCase(AbstractClientAdminTestCase):
    """Client put test case"""

    def test_update(self):
        # Expect to fail - update client not supported at this time
        self.login()
        self.assert_update(self.detail_url, self.object_id())
        self.logout()

class ClientPartialUpdateAdminTestCase(AbstractClientAdminTestCase):
    """Client patch test case"""

    def test_patch(self):
        # Expect to fail - patch client not supported at this time
        self.login()
        self.assert_update(self.detail_url, self.object_id())
        self.logout()

class ClientDestroyAdminTestCase(AbstractClientAdminTestCase):
    """Client delete test case"""

    def test_delete(self):
        # Expect to fail - delete client not supported at this time
        self.login()
        self.assert_update(self.detail_url, self.object_id())
        self.logout()

class ClientRetrieveAdminTestCase(AbstractClientAdminTestCase):
    """Client retrieve test case"""

    def test_retrieve(self):
        # Expect to fetch client instance
        self.login()
        self.assert_retrieve(self.detail_url, self.object_id())
        self.logout()

class ClientListAdminTestCase(AbstractClientAdminTestCase):
    """Client list test case"""

    def test_list(self):
        # Expect to fetch client list
        self.login()
        self.assert_list(self.list_url, expected_count=1, result_index=0)
        self.logout()


class NonStaffClientRetrieveAdminTestCase(NonStaffMixin, AbstractClientAdminTestCase):
    """Client retrieve test case as non staff
    Designed to prove that non staff users have access to client
    """
    def test_retrieve(self):
        # Expect to fetch user instance
        self.login()
        self.assert_retrieve(self.detail_url, self.object_id())
        self.logout()
