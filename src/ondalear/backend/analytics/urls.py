"""
.. module:: ondalear.backend.analytics.urls
   :synopsis: ondalear analytics urls  module.

"""
from django.urls import path
from ondalear.backend.docmgmt import views


urlpatterns = [
    path('index/', views.index, name='index-analytics'),
]
