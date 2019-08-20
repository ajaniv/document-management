"""
.. module::  ondalear.backend.config.common.root
   :synopsis:  ondalear backend config  root settings module.

Root settings file.

"""
import os
from os import path

ENV_APP = 'APP_ENV'
ENV_DEBUG = 'DJANGO_DEBUG'

LOCAL_ENV = 'LOCAL'
DEV_ENV = 'DEV'
STAGING_ENV = 'STAGING'
PROD_ENV = 'PRODUCTION'

CONFIG_DIR = path.dirname(path.realpath(__file__))
PROJECT_ROOT = path.abspath(path.join(CONFIG_DIR, '../..'))
DB_DIR = path.join(PROJECT_ROOT, 'databases')
LOG_DIR = path.join(PROJECT_ROOT, 'logs')
CURRENT_ENV = os.getenv(ENV_APP, LOCAL_ENV)

_default_debug = True if CURRENT_ENV in (LOCAL_ENV, DEV_ENV) else False  # pylint: disable=simplifiable-if-expression
DEBUG = bool(os.getenv(ENV_DEBUG, _default_debug))

os.environ[ENV_APP] = CURRENT_ENV
os.environ[ENV_DEBUG] = str(DEBUG)
