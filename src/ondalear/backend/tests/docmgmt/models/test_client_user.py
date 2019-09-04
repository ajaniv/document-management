"""
.. module:: ondalear.backend.tests.docmgmt.models.test_client_user
   :synopsis: ClientUser model unit test   module.


"""
import logging

from ondalear.backend.docmgmt.models import ClientUser
from . import factories
from .base import AbstractModelTestCase

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,no-self-use,missing-docstring


class ClientUserModelCRUDTests(AbstractModelTestCase):
    """ClientUser model basic lifecycle test case"""

    def test_crud(self):
        # expect to create client, find, update, and delete client user

        # create the instance; it is saved to the db
        instance = factories.ClientUserModelFactory()
        assert instance.client.client_id == "test_client_id"

        # fetch the instance
        fetched = ClientUser.objects.get(pk=instance.id)
        assert fetched

        # verify update
        description = 'some description'
        instance.description = description
        instance .save()
        assert ClientUser.objects.get(pk=instance.id).description == description

        # verify delete
        deleted = instance.delete()
        assert deleted[0] == 1
        try:
            ClientUser.objects.get(pk=instance.id)
        except ClientUser.DoesNotExist:
            pass
