"""
.. module::  ondalear.backend.core.django.admin
   :synopsis:  django admin  utilities module.

The *admin* module is a collection of Django admin fields utilities.

"""
from __future__ import absolute_import
import logging

from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User

_logger = logging.getLogger(__name__)

class ModelAdminMixin:
    """ModelAdmin mixin class."""
    def prepare(self, request, obj, form, change):
        """Subclass hook to prepare for saving.
        """
        self.prepare_system_fields(request, obj,
                                   form, change)

    def prepare_system_fields(self, request, obj, form, change):   # pylint: disable=unused-argument,no-self-use
        """Populate system related fields.
        """
        # Allowing admin to set critical system fields for testing, correcting data quality issues

        def get_user(attr_name):
            """get user instance per attribute name"""
            user = request.POST.get(attr_name)
            if user:
                user = User.objects.get(pk=int(user))
            else:
                user = request.user
            return user

        if obj.id is None:
            obj.site = get_current_site(request)
            obj.creation_user = get_user('creation_user')

        obj.update_user = get_user('update_user')
        obj.effective_user = get_user('effective_user')

base_model_readonly_fields = (
    'id', 'creation_time', 'creation_user', 'effective_user',
    'site', 'update_time', 'update_user',
    'uuid', 'version')

def system_fields():
    """return system fields"""
    return (("id",),
            ("uuid",),
            ("version"),
            ("site",))


def system_field_set():
    """return system fields set"""
    return ('System', {
        'classes': ('collapse',),
        'fields': system_fields(),
        })


def audit_fields():
    """return audit fields"""
    return(('effective_user',),
           ('update_time',), ('update_user',),
           ('creation_time',), ('creation_user',))


def audit_field_set():
    """return audit fields set"""
    return ('Audit', {
        'classes': ('collapse',),
        'fields': audit_fields(),
        })


def detail_fields():
    """return detail fields"""
    return('is_enabled', 'is_deleted')


def detail_field_set():
    """return detail fields set"""
    return ('Details',
            {
                'classes': ('collapse',),
                'fields': detail_fields()
            })

class AbstractModelAdmin(ModelAdminMixin, admin.ModelAdmin):
    """Base model admin class"""
    list_display = ('id', 'update_time', 'update_user')
    list_filter = ('update_time',)
    date_hierarchy = 'update_time'
    exclude = tuple()
    readonly_fields = base_model_readonly_fields
    ordering = ('id',)

    limit_qs_to_request_user = False

    def save_model(self, request, obj, form, change):
        """Given a model instance save it to the database.

        Override save model implementation.
        """
        self.prepare(request, obj, form, change)
        super(AbstractModelAdmin, self).save_model(request, obj, form, change)

    @classmethod
    def field_sets(cls):
        """return field set."""
        return (detail_field_set(),
                audit_field_set(),
                system_field_set())
