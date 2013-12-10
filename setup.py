
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


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
HISTORY = open(os.path.join(here, 'HISTORY.rst')).read()


install_requires = ['babelfish', 'stevedore']

tests_require = ['PyYAML', 'nose']  # Fabric not available (yet!) for python3

setup_requires=['nose']

entry_points = {
    'console_scripts': [
        'guessit = guessit.__main__:main'
    ],
    'guessit.transformer': [
        'split_path_components = guessit.transfo.split_path_components:SplitPathComponents',
        'guess_filetype = guessit.transfo.guess_filetype:GuessFiletype',
        'split_explicit_groups = guessit.transfo.split_explicit_groups:SplitExplicitGroups',
        'guess_date = guessit.transfo.guess_date:GuessDate',
        'guess_website = guessit.transfo.guess_website:GuessWebsite',
        'guess_release_group = guessit.transfo.guess_release_group:GuessReleaseGroup',
        'guess_properties = guessit.transfo.guess_properties:GuessProperties',
        'guess_language = guessit.transfo.guess_language:GuessLanguage',
        'guess_video_rexps = guessit.transfo.guess_video_rexps:GuessVideoRexps',
        'guess_episodes_rexps = guessit.transfo.guess_episodes_rexps:GuessEpisodesRexps',
        'guess_weak_episodes_rexps = guessit.transfo.guess_weak_episodes_rexps:GuessWeakEpisodesRexps',
        'guess_bonus_features = guessit.transfo.guess_bonus_features:GuessBonusFeatures',
        'guess_year = guessit.transfo.guess_year:GuessYear',
        'guess_country = guessit.transfo.guess_country:GuessCountry',
        'guess_idnumber = guessit.transfo.guess_idnumber:GuessIdnumber',
        'split_on_dash = guessit.transfo.split_on_dash:SplitOnDash',
        'guess_episode_info_from_position = guessit.transfo.guess_episode_info_from_position:GuessEpisodeInfoFromPosition',
        'guess_movie_title_from_position = guessit.transfo.guess_movie_title_from_position:GuessMovieTitleFromPosition',
        'post_process = guessit.transfo.post_process:PostProcess',
    ],
}

version = '0.7.dev0'

args = dict(name='guessit',
            version=version,
            description='GuessIt - a library for guessing information from video files.',
            long_description=README + '\n\n' + HISTORY,
            # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
            classifiers=['Development Status :: 5 - Production/Stable',
                         'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                         'Operating System :: OS Independent',
                         'Intended Audience :: Developers',
                         'Programming Language :: Python :: 2',
                         'Programming Language :: Python :: 2.6',
                         'Programming Language :: Python :: 2.7',
                         'Programming Language :: Python :: 3',
                         'Programming Language :: Python :: 3.2',
                         'Programming Language :: Python :: 3.3'
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
            extras_require={'language_detection': ['guess-language>=0.2']},
            test_suite='guessit.test',
            )

setup(**args)
