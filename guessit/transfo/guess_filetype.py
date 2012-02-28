#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2012 Nicolas Wack <wackou@gmail.com>
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

from guessit import Guess
from guessit.patterns import subtitle_exts, video_exts, episode_rexps, find_properties, canonical_form
import os.path
import re
import mimetypes
import logging

log = logging.getLogger("guessit.transfo.guess_filetype")




def guess_filetype(filename, filetype):
    other = {}

    # look at the extension first
    fileext = os.path.splitext(filename)[1][1:].lower()
    if fileext in subtitle_exts:
        if 'movie' in filetype:
            filetype = 'moviesubtitle'
        elif 'episode' in filetype:
            filetype = 'episodesubtitle'
        else:
            filetype = 'subtitle'
        other = { 'container': fileext }
    elif fileext in video_exts:
        if filetype == 'autodetect':
            filetype = 'video'
        other = { 'container': fileext }
    else:
        if filetype == 'autodetect':
            filetype = 'unknown'
        other = { 'extension': fileext }

    # now look whether there are some specific hints for episode vs movie
    if filetype in ('video', 'subtitle'):
        for rexp, _, _ in episode_rexps:
            match = re.search(rexp, filename, re.IGNORECASE)
            if match:
                if   filetype == 'video':    filetype = 'episode'
                elif filetype == 'subtitle': filetype = 'episodesubtitle'
                break

        for prop, value, _, _ in find_properties(filename):
            log.debug('prop: %s = %s' % (prop, value))
            if prop == 'episodeFormat':
                if   filetype == 'video':    filetype = 'episode'
                elif filetype == 'subtitle': filetype = 'episodesubtitle'
                break

            elif canonical_form(value) == 'DVB':
                if   filetype == 'video':    filetype = 'episode'
                elif filetype == 'subtitle': filetype = 'episodesubtitle'
                break

        # if no episode info found, assume it's a movie
        if filetype == 'video':
            filetype = 'movie'
        elif filetype == 'subtitle':
            filetype = 'moviesubtitle'


    return filetype, other


def process(mtree, filetype = 'autodetect'):
    filetype, other = guess_filetype(mtree.string, filetype)

    mtree.guess.set('type', filetype, confidence = 1.0)
    log.debug('Found with confidence %.2f: %s' % (1.0, mtree.guess))

    filetype_info = Guess(other, confidence = 1.0)
    # guess the mimetype of the filename
    # TODO: handle other mimetypes not found on the default type_maps
    # mimetypes.types_map['.srt']='text/subtitle'
    mime, _ = mimetypes.guess_type(mtree.string, strict=False)
    if mime is not None:
        filetype_info.update({ 'mimetype': mime }, confidence = 1.0)

    node_ext = mtree.node_at((-1,))
    node_ext.guess = filetype_info
    log.debug('Found with confidence %.2f: %s' % (1.0, node_ext.guess))
