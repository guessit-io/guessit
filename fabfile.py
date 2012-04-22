#!/usr/bin/env python

import sys
import re
from fabric.api import *

def doctests():
    """Run the doctests found in GuessIt classes."""
    local('nosetests --with-doctest -vv guessit')

def test_movie():
    """Run the unittests for movies."""
    local('PYTHONPATH=. python test/test_movie.py')

def test_episode():
    """Run the unittests for episodes."""
    local('PYTHONPATH=. python test/test_episode.py')

def test_autodetect():
    """Run the unittests for autodetected files."""
    local('PYTHONPATH=. python test/test_autodetect.py')

def test_language():
    """Run the unittests for languages."""
    local('PYTHONPATH=. python test/test_language.py')

def unittests():
    """Run all the unittests."""
    test_movie()
    test_episode()
    test_autodetect()
    test_language()

def tests():
    """Run both the doctests and the unittests."""
    doctests()
    unittests()


def clean_pyc():
    """Removes all the *.pyc files found in the repository."""
    local('find . -iname "*.pyc" -delete')


def pylint():
    """Runs pylint on GuessIt's source code. Only show problems, no report."""
    local('pylint --reports=n --include-ids=y --disable=C,I,W0703 guessit')

def pylint_report():
    """Runs pylint on GuessIt's source code, full report."""
    local('pylint --include-ids=y --disable=C0103,C0111 guessit')

def open_file(filename):
    """Open the given file using the OS's native programs."""
    if sys.platform.startswith('linux'):
        local('xdg-open "%s"' % filename)
    elif sys.platform == 'darwin':
        local('open "%s"' % filename)
    else:
        print 'Platform not supported:', sys.platform

def doc():
    """Build the Sphinx documentation and open it in a web browser."""
    with lcd('docs'):
        local('make html')
        open_file('_build/html/index.html')

def pypi_doc():
    """Builds the main page that will be uploaded to PyPI and open it in a
    web browser."""
    local('python setup.py --long-description | rst2html.py > /tmp/guessit_pypi_doc.html')
    open_file('/tmp/guessit_pypi_doc.html')


# Release management functions

def set_version(version):
    """Set the version in the guessit/__init__.py file."""
    initfile = open('guessit/__init__.py').read()
    initfile = re.sub(r"__version__ = '\S*'",
                      r"__version__ = '%s'" % version,
                      initfile)
    open('guessit/__init__.py', 'w').write(initfile)

def upload_pypi():
    local('python setup.py register sdist upload')

def test_pypi_sdist():
    d = '_tmp_pypi_guessit'
    local('rm -fr dist %s' % d)
    local('python setup.py sdist')
    local('virtualenv %s' % d)
    with lcd(d):
        with prefix('source bin/activate'):
            local('pip install ../dist/*')
            local('pip install PyYaml') # to be able to run the tests
            local('cp ../test/*.py ../test/*.yaml .')
            local('python test_autodetect.py')
            local('python test_movie.py')
            local('python test_episode.py')
            local('python test_languages.py')
    local('rm -fr %s' % d)
