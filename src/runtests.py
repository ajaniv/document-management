"""
.. module::  runtests
   :synopsis:  Enable python setup.py test to work
"""
import os
from os import path
import sys

import django
from django.test.utils import get_runner
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ondalear.backend.site.settings_test')
root_dir = path.dirname(os.path.abspath(__file__))
app_dir = path.join(root_dir, 'ondalear/backend')

sys.path.insert(0, app_dir)     # required for django app config
sys.path.insert(0, root_dir)    # ensure that ondalear can be imported

def runtests():
    """run the tests"""

    if hasattr(django, 'setup'):
        django.setup()

    TestRunner = get_runner(settings)

    test_runner = TestRunner(verbosity=1, interactive=True)

    failures = test_runner.run_tests([app_dir])
    sys.exit(bool(failures))

if __name__ == '__main__':
    runtests()
