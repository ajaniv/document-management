"""
.. module:: ondalear.backend.docmgmt.models.base
   :synopsis: ondalear backend models base  module.

The *base* module contains common server model abstractions.

"""
import logging
from ondalear.backend.core.django.models import AbstractModel
from ondalear.backend.docmgmt.apps import DocumentManagementConfig

_logger = logging.getLogger(__name__)
app_label = DocumentManagementConfig.name

class AbstractDocumentManagementModel(AbstractModel):
    """Base document model class
    """
    class Meta(AbstractModel.Meta):
        """Meta class definition"""
        abstract = True
        app_label = app_label
