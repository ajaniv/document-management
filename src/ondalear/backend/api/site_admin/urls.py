"""
.. module::  ondalear.backend.api.site_admin.urls
   :synopsis:  ondalear site admin urls module.

"""
from django.urls import path, include
from rest_framework import routers
from ondalear.backend.api.site_admin import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'groups', views.GroupViewSet, basename='group')
router.register(r'clients', views.ClientViewSet, basename='client')
router.register(r'client-users', views.ClientUserViewSet, basename='client-user')

urlpatterns = [
    path('', include(router.urls)),
]
