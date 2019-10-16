"""
.. module:: ondalear.backend.analytics.models.analysis_results
   :synopsis: ondalear backend analysis results  module.



"""
import logging
from inflection import humanize, pluralize, underscore
from django.db.models import CASCADE
from django.utils.translation import ugettext_lazy as _

from ondalear.backend.core.django import fields
from ondalear.backend.core.django.models import db_table

from ondalear.backend.docmgmt.models import constants
from ondalear.backend.docmgmt.models.client import Client
from ondalear.backend.docmgmt.models import DocumentAssociation
from ondalear.backend.analytics.models.base import app_label, AbstractAnalyticsModel


_logger = logging.getLogger(__name__)

class AbstractResultsModel(AbstractAnalyticsModel):
    """Base results model class
    """
    input = fields.json_field(blank=False, null=False)
    output = fields.json_field(blank=False, null=False)
    name = fields.char_field(blank=True, null=True, max_length=constants.NAME_FIELD_MAX_LENGTH)

    # deletion of client will result in deletion of its associated documents
    client = fields.foreign_key_field(Client, on_delete=CASCADE)

    description = fields.description_field(blank=True, null=True,
                                           max_length=constants.DESCRIPTION_FIELD_MAX_LENGTH)


    class Meta(AbstractAnalyticsModel.Meta):
        """Meta class definition"""
        abstract = True

    def __str__(self):
        """pretty format instance as string"""
        return self.name if self.name else super().__str__()


_analysis_results = 'AnalysisResults'
_analysis_results_verbose = humanize(underscore(_analysis_results))

class AnalysisResults(AbstractResultsModel):
    """ Analysis results model class
    """
    documents = fields.foreign_key_field(DocumentAssociation,
                                         on_delete=CASCADE, blank=True, null=True)


    class Meta(AbstractResultsModel.Meta):
        """Meta class definition"""
        db_table = db_table(app_label, _analysis_results)
        verbose_name = _(_analysis_results_verbose)
        verbose_name_plural = _(pluralize(_analysis_results_verbose))


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """save the instance
        """
        self.full_clean()

        # auto assign a name
        if self.documents and not self.name:
            # pylint: disable=no-member
            self.name = '{}:{}'.format(self.documents.from_document.name,
                                       self.documents.to_document.name)
        return super(AnalysisResults, self).save(force_insert, force_update,
                                                 using, update_fields)
