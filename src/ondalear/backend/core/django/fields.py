"""
.. module::  ondalear.backend.core.django.fields
   :synopsis:  django fields model  utilities module.

The *fields* module is a collection of Django model fields utilities
designed to foster common field usage and facilitate configuration changes.
"""
import os
import uuid
import inspect
import inflection
import magic

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import JSONField
from django.template.defaultfilters import filesizeformat
from jsonfield import JSONField as CustomJSONField

from phonenumber_field.modelfields import PhoneNumberField
from constrainedfilefield.fields import ConstrainedFileField
from timezone_field import TimeZoneField

from ondalear.backend.core.django.utils import is_connection_sqlite, is_connection_postgres
from ondalear.backend.core.python.utils import class_name


# Note: each factory function has '_field' suffix to minimize conflicts with
# core and 3rd party python modules and foster naming consistency albeit
# while introducing somewhat undesirable verbosity
#

class MimeTypeConstrainedFileField(ConstrainedFileField):
    """Enhanced implementation to obtain mime type"""
    # pylint: disable=arguments-differ,no-member,attribute-defined-outside-init,arguments-differ
    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        data = models.FileField.clean(self, value, model_instance)

        if self.max_upload_size and data.size > self.max_upload_size:
            # Ensure no one bypasses the js checker
            raise ValidationError(
                _('File size exceeds limit: %(current_size)s. Limit is %(max_size)s.') %
                {'max_size': filesizeformat(self.max_upload_size),
                 'current_size': filesizeformat(data.size)})

        if self.content_types:
            file = data.file
            uploaded_content_type = getattr(file, 'content_type', '')

            # magic_file_path used only for Windows.
            magic_file_path = getattr(settings, "MAGIC_FILE_PATH", None)
            if magic_file_path and os.name == 'nt':
                mg = magic.Magic(mime=True, magic_file=magic_file_path)
            else:
                mg = magic.Magic(mime=True)
            content_type_magic = mg.from_buffer(file.read(self.mime_lookup_length))
            file.seek(0)

            # Prefer mime-type from magic over mime-type from http header
            if uploaded_content_type != content_type_magic:
                uploaded_content_type = content_type_magic

            if uploaded_content_type not in self.content_types:
                raise ValidationError(
                    _('Unsupported file type: %(type)s. Allowed types are %(allowed)s.') %
                    {'type': content_type_magic,
                     'allowed': self.content_types})
            self.content_type = content_type_magic
        return data

def auto_field(**kwargs):
    """Return a new instance of auto increment model field.
    """
    defaults = dict(
        blank=True,
        null=False,
        primary_key=True,
        unique=True)
    defaults.update(kwargs)
    return models.AutoField(**defaults)


def boolean_field(**kwargs):
    """Return a new instance of boolean model field.
    """
    defaults = dict(
        blank=False,
        null=False,
        default=False)
    defaults.update(kwargs)
    return models.BooleanField(**defaults)

def constrained_file_field(upload_to, **kwargs):
    """
    Return a new instance of a constrained file model field
    """

    return MimeTypeConstrainedFileField(upload_to=upload_to, **kwargs)

def file_field(upload_to, **kwargs):
    """
    Return a new instance of file model field.
    """
    breakpoint()
    return models.FileField(upload_to=upload_to, **kwargs)

CHAR_FIELD_MAX_LENGTH = 1024


def char_field(**kwargs):
    """Return a new instance of char model field.
    """
    defaults = dict(
        max_length=CHAR_FIELD_MAX_LENGTH,
        blank=False,
        null=False,
        unique=False)
    defaults.update(kwargs)
    return models.CharField(**defaults)


def date_field(**kwargs):
    """Return a new instance of date model field.
    """
    defaults = dict(auto_now=False,
                    auto_now_add=False,
                    blank=False,
                    null=False)
    defaults.update(kwargs)
    return models.DateField(**defaults)


def datetime_field(**kwargs):
    """Return a new instance of datetime model field.
    """
    defaults = dict(auto_now=False,
                    auto_now_add=False,
                    blank=False,
                    null=False)
    defaults.update(kwargs)
    return models.DateTimeField(**defaults)


def decimal_field(max_digits, decimal_places, **kwargs):
    """Return a new instance of decimal model field.
    """
    defaults = dict(
        decimal_places=decimal_places,
        max_digits=max_digits,
        default=0,
        blank=False, null=False)
    defaults.update(kwargs)
    return models.DecimalField(**defaults)


def floating_point_field(**kwargs):
    """Return a new instance of floating point model field.
    """
    defaults = dict(
        blank=False,
        null=False,
        default=0.0)
    defaults.update(kwargs)
    return models.FloatField(**defaults)


def foreign_key_field(to_class, **kwargs):
    """Return a new instance of foreign key model field.
    """
    defaults = dict(
        blank=False,
        db_constraint=True,
        null=False,
        on_delete=models.PROTECT)

    defaults.update(kwargs)
    return models.ForeignKey(to_class, **defaults)


def image_field(**kwargs):
    """Return a new instance of image model field.
    """
    return models.ImageField(**kwargs)


def integer_field(**kwargs):
    """Return a new instance of integer model field.
    """
    defaults = dict(
        default=0,
        blank=False, null=False)
    defaults.update(kwargs)
    return models.IntegerField(**defaults)


def ip_address_field(**kwargs):
    """Return a new instance of ip address model field.
    """
    defaults = dict(
        null=False,
        blank=False)
    defaults.update(kwargs)
    return models.GenericIPAddressField(**defaults)


def many_to_many_field(to_class, db_table=None, **kwargs):
    """Return a new instance of many to many model field.
    """
    defaults = dict(
        db_constraint=True)

    related_name = kwargs.pop('related_name', None)
    defaults.update(kwargs)

    if inspect.isclass(to_class):
        related_name = (
            related_name or
            '{}_set'.format(inflection.camelize(class_name(to_class))))

    return models.ManyToManyField(
        to_class,
        db_table=db_table,
        related_name=related_name,
        **defaults)


def one_to_one_field(to_class, **kwargs):
    """Return a new instance of one-to-one model field.
    """
    defaults = dict(
        blank=False,
        db_constraint=True,
        null=False,
        on_delete=models.PROTECT)

    defaults.update(kwargs)
    return models.OneToOneField(to_class, **defaults)


def small_integer_field(**kwargs):
    """Return a new instance of small integer model field.
    """
    defaults = dict(
        default=0,
        blank=False, null=False)
    defaults.update(kwargs)
    return models.SmallIntegerField(**defaults)


def text_field(**kwargs):
    """Return a new instance of text model field.
    """
    defaults = dict(
        blank=True,
        null=True,
        unique=False)
    defaults.update(kwargs)
    return models.TextField(**defaults)

URL_FIELD_MAX_LENGTH = 255


def url_field(**kwargs):
    """Return a new instance of url model field.
    """
    defaults = dict(
        max_length=URL_FIELD_MAX_LENGTH,
        null=False,
        blank=False)
    defaults.update(kwargs)
    return models.URLField(**defaults)


def uuid_field(**kwargs):
    """Return a new instance of uuid model field.
    """
    defaults = dict(
        unique=True,
        default=uuid.uuid4,
        db_index=True,
        editable=False)
    defaults.update(kwargs)
    return models.UUIDField(**defaults)


def annotation_field(**kwargs):
    """Return a new instance of annotation model field.
    """
    defaults = dict(
        blank=False,
        null=False,
        unique=False)
    defaults.update(kwargs)
    return text_field(**defaults)


def comments_field(**kwargs):
    """Return a new instance of comments model field.
    """
    defaults = dict(
        blank=True,
        null=True,
        unique=False)
    defaults.update(kwargs)
    return text_field(**defaults)


def description_field(**kwargs):
    """Return a new instance of description model field.
    """
    defaults = dict(
        blank=False,
        null=False,
        unique=False)
    defaults.update(kwargs)
    return text_field(**defaults)

GEO_LOCATION_MAX_DIGITS = 9
GEO_LOCATION_DECIMAL_PLACES = 6


def latitude_validator(value):
    """Perform latitude validation.
    """
    valid = -90 < value < 90
    if not valid:
        raise ValidationError(_('latitude not in range of -90 < value < 90'))
    return value


def longitude_validator(value):
    """Perform longitude validation.
    """
    valid = -180 < value < 180
    if not valid:
        raise ValidationError(_('longitude not in range of -90 < value < 90'))
    return value


def geo_location_field(**kwargs):
    """Return a new instance of geo location model field.
    """
    defaults = dict(
        max_digits=GEO_LOCATION_MAX_DIGITS,
        decimal_places=GEO_LOCATION_DECIMAL_PLACES)
    defaults.update(kwargs)
    return decimal_field(**defaults)


def longitude_field(**kwargs):
    """Return new instance of longitude field.
    """
    defaults = dict(
        validators=[longitude_validator])
    defaults.update(kwargs)
    return geo_location_field(**defaults)


def latitude_field(**kwargs):
    """Return new instance of latitude field.
    """
    defaults = dict(
        validators=[latitude_validator])
    defaults.update(kwargs)
    return geo_location_field(**defaults)


NAME_FIELD_MAX_LENGTH = 255


def name_field(**kwargs):
    """Return a new instance of name model field.
    """
    defaults = dict(
        max_length=NAME_FIELD_MAX_LENGTH,
        unique=True,
        db_index=True,
        null=False,
        blank=False)
    defaults.update(kwargs)
    return char_field(**defaults)


def user_field(**kwargs):
    """Return a new instance of a user model field.
    """
    return foreign_key_field(User, **kwargs)



USER_AGENT_FIELD_MAX_LENGTH = 512


def user_agent_field(**kwargs):
    """Return a new instance of user agent model field.
    """
    defaults = dict(
        null=False,
        blank=False,
        max_length=USER_AGENT_FIELD_MAX_LENGTH)
    defaults.update(kwargs)
    return char_field(**defaults)

# @TODO: revisit approach for default time zone field
DEFAULT_TIMEZONE = 'America/New_York'


def timezone_field(**kwargs):
    """Create time zone field instance.
    """
    defaults = dict(
        null=False,
        blank=False,
        default=DEFAULT_TIMEZONE)
    defaults.update(kwargs)
    return TimeZoneField(**defaults)


def phone_number_field(**kwargs):
    """Create phone number field instance.
    """
    defaults = dict(
        null=False,
        blank=False)
    defaults.update(kwargs)
    return PhoneNumberField(**defaults)


def email_field(**kwargs):
    """Create email field instance.
    """
    defaults = dict(
        null=False,
        blank=False)
    defaults.update(kwargs)
    return models.EmailField(**defaults)

# @TODO: make im schemes configurable
im_schemes = ["aim", "gtalk", "im", "msnim", "skype", "sms", "xmpp", ]


class InstantMessagingField(models.URLField):
    """Instant messaging field class."""
    default_validators = [validators.URLValidator(schemes=im_schemes)]


def instant_messaging_field(**kwargs):
    """Create instance messaging field instance.
    """
    defaults = dict(
        null=False,
        blank=False)
    defaults.update(kwargs)
    return InstantMessagingField(**defaults)

_url_schemes = ['http', 'https', 'ftp', 'ftps']
_other_schemes = ['tel', 'mailto', 'urn']
_uri_schemes = im_schemes + _url_schemes + _other_schemes


def uri_field(**kwargs):
    """Create uri field instance.

    Generic uri capture and validation.
    """
    defaults = dict(
        null=False,
        blank=False,
        validators=[validators.URLValidator(schemes=_uri_schemes)])
    defaults.update(kwargs)
    return url_field(**defaults)


def percent_validator(value):
    """Perform percent validation.
    """
    valid = 0 <= value <= 100
    if not valid:
        raise ValidationError(_('value not in range of 0 <= value <= 100'))
    return value


def percentage_field(**kwargs):
    """Create a percentage field instance.
    """
    defaults = dict(validators=[percent_validator])
    defaults.update(kwargs)
    return floating_point_field(**defaults)


def json_field(**kwargs):
    """Create a json field instance.
    """
    defaults = dict(
        null=False,
        blank=False)
    defaults.update(kwargs)
    if is_connection_postgres():
        cls = JSONField
    elif is_connection_sqlite():
        cls = CustomJSONField
    else:
        cls = models.CharField
    return cls(**defaults)
