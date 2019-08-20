"""
.. module::  ondalear.backend.core.django.storage
   :synopsis:  Django storage module.

Django storage utilities and classes.
"""
from __future__ import absolute_import
import os
import ntpath  #  support non unix file upload
import logging
from django.core.files.storage import get_storage_class

_logger = logging.getLogger(__name__)

class OverwriteStorage(get_storage_class()):
    """OverwriteStorage class definition.

    Delete existing file before saving it.
    """
    def save(self, name, content, max_length=None):
        """
        Save new content to the file specified by name. The content should be
        a proper File object or any Python file-like object, ready to be read
        from the beginning.
        """
        self.delete(name)
        return super(OverwriteStorage, self).save(name, content, max_length)

def client_directory_path(instance, filename):
    """Upload file to client directory"""
    # @TODO:
    #  need to get client from instance, workout details of upload
    # file will be uploaded to MEDIA_ROOT/client_<id>/<filename>
    file_name = ntpath.split(filename)[1]
    dir_path = instance.dir_path
    if dir_path:
        if os.path.isabs(dir_path):
            dir_path = dir_path[1:]
        file_path = os.path.join(instance.document.client.client_id,
                                 instance.document.effective_user.username, dir_path, file_name)
    else:
        file_path = os.path.join(instance.document.client.client_id,
                                 instance.document.effective_user.username, file_name)
    return file_path

overwrite_storage = OverwriteStorage()
