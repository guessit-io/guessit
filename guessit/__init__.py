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
__all__ = [ 'Guess', 'guess_file_info', 'guess_video_info',
            'guess_movie_info', 'guess_episode_info' ]


from guessit.guess import Guess, merge_all
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
    for infotype in info:
        if infotype == 'filename':
            m = IterativeMatcher(filename, filetype = 'autodetect')
            result.append(m.matched())

        if infotype == 'hash_mpc':
            import hash_mpc
            try:
                result.append(Guess({ 'hash_mpc': hash_mpc.hash_file(filename) },
                                    confidence = 1.0))
            except Exception, e:
                log.warning('Could not compute MPC-style hash because: %s' % e)

        if infotype == 'md5':
            log.error('MD5 not implemented yet')
            pass

        """For plugins which depend on some optional library, import them like that:

        if 'plugin_name' in info:
            try:
                import optional_lib
            except ImportError:
                raise Exception, 'The plugin module cannot be loaded because the optional_lib lib is missing'

        # do some stuff
        """

    return merge_all(result)


def guess_video_info(filename, info = [ 'filename' ]):
    return guess_file_info(filename, 'autodetect', info)

def guess_movie_info(filename, info = [ 'filename' ]):
    return guess_file_info(filename, 'movie', info)

def guess_episode_info(filename, info = [ 'filename' ]):
    return guess_file_info(filename, 'episode', info)


