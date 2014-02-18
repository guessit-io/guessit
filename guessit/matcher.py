#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
# Copyright (c) 2013 Rémi Alvergnat <toilal.dev@gmail.com>
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

from __future__ import absolute_import, division, print_function, \
    unicode_literals

import logging

from guessit import PY3, u
from guessit.transfo import TransformerException
from guessit.matchtree import MatchTree
from guessit.textutils import normalize_unicode, clean_string

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

    ``transformers_options`` is a dict of args to be passed to the transformations used
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
    def __init__(self, filename, filetype='autodetect', options=None, transformer_options=None):
        if options is None:
            options = {}
        if transformer_options is None:
            transformer_options = {}
        if not isinstance(transformer_options, dict):
            raise ValueError('transformers_options must be a dict of { transfo_name: options }. ' +
                             'Received: type=%s val=%s', type(transformer_options), transformer_options)

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
        self.options = options
        self.transformers_options = transformer_options
        self._transfo_calls = []

        # sanity check: make sure we don't process a (mostly) empty string
        if clean_string(filename) == '':
            return

        from guessit.plugins import transformers

        try:
            mtree = self.match_tree
            mtree.guess.set('type', filetype, confidence=0.0)

            # Process
            for transformer in transformers.all_transformers():
                self._process(transformer, options, False)

            # Post-process
            for transformer in transformers.all_transformers():
                self._process(transformer, options, True)

            log.debug('Found match tree:\n%s' % u(mtree))
        except TransformerException as e:
            log.debug('An error has occured in Transformer %s: %s' % (e.transformer, e))

    def _process(self, transformer, options={}, post=False):
        transformer_options = self.transformers_options.get(transformer.fullname, None)
        options = dict(self.options)
        if transformer_options:
            options.update(transformer_options)
        if not hasattr(transformer, 'should_process') or transformer.should_process(self.match_tree, options):
            if post:
                transformer.post_process(self.match_tree, options)
            else:
                transformer.process(self.match_tree, options)
                self._transfo_calls.append((transformer, options))

    @property
    def second_pass_options(self):
        transformers_options = dict(self.transformers_options.items())
        for transformer, options in self._transfo_calls:
            if hasattr(transformer, 'second_pass_options'):
                second_pass_options = transformer.second_pass_options(self.match_tree, options)
                if second_pass_options:
                    transformers_options[transformer.fullname] = second_pass_options

        return transformers_options

    def matched(self):
        return self.match_tree.matched()
