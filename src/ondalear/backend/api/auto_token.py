"""
.. module::  ondalear.backend.api.auto_token
   :synopsis:  auto token generation   module.

File needs to be imported to have auto token generated.
"""
import logging
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

_logger = logging.getLogger(__name__)

enable_token_registration = False  # change to True to have users issued token on creation

if enable_token_registration:
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):  # pylint: disable=unused-argument
        """
        Auto auth taken generation
        """
        if created:
            Token.objects.create(user=instance)             # pylint: disable=no-member
