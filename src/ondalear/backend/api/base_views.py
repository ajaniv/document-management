"""
.. module::  ondalear.backend.api.base_views
   :synopsis:  api base views module.

"""
import logging
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions

from ondalear.backend.docmgmt.models import ClientUser
from ondalear.backend.api import constants

_logger = logging.getLogger(__name__)


def response_header(msg, username, api_status=constants.STATUS_OK):
    """build response header"""
    return {
        'user': username,
        'api_version': constants.API_VERSION,
        'api_status': api_status,
        'msg': _(msg)
    }


def api_exception_handler(exc, context):
    """Custom exception handler
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        errors = []
        try:
            for key, value in response.data.items():
                if isinstance(value, (list, tuple)):
                    value = value[0]
                elif isinstance(value, (dict)):
                    value = next(iter(value.values()))
                error = dict(key=key, title=value.title(), code=value.code)
                errors.append(error)
        except (KeyError, AttributeError):
            errors = str(response.data)

        data = {
            'header': response_header(msg='Application error',
                                      username=context['request'].user.username,
                                      api_status=constants.STATUS_ERROR),
            'detail': errors
        }
        response.data = data
    else:
        # @TODO: handling system errors, revisit approach
        data = {
            'header': response_header(msg='System error',
                                      username=context['request'].user.username,
                                      api_status=constants.STATUS_ERROR),
            'detail': str(exc)
        }
        response = Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response



class DRFMixin:
    """Django Rest Framework mixin class"""

    def raise_uncaught_exception(self, exc):
        """handle uncaught exception"""
        _logger.exception('uncaught exception')
        breakpoint()
        super(DRFMixin, self).raise_uncaught_exception(exc)

    def initial(self, request, *args, **kwargs):
        """
            Runs anything that needs to occur prior to calling the method handler.
        """
        super(DRFMixin, self).initial(request, *args, **kwargs)

        # fetch the client associated with the user
        user = request.user
        if user.is_authenticated:
            if not user.is_active:
                raise PermissionDenied(detail='User is inactive')
            client_user = ClientUser.objects.get_or_none(user=user)
            if client_user:
                client = client_user.client
                if not client.is_enabled:
                    raise PermissionDenied(detail='Client is disabled')
                request.client = client
            else:
                _logger.warning('no client defined for request user %s', request.user.username)

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.

        Implemented to log requests.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)

        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            _logger.info('start processing method(%s) path(%s) username(%s)',
                         request.method, request.get_full_path(), request.user.username)
            self.initial(request, *args, **kwargs)
            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:                                # pylint: disable=broad-except
            response = self.handle_exception(exc)
            _logger.error('Application error header:%s detail: %s',
                          response.data['header'], response.data['detail'],
                          exc_info=True)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        _logger.info('end processing method(%s) path(%s) username(%s)',
                     request.method, request.get_full_path(), request.user.username)
        return self.response


# pylint: disable=unused-argument,too-many-ancestors,no-self-use

class DRFListModelMixin:
    """Django rest framework list  model mixin class"""

    def build_list_data(self, serializer, username, msg=None, add_pagination=False):
        """build list data"""
        msg = msg or 'List request successfully processed.'
        data = {
            'header': response_header(msg=msg,
                                      username=username,
                                      api_status=constants.STATUS_OK),
            'detail': serializer.data
        }
        if add_pagination:
            data['header']['pagination'] = dict()
        return data

    def list(self, request, *args, **kwargs):
        """Fetch instance list

        Called on GET request for collection endpoint
        """

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        data = dict()
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.build_list_data(serializer=serializer,
                                        username=request.user.username,
                                        add_pagination=True)
            # @TODO: somewhat inefficient usage of pagination, review
            response = self.get_paginated_response(serializer.data)
            for attr in ('count', 'next', 'previous'):
                data['header']['pagination'][attr] = response.data[attr]
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = self.build_list_data(serializer=serializer, username=request.user.username)

        return Response(data=data, status=status.HTTP_200_OK)

class PermissionsMixin:
    """permission mixin class"""
    permission_classes = (permissions.DjangoModelPermissions,)

class AbstractModelViewSet(DRFMixin, PermissionsMixin,
                           DRFListModelMixin, viewsets.ModelViewSet):
    """Base  model view set class.

    """
    # @TODO: This override of ModelViewSet may cause issues in the future
    # if and when the underlying code base changes.

    # apply both authenitcation and model based permissions
    permission_classes = (permissions.DjangoModelPermissions,)

    def _short_response(self, request):         # pylint: disable=no-self-use
        """check if short form of results should be returned on  post or put

        """
        # @TODO: Should check  reqeust header using custom header for setting override
        # @TODO: revisit this approach, still performance imppact in serialization of uneeded data
        return settings.POST_PUT_REQUEST_SHORT_RESPONSE

    def _create_response_detail(self, request, serializer):
        """build create request response detail"""
        def build_item(source):
            """build time data"""
            return dict(id=source['id'],
                        uuid=source['uuid'],
                        creation_time=source['creation_time'],
                        version=source['version'])
        if self._short_response(request):
            data = serializer.data
            if isinstance(data, (list)):
                detail = [build_item(item) for item in data]
            else:
                detail = build_item(data)
        else:
            detail = serializer.data
        return detail

    def _update_response_detail(self, request, serializer):
        """build update request response detail"""
        if self._short_response(request):
            data = serializer.data
            detail = dict(id=data['id'],
                          update_time=data['update_time'],
                          uuid=data['uuid'],
                          version=data['version'])
        else:
            detail = serializer.data
        return detail

    def create(self, request, *args, **kwargs):
        """Create an instance.

        Called on POST request for collection endpoint
        """
        data = request.data
        serializer = self.get_serializer(data=data, many=isinstance(data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        data = {
            'header': response_header(msg='Create request successfully processed.',
                                      username=request.user.username,
                                      api_status=constants.STATUS_OK),
            'detail': self._create_response_detail(request, serializer)
            }

        return Response(data=data, status=status.HTTP_201_CREATED, headers=headers)


    def retrieve(self, request, *args, **kwargs):
        """Fetch an instance.

        Called on GET request for specific instance
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = {
            'header': response_header(msg='Retrieve request successfully processed.',
                                      username=request.user.username,
                                      api_status=constants.STATUS_OK),
            'detail': serializer.data
            }

        return Response(data=data, status=status.HTTP_200_OK)

    def prepare_update(self, request, *args, **kwargs):
        """prepare update hook for subclassing"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return serializer, instance

    def update(self, request, *args, **kwargs):
        """Update an instance.

        Called on PUT and PATCH requests.
        """
        serializer, instance = self.prepare_update(request, *args, **kwargs)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}  # pylint: disable=protected-access

        data = {
            'header': response_header(msg='Update request successfully processed.',
                                      username=request.user.username,
                                      api_status=constants.STATUS_OK),
            'detail': self._update_response_detail(request, serializer)
            }
        return Response(data=data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """delete the instance"""
        return instance.delete()

    def destroy(self, request, *args, **kwargs):
        """Delete an instance

        Called on DELETE request
        """
        instance = self.get_object()

        count_deleted = self.perform_destroy(instance)[0]
        if count_deleted == 0:
            _logger.warning('failed to deleted instance id: %s of type: %s',
                            instance.id, instance.__class__)
        data = {
            'header': response_header(msg='Delete request successfully processed.',
                                      username=request.user.username,
                                      api_status=constants.STATUS_OK),
            'detail': dict(count_deleted=count_deleted)
            }
        return Response(data=data, status=status.HTTP_200_OK)
