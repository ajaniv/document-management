"""
.. module::  ondalear.server.api.docmgmt.urls
   :synopsis:  document api urls module.

"""
from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from ondalear.backend.api.docmgmt import views

router = routers.DefaultRouter()

router.register(r'document-association',
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
router.register(r'document-tag',
                views.DocumentTagViewSet,
                basename='document-tag')
router.register(r'tags-hiearchy',
                views.TagHierarchyViewSet,
                basename='tag-hierarchy')

router.register(r'categories',
                views.CategoryViewSet,
                basename='category')
router.register(r'categories-hiearchy',
                views.CategoryHierarchyViewSet,
                basename='category-hierarchy')

router.register(r'annotations',
                views.AnnotationViewSet,
                basename='annotation')
router.register(r'document-annotation',
                views.DocumentAnnotationViewSet,
                basename='document-annotation')

urlpatterns = [
    path('', include(router.urls)),
    url(r'document-annotation-delete-many/$',
        views.DocumentAnnotationDeleteView.as_view(),
        name='document-annotation-delete-many-list'),
    url(r'document-association-delete-many/$',
        views.DocumentAssociationDeleteView.as_view(),
        name='document-association-delete-many-list'),
    url(r'document-tag-delete-many/$',
        views.DocumentTagDeleteView.as_view(),
        name='document-tag-delete-many-list'),
]
