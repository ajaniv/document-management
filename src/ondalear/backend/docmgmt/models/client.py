"""
.. module:: ondalear.backend.document.models.client
   :synopsis: ondalear backend document client  module.

The *client* module contains *Client* model abstractions.

"""
import logging
from inflection import humanize, pluralize, underscore

from django.db.models import CASCADE
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from ondalear.backend.core.django import fields
from ondalear.backend.core.django.models import db_table
from ondalear.backend.docmgmt.models.base import AbstractDocumentManagementModel, app_label
from ondalear.backend.docmgmt.models import constants

_logger = logging.getLogger(__name__)

_client = "Client"
_client_verbose = humanize(underscore(_client))

class Client(AbstractDocumentManagementModel):
    """Client class definition

    A system client is one designed to support 'free standing' users not
    associated with an official client.
    """
    client_id = fields.char_field(blank=False, null=False, max_length=constants.ID_FIELD_MAX_LEGNTH)
    name = fields.char_field(blank=False, null=False, max_length=constants.NAME_FIELD_MAX_LENGTH)
    email = fields.email_field(blank=True, null=True)
    phone = fields.phone_number_field(blank=True, null=True)
    description = fields.description_field(blank=True, null=True,
                                           max_length=constants.DESCRIPTION_FIELD_MAX_LENGTH)

    # indicate whether the client type is system or not
    is_system = fields.boolean_field(blank=False, null=False, default=False)

    class Meta(AbstractDocumentManagementModel.Meta):
        """Model meta class declaration."""
        db_table = db_table(app_label, _client)
        verbose_name = _(_client_verbose)
        verbose_name_plural = _(pluralize(_client_verbose))

    def __str__(self):
        """pretty format instance as string"""
        return self.client_id

_client_user = "ClientUser"
_client_user_verbose = humanize(underscore(_client_user))


class ClientUser(AbstractDocumentManagementModel):
    """Client user  model class.

    Capture client user  attributes.  A client may be associated
    with 0 or more  users:
        Client(1) ------> Annotation(0..*)

    A user can only be associated with a single client
    """
    # when client or user are deleted, the associated ClientUser instance
    # is deleted.
    client = fields.foreign_key_field(Client, on_delete=CASCADE)
    user = fields.one_to_one_field(to_class=User, on_delete=CASCADE)
    phone = fields.phone_number_field(blank=True, null=True)
    description = fields.description_field(blank=True, null=True,
                                           max_length=constants.DESCRIPTION_FIELD_MAX_LENGTH)


    def has_logged_in(self):
        """Determine if user has ever logged in"""
        return self.user.last_login  is not None    # pylint: disable=no-member


    class Meta(AbstractDocumentManagementModel.Meta):
        """ClientUser meta class"""
        db_table = db_table(app_label, _client_user)
        verbose_name = _(_client_user_verbose)
        verbose_name_plural = _(pluralize(_client_user_verbose))

    def __str__(self):
        """pretty format instance as string"""
        return "{},{}".format(self.client, self.user)
