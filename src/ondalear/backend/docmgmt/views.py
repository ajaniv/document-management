"""
.. module:: ondalear.backend.views
   :synopsis: ondalear server views  module.

"""
from __future__ import absolute_import
import logging
from django.http import HttpResponse

_logger = logging.getLogger(__name__)

def index(request):             # pylint: disable=unused-argument
    """basic check"""
    _logger.info('index request was made')
    return HttpResponse("You're at the ondalear backend index.")
