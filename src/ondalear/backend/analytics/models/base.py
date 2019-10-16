"""
.. module:: ondalear.backend.analytics.models.base
   :synopsis: ondalear backend analytics models base  module.


"""
import logging
from ondalear.backend.core.django.models import AbstractModel
from ondalear.backend.analytics.apps import AnalyticsConfig

_logger = logging.getLogger(__name__)
app_label = AnalyticsConfig.name

class AbstractAnalyticsModel(AbstractModel):
    """Base analytics model class
    """
    class Meta(AbstractModel.Meta):
        """Meta class definition"""
        abstract = True
        app_label = app_label
