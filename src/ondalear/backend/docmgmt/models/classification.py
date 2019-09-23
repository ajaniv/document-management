"""
.. module:: ondalear.backend.docmgmt.models.tag
   :synopsis: ondalear backend  models tag  module.

The *tag* module contains *Tag* model abstractions.

"""
import logging
from inflection import humanize, pluralize, underscore

from django.db.models import CASCADE, SET_NULL
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from ondalear.backend.core.django import fields
from ondalear.backend.core.django.models import db_table

from ondalear.backend.docmgmt.models import constants
from ondalear.backend.docmgmt.models.base import AbstractDocumentManagementModel, app_label
from ondalear.backend.docmgmt.models.client import Client

_logger = logging.getLogger(__name__)


class AbstractClassification(AbstractDocumentManagementModel):
    """Abstract classification class definition
    Allows to associate a classification with an  instance.
    """
    name = fields.char_field(blank=False, null=False, max_length=constants.NAME_FIELD_MAX_LENGTH)
    # deletion of client will result in deletion of associated classifications
    client = fields.foreign_key_field(Client, on_delete=CASCADE)
    # deletion of parent will result in parent being set to null
    parent = fields.foreign_key_field('self', blank=True, null=True,
                                      related_name='children', on_delete=SET_NULL)
    description = fields.description_field(
        blank=True, null=True, max_length=constants.DESCRIPTION_FIELD_MAX_LENGTH)
    # the classification population (i.e. AuxiliaryDocument, Reference Document)
    target = fields.char_field(blank=False, null=False,
                               default=constants.CLASSIFICATION_TARGET_REFERENCE_DOCUMENT,
                               choices=constants.CLASSIFICATION_TARGET_CHOICES)
    # the industry or other top level classification such as finance, insurance, shipping, general
    domain = fields.char_field(blank=False, null=False,
                               default=constants.CLASSIFICATION_DOMAIN_GENERAL,
                               choices=constants.CLASSIFICATION_DOMAIN_CHOICES)

    class Meta(AbstractDocumentManagementModel.Meta):
        """Meta class definition"""
        abstract = True
        unique_together = ('client', 'name')

    def clean(self):
        """Model wide validation"""
        # pylint: disable=no-member
        if self.parent:
            if not self.parent.id:
                raise ValidationError(_('Invalid parent - has not been saved.'))
            # verify that parent exists - if not exception will be thrown
            self.__class__.objects.get(pk=self.parent.id)

        # check the entire hierarchy for name and id duplicates
        depth = 0
        max_depth = 10
        current = self
        name_cache = dict()
        id_cache = dict()
        while current and depth < max_depth:
            current_name = current.name
            current_id = current.id
            if current_name in name_cache:
                raise ValidationError(_(f'Duplicate name {current_name} in hierarchy.'))
            if current_id in id_cache:
                raise ValidationError(_(f'Duplicate id {current_id} in hierarchy.'))

            name_cache[current_name] = current
            id_cache[current_id] = current
            if current.parent:
                current = self.__class__.objects.get(pk=current.parent.id)
                depth += 1
            else:
                current = current.parent

        if depth >= max_depth:
            raise ValidationError(_(f'Max depth of {max_depth} exceeded.'))

        super(AbstractClassification, self).clean()

    def __str__(self):
        """generate pretty string representation"""
        full_path = [self.name]
        current = self.parent

        while current is not None:
            full_path.append(current.name)
            current = current.parent        # pylint: disable=no-member

        return ' -> '.join(full_path[::-1])

_tag = 'Tag'
_tag_verbose = humanize(underscore(_tag))

class Tag(AbstractClassification):
    """Tag class definition.

    Allows association of a document with 0->N searchable tags.
    """
    class Meta(AbstractClassification.Meta):
        """Meta class definition"""
        db_table = db_table(app_label, _tag)
        verbose_name = _(_tag_verbose)
        verbose_name_plural = _(pluralize(_tag_verbose))


_category = 'Category'
_category_verbose = humanize(underscore(_category))

class Category(AbstractClassification):
    """Category class definition.

    Allows classification of a document, and their hierarchical grouping.
    """
    class Meta(AbstractClassification.Meta):
        """Meta class definition"""
        db_table = db_table(app_label, _category)
        verbose_name = _(_category_verbose)
        verbose_name_plural = _(pluralize(_category_verbose))
