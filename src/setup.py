"""
.. module::  setup
   :synopsis: A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
"""
import sys
import re
import os
from os import path

from setuptools import find_packages, setup

this_dir = os.path.dirname(os.path.abspath(__file__))

def check_python():
    """check python version"""
    CURRENT_PYTHON = sys.version_info[:2]
    REQUIRED_PYTHON = (3, 5)

    # This check and everything above must remain compatible with Python 2.7.
    if CURRENT_PYTHON < REQUIRED_PYTHON:
        sys.stderr.write("""
    ==========================
    Unsupported Python version
    ==========================

    This version of this package requires Python {}.{}, but you're trying
    to install it on Python {}.{}.

    """.format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
        sys.exit(1)


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


check_python()
version = get_version('ondalear/backend')

try:
    with open(path.join(this_dir, '../README.md')) as readme:
        README = readme.read()
except IOError:
    README = ''


# allow setup.py to be run from any path
os.chdir(path.normpath(path.join(path.abspath(__file__), os.pardir)))

_git_url_root = 'git+ssh://git@github.com/ajaniv/'
setup(
    name='docmgmt-backend',
    version=version,
    include_package_data=True,
    license='BSD', 
    description='Django text document management application',
    long_description=README,
    url='http://www.ondalear.com/',
    author='Amnon Janiv',
    author_email='amnon.janiv@ondalear.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'Django>=2.2.3',
        'djangorestframework>=3.9.4'
    ],
    dependency_links=[
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    test_suite='runtests.runtests',
)