"""
.. module:: ondalear.backend.tests.docmgmt.models.test_client
   :synopsis: Client model unit test   module.


"""
import logging

from ondalear.backend.docmgmt.models import Client
from . import factories
from .base import AbstractModelTestCase

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,no-self-use,missing-docstring


class ClientModelCRUDTests(AbstractModelTestCase):
    """Client model basic lifecycle test case"""

    def test_crud(self):
        # expect to create, update, fetch, and delete client

        # create instance
        client_id = 'ondalear'
        instance = factories.ClientModelFactory(client_id=client_id, name='OndaLear LLC.')
        # verify it was saved
        assert instance.client_id == client_id

        # fetch the instance
        fetched = Client.objects.get(pk=instance.id)
        assert fetched

        # update the instance
        new_name = 'New Name'
        instance.name = new_name
        instance.save()
        # verify update
        assert Client.objects.get(pk=instance.id).name == new_name

        # delete the instance
        deleted = instance.delete()
        # verify deletion
        assert deleted[0] == 1
        try:
            Client.objects.get(pk=instance.id)
        except Client.DoesNotExist:
            pass
