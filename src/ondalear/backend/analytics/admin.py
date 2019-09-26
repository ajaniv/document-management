"""
.. module::  ondalear.backend.analytics.admin
   :synopsis: analytics admin module.

This module contains analytics admin abstractions.

"""
import logging

from ondalear.backend.core.django.admin import register, AbstractModelAdmin
from ondalear.backend.analytics.models import  AnalysisResults

_logger = logging.getLogger(__name__)


_analysis_results_fields = ('client', 'name', 'description', 'input', 'output', 'documents')

class AnalysisResultsAdmin(AbstractModelAdmin):
    """AnalysisResults model admin class.
    """
    list_display = AbstractModelAdmin.list_display + ('client_id', 'name')
    fieldsets = (
        ('Analysis results',
         {'fields': _analysis_results_fields}),
    ) + AbstractModelAdmin.field_sets()     # pylint: disable=no-member

# Register the models and admin classes
model_classes = (AnalysisResults,)
admin_classes = (AnalysisResultsAdmin,)

register(model_classes, admin_classes)
