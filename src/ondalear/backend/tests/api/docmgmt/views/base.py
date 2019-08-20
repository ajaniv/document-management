"""
.. module:: ondalear.backend.tests.api.docmgmt.views.base
   :synopsis: docmgmt api views base  unittest module.


"""
from copy import deepcopy
import logging
from django.urls import reverse
from rest_framework import status
from ondalear.backend.tests.api.base import AbstractAPITestCase

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,too-many-ancestors,attribute-defined-outside-init,no-self-use

class AssertMixin:
    """Assert Mixin class"""
    def extract_object_id(self, data):
        """extract object id"""
        object_id = data.get('id')
        return object_id

    def assert_is_set(self, data, keys):
        """verify data[key] has value"""
        # @TODO: only handling one level of nesting, need to make recursive, generic
        if isinstance(keys, (dict,)):
            for key, value in keys.items():
                self.assertIsNotNone(data[key], msg=f'unexpectedly None {key}')
                if isinstance(value, (tuple, list)):
                    for nested_key in value:
                        self.assertIsNotNone(data[key][nested_key],
                                             msg=f'unexpectedly None {key}{nested_key}')
        else:
            for key in keys:
                self.assertIsNotNone(data[key], msg=f'unexpectedly None {key}')

    def assert_response_detail(self, data, expected=None):
        """Assert response detail"""
        # check equality
        expected = expected or self.expected_data()
        for key, value in expected.items():
            # @TODO: only handling one level of nesting
            if isinstance(value, (dict,)):
                for nested_key in value:
                    self.assertEqual(data[key][nested_key], value[nested_key])
            else:
                self.assertEqual(data[key], expected[key])

        # check for not none
        self.assert_is_set(data, self.response_has_values)
        for key in self.response_no_values:
            self.assertIsNone(data[key])

    def assert_short_response(self, data, expected_data):
        """validate short response data"""
        if len(data) == len(expected_data): # id, creation_time ...
            for key in expected_data:
                assert  data[key], f'{key} not set'
            return True
        return False

    def assert_create(self, expected_status=None, request_data=None, fmt=None):
        """verify create  model instance"""
        expected_status = expected_status or status.HTTP_201_CREATED
        fmt = fmt or 'json'
        request_data = request_data or self.create_data().copy()

        url = reverse(self.create_url_name)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.post(url, request_data, format=fmt)
        self.assertEqual(response.status_code, expected_status, f'{response.data}')
        if expected_status != status.HTTP_201_CREATED:
            return response
        response_data = response.data

        # verify the header
        self.assert_response_header(
            data=response_data['header'],
            msg='Create request successfully processed.')

        # verify the detail
        detail = response_data['detail']
        if not self.assert_short_response(detail, self.short_create_response_fields):
            self.assert_response_detail(detail)
        return response

    def assert_list_item(self, data):
        """assert list item"""

        self.assert_response_detail(data)

    def assert_list(self, query_str=None, expected_count=1):
        """Verify list processing"""
        self.assert_create()
        url = reverse(self.url_name)

        if query_str:
            url = f'{url}?{query_str}'

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'{response.data}')
        response_data = response.data

        # verify the header
        header = response_data['header'].copy()
        pagination = header.pop('pagination')
        self.assertEqual(pagination, {'count': expected_count, 'next': None, 'previous': None})
        self.assert_response_header(
            data=header,
            msg='List request successfully processed.',
            exclude=['pagination'])

        # verify the detail
        detail = response_data['detail']
        self.assertEqual(len(detail), expected_count)
        if expected_count == 1:
            data = dict(detail[0])
            self.assert_list_item(data)
        return response

    def assert_retrieve(self):
        """Verify retrieve operation"""
        create_data = self.assert_create().data['detail']
        object_id = self.extract_object_id(create_data)
        url = reverse(self.url_name, args=[object_id])

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
        data = response_data['detail']

        self.assert_response_detail(data)

        return response

    def tweak_put_data(self, put_data):
        """tweak put data hook"""

    def assert_put(self, attr_name=None, attr_value=None):
        """Verify put operation"""
        # create the instance
        created_data = self.assert_create().data

        # parse the response
        create_detail = created_data['detail']
        object_id = self.extract_object_id(create_detail)

        url = reverse(self.url_name, args=[object_id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        get_response = self.client.get(url)
        put_data = get_response.data['detail']

        # make api request
        attr_name = attr_name or 'name'
        attr_value = attr_value or 'new name'

        put_data[attr_name] = attr_value

        self.tweak_put_data(put_data)
        response = self.client.put(url, data=put_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, f'{response.data}')
        response_data = response.data

        # verify the header
        self.assert_response_header(
            data=response_data['header'],
            msg='Update request successfully processed.')

        # verify the detail
        detail = response_data['detail']
        if not self.assert_short_response(detail, self.short_update_response_fields):
            self.assertEqual(detail[attr_name], attr_value)
        return response

    def assert_patch(self, attr_name=None, attr_value=None):
        """Verify patch request"""
        # create the instance
        created_data = self.assert_create().data

        # parse the response
        instance_data = created_data['detail']
        object_id = self.extract_object_id(instance_data)

        url = reverse(self.url_name, args=[object_id])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        attr_name = attr_name or 'name'
        attr_value = attr_value or 'new name'

        new_document = {attr_name: attr_value}
        response = self.client.patch(url, data=new_document, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, f'{response.data}')
        response_data = response.data

        # verify the header
        self.assert_response_header(
            data=response_data['header'],
            msg='Update request successfully processed.')

         # verify the detail
        detail = response_data['detail']

        if self.assert_short_response(detail, self.short_update_response_fields):
            return response

        # @TODO: handles only one level nesting
        if isinstance(attr_value, (dict,)):
            for key, value in attr_value.items():
                self.assertEqual(detail[key], value)
        else:
            self.assertEqual(detail[attr_name], attr_value)
        return response

    def assert_delete(self):
        """assert delete"""
        # create the instance
        created_data = self.assert_create().data

        # parse the response
        instance_data = created_data['detail']
        object_id = self.extract_object_id(instance_data)

        url = reverse(self.url_name, args=[object_id])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # make api request
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, f'{response.data}')
        response_data = response.data

        # verify the header
        self.assert_response_header(
            data=response_data['header'],
            msg='Delete request successfully processed.')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, f'{response.data}')

        return response

    def assert_post_client_disabled(self):
        """ expect to fail to create instance"""
        self.ondalear_client.is_enabled = False
        self.ondalear_client.save()

        self.assert_create(expected_status=status.HTTP_403_FORBIDDEN)

        # restore so that logout does not fail
        self.ondalear_client.is_enabled = True
        self.ondalear_client.save()



class AbstractDocMgmtAPITestCase(AssertMixin, AbstractAPITestCase):
    """Base docmgmt api test case class"""

    short_create_response_fields = ('creation_time', 'id', 'uuid', 'version')
    short_update_response_fields = ('update_time', 'id', 'uuid', 'version')

    response_has_values = (
        'client', 'creation_time',
        'creation_user', 'effective_user',
        'id', 'site', 'update_time',
        'update_user', 'uuid', 'version',
        'is_deleted', 'is_enabled'
    )

    response_no_values = tuple()

    @classmethod
    def setUpClass(cls):
        """Class setup"""
        super(AbstractDocMgmtAPITestCase, cls).setUpClass()
        cls.create_group()
        cls.create_client()
        cls.create_client_user()

    def setUp(self):
        """test case level setup"""
        super(AbstractDocMgmtAPITestCase, self).setUp()

        # configure user group and permissions relationships
        self.configure_group(model_class=self.model_class)

        # login
        self.login()

    def tearDown(self):
        """test case level tear down"""
        self.logout()
        super(AbstractDocMgmtAPITestCase, self).tearDown()

    def create_data(self):
        """create data"""
        return deepcopy(self.create_request_data)

    def expected_data(self):
        """return expected data"""
        return deepcopy(self.create_request_data)
