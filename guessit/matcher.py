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

from __future__ import unicode_literals

import logging

from guessit import PY3, u
from guessit.matchtree import MatchTree
from guessit.textutils import normalize_unicode, clean_string

from guessit.transfo import TransfoException


log = logging.getLogger(__name__)


class IterativeMatcher(object):
    """An iterative matcher tries to match different patterns that appear
    in the filename.

    The ``filetype`` argument indicates which type of file you want to match.
    If it is ``'autodetect'``, the matcher will try to see whether it can guess
    that the file corresponds to an episode, or otherwise will assume it is
    a movie.

    The recognized ``filetype`` values are:
    ``['autodetect', 'subtitle', 'info', 'movie', 'moviesubtitle', 'movieinfo', 'episode',
    'episodesubtitle', 'episodeinfo']``

    ``opts`` is a list of option names, that act as global flags for the matcher

    ``transfo_opts`` is a dict of args to be passed to the transformations used
    by the matcher. Its schema is: ``{ transfo_name: (transfo_args, transfo_kwargs) }``


    The IterativeMatcher works mainly in 2 steps:

    First, it splits the filename into a match_tree, which is a tree of groups
    which have a semantic meaning, such as episode number, movie title,
    etc...

    The match_tree created looks like the following::

      0000000000000000000000000000000000000000000000000000000000000000000000000000000000 111
      0000011111111111112222222222222233333333444444444444444455555555666777777778888888 000
      0000000000000000000000000000000001111112011112222333333401123334000011233340000000 000
      __________________(The.Prestige).______.[____.HP.______.{__-___}.St{__-___}.Chaps].___
      xxxxxttttttttttttt               ffffff  vvvv    xxxxxx  ll lll     xx xxx         ccc
      [XCT].Le.Prestige.(The.Prestige).DVDRip.[x264.HP.He-Aac.{Fr-Eng}.St{Fr-Eng}.Chaps].mkv

    The first 3 lines indicates the group index in which a char in the
    filename is located. So for instance, ``x264`` (in the middle) is the group (0, 4, 1), and
    it corresponds to a video codec, denoted by the letter ``v`` in the 4th line.
    (for more info, see guess.matchtree.to_string)

    Second, it tries to merge all this information into a single object
    containing all the found properties, and does some (basic) conflict
    resolution when they arise.
    """
    def __init__(self, filename, filetype='autodetect', opts=None, transfo_opts=None):
        if opts is None:
            opts = []
        if not isinstance(opts, list):
            raise ValueError('opts must be a list of option names! Received: type=%s val=%s',
                             type(opts), opts)

        if transfo_opts is None:
            transfo_opts = {}
        if not isinstance(transfo_opts, dict):
            raise ValueError('transfo_opts must be a dict of { transfo_name: (args, kwargs) }. ' +
                             'Received: type=%s val=%s', type(transfo_opts), transfo_opts)

        valid_filetypes = ('autodetect', 'subtitle', 'info', 'video',
                           'movie', 'moviesubtitle', 'movieinfo',
                           'episode', 'episodesubtitle', 'episodeinfo')
        if filetype not in valid_filetypes:
            raise ValueError("filetype needs to be one of %s" % valid_filetypes)
        if not PY3 and not isinstance(filename, unicode):
            log.warning('Given filename to matcher is not unicode...')
            filename = filename.decode('utf-8')

        filename = normalize_unicode(filename)

        self.filename = filename
        self.match_tree = MatchTree(filename)
        self.filetype = filetype
        self.opts = opts
        self.transfo_opts = transfo_opts
        self._transfo_calls = []

        # sanity check: make sure we don't process a (mostly) empty string
        if clean_string(filename) == '':
            return

        try:
            mtree = self.match_tree
            mtree.guess.set('type', filetype, confidence=1.0)

            # 1- first split our path into dirs + basename + ext
            self._apply_transfo('split_path_components')

            # 2- guess the file type now (will be useful later)
            self._apply_transfo('guess_filetype', filetype)

            # 3- split each of those into explicit groups (separated by parentheses
            #    or square brackets)
            self._apply_transfo('split_explicit_groups')

            # 4- try to match information for specific patterns
            # NOTE: order needs to comply to the following:
            #       - website before language (eg: tvu.org.ru vs russian)
            #       - language before episodes_rexps
            #       - properties before language (eg: he-aac vs hebrew)
            #       - release_group before properties (eg: XviD-?? vs xvid)
            if mtree.guess['type'] in ('episode', 'episodesubtitle', 'episodeinfo'):
                strategy = ['guess_date', 'guess_website', 'guess_release_group',
                            'guess_properties', 'guess_language',
                            'guess_video_rexps',
                            'guess_episodes_rexps', 'guess_weak_episodes_rexps']
            else:
                strategy = ['guess_date', 'guess_website', 'guess_release_group',
                            'guess_properties', 'guess_language',
                            'guess_video_rexps']

            if 'nolanguage' in opts:
                strategy.remove('guess_language')

            for name in strategy:
                self._apply_transfo(name)

            # more guessers for both movies and episodes
            self._apply_transfo('guess_bonus_features')
            self._apply_transfo('guess_year')

            if 'nocountry' not in opts:
                self._apply_transfo('guess_country')

            self._apply_transfo('guess_idnumber')

            # split into '-' separated subgroups (with required separator chars
            # around the dash)
            self._apply_transfo('split_on_dash')

            # 5- try to identify the remaining unknown groups by looking at their
            #    position relative to other known elements
            if mtree.guess['type'] in ('episode', 'episodesubtitle', 'episodeinfo'):
                self._apply_transfo('guess_episode_info_from_position')
            else:
                self._apply_transfo('guess_movie_title_from_position')

            # 6- perform some post-processing steps
            self._apply_transfo('post_process')

            log.debug('Found match tree:\n%s' % u(mtree))
        except TransfoException as e:
            log.debug('An error has occured in Transformer %s: %s' % (e.transformer, e.message))

    def _apply_transfo(self, transfo_name, *args, **kwargs):
        transfo = __import__('guessit.transfo.' + transfo_name,
                             globals=globals(), locals=locals(),
                             fromlist=['process', 'second_pass_options'], level=0)
        default_args, default_kwargs = self.transfo_opts.get(transfo_name, ((), {}))
        all_args = args or default_args or ()
        all_kwargs = dict(default_kwargs) if default_kwargs else {}
        all_kwargs.update(kwargs)  # keep all kwargs merged together
        transfo.process(self.match_tree, *all_args, **all_kwargs)
        self._transfo_calls.append((transfo_name, transfo, all_args, all_kwargs))

    @property
    def second_pass_options(self):
        opts = list(self.opts)
        transfo_opts = dict(self.transfo_opts.items())
        for transfo_name, transfo, _, _ in self._transfo_calls:
            if hasattr(transfo, 'second_pass_options'):
                c_opts, c_transfo_opts = transfo.second_pass_options(self.match_tree)
                if c_opts or c_transfo_opts:
                    transfo_opts[transfo_name] = c_opts, c_transfo_opts

        return opts, transfo_opts

    def matched(self):
        return self.match_tree.matched()
