"""
.. module::  ondalear.backend.api.analytics.urls
   :synopsis:  analytics urls module.

"""
from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from ondalear.backend.api.analytics import views

router = routers.DefaultRouter()
router.register(r'analysis-results/crud',
                views.AnalysisResultsViewSet,
                basename='analysis-results-crud')

urlpatterns = [
    url(r'analyze/$', views.NLPAnalysisView.as_view(), name='analyze'),
    path('', include(router.urls)),
]
