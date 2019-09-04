"""
.. module::  ondalear.server.api.docmgmt.urls
   :synopsis:  document api urls module.

"""
from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from ondalear.backend.api.docmgmt import views

router = routers.DefaultRouter()

router.register(r'documents/associations/crud',
                views.DocumentAssociationViewSet,
                basename='document-association-crud')

router.register(r'documents/auxiliary/crud',
                views.AuxiliaryDocumentViewSet,
                basename='auxiliary-document-crud')
router.register(r'documents/auxiliary/summary',
                views.AuxiliaryDocumentSummaryViewset,
                basename='auxiliary-document-summary')

router.register(r'documents/reference/crud',
                views.ReferenceDocumentViewSet,
                basename='reference-document-crud')
router.register(r'documents/reference/summary',
                views.ReferenceDocumentSummaryViewset,
                basename='reference-document-summary')

router.register(r'tags/crud',
                views.TagViewSet,
                basename='tag-crud')
router.register(r'tags/hiearchy',
                views.TagHierarchyViewSet,
                basename='tag-hierarchy')
router.register(r'documents/tags/crud',
                views.DocumentTagViewSet,
                basename='document-tag-crud')


router.register(r'categories/crud',
                views.CategoryViewSet,
                basename='category-crud')
router.register(r'categories/hiearchy',
                views.CategoryHierarchyViewSet,
                basename='category-hierarchy')

router.register(r'annotations/crud',
                views.AnnotationViewSet,
                basename='annotation-crud')
router.register(r'documents/annotations/crud',
                views.DocumentAnnotationViewSet,
                basename='document-annotation-crud')

urlpatterns = [
    path('', include(router.urls)),
    url(r'documents/annotations/delete-many/$',
        views.DocumentAnnotationDeleteView.as_view(),
        name='document-annotation-delete-many-list'),
    url(r'documents/associations/delete-many/$',
        views.DocumentAssociationDeleteView.as_view(),
        name='document-association-delete-many-list'),
    url(r'documents/tags/delete-many/$',
        views.DocumentTagDeleteView.as_view(),
        name='document-tag-delete-many-list'),
]
