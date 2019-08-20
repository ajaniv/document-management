"""
.. module:: ondalear.backend.docmgmt.models.validators
   :synopsis: ondalear backend models validator  module.

The *validator* module contains model validation abstractions.

"""
import logging
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ondalear.backend.docmgmt.models import constants
_logger = logging.getLogger(__name__)


def content_type_validator(value):
    """validate content type"""
    if value not in constants.MIME_TYPES:
        raise ValidationError(
            _('%(value)s is not a valid content type'),
            params={'value': value},
        )
