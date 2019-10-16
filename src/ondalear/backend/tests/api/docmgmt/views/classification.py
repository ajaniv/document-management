"""
.. module:: ondalear.backend.tests.api.docmgmt.views.classification
   :synopsis: Classification view unit test  module.

"""
import logging
from django.urls import reverse
from rest_framework import status

from ondalear.backend.docmgmt.models import constants
from ondalear.backend.tests.docmgmt.models import factories
from ondalear.backend.tests.api.model_viewset  import AbstractModelViewsetTestCase

_logger = logging.getLogger(__name__)

# pylint: disable=too-many-ancestors,attribute-defined-outside-init,missing-docstring,no-member

class AbstractClassificationApiTest(AbstractModelViewsetTestCase):
    """Base classification api test"""
    def assert_list_system_classification(self):
        """expect to fetch classification given that the client  is system client"""
        # create system client
        try:
            client = self.raw_create_client(is_system=True)
            saved_client = self.ondalear_client
            self.ondalear_client = client
            # create a classificaiton  associated with system client and fetch list
            self.assert_list()
            self.ondalear_client = saved_client
        finally:
            client.delete()

    def assert_list_system_and_client_classification(self):
        """expect to fetch 2 classifications one associated with system client"""
        # create a system-client classification
        try:
            client = factories.ClientModelFactory(is_system=True,
                                                  client_id='test system_client_id',
                                                  name='test system client name')
            classification = self.factory_class(client=client, name='system created classification')
            data = self.assert_list(expected_count=2).data

            self.assertEqual(data['detail'][1]['name'], 'system created classification')
        finally:
            classification.delete()
            client.delete()

    def assert_post_parent(self):
        """expect to create classification and parent classificaiton"""
        data_parent = self.create_request_data.copy()
        data_parent['name'] = 'root_classification'
        self.create_request_data = data_parent
        parent = self.assert_create()
        assert parent

        data_child = self.create_request_data.copy()
        data_child['name'] = 'child_classification'
        data_child['parent'] = parent.data['detail']['id']
        self.create_request_data = data_child
        self.response_no_values = tuple()
        child = self.assert_create()

        assert child

    def assert_post_invalid_parent(self):
        """expect to fail in child classification creation"""
        data_parent = self.create_request_data.copy()
        data_parent['name'] = 'root_classification'
        self.create_request_data = data_parent
        parent = self.assert_create()
        assert parent

        data_child = self.create_request_data.copy()
        data_child['name'] = 'child_classification'
        data_child['parent'] = -1
        self.create_request_data = data_child
        self.response_no_values = tuple()
        child = self.assert_create(expected_status=status.HTTP_400_BAD_REQUEST)

        assert child

class ClassificationPostTestMixin:
    """Classification post mixin class"""

    def test_post(self):
        # expect to create classification through api
        self.assert_create()

    def test_post_client_disabled(self):
        # expect to fail to create classification
        self.assert_post_client_disabled()

    def test_post_parent(self):
        # expect to create classification and parent classification
        self.assert_post_parent()

    def test_post_invalid_parent(self):
        # expect to fail in child classification creation
        self.assert_post_invalid_parent()

class ClassificationListTestMixin:
    """Classification list test mixin class"""

    def test_list(self):
        # expect to fetch classification list
        self.assert_list()

    def test_list_system_classification(self):
        # expect to fetch classification given that the client  is system client
        self.assert_list_system_classification()

    def test_list_system_and_client_classification(self):
        # expect to fetch 2 classification one associated with system client
        self.assert_list_system_and_client_classification()


class ClassificationRetrieveTestMixin:
    """Classification retrieve test mixin class"""

    def test_retrieve(self):
        # expect to retrive the classification instance
        self.assert_retrieve()

class ClassificationPutTestMixin:
    """Classification put test mixin class"""

    def test_put(self):
        # expect to update the classification instance
        self.assert_put()

class ClassificationPatchTestMixin:
    """Classification patch test mixin class"""

    def test_patch(self):
        # expect to patch the classification instance
        self.assert_patch()

class ClassificationDeleteTestMixin:
    """Classification delete test mixin class"""

    def test_delete(self):
        # expect to delete the classification instance
        self.assert_delete()

class HierarchyMixin:
    """Hierarcy mixin class"""

    expected_hierarchy_data = {'test client name': [
        {
            'auxiliary': [
                {'children': [
                    {'children': [
                        {'children': [],
                         'name': 'root_3_child_1_child_1'}
                        ],
                     'name': 'root_3_child_1'
                     }],
                 'name': 'root_3'}
            ],
            'reference': [
                {'children': [
                    {'children': [],
                     'name': 'root_2_child_2'},
                    {'children': [],
                     'name': 'root_2_child_1'}],
                 'name': 'root_2'},
                {'children': [],
                 'name': 'root_1'}
            ]
        }
    ]}

    def create_instance(self, name, parent=None, target=None, user=None, client=None): # pylint: disable=too-many-arguments
        """create an instance"""
        client = client or self.ondalear_client
        user = user or self.user
        target = target or constants.CLASSIFICATION_TARGET_REFERENCE_DOCUMENT
        return self.factory_class(name=name,
                                  client=client,
                                  parent=parent,
                                  target=target,
                                  creation_user=user,
                                  update_user=user,
                                  effective_user=user)
    def create_instances(self):
        """Create the instances"""
        # Tag one - reference document target, no parent, client is non-system
        root_1 = self.create_instance(name='root_1')

        # Tag two - reference document target, tag three is child, client is non-system
        root_2 = self.create_instance(name='root_2')

        # Tag three/four - reference document target, two children,, client is non-system
        root_2_child_1 = self.create_instance(name='root_2_child_1',
                                              parent=root_2)
        root_2_child_2 = self.create_instance(name='root_2_child_2',
                                              parent=root_2)

        # Tag five - auxiliary document, one child, client is non-system
        root_3 = self.create_instance(name='root_3',
                                      target=constants.CLASSIFICATION_TARGET_AUXILIARY_DOCUMENT)

        # Tag six - auxiliary document,  client is non-system
        root_3_child_1 = self.create_instance(name='root_3_child_1',
                                              parent=root_3)
        # Tag seven - auxiliary document,  client is non-system
        root_3_child_1_child_1 = self.create_instance(name='root_3_child_1_child_1',
                                                      parent=root_3_child_1)

        instances = [root_1, root_2, root_2_child_1, root_2_child_2,
                     root_3, root_3_child_1, root_3_child_1_child_1]
        self.created_models.extend(instances)
        # @TODO: create system client, system user, and associated tags
        return instances

    def assert_hierarchy(self):
        """Verify hierarchy processing"""

        self.create_instances()
        url = reverse(self.url_name)

        # make api request
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, f'{response.data}')

        # verify the header
        response_data = response.data
        header = response_data['header'].copy()

        self.assert_response_header(
            data=header,
            msg='Hierarchy request successfully processed.')

        # verify the detail
        detail = response_data['detail']
        assert self.ondalear_client.name in detail
        self.assertEqual(detail, self.expected_hierarchy_data)
        return response
