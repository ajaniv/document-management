"""
.. module::  ondalear.backend.core.django.utils
   :synopsis:  basic  Django utilities module.

The *utils* module is a collection of Django utility functions.

"""
from django.contrib.sites.models import Site
from django.utils import timezone
from django.db import connection

def current_site(request=None):
    """Return site instances.
    """
    return Site.objects.get_current(request)


def oldest_timestamp():
    """Return oldest environment timestamp
    """
    return timezone.now().replace(year=2000, month=1, day=1,
                                  hour=0, minute=0, second=0,
                                  microsecond=0)

def connection_vendor():
    """return name of current connection vendor"""
    return connection.vendor

def is_connection_sqlite():
    """return true if current connection is to an sqlite db"""
    return connection_vendor() == 'sqlite'

def is_connection_postgres():
    """return true if current connection is to an postgres db"""
    return connection_vendor() == 'postgresql'
