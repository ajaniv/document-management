"""
.. module::  ondalear.backend.docmgmt.models.factories
   :synopsis:  Models factory module.


Note: Factory Meta inheritance does not appear to work consistently
"""

import factory

from ondalear.backend.analytics.models import AnalysisResults
from ondalear.backend.tests.base_factories import AbstractModelFactory
from ondalear.backend.tests.docmgmt.models.factories import ClientModelFactory

class AnalysisResultsModelFactory(AbstractModelFactory):
    """Analysis results model factory class"""
    client = factory.SubFactory(ClientModelFactory)
    name = 'analysis results'
    input = dict()
    output = dict()
    documents = None


    class Meta:
        """Model meta class."""
        abstract = False
        model = AnalysisResults
        django_get_or_create = ('client', 'name')
       