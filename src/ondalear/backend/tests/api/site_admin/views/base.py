"""
.. module:: ondalear.backend.api.site_admin.views.test_user
   :synopsis: site admin  user viewsunit test  module.


"""
import logging

from django.urls import reverse
from rest_framework import status

from ondalear.backend.tests.api.base import (build_expected_header,
                                             build_login_detail,
                                             AbstractAPITestCase)

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring,too-many-ancestors

_username = 'staff'
_email = f'{_username}@gmail.com'
_first_name = ' staff First'
_last_name = 'staff Last'

class AbstractSiteAdminTests(AbstractAPITestCase):
    """base site  admin api login test case"""
    auto_create_user = False
    group_name = 'admin_group'
    username = _username
    password = 'staff123'

    expected_header = build_expected_header(_username)
    expected_login_detail = build_login_detail(_email, _first_name, _last_name)

    def _create_staff_user(self):
        """create admin user"""
        user_details = dict(username=self.username,
                            password=self.password,
                            first_name=_first_name,
                            last_name=_last_name,
                            email=_email,
                            is_staff=True)
        return self.raw_create_user(**user_details)

    def setUp(self):
        """Setup testcase"""
        super(AbstractSiteAdminTests, self).setUp()

        staff_user = self._create_staff_user()
        staff_group = self.raw_create_group()
        self.create_client(effective_user=staff_user,
                           update_user=staff_user,
                           creation_user=staff_user)
        self.create_client_user(client=self.ondalear_client, user=staff_user)
        self.configure_group(model_class=self.model_class, user=staff_user, group=staff_group)
        self.staff_user = staff_user
        self.staff_group = staff_group
        self.__class__.class_created_models.extend([staff_group, staff_user])

class AssertMixin:
    """Test verification mixin class"""

    def assert_not_implemeted(self, response):
        """assert not implemented error"""
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR,
                         f'{response.data}')
        self.assertEqual(response.data['detail'], 'Further analysis is required')

    def assert_create(self, url_name):
        """Verify create operation"""
        url = reverse(url_name)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.post(url, data={}, format='json')
        self.assert_not_implemeted(response)

    def assert_update(self, url_name, object_id):
        """Verify update operation"""
        url = reverse(url_name, args=[object_id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.put(url, data={}, format='json')
        self.assert_not_implemeted(response)


    def assert_patch(self, url_name, object_id):
        """Verify patch operation"""
        url = reverse(url_name, args=[object_id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.patch(url, data={}, format='json')
        self.assert_not_implemeted(response)


    def assert_delete(self, url_name, object_id):
        """Verify delete operation"""
        url = reverse(url_name, args=[object_id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.delete(url, data={}, format='json')
        self.assert_not_implemeted(response)


    def assert_retrieve(self, url_name, object_id):
        """Verify retrieve operation"""

        url = reverse(url_name, args=[object_id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'{response.data}')
        response_data = response.data

        # verify the header
        self.assert_response_header(
            data=response_data['header'],
            msg='Retrieve request successfully processed.')

        # verify the detail
        self.assert_response_detail(response_data['detail'])

        return response

    def assert_list(self, url_name, expected_count=1, result_index=0):
        """Verify list operation"""

        url = reverse(url_name)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, f'{response.data}')
        response_data = response.data

        # verify the header
        header = response_data['header'].copy()
        pagination = header.pop('pagination')
        self.assertIsNone(pagination['next'])
        self.assertIsNone(pagination['previous'])
        assert pagination['count'] == expected_count
        self.assert_response_header(
            data=header,
            msg='List request successfully processed.')

        # verify the detail
        data = response_data['detail'][result_index]

        self.assert_response_detail(data)

        return response

class NonStaffMixin:
    """Non staff user  test case mixin"""
    username = AbstractAPITestCase.username
    password = AbstractAPITestCase.password
    expected_header = AbstractAPITestCase.expected_header
    expected_login_detail = AbstractAPITestCase.expected_login_detail
    auto_create_user = True
