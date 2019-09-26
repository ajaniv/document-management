"""
.. module:: ondalear.backend.docmgmt.urls
   :synopsis: ondalear docmgmt  urls  module.

"""
from django.urls import path
from ondalear.backend.docmgmt import views


urlpatterns = [
    path('index/', views.index, name='index'),
]
