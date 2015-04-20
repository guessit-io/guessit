#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import re
import subprocess

DOIT_CONFIG = {'default_tasks': ['show_cmds']}


def task_show_cmds():
    """Show the list of available doit commands"""
    def noargs():
        print('doit has been run without arguments. Please specify which command to run.\n')
    return {'actions': [noargs, 'doit list'],
            'verbosity': 2}


def task_clean_pyc():
    """Clean all the .pyc files."""
    return {'actions': ['find . -iname "*.pyc" -delete']}


# TODO: add tasks for unittests and doctests


def task_pylint():
    """Run pylint on GuessIt's source code. Only show problems, no report"""
    return {'actions': ['pylint --reports=n --include-ids=y --disable=C,I,W0703 guessit']}


def task_pylint_report():
    """Run pylint on GuessIt's source code, full report"""
    return {'actions': ['pylint --include-ids=y --disable=C0103,C0111 guessit']}


def open_file(filename):
    """Open the given file using the OS's native programs"""
    if sys.platform.startswith('linux'):
        return 'xdg-open "%s"' % filename
    elif sys.platform == 'darwin':
        return 'open "%s"' % filename
    else:
        raise OSError('Platform not supported: %s' % sys.platform)

def task_doc():
    """Build the Sphinx documentation and open it in a web browser"""
    return {'actions': ['cd docs; make html',
                        open_file('docs/_build/html/index.html')]}


def task_pypi_doc():
    """Build the main page that will be uploaded to PyPI and open it in a
    web browser"""
    return {'actions': ['python setup.py --long-description | rst2html.py > /tmp/guessit_pypi_doc.html',
                        open_file('/tmp/guessit_pypi_doc.html')]}


# Release management functions

def set_version(pos):
    """Set the version in the guessit/__version__.py file"""
    if len(pos) != 1:
        print('You need to specify a single version number...', file=sys.stderr)
        sys.exit(1)

    version = pos[0]
    print('setting version %s' % version)

    version_filename = 'guessit/__version__.py'
    vfile = open(version_filename).read()
    vfile = re.sub(r"__version__ = '\S*'",
                   r"__version__ = '%s'" % version,
                   vfile)
    open(version_filename, 'w').write(vfile)


def task_set_version():
    """Set the version in the guessit/__version__.py file"""
    return {'actions': [set_version],
            'pos_arg': 'pos',
            'verbosity': 2}


def task_upload_pypi():
    """Build and upload the package on PyPI"""
    return {'actions': ['python setup.py register sdist upload'],
            'verbosity': 2}



def task_test_pypi_sdist():
    """Build the PyPI package and test whether it is installable and passes
    the tests"""
    cwd = os.getcwd()
    d = '_tmp_pypi_guessit'
    install_actions = ['rm -fr dist %s' % d,
                       'python setup.py sdist',
                       'virtualenv %s' % d]

    test_actions = ['cd {}'.format(d),
                    'bin/pip install --upgrade ../dist/*',
                    'bin/pip install PyYaml',
                    'bin/python -m guessit.test', # FIXME: use pytest
                    'cd {}'.format(cwd)
                    ]

    clean_actions = ['rm -fr %s' % d]

    result = {'actions': install_actions + test_actions + clean_actions,
              'verbosity': 2}

    str_actions = ' && '.join(result['actions'])

    def doit_pypi_sdist():
        print('For some reason, this doesn\'t work when run from doit. Please run this manually:\n'),
        print(str_actions),
        sys.exit(0)

    result['actions'] = [doit_pypi_sdist]

    return result
