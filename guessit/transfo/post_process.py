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

from guessit.patterns.extension import subtitle_exts
from guessit.patterns import sep
from guessit.textutils import reorder_title, find_words
from guessit.language import subtitle_prefixes, subtitle_suffixes


class PostProcess(Transformer):
    def __init__(self):
        Transformer.__init__(self, -255)
        
    def supported_properties(self):
        return ['subtitleLanguage']

    def promote_subtitle(self, node):
        node.guess.set('subtitleLanguage', node.guess['language'],
                       confidence=node.guess.confidence('language'))
        del node.guess['language']

    def find_prefix(self, node):
        global_str = node.root.value().lower()

        prefix = ""
        i = node.span[0] - 1
        sep_found = False
        while i > -1:
            if not global_str[i] in sep:
                if not sep_found:
                    sep_found = True
            else:
                if sep_found:
                    break
            if sep_found:
                prefix = global_str[i] + prefix
            i = i - 1

        return prefix

    def process(self, mtree):
        """perform some post-processing steps
        """

        # 1- try to promote language to subtitle language where it makes sense
        for node in mtree.nodes():
            if 'language' not in node.guess:
                continue

            # - if we matched a language in a file with a sub extension and that
            #   the group is the last group of the filename, it is probably the
            #   language of the subtitle
            #   (eg: 'xxx.english.srt')
            if (mtree.node_at((-1,)).value.lower() in subtitle_exts and
                node == mtree.leaves()[-2]):
                self.promote_subtitle(node)

            # - if we find in the same explicit group
            # a subtitle prefix before the language,
            # or a subtitle suffix after the language,
            # then upgrade the language
            explicit_group = mtree.node_at(node.node_idx[:2])
            group_str = explicit_group.value.lower()

            for sub_prefix in subtitle_prefixes:
                if (sub_prefix in find_words(group_str) and
                    0 <= group_str.find(sub_prefix) < (node.span[0] - explicit_group.span[0])):
                    self.promote_subtitle(node)

            for sub_suffix in subtitle_suffixes:
                if (sub_suffix in find_words(group_str) and
                    (node.span[0] - explicit_group.span[0]) < group_str.find(sub_suffix)):
                    self.promote_subtitle(node)

            # - if a language is in an explicit group just preceded by "st",
            #   it is a subtitle language (eg: '...st[fr-eng]...')
            try:
                idx = node.node_idx
                previous = mtree.node_at((idx[0], idx[1] - 1)).leaves()[-1]
                if previous.value.lower()[-2:] == 'st':
                    self.promote_subtitle(node)
            except IndexError:
                pass

        # 2- ", the" at the end of a series title should be prepended to it
        for node in mtree.nodes():
            if 'series' not in node.guess:
                continue

            node.guess['series'] = reorder_title(node.guess['series'])
