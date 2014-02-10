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

from __future__ import absolute_import, division, print_function, unicode_literals

from guessit.plugins.transformers import Transformer, get_transformer, TransfoException
from guessit.guess import Guess
from guessit.patterns.extension import subtitle_exts, info_exts, video_exts
from guessit.textutils import clean_string
import os.path
import re
import mimetypes


class GuessFiletype(Transformer):
    def __init__(self):
        Transformer.__init__(self, 250)

    # List of well known movies and series, hardcoded because they cannot be
    # guessed appropriately otherwise
    MOVIES = ['OSS 117']
    SERIES = ['Band of Brothers']

    MOVIES = [m.lower() for m in MOVIES]
    SERIES = [s.lower() for s in SERIES]

    def guess_filetype(self, mtree):
        # put the filetype inside a dummy container to be able to have the
        # following functions work correctly as closures
        # this is a workaround for python 2 which doesn't have the
        # 'nonlocal' keyword (python 3 does have it)
        filetype_container = [mtree.guess.get('type', 'autodetect')]
        other = {}
        filename = mtree.string

        def upgrade_episode():
            if filetype_container[0] == 'video':
                filetype_container[0] = 'episode'
            elif filetype_container[0] == 'subtitle':
                filetype_container[0] = 'episodesubtitle'
            elif filetype_container[0] == 'info':
                filetype_container[0] = 'episodeinfo'

        def upgrade_movie():
            if filetype_container[0] == 'video':
                filetype_container[0] = 'movie'
            elif filetype_container[0] == 'subtitle':
                filetype_container[0] = 'moviesubtitle'
            elif filetype_container[0] == 'info':
                filetype_container[0] = 'movieinfo'

        def upgrade_subtitle():
            if filetype_container[0] == 'movie':
                filetype_container[0] = 'moviesubtitle'
            elif filetype_container[0] == 'episode':
                filetype_container[0] = 'episodesubtitle'
            else:
                filetype_container[0] = 'subtitle'

        def upgrade_info():
            if filetype_container[0] == 'movie':
                filetype_container[0] = 'movieinfo'
            elif filetype_container[0] == 'episode':
                filetype_container[0] = 'episodeinfo'
            else:
                filetype_container[0] = 'info'

        def upgrade(type='unknown'):
            if filetype_container[0] == 'autodetect':
                filetype_container[0] = type

        # look at the extension first
        fileext = os.path.splitext(filename)[1][1:].lower()
        if fileext in subtitle_exts:
            upgrade_subtitle()
            other = {'container': fileext}
        elif fileext in info_exts:
            upgrade_info()
            other = {'container': fileext}
        elif fileext in video_exts:
            upgrade(type='video')
            other = {'container': fileext}
        else:
            upgrade(type='unknown')
            if fileext:
                other = {'extension': fileext}

        # check whether we are in a 'Movies', 'Tv Shows', ... folder
        folder_rexps = [
                        (r'Movies?', upgrade_movie),
                        (r'Tv[ _-]?Shows?', upgrade_episode),
                        (r'Series', upgrade_episode)
                        ]
        for frexp, upgrade_func in folder_rexps:
            frexp = re.compile(frexp, re.IGNORECASE)
            for pathgroup in mtree.children:
                if frexp.match(pathgroup.value):
                    upgrade_func()

        # check for a few specific cases which will unintentionally make the
        # following heuristics confused (eg: OSS 117 will look like an episode,
        # season 1, epnum 17, when it is in fact a movie)
        fname = clean_string(filename).lower()
        for m in self.MOVIES:
            if m in fname:
                self.log.debug('Found in exception list of movies -> type = movie')
                upgrade_movie()
        for s in self.SERIES:
            if s in fname:
                self.log.debug('Found in exception list of series -> type = episode')
                upgrade_episode()

        # now look whether there are some specific hints for episode vs movie
        if filetype_container[0] in ('video', 'subtitle', 'info'):
            # if we have an episode_rexp (eg: s02e13), it is an episode
            episode_transformer = get_transformer('guess_episodes_rexps')
            if episode_transformer:
                guess = episode_transformer.guess_episodes_rexps(filename)
                if guess:
                    self.log.debug('Found guess_episodes_rexps: %s -> type = episode', guess)
                    upgrade_episode()

            weak_episode_transformer = get_transformer('guess_weak_episodes_rexps')
            if weak_episode_transformer:
                guess = weak_episode_transformer.guess_weak_episodes_rexps(filename)
                if guess:
                    self.log.debug('Found guess_weak_episodes_rexps: %s -> type = episode', guess)
                    upgrade_episode()

            properties_transformer = get_transformer('guess_properties')

            if properties_transformer:
                # if we have certain properties characteristic of episodes, it is an ep
                found = properties_transformer.container.find_properties(filename, mtree, 'episodeFormat')
                guess = properties_transformer.container.as_guess(found, filename)
                if guess:
                    self.log.debug('Found characteristic property of episodes: %s"', guess)
                    upgrade_episode()

                found = properties_transformer.container.find_properties(filename, mtree, 'format')
                guess = properties_transformer.container.as_guess(found, filename, lambda g: g['format'] == 'DVB')
                if guess:
                    self.log.debug('Found characteristic property of episodes: %s', guess)
                    upgrade_episode()

            # origin-specific type
            if 'tvu.org.ru' in filename:
                self.log.debug('Found characteristic property of episodes: %s', 'tvu.org.ru')
                upgrade_episode()

            # if no episode info found, assume it's a movie
            self.log.debug('Nothing characteristic found, assuming type = movie')
            upgrade_movie()

        filetype = filetype_container[0]
        return filetype, other

    def process(self, mtree, options={}):
        """guess the file type now (will be useful later)
        """
        filetype, other = self.guess_filetype(mtree)

        mtree.guess.set('type', filetype, confidence=1.0)
        self.log.debug('Found with confidence %.2f: %s' % (1.0, mtree.guess))

        filetype_info = Guess(other, confidence=1.0)
        # guess the mimetype of the filename
        # TODO: handle other mimetypes not found on the default type_maps
        # mimetypes.types_map['.srt']='text/subtitle'
        mime, _ = mimetypes.guess_type(mtree.string, strict=False)
        if mime is not None:
            filetype_info.update({'mimetype': mime}, confidence=1.0)

        node_ext = mtree.node_at((-1,))
        node_ext.guess = filetype_info
        self.log.debug('Found with confidence %.2f: %s' % (1.0, node_ext.guess))

        if mtree.guess.get('type') in [None, 'unknown']:
            raise TransfoException(__name__, 'Unknown file type')
