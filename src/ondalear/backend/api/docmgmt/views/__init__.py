"""
.. module::  ondalear.backend.api.docmgmt.views
   :synopsis:  docmgmt api views package.

"""
from ondalear.backend.api.docmgmt.views.annotation import (AnnotationViewSet,
                                                           DocumentAnnotationViewSet,
                                                           DocumentAnnotationDeleteView)
from ondalear.backend.api.docmgmt.views.classification import (CategoryViewSet,
                                                               CategoryHierarchyViewSet,
                                                               DocumentTagViewSet,
                                                               DocumentTagDeleteView,
                                                               TagViewSet,
                                                               TagHierarchyViewSet)
from ondalear.backend.api.docmgmt.views.document import  (AuxiliaryDocumentSummaryViewset,
                                                          DocumentAssociationViewSet,
                                                          DocumentAssociationDeleteView,
                                                          DocumentViewSet,
                                                          ReferenceDocumentSummaryViewset)
from ondalear.backend.api.docmgmt.views.derived_document import (AuxiliaryDocumentViewSet,
                                                                 ReferenceDocumentViewSet)
