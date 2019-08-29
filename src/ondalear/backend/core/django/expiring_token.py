"""
.. module:: ondalear.backend.core.django.expiring_token
   :synopsis: Expirint token module.


"""
import logging
from  datetime import datetime, timedelta
import pytz
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

_logger = logging.getLogger(__name__)

class ExpiringTokenAuthentication(TokenAuthentication):
    """Expiring token authentication"""

    def authenticate_credentials(self, key):
        """authenticate the credentials"""
        user, token = super().authenticate_credentials(key)
        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(hours=settings.TOKEN_EXPIRY):
            _logger.warning('token for user % has expired', user.username)
            token.delete()
            raise AuthenticationFailed('Token has expired')

        return user, token
