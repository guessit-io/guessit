#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2011 Nicolas Wack <wackou@gmail.com>
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
import os, sys

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


args = dict(name = 'guessit',
            version = '0.1b2',
            description = 'Guessit - a library for guessing video information from their filename.',
            long_description = README + '\n\n' + NEWS,
            # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
            classifiers = [ 'Development Status :: 4 - Beta',
                            'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                            'Operating System :: OS Independent',
                            'Programming Language :: Python :: 2',
                            'Topic :: Multimedia',
                            'Topic :: Software Development :: Libraries'
                            ],
            keywords = 'smewt media video metadata python library',
            author = 'Nicolas Wack',
            author_email = 'wackou@gmail.com',
            url = 'http://www.smewt.com/',
            license = 'LGPLv3',
            packages = find_packages(exclude = [ 'ez_setup', 'examples', 'tests', 'utils' ]),
            #package_data = dict((package, datafiles_exts) for package in find_packages()),
            include_package_data = True,
            install_requires = []
            )


setup(**args)
