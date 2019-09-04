"""
.. module::  ondalear.backend.docmgmt.admin.client
   :synopsis: document management client admin module.

This module contains client admin abstractions.

"""
import logging

from ondalear.backend.core.django.admin import AbstractModelAdmin
from ondalear.backend.docmgmt.admin.base import register
from ondalear.backend.docmgmt.models import  (Client,
                                              ClientUser)

_logger = logging.getLogger(__name__)

_client_fields = ('client_id', 'name', 'email', 'phone', 'description',)

class ClientAdmin(AbstractModelAdmin):
    """Client model admin class.
    """
    list_display = AbstractModelAdmin.list_display + ('client_id', 'name')
    fieldsets = (
        ('Client',
         {'fields': _client_fields}),
    ) + AbstractModelAdmin.field_sets()     # pylint: disable=no-member

_client_user_fields = ('client', 'user', 'phone', 'description')

class ClientUserAdmin(AbstractModelAdmin):
    """Client user model admin class.
    """
    list_display = AbstractModelAdmin.list_display + ('client', 'user')
    readonly_fields = AbstractModelAdmin.readonly_fields
    fieldsets = (
        ('ClientUser',
         {'fields': _client_user_fields}),
    ) + AbstractModelAdmin.field_sets()     # pylint: disable=no-member


# Register the models and admin classes.
model_classes = (Client,
                 ClientUser)
admin_classes = (ClientAdmin,
                 ClientUserAdmin)

register(model_classes, admin_classes)
