"""
.. module::  ondalear.backend.api.user_admin.views
   :synopsis:  user admin views module.

"""
import logging

from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_auth.app_settings import (
    LoginSerializer,
    PasswordChangeSerializer, JWTSerializer, create_token
)
from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode

from ondalear.backend.api.user_admin.serializers import TokenSerializer
from ondalear.backend.api import constants
from ondalear.backend.api.base_views import DRFMixin, response_header

_logger = logging.getLogger(__name__)

sensitive_post_parameters_wrapper = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

def get_response_serializer():
    """build response serializer"""
    if getattr(settings, 'REST_USE_JWT', False):
        response_serializer = JWTSerializer
    else:
        response_serializer = TokenSerializer
    return response_serializer

def update_last_login(user):
    """
    Update last login
    """
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])

# pylint: disable=attribute-defined-outside-init
class UserLoginView(DRFMixin, GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework if configured.
    Accept the following POST parameters: username, password, email
    Return the REST Framework Token Object's key and user details
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel

    @sensitive_post_parameters_wrapper
    def dispatch(self, request, *args, **kwargs):
        return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    def process_login(self):
        """process log in """
        django_login(self.request, self.user)


    def login(self):
        """handle login request

        Only called if the user is active
        """
        self.user = self.serializer.validated_data['user']
        if getattr(settings, "REST_USE_JWT", False):
            self.token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user,
                                      self.serializer)

        if getattr(settings, "REST_SESSION_LOGIN", False):
            self.process_login()
        else:
            update_last_login(self.user)

    def _build_response_data(self, token): # pylint: disable=unused-argument

        """build response data"""
        header = response_header(msg='Successfully logged in.',
                                 username=self.user.username)
        data = {
            'header': header,
            'detail' :{
                'email': self.user.email,
                'token': token,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name
            }
        }
        return data

    def get_response(self):
        """build the response"""
        serializer_class = get_response_serializer()
        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})

        response = Response(
            data=self._build_response_data(serializer.data['key']),
            status=status.HTTP_200_OK)

        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)
        return response

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Handle login post request"""
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        response = self.get_response()
        _logger.info('user logged in: %s', self.user.username)
        return response


class UserLogoutView(DRFMixin, APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.
    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        """Handle get request"""
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            # raises an exceptions
            self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def _build_response_data(self, request, username): # pylint: disable=unused-argument,no-self-use

        """build response data"""
        if username != constants.UNKNOWN_USER:
            api_status = constants.STATUS_OK
            msg = 'Successfully logged out.'
        else:
            api_status = constants.STATUS_ERROR
            msg = 'Failed to log out.'

        header = response_header(msg=msg,
                                 username=username,
                                 api_status=api_status)
        data = {
            'header': header,
            'detail': {}
        }
        return data

    def post(self, request, *args, **kwargs): # pylint: disable=unused-argument
        """Handle logout post request"""
        # If  a valid token has been defined, the user will be authenticated
        # before this methodd is calldd
        return self.logout(request)


    def logout(self, request):  # pylint: disable=no-self-use
        """Handle logout"""
        username = request.user.username or constants.UNKNOWN_USER
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            _logger.warning('failed to delete auth token: %s', username)

        if getattr(settings, 'REST_SESSION_LOGIN', False):
            django_logout(request)
        response = Response(data=self._build_response_data(request, username),
                            status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
        _logger.info('user logged out: %s', username)
        return response

class UserPasswordChangeView(DRFMixin, GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    def _build_response_data(self, request): # pylint: disable=unused-argument,no-self-use
        """build response data"""
        msg = 'New password has been saved.'
        data = {
            'header': response_header(msg, request.user.username),
            'detail': {}
        }
        return data

    @sensitive_post_parameters_wrapper
    def dispatch(self, request, *args, **kwargs):
        """dispatch the request"""
        return super(UserPasswordChangeView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):               # pylint: disable=unused-argument
        """handle password change post request"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response(data=self._build_response_data(request),
                            status=status.HTTP_200_OK)
        _logger.info('user changed password: %s', request.user.username)
        return response
