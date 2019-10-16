"""
.. module:: ondalear.backend.docmgmt.views
   :synopsis: ondalear docmgmt views  module.

"""
import logging
from django.http import HttpResponse

_logger = logging.getLogger(__name__)

def index(request):             # pylint: disable=unused-argument
    """basic check"""
    _logger.info('docmgmt index request was made')
    return HttpResponse("You're at the ondalear docmgmt index.")
