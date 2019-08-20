"""
.. module::  ondalear.backend.docmgmt.admin
   :synopsis: document management admin package.

This package contains server Django  admin abstractions.

"""
from django.contrib import admin
from ondalear.backend.docmgmt.admin.user_admin import RestrictedUserAdmin
from ondalear.backend.docmgmt.admin.annotation import AnnotationAdmin
from ondalear.backend.docmgmt.admin.classification import Category, Tag
from ondalear.backend.docmgmt.admin.client import ClientAdmin, ClientUserAdmin
from ondalear.backend.docmgmt.admin.derived_document import (AuxiliaryDocumentAdmin,
                                                             ReferenceDocumentAdmin)
from ondalear.backend.docmgmt.admin.document import (DocumentAdmin,
                                                     DocumentAnnotationAdmin,
                                                     DocumentTagAdmin)

admin.site.site_header = "Ondalear Document Managment"          # default: "Django Administration"
admin.site.index_title = "Features"                             # default: "Site administration"
admin.site.site_title = "Ondalear site admin"                   # default: "Django site admin"
