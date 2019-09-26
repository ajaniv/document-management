"""
.. module:: ondalear.backend.analytics.views
   :synopsis: ondalear analytics views module.

"""
import logging
from django.http import HttpResponse

_logger = logging.getLogger(__name__)

def index(request):             # pylint: disable=unused-argument
    """basic check"""
    _logger.info('analytics index request was made')
    return HttpResponse("You're at the ondalear analytics index.")
