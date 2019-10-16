"""
.. module::  ondalear.backend.api.base_queries
   :synopsis:  api base queries module.

"""
import logging
from django.db.models import Q

_logger = logging.getLogger(__name__)



class AbstractQueryMixin:
    """Base class queryset mixin class"""
    def prepare(self):
        """prepare query"""
        request = self.request
        user = request.user
        model_class = self.serializer_class.Meta.model

        # drf checks for model permissions, at which point client has not beed defined yet
        if hasattr(request, 'client'):
            client = request.client
        else:
            client = None

        return model_class, user, client, request

    def protected_model_q(self, user, client):  # pylint: disable=no-self-use
        """protected model qs builder"""
        q_effective = Q(effective_user=user)
        q_client = Q(client=client)
        if not client.is_system:
            # this is a user who belongs to a real client (i.e. Morgan Stanley)
            # get all the groups associated with the user
            qs_groups = user.groups.all()
            q = (Q(effective_user__groups__in=qs_groups) | q_effective) & q_client
            # Filter the documents where the document effective_user group is in the user groups
            # As a safety valve, In case user is not in any group,
            #   still search for user owned documents.
        else:
            # this is a user associated with a pseudo client - system type client.
            q = q_effective & q_client
        return q

    def get_queryset(self):
        """
        This query set should return a list of all the model instances
        for the currently authenticated user.
        """
        # @TODO: analyze query performance
        model_class, user, client, _ = self.prepare()
        # drf checks for model permissions, at which point client has not beed defined yet
        if not client:
            return model_class.objects.all()

        q = self.protected_model_q(user, client)
        qs = model_class.objects.filter(q).order_by('-update_time')
        return qs
