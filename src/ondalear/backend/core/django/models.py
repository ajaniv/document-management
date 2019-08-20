"""
.. module::  ondalear.backend.core.django.models
   :synopsis:  Django core  models module.

Django  model utilities and classes.
"""
from __future__ import absolute_import

import logging

import inflection
from django.contrib.sites.models import Site
from django.db import models

from ondalear.backend.core.python.utils import instance_class_name
from ondalear.backend.core.django import constants, fields

_logger = logging.getLogger(__name__)


def verbose_class_name(name):
    """Generate verbose name from class name.
    """
    verbose_name = inflection.underscore(name)
    verbose_name = verbose_name.replace('_', ' ')
    return verbose_name


def pluralize(name):
    """Pluralize a name.
    """
    return inflection.pluralize(name)


def db_table_for_class(name):
    """Convert class name to db table name.
    """
    table_name = inflection.underscore(name)
    return table_name


def db_table_for_app_and_class(app_name, table_name, site_label):
    """Generate application table name.
    """
    site_label = site_label or constants.SITE_LABEL
    return '{}_{}_{}'.format(site_label, app_name, table_name)


def db_table(app_name, name, site_label=None):
    """Generate db table name from app and class.
    """
    return db_table_for_app_and_class(
        app_name, db_table_for_class(name), site_label)


class BaseModelManager(models.Manager):
    """Base object manager class.
    """

    def get_or_none(self, *args, **kwargs):
        """Return an object instance or none.

        :param args: Positional argument list.
        :type args: list.
        :param kwargs: Key words arguments.
        :type kwargs: dict.
        :returns:  An instance of Model or None.
        """
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None

related_name_base = "%(app_label)s_%(class)s_related_"


class AbstractModel(models.Model):
    """An abstract base class for application models.
    """

    id = fields.auto_field()
    uuid = fields.uuid_field(blank=False, null=False,)
    version = fields.integer_field(blank=False, null=False)
    is_enabled = fields.boolean_field(blank=False, null=False, default=True)
    is_deleted = fields.boolean_field(blank=False, null=False, default=False)
    creation_time = fields.datetime_field(blank=False, null=False, auto_now_add=True)
    update_time = fields.datetime_field(blank=False, null=False, auto_now=True)

    # user who created the instance
    creation_user = fields.user_field(
        related_name=related_name_base + "creation_user")

    # user who triggered the instance update
    update_user = fields.user_field(
        related_name=related_name_base + "update_user")

    # user on whose behalf change is made
    effective_user = fields.user_field(
        related_name=related_name_base + "effective_user")

    site = fields.foreign_key_field(
        Site,
        related_name=related_name_base + "site")

    objects = BaseModelManager()

    class Meta:
        """Meta class declaration."""
        abstract = True
        get_latest_by = "update_time"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """Save an instance.
        """
        self.full_clean()
        self.version += 1
        super(AbstractModel, self).save(force_insert=False, force_update=False, using=None,
                                        update_fields=None)

    def __str__(self):
        return '{0} object {1.id!s} {1.uuid!s} {1.version!s}'.format(
            instance_class_name(self), self)
