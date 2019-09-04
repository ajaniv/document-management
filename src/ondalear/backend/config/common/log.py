"""
.. module::  ondalear.backend.config.common.log
   :synopsis:  ondalear backend config  log settings file.

Django log settings file.

"""
from __future__ import absolute_import
import os
from ondalear.backend.config.common.root import CURRENT_ENV, LOCAL_ENV, DEV_ENV, LOG_DIR

LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_DEBUG = 'DEBUG'


LOG_LEVEL = (LOG_LEVEL_DEBUG
             if CURRENT_ENV in (DEV_ENV, LOCAL_ENV)
             else LOG_LEVEL_INFO)

# create log directory if required
try:
    os.makedirs(LOG_DIR)
except OSError:
    if not os.path.isdir(LOG_DIR):
        raise

_verbose_format = ('%(asctime)s | %(levelname)s | %(process)d |' +
                   ' %(module)s | %(lineno)d | %(message)s ')

_simple_format = '%(levelname)s %(message)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': _verbose_format
        },
        'simple': {
            'format': _simple_format
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'null': {
            'level': LOG_LEVEL_DEBUG,
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': LOG_LEVEL_DEBUG,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'log_file': {
            'level': LOG_LEVEL_DEBUG,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'maxBytes': 16777216,  # 16megabytes
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': LOG_LEVEL_ERROR,
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        }
    },
    'loggers': {
        'django.db': {
            'handlers': ['console', 'log_file'],
            'level': LOG_LEVEL_INFO,
            'propagate': True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'ondalear.backend.api': {
            'handlers': ['log_file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'ondalear.backend.core': {
            'handlers': ['log_file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'ondalear.backend.docmgmt': {
            'handlers': ['log_file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'ondalear.backend.tests': {
            'handlers': ['log_file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        }
    }
}
