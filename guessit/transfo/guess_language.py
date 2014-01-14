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

from guessit.plugins import Transformer

from guessit.transfo import SingleNodeGuesser
from guessit.language import search_language
from guessit.textutils import clean_string


class GuessLanguage(Transformer):
    def __init__(self):
        Transformer.__init__(self, 30)

    def supported_properties(self):
        return ['language']

    def guess_language(self, string):
        guess = search_language(string)
        return guess

    def _skip_language_on_second_pass(self, mtree, node):
        """Check if found node is a valid language node, or if it's a false positive.

        :param mtree: Tree detected on first pass.
        :type mtree: :class:`guessit.matchtree.MatchTree`
        :param node: Node that contains a language Guess
        :type node: :class:`guessit.matchtree.MatchTree`

        :return: True if a second pass skipping this node is required
        :rtype: bool
        """
        unidentified_starts = {}
        unidentified_ends = {}

        property_starts = {}
        property_ends = {}

        title_starts = {}
        title_ends = {}

        for unidentified_node in mtree.unidentified_leaves():
            unidentified_starts[unidentified_node.span[0]] = unidentified_node
            unidentified_ends[unidentified_node.span[1]] = unidentified_node

        for property_node in mtree.leaves_containing('year'):
            property_starts[property_node.span[0]] = property_node
            property_ends[property_node.span[1]] = property_node

        for title_node in mtree.leaves_containing(['title', 'series']):
            title_starts[title_node.span[0]] = title_node
            title_ends[title_node.span[1]] = title_node

        return node.span[0] in title_ends.keys() and (node.span[1] in unidentified_starts.keys() or node.span[1] + 1 in property_starts.keys()) or\
                node.span[1] in title_starts.keys() and (node.span[0] == 0 or node.span[0] in unidentified_ends.keys() or node.span[0] in property_ends.keys())

    def second_pass_options(self, mtree):
        m = mtree.matched()
        to_skip_language_nodes = []

        for lang_key in ('language', 'subtitleLanguage'):
            langs = {}
            lang_nodes = set(n for n in mtree.leaves_containing(lang_key))

            for lang_node in lang_nodes:
                lang = lang_node.guess.get(lang_key, None)
                if self._skip_language_on_second_pass(mtree, lang_node):
                    # Language probably split the title. Add to skip for 2nd pass.

                    # if filetype is subtitle and the language appears last, just before
                    # the extension, then it is likely a subtitle language
                    parts = clean_string(lang_node.root.value).split()
                    if m['type'] in ['moviesubtitle', 'episodesubtitle'] and (parts.index(lang_node.value) == len(parts) - 2):
                        continue

                    to_skip_language_nodes.append(lang_node)
                elif not lang in langs:
                    langs[lang] = lang_node
                else:
                    # The same language was found. Keep the more confident one, and add others to skip for 2nd pass.
                    existing_lang_node = langs[lang]
                    to_skip = None
                    if existing_lang_node.guess.confidence('language') >= lang_node.guess.confidence('language'):
                        # lang_node is to remove
                        to_skip = lang_node
                    else:
                        # existing_lang_node is to remove
                        langs[lang] = lang_node
                        to_skip = existing_lang_node
                    to_skip_language_nodes.append(to_skip)

        if to_skip_language_nodes:
            return None, {'skip_nodes': to_skip_language_nodes}
        return None, None

    def should_process(self, matcher):
        return not 'nolanguage' in matcher.opts

    def process(self, mtree, *args, **kwargs):
        SingleNodeGuesser(self.guess_language, None, self.log, *args, **kwargs).process(mtree)
        # Note: 'language' is promoted to 'subtitleLanguage' in the post_process transfo
