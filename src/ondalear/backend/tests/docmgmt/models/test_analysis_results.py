"""
.. module:: ondalear.backend.tests.docmgmt.models.test_analysis_results
   :synopsis: Analysis results model unit test module.


"""
import logging

from ondalear.backend.docmgmt.models import AnalysisResults
from . import factories
from .test_document import DocumentCRUDMixin
from .base import AbstractModelTestCase

_logger = logging.getLogger(__name__)

# pylint: disable=no-member,no-self-use,missing-docstring


class AnalysisResultsCRUDTests(DocumentCRUDMixin, AbstractModelTestCase):
    """Client model basic lifecycle test case"""

    document_factory = factories.DocumentModelFactory
    doc_to_doc_association_factory = factories.DocumentAssociationModelFactory

    def test_crud(self):
        # expect to create, update, fetch, and delete analysis results

        # create instance
        (fetched,
         to_document,
         from_document,
         document_association) = self.assert_doc_to_doc_association()
        model_input = dict(passage='some passage', question='some question')
        model_parms = dict(param1='param 1', param2='param 2')
        model_output = dict(result=[1.95, 2.95, 3.95])
        request_input = dict(model_input=model_input, model_parms=model_parms)
        instance = factories.AnalysisResultsModelFactory(name='my results',
                                                         description='my results description',
                                                         input=request_input,
                                                         output=model_output,
                                                         documents=document_association)
        # verify it was saved
        assert instance.id

        # fetch the instance
        fetched = AnalysisResults.objects.get(pk=instance.id)
        assert fetched

        # update the instance
        new_name = 'New Name'
        instance.name = new_name
        instance.save()
        # verify update
        assert AnalysisResults.objects.get(pk=instance.id).name == new_name

        # delete the from document instance
        deleted = from_document.delete()

        # verify deletion
        assert deleted[0] == 3  # document association, document results, document
        try:
            AnalysisResults.objects.get(pk=instance.id)
        except AnalysisResults.DoesNotExist:
            pass

        # delete the to document instance
        deleted = to_document.delete()
        assert deleted[0] == 1
