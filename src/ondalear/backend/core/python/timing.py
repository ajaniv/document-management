"""
.. module::  ondalear.backend.core.python.timing
   :synopsis: python timing module.

The *python_utils* module contains core Python helper functions and classes.

"""
from __future__ import absolute_import
import functools
import logging
import time

_logger = logging.getLogger(__name__)


def timeit(method):
    """
    Time function execution.
    """
    @functools.wraps(method)
    def timed(*args, **kw):
        """timer wrapper function."""
        time_start = time.time()
        result = method(*args, **kw)
        time_end = time.time()

        print('%r (%r, %r) %2.2f sec' %
              (method.__name__, args, kw, time_end - time_start))
        return result

    return timed

class Timer:
    """
    Class which measures code block execution time.

    """
    # pylint: disable=too-many-instance-attributes
    # These are reasonable in this case.
    msg = '%s elapsed time: %f ms'
    verbose = False

    def __init__(self, user_msg, use_clock=False,
                 verbose=None, logger=None):
        self.verbose = verbose if verbose is not None else Timer.verbose
        self.logger = logger or _logger
        self.extra_msg = user_msg
        self.timer_fn = time.clock if use_clock else time.time
        self.start = None

    def __enter__(self):
        self.start = self.now()
        return self

    def __exit__(
            self,
            exception_type, exception_value, trace_back):  # @UnusedVariable
        self.end = self.now()               # pylint: disable=attribute-defined-outside-init
        self.secs = self.end - self.start   # pylint: disable=attribute-defined-outside-init
        self.msecs = self.secs * 1000       # pylint: disable=attribute-defined-outside-init

        if self.verbose:
            self.logger.debug(self.msg, self.extra_msg, self.msecs)

    def now(self):
        """return current time."""
        return self.timer_fn()

    @staticmethod
    def set_verbose(value):
        """Set default verbose option.

        Args:
            value(bool): New value of verbose attribute.
        """
        Timer.verbose = value
