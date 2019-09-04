"""
.. module::  ondalear.backend.api.user_admin.urls
   :synopsis:  user admin urls module.

"""
from django.conf.urls import url

from ondalear.backend.api.user_admin import views

urlpatterns = [
    # URLs that do not require a valid token
    url(r'login/$', views.UserLoginView.as_view(), name='user_login'),

    # URLs that require a user to be logged in with a valid session / token.
    url(r'logout/$', views.UserLogoutView.as_view(), name='user_logout'),
    url(r'password/change/$', views.UserPasswordChangeView.as_view(), name='user_password_change'),
]
