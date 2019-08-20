"""
.. module::  ondalear.backend.config.dev
   :synopsis:  dev environment settings file.

dev environment settings file.

"""
# pylint: disable=wildcard-import,unused-wildcard-import
from __future__ import absolute_import
import os
from ondalear.backend.config.common.root import *
from ondalear.backend.config.common.django import *
from ondalear.backend.config.common.log import *


# @TODO: revisit approach to allowed hosts; would require changes for different
#     docker machine configurations
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# these need to be redefined per deployment target (LOCAL, GCP, AWS)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
