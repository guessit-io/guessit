#!/usr/bin/env python

import sys
import re
from fabric.api import *
from fabric.tasks import Task

@task
def doctests():
    """Run the doctests found in GuessIt classes"""
    local('nosetests --with-doctest -vv guessit')


class TestTask(Task):
    name = 'testtask'
    def __init__(self, testname, docstring):
        super(Task, self).__init__()
        self.name = 'test_' + testname
        self.__doc__ = 'Run the unittests for %s' % docstring

    def run(self):
        local('PYTHONPATH=. python tests/%s.py' % self.name)

test_ep = TestTask('episode', 'episodes')
test_movie = TestTask('movie', 'movies')
test_auto = TestTask('autodetect', 'autodetected files')
test_lang = TestTask('language', 'languages')
test_utils = TestTask('utils', 'utility functions')
test_matchtree = TestTask('matchtree', 'MatchTree')

@task
def unittests():
    """Run all the unittests"""
    EXCLUDE = ['test_pypi_sdist']
    def is_unittest(t):
        return t[0].startswith('test_') and t[0] not in EXCLUDE

    alltests = filter(is_unittest, globals().items())
    for name, testcase in alltests:
        testcase.run()


@task
def tests():
    """Run both the doctests and the unittests"""
    unittests()
    doctests()


@task
def clean_pyc():
    """Removes all the *.pyc files found in the repository"""
    local('find . -iname "*.pyc" -delete')


@task
def pylint():
    """Runs pylint on GuessIt's source code. Only show problems, no report"""
    local('pylint --reports=n --include-ids=y --disable=C,I,W0703 guessit')


@task
def pylint_report():
    """Runs pylint on GuessIt's source code, full report"""
    local('pylint --include-ids=y --disable=C0103,C0111 guessit')

def open_file(filename):
    """Open the given file using the OS's native programs"""
    if sys.platform.startswith('linux'):
        local('xdg-open "%s"' % filename)
    elif sys.platform == 'darwin':
        local('open "%s"' % filename)
    else:
        print 'Platform not supported:', sys.platform

@task
def doc():
    """Build the Sphinx documentation and open it in a web browser"""
    with lcd('docs'):
        local('make html')
        open_file('_build/html/index.html')

@task
def pypi_doc():
    """Builds the main page that will be uploaded to PyPI and open it in a
    web browser"""
    local('python setup.py --long-description | rst2html.py > /tmp/guessit_pypi_doc.html')
    open_file('/tmp/guessit_pypi_doc.html')


# Release management functions

@task
def set_version(version):
    """Set the version in the guessit/__init__.py file"""
    initfile = open('guessit/__init__.py').read()
    initfile = re.sub(r"__version__ = '\S*'",
                      r"__version__ = '%s'" % version,
                      initfile)
    open('guessit/__init__.py', 'w').write(initfile)

@task
def upload_pypi():
    """Build and upload the package on PyPI"""
    local('python setup.py register sdist upload')

@task
def test_pypi_sdist():
    """Build the PyPI package and test whether it is installable and passes
    the tests"""
    d = '_tmp_pypi_guessit'
    local('rm -fr dist %s' % d)
    local('python setup.py sdist')
    local('virtualenv %s' % d)
    with lcd(d):
        with prefix('source bin/activate'):
            local('pip install ../dist/*')
            local('pip install PyYaml') # to be able to run the tests
            local('cp ../tests/*.py ../tests/*.yaml ../tests/*.txt .')
            local('python test_autodetect.py')
            local('python test_movie.py')
            local('python test_episode.py')
            local('python test_language.py')
    local('rm -fr %s' % d)
