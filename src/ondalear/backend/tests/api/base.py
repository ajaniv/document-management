"""
.. module:: ondalear.backend.tests.api.base
   :synopsis: Base api unit test   module.


"""
import logging
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.test import APITestCase

from ondalear.backend.tests.docmgmt.models import factories

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,no-self-use,attribute-defined-outside-init

_username = 'test_client_1_user_1'
_first_name = 'Client_1_user_1_first'
_last_name = 'Client_1_user_1_last'
_email = f'{_username}@gmail.com'

def build_expected_header(username):
    """return expected response header"""
    header = {
        'user': username,
        'api_version': 1,
        'api_status': "OK",
        'msg': ''
        }
    return header

def build_login_detail(email, first_name, last_name):
    """build login detail"""
    login_detail = {
        'email': email,
        'token': '',
        'first_name': first_name,
        'last_name': last_name
        }
    return login_detail

class AbstractAPITestCase(APITestCase):
    """Base  api test case"""
    auto_create_user = True

    username = _username
    password = 'ondalear123'
    first_name = _first_name
    last_name = _last_name
    email = _email
    group_name = 'test_group_1'

    expected_header = build_expected_header(_username)
    expected_login_detail = build_login_detail(_email, _first_name, _last_name)


    def assert_login_response_detail(self, data):
        """Verify response header"""
        self.assert_dict(data, self.expected_login_detail, exclude=['token'])
        self.assertIsNotNone(data['token'])

    def assert_dict(self, data, expected, exclude=None):
        """assert dict"""
        exclude = exclude or []
        self.assertEqual(len(data), len(expected))
        for key in expected.keys():
            if key not in exclude:
                self.assertEqual(data[key], expected[key])

    def assert_response_header(self, data, msg, exclude=None):
        """Verify response header"""
        exclude = exclude or []
        copied = exclude.copy() + ['msg']
        self.assert_dict(data, self.expected_header, copied)
        self.assertEqual(data['msg'], msg)

    @classmethod
    def raw_create_user(cls, **kwargs):
        """low level create test user instance"""
        defaults = dict(username=cls.username,
                        password=cls.password,
                        first_name=cls.first_name,
                        last_name=cls.last_name,
                        email=cls.email)
        defaults.update(kwargs)
        user = factories.UserFactory(**defaults)
        assert user, 'user creation failed'
        # need to force password setting following creation
        user.set_password(cls.password)
        user.save()
        return user

    @classmethod
    def create_user(cls):
        """create test user instance and manage instance"""
        user = cls.raw_create_user()
        cls.user = user
        cls.class_created_models.append(user)

    @classmethod
    def raw_create_group(cls, **kwargs):
        """low level create test group instance"""
        if hasattr(cls, 'group_name'):
            defaults = dict(name=cls.group_name)
        else:
            defaults = dict()
        defaults.update(kwargs)
        group = factories.GroupFactory(**defaults)
        assert group, 'group creation failed'
        return group

    @classmethod
    def create_group(cls):
        """create test group instance and manage it"""
        group = cls.raw_create_group()
        cls.group = group
        cls.class_created_models.append(group)

    @classmethod
    def raw_create_client(cls, **kwargs):
        """low level create test client instance"""
        defaults = dict()
        defaults.update(kwargs)
        client = factories.ClientModelFactory(**defaults)
        assert client, 'client creation failed'
        return client

    @classmethod
    def create_client(cls, **kwargs):
        """create test client instance and manage it"""
        client = cls.raw_create_client(**kwargs)
        cls.ondalear_client = client
        cls.class_created_models.append(client)

    @classmethod
    def raw_create_client_user(cls, user, client):
        """low level create test client instance"""
        client_user = factories.ClientUserModelFactory(user=user,
                                                       client=client,
                                                       effective_user=user,
                                                       creation_user=user,
                                                       update_user=user)
        assert client_user, 'client user creation failed'
        return client_user

    @classmethod
    def create_client_user(cls, user=None, client=None):
        """create test client instance and manage it"""
        user = user or cls.user
        client = client or cls.ondalear_client
        client_user = cls.raw_create_client_user(user=user, client=client)
        cls.client_user = client_user
        cls.class_created_models.append(client_user)

    @classmethod
    def setUpClass(cls):
        """Class setup"""
        super(AbstractAPITestCase, cls).setUpClass()
        cls.class_created_models = []
        if cls.auto_create_user:
            cls.create_user()

    @classmethod
    def tearDownClass(cls):
        """Class teardown"""
        # delete all model instances - deletion order is critical
        if hasattr(cls, 'class_created_models'):
            for instance in reversed(cls.class_created_models):
                instance.delete()
        super(AbstractAPITestCase, cls).tearDownClass()

    def setUp(self):
        """Testcase instance setup"""
        self.created_models = []

    def tearDown(self):
        """Testcase instance teardown"""
        for instance in self.created_models:
            instance.delete()

    def configure_group(self, model_class, user=None, group=None):
        """prepare group"""
        group = group or self.group
        user = user or self.user
        group.user_set.add(user)

        # obtaining the content type for model
        content_type = ContentType.objects.get_for_model(model_class)

        # getting the model permissions
        permissions = list(Permission.objects.filter(content_type=content_type))

        # adding permissions to group
        group.permissions.add(*permissions)

    def login(self, expected_status=None):
        """User login.
        """
        expected_status = expected_status or status.HTTP_200_OK
        url = reverse('user_login')
        request_data = {'username': self.username, 'password': self.password}

        # make api request
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, expected_status)
        if expected_status != status.HTTP_200_OK:
            return response
        response_data = response.data

        # verify the response header
        self.assert_response_header(
            data=response_data['header'],
            msg='Successfully logged in.')

        # verify the response detail
        self.assert_login_response_detail(response_data['detail'])
        self.token = response_data['detail']['token']

        return response

    def logout(self):
        """User logout"""
        url = reverse('user_logout')
        request_data = {}

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.data

        # verify the header
        self.assert_response_header(
            data=response_data['header'],
            msg='Successfully logged out.')

        # verify the detail
        self.assertEqual(response_data['detail'], {})

        return response

    def create_defaults(self):
        """instance creation defaults"""
        client = self.ondalear_client
        user = self.user

        defaults = dict(
            client=client, update_user=user,
            effective_user=user, creation_user=user)
        return defaults
