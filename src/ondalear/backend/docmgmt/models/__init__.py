"""
.. module::  ondalear.backend.docmgmt.models
   :synopsis: documents models package.

This package contains server model abstractions.

"""
from ondalear.backend.docmgmt.models.annotation import Annotation
from ondalear.backend.docmgmt.models.classification import Tag, Category
from ondalear.backend.docmgmt.models.client import Client, ClientUser
from ondalear.backend.docmgmt.models.document import (AuxiliaryDocument,
                                                      Document,
                                                      ReferenceDocument)

from ondalear.backend.docmgmt.models.document_annotation import DocumentAnnotation
from ondalear.backend.docmgmt.models.document_association import DocumentAssociation
from ondalear.backend.docmgmt.models.document_tag import DocumentTag



# @TODO: User: add custom user
# @TODO: Client: add address, phone, email, description
# @TODO: which document types are loaded: html, pdf, .doc, .txt,
#   what conversion, validation is required for each one
# @TODO need to figure out whether Document.dir_path requires a level
#   of naming constrainsts, validation
# @TODO: is the field effective_user required?
# @TODO: per model review missing validation
# @TODO: save is calling full clean, will result in full clean being called twice when
#   working within context of django admin
