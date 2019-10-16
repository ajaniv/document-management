"""
.. module:: ondalear.backend.services.cache
   :synopsis: text analytics cache module

"""
import logging
from cachetools import TTLCache


_logger = logging.getLogger(__name__)

class AnalysisResultsCache:
    """Analysis cache"""
    TIME_TO_LIVE = 600  # 10 minutes
    MAX_SIZE = 1024

    def __init__(self):
        self.cache = TTLCache(maxsize=self.MAX_SIZE, ttl=self.TIME_TO_LIVE)

    def find(self, key):
        """find an entry"""
        try:
            return self.cache[key]
        except KeyError:
            pass
        return None

    def add(self, key, value):
        """add entry to cache"""
        self.cache[key] = value
