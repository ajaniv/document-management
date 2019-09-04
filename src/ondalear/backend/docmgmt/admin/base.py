"""
.. module::  ondalear.backend.docmgmt.admin.base
   :synopsis: document management admin base module.



"""
import logging
from django.contrib import admin


_logger = logging.getLogger(__name__)

def register(model_classes, admin_classes):
    """register model and admin classes with admin"""
    for model_class, admin_class in zip(model_classes, admin_classes):
        admin.site.register(model_class, admin_class)
