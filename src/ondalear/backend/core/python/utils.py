"""
.. module::  ondalear.backend.core.python.utils
   :synopsis: python  utilities module.

The *utils* module contains core Python helper functions and classes.

"""
from __future__ import absolute_import
from datetime import datetime, timezone
import traceback
import logging
import os
import shutil
import getpass

_logger = logging.getLogger(__name__)


def utc_now():
    """Return a new time zone aware datetime initialize with utc timezone.

    Returns:
        datetime

    """
    return datetime.now(tz=timezone.utc)


def file_exists(path):
    """Check if file exists.

    Args:
        path (str): File path

    Returns:
        bool
    """
    return os.path.exists(path)


def module_directory(file_path):
    """Return directory of file.

    Args:
        file_path(str): file path.

    Returns:
        str: directory name
    """
    return os.path.dirname(os.path.realpath(file_path))


def stack_trace():
    """Return stack trace.

    Returns:
        str: stack trace

    """
    return traceback.format_exc()


def dict_merge(dict1, dict2):
    """
    Return a dict combining two underlying dict instances.

    Args:
        dict1 (dict): first dict

        dict2 (dic2): second dict

    returns:
        dict: merged dict
    """
    combined = dict(dict1)
    combined.update(dict2)
    return combined


def class_name(cls):
    """
    Return class name given a class instance.

    Args:
        cls (type): class instance.

    Returns:
        str: class name.
    """
    return cls.__name__


def instance_class_name(instance):
    """
    Return class name given an object.

    Args:
        instance (object): object instance.

    Returns:
        str: instance class name.
    """
    return class_name(instance.__class__)


def mkdir(path):
    """
    Create a directory if it does not exist.

    Args:
        path (str): directory path

    Raises:
        OSError if the path exists and it is not a directory
    """
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def rmdir(path):
    """
    Remove directory.

    Args:
        path (str): directory path
    """
    shutil.rmtree(path, ignore_errors=True)


def remove(path):
    """
    Remove a file given the path.

    Args:
        path (str): file path
    """
    try:
        os.remove(path)
    except FileNotFoundError:
        _logger.error('file does not exist %s; stack: %s', path, stack_trace())


def touch(path, times=None):
    """
    Touch a file.

    Args:
        path (str): file path.
    """
    with open(path, 'a'):
        os.utime(path, times)

def get_user():
    """
    Get os user id.
    """
    return getpass.getuser()


class DictObject:
    """
    Python class to give dict non-keyed attribute access.
    Used to convert dictionaries to object instances.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
