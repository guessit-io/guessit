#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
#
# GuessIt is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessIt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages

import os
import sys
import io
import re


here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

with io.open(os.path.join(here, 'HISTORY.rst'), encoding='utf-8') as f:
    history = f.read()


install_requires = ['babelfish>=0.5.5', 'stevedore>=0.14', 'requests', 'python-dateutil>=2.1']
if sys.version_info < (2, 7):
    # argparse is part of the standard library in python 2.7+
    install_requires.append('argparse')

setup_requires = ['pytest-runner']

dev_require = ['zest.releaser[recommended]', 'pylint', 'tox', 'sphinx', 'sphinx-autobuild', 'Pygments']

tests_require = ['pytest>=2.7.3', 'pytest-benchmark', 'pytest-capturelog', 'PyYAML']

language_detection_require = ['guess-language>=0.2']

video_metadata_require = ['enzyme']

entry_points = {
    'console_scripts': [
        'guessit = guessit.__main__:main'
    ],
}

dependency_links = []


with io.open('guessit/__version__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]$', f.read(), re.MULTILINE).group(1)

args = dict(name='guessit',
            version=version,
            description='GuessIt - a library for guessing information from video filenames.',
            long_description=readme + '\n\n' + history,
            # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
            classifiers=['Development Status :: 5 - Production/Stable',
                         'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                         'Operating System :: OS Independent',
                         'Intended Audience :: Developers',
                         'Programming Language :: Python :: 2',
                         'Programming Language :: Python :: 2.7',
                         'Programming Language :: Python :: 3',
                         'Programming Language :: Python :: 3.3',
                         'Programming Language :: Python :: 3.4',
                         'Programming Language :: Python :: 3.5',
                         'Topic :: Multimedia',
                         'Topic :: Software Development :: Libraries :: Python Modules'
                         ],
            keywords='smewt media video metadata python library',
            author='Nicolas Wack',
            author_email='wackou@gmail.com',
            url='http://guessit.readthedocs.org/',
            download_url='https://pypi.python.org/packages/source/g/guessit/guessit-%s.tar.gz' % version,
            license='LGPLv3',
            packages=find_packages(),
            include_package_data=True,
            install_requires=install_requires,
            setup_requires=setup_requires,
            tests_require=tests_require,
            entry_points=entry_points,
            dependency_links=dependency_links,
            zip_safe=True,
            test_suite='guessit.test',
            extras_require={
                'test': tests_require,
                'dev': dev_require,
                'language_detection': language_detection_require,
                'video_metadata': video_metadata_require
            })

setup(**args)
