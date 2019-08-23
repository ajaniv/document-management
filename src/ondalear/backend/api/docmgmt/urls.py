"""
.. module::  ondalear.server.api.docmgmt.urls
   :synopsis:  document api urls module.

"""
from django.urls import include, path
from rest_framework import routers
from ondalear.backend.api.docmgmt import views

router = routers.DefaultRouter()

router.register(r'document-associations',
                views.DocumentAssociationViewSet,
                basename='document-association')

router.register(r'auxiliary-documents',
                views.AuxiliaryDocumentViewSet,
                basename='auxiliary-document')
router.register(r'auxiliary-document-summary',
                views.AuxiliaryDocumentSummaryViewset,
                basename='auxiliary-document-summary')

router.register(r'reference-documents',
                views.ReferenceDocumentViewSet,
                basename='reference-document')
router.register(r'reference-document-summary',
                views.ReferenceDocumentSummaryViewset,
                basename='reference-document-summary')

router.register(r'tags',
                views.TagViewSet,
                basename='tag')
router.register(r'document-tags',
                views.DocumentTagViewSet,
                basename='document-tag')

router.register(r'categories',
                views.CategoryViewSet,
                basename='category')

router.register(r'annotations',
                views.AnnotationViewSet,
                basename='annotation')
router.register(r'document-annotations',
                views.DocumentAnnotationViewSet,
                basename='document-annotation')

urlpatterns = [
    path('', include(router.urls)),
]
