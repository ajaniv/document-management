"""
.. module::  ondalear.backe.site.settings_test
   :synopsis:  test settings module.

"""
# pylint: disable=wildcard-import,unused-wildcard-import
from ondalear.backend.site.settings import *  # @UnusedWildImport

# disable throttling during unit tests
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = tuple()
