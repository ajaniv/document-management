"""
.. module::  ondalear.backend.api.docmgmt.views.classification
   :synopsis:  ondalaer docmgmt classification views module.

"""
import logging
from collections import defaultdict
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from ondalear.backend.docmgmt.models import Category, DocumentTag, Tag
from ondalear.backend.api import constants
from ondalear.backend.api.base_views import response_header, AbstractModelViewSet
from ondalear.backend.api.docmgmt.serializers import (CategorySerializer,
                                                      DocumentTagSerializer,
                                                      TagSerializer)

from ondalear.backend.api.docmgmt.views.queries import (ClassificationQueryMixin,
                                                        DocumentTagQueryMixin)
from ondalear.backend.api.docmgmt.views.base import AssociationViewSet

# pylint: disable=too-many-ancestors

_logger = logging.getLogger(__name__)

class HierarchyMixin:
    """Hierachy action mixin class"""
    def response_data(self, data, username):  # pylint: disable=no-self-use
        """build response data"""
        msg = 'Hierarchy request successfully processed.'
        data = {
            'header': response_header(msg=msg,
                                      username=username,
                                      api_status=constants.STATUS_OK),
            'detail': data
        }
        return data

    def build_child_data(self, cache, instance):
        """build child data"""
        children = []
        sub_children = []
        for child in cache[instance.id]['children']:
            if child.id in cache:
                sub_children = self.build_child_data(cache, child)
            children.append(dict(name=child.name, children=sub_children))
        return children

    def process_query(self):
        """process query"""
        queryset = self.filter_queryset(self.get_queryset())
        instances = list(queryset)
        cache = {}
        for instance in instances:
            if instance.parent:
                # has a parent
                if instance.parent.id not in cache:
                    # parent not yet in cache
                    cache[instance.parent.id] = dict(instance=instance.parent, children=[instance])
                else:
                    # parent in cache
                    cache[instance.parent.id]['children'].append(instance)
            else:
                if instance.id not in cache:
                    cache[instance.id] = dict(instance=instance, children=[])
        roots = [instance for instance in instances if instance.parent is None]
        clients = {instance.client for instance in roots}
        return cache, roots, clients

    def build_hierarchy(self, request):
        """Return tag hierarchy"""
        instance_cache, roots, clients = self.process_query()

        client_cache = defaultdict(list)

        for client in clients:
            root_cache = defaultdict(list)
            # There can be a mixture of system and non-system clients for which there is data
            for root in roots:
                if root.client.id == client.id:
                    children = self.build_child_data(instance_cache, root)
                    parent = dict(name=root.name, children=children)
                    root_cache[root.target].append(parent)
            client_cache[client.name].append(root_cache)

        data = self.response_data(client_cache, username=request.user.username)

        return Response(data=data, status=status.HTTP_200_OK)

class TagViewSet(ClassificationQueryMixin, HierarchyMixin, AbstractModelViewSet):
    """Tag view class"""
    queryset = Tag.objects.all().order_by('-update_time')
    serializer_class = TagSerializer

    @action(detail=False)
    def hierarchy(self, request):
        """handle tag hierarchy request"""
        return self.build_hierarchy(request)

class DocumentTagViewSet(AssociationViewSet,            # pylint: disable=abstract-method
                         DocumentTagQueryMixin,
                         AbstractModelViewSet):
    """Document tag association view class"""
    queryset = DocumentTag.objects.all().order_by('-update_time')
    serializer_class = DocumentTagSerializer



class CategoryViewSet(ClassificationQueryMixin, HierarchyMixin, AbstractModelViewSet):
    """Category view class"""
    queryset = Category.objects.all().order_by('-update_time')
    serializer_class = CategorySerializer

    @action(detail=False)
    def hierarchy(self, request):
        """handle category hierarchy request"""
        return self.build_hierarchy(request)
