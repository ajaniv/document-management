"""
.. module::  ondalear.backend.docmgmt.admin.user_admin
   :synopsis: document management user admin module.

"""
import logging

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

_logger = logging.getLogger(__name__)



# Unregister the default model admin
admin.site.unregister(User)

# Register  restricted model admin, based on the default UserAdmin
@admin.register(User)
class RestrictedUserAdmin(UserAdmin):
    """Restricted user admin"""
    readonly_fields = ('date_joined',)

    def get_form(self, request, obj=None, **kwargs):
        """get form for editing"""
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        disabled_fields = set()  # type: Set[str]

        # constrain fields
        if not is_superuser:
            disabled_fields |= {
                'username',          # non-admin cannot change username
                'is_superuser',      # non-admin cannot change super user
                'user_permissions'   # allow only group level permission
            }

        # Prevent non-superusers from editing their own permissions
        if (not is_superuser and obj is not None and obj == request.user):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True

        return form
