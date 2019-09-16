"""
.. module:: ondalear.backend.api.user_admin.views.test_user_admin
   :synopsis: user admin  views unit test  module.


"""
import logging

from django.urls import reverse
from rest_framework import status

from ondalear.backend.tests.api.base import AbstractAPITestCase

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,missing-docstring

class UserAdminApiLoginTest(AbstractAPITestCase):
    """User admin api login test case"""

    def test_login(self):
        # Expect to login and return user token.
        self.login()

    def test_login_inactive_user(self):
        # Expect to fail login is user is inactive
        self.user.is_active = False
        self.user.save()
        self.login(expected_status=status.HTTP_400_BAD_REQUEST)


class UserAdminApiLogoutTest(AbstractAPITestCase):
    """user admin api logout test case"""

    expected_detail = {}

    def assert_response_detail(self, data):
        """Verify response header"""
        self.assert_dict(data, self.expected_detail)

    def test_logout(self):
        # Expect to log out.

        # login
        self.login()

        # logout
        self.logout()


class UserAdminApiChangePasswordTest(AbstractAPITestCase):
    """User admin api logout test case"""

    expected_detail = {}

    def assert_response_detail(self, data):
        """Verify response header"""
        self.assert_dict(data, self.expected_detail)

    def test_change_password(self):
        # Expect to log out.

        # login
        self.login()

        url = reverse('user_password_change')
        request_data = {'new_password1': self.password, 'new_password2':self.password}

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'{response.data}')
        response_data = response.data

        # verify the header
        self.assert_response_header(
            data=response_data['header'],
            msg='New password has been saved.')

        # verify the detail
        self.assert_response_detail(response_data['detail'])

        # logout
        self.logout()
