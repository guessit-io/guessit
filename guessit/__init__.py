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

__version__ = '0.1-dev'
__all__ = [ 'guess_file_info', 'guess_video_info',
            'guess_movie_info', 'guess_episode_info' ]


from guessit.guess import merge_all
from guessit.matcher import IterativeMatcher
import logging

log = logging.getLogger("guessit")

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

# let's be a nicely behaving library
h = NullHandler()
log.addHandler(h)




def guess_file_info(filename, filetype, info = [ 'filename' ]):
    """info can contain the names of the various plugins, such as 'filename' to
    detect filename info, or 'md5' to get the md5 hash of the file."""
    result = []
    if 'filename' in info:
        m = IterativeMatcher(filename, filetype = 'autodetect')
        result.append(m.matched())

    if 'md5' in info:
        pass

    """For plugins which depend on some optional library, import them like that:

    if 'plugin_name' in info:
        try:
            import optional_lib
        except ImportError:
            raise Exception, 'The plugin module cannot be loaded because the optional_lib lib is missing'

        # do some stuff
    """

    return result


def guess_video_info(filename, info = [ 'filename' ]):
    return merge_all(guess_file_info(filename, 'autodetect', info))

def guess_movie_info(filename, info = [ 'filename' ]):
    return merge_all(guess_file_info(filename, 'movie', info))

def guess_episode_info(filename, info = [ 'filename' ]):
    return merge_all(guess_file_info(filename, 'episode', info))


