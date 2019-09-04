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

# SECURITY WARNING: keep the secret key used in production secret!
DEFAULT_SECRET_KEY = 's@(%n-fg3c$)#%#)#7#9$nudp*2%arq)^_1m0w!!rl!k_&9f##'
SECRET_KEY = os.getenv(ENV_APP_KEY, DEFAULT_SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# @TODO: revisit approach to allowed hosts; would require changes for different
#     docker machine configurations
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# these need to be redefined per deployment target (LOCAL, GCP, AWS)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
