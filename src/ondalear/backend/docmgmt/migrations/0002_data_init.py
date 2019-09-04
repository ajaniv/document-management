"""
.. module::  ondalear.migrations.data_init
   :synopsis:  database data initialization.

"""
from __future__ import unicode_literals, absolute_import
import os
import logging
from django.db import migrations
from django.contrib.auth.models import User     # where User lives

_logger = logging.getLogger(__name__)

#pylint: disable=unused-argument

def forwards_func(apps, schema_editor):
    """Create required data
       build the user you now have access to via Django magic
    """
    # User = apps.get_model("auth", "User")
    admin = User.objects.create_superuser(
        username=os.getenv("SITE_ADMIN_USER", "admin"),
        email=os.getenv("SITE_ADMIN_USER_EMAIL", "admin@ondalear.com"),
        password=os.getenv("SITE_ADMIN_PASSWORD", "admin"),
        is_staff=True,
        is_superuser=True)
    assert isinstance(admin, (User,))
    _logger.info("created super user: %s", admin.username)


def reverse_func(apps, schema_editor):
    """destroy what forward_func builds"""


class Migration(migrations.Migration):
    """Migration class declaration"""

    dependencies = [
        ('docmgmt', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
