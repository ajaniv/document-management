"""
.. module::  ondalear.backend.api.docmgmt.serializers
   :synopsis:  docmgmt api serializers package.

"""
from ondalear.backend.api.docmgmt.serializers.annotation import (DocumentAnnotationSerializer,
                                                                 AnnotationSerializer)
from ondalear.backend.api.docmgmt.serializers.classification import (CategorySerializer,
                                                                     DocumentTagSerializer,
                                                                     TagSerializer)
from ondalear.backend.api.docmgmt.serializers.derived_document import (AuxiliaryDocumentSerializer,
                                                                       ReferenceDocumentSerializer)
from ondalear.backend.api.docmgmt.serializers.document import (DocumentSerializer,
                                                               DocumentAssociationSerializer,
                                                               DocumentSummarySerializer)
