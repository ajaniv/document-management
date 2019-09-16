"""
.. module:: ondalear.backend.urls
   :synopsis: django top level urls module

ondalear document URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from django.views.generic.base import RedirectView

from django.conf.urls.static import static

# pylint: disable=unused-import
from ondalear.backend.config.common.root import (CURRENT_ENV, DEV_ENV,
                                                 LOCAL_ENV, STAGING_ENV, PROD_ENV)

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/admin/')),
    path('docmgmt/', include('ondalear.backend.docmgmt.urls')),
    path('api/analytics/', include('ondalear.backend.api.analytics.urls')),
    path('api/docmgmt/', include('ondalear.backend.api.docmgmt.urls')),
    path('api/admin/site/', include('ondalear.backend.api.site_admin.urls')),
    path('api/admin/user/', include('ondalear.backend.api.user_admin.urls')),
    path('admin/', admin.site.urls)
]

# @TODO: revisit these two urls before pushing out to stage, integ, prod, may be dev only
if CURRENT_ENV in (DEV_ENV, LOCAL_ENV):
    urlpatterns += [
        #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        #path('rest-auth/', include('rest_auth.urls'))
    ]
    urlpatterns += [
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Ondalear Document API",
            default_version='v1',
            description="Document api",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="amnon.janiv@ondalear.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        url(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
    ]
