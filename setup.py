
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

from setuptools import setup
import os
import guessit


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.rst')).read()

args = dict(name = 'guessit',
            version = guessit.__version__,
            description = 'GuessIt - a library for guessing information from video files.',
            long_description = README + '\n\n' + NEWS,
            # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
            classifiers = [ 'Development Status :: 5 - Production/Stable',
                            'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                            'Operating System :: OS Independent',
                            'Intended Audience :: Developers',
                            'Programming Language :: Python :: 2',
                            'Programming Language :: Python :: 2.6',
                            'Programming Language :: Python :: 2.7',
                            'Programming Language :: Python :: 3',
                            'Programming Language :: Python :: 3.2',
                            'Topic :: Multimedia',
                            'Topic :: Software Development :: Libraries :: Python Modules'
                            ],
            keywords = 'smewt media video metadata python library',
            author = 'Nicolas Wack',
            author_email = 'wackou@gmail.com',
            url = 'http://guessit.readthedocs.org/',
            license = 'LGPLv3',
            packages = [ 'guessit', 'guessit.transfo' ],
            include_package_data=True,
            install_requires = []
            )


setup(**args)
