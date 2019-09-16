"""
.. module:: ondalear.backend.services.base
   :synopsis: text analytics base service  module

"""
import os
from os import path
import logging

from abc import abstractmethod, ABC

_logger = logging.getLogger(__name__)

class AbstractService(ABC):
    """Base serivce class"""

    def __init__(self, name):
        self.name = name
        self.initialized = False

    def is_initialized(self):
        """return True if service has been initialized and False otherwise"""
        return self.initialized

    def config_file_path(self, file_name):  # pylint: disable=no-self-use
        """Construct config file path"""
        this_dir = path.dirname(path.realpath(__file__))
        data_dir = path.join(this_dir, 'config')
        return os.path.join(data_dir, file_name)

    @abstractmethod
    def initialize(self):
        """service initialization"""


_registry = dict()

def register(name, service):
    """register a service"""
    _registry[name] = service

def find(name):
    """find a service"""
    return _registry[name]
