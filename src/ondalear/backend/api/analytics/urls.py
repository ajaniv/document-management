"""
.. module::  ondalear.backend.api.analytics.urls
   :synopsis:  analytics urls module.

"""
from django.conf.urls import url

from ondalear.backend.api.analytics import views

urlpatterns = [
    url(r'analyze/$', views.NLPAnalysisView.as_view(), name='analyze'),
]
