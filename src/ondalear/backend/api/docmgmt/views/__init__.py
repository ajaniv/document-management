"""
.. module::  ondalear.backend.api.docmgmt.views
   :synopsis:  docmgmt api views package.

"""
from ondalear.backend.api.docmgmt.views.annotation import (AnnotationViewSet,
                                                           DocumentAnnotationViewSet)
from ondalear.backend.api.docmgmt.views.classification import (CategoryViewSet,
                                                               DocumentTagViewSet,
                                                               TagViewSet)
from ondalear.backend.api.docmgmt.views.document import  (AuxiliaryDocumentSummaryViewset,
                                                          DocumentAssociationViewSet,
                                                          DocumentViewSet,
                                                          ReferenceDocumentSummaryViewset)
from ondalear.backend.api.docmgmt.views.derived_document import (AuxiliaryDocumentViewSet,
                                                                 ReferenceDocumentViewSet)
