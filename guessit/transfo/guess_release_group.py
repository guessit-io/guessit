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

from guessit.plugins.transformers import Transformer, SingleNodeGuesser
from guessit.patterns.containers import PropertiesContainer
from guessit.patterns import sep
from guessit.guess import Guess


class GuessReleaseGroup(Transformer):
    def __init__(self):
        Transformer.__init__(self, -190)
        self.container = PropertiesContainer(canonical_from_pattern=False)
        self._allowed_groupname_pattern = r'[\w@#€£$&]'
        self._forbidden_groupname_lambda = [lambda elt: elt in ['rip', 'by', 'for', 'par', 'pour', 'bonus'],
                               lambda elt: self._is_number(elt),
                               ]
        # If the previous property in this list, the match will be considered as safe
        # and group name can contain a separator.
        self.previous_safe_properties = ['videoCodec', 'format', 'videoApi', 'audioCodec', 'audioProfile', 'videoProfile', 'audioChannels']

        self.container.sep_replace_char = '-'
        self.container.canonical_from_pattern = False
        self.container.enhance = True
        self.container.register_property('releaseGroup', self._allowed_groupname_pattern + '+')
        self.container.register_property('releaseGroup', self._allowed_groupname_pattern + '+-' + self._allowed_groupname_pattern + '+')

    def supported_properties(self):
        return self.container.get_supported_properties()

    def _is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def validate_group_name(self, guess):
        if guess.metadata().span[1] - guess.metadata().span[0] >= 2:
            val = guess['releaseGroup']

            if '-' in guess['releaseGroup']:
                checked_val = ""
                for elt in val.split('-'):
                    forbidden = False
                    for forbidden_lambda in self._forbidden_groupname_lambda:
                        forbidden = forbidden_lambda(elt.lower())
                        if forbidden:
                            break
                    if not forbidden:
                        if checked_val:
                            checked_val += '-'
                        checked_val += elt
                    else:
                        break
                val = checked_val
                if not val:
                    return False
                guess['releaseGroup'] = val

            forbidden = False
            for forbidden_lambda in self._forbidden_groupname_lambda:
                forbidden = forbidden_lambda(val.lower())
                if forbidden:
                    break
            if not forbidden:
                return True
        return False

    def is_leaf_previous(self, leaf, node):
        if leaf.span[1] <= node.span[0]:
            for idx in range(leaf.span[1], node.span[0]):
                if not leaf.root.value[idx] in sep:
                    return False
            return True
        return False

    def guess_release_group(self, string, node):
        found = self.container.find_properties(string, node, 'releaseGroup')
        guess = self.container.as_guess(found, string, self.validate_group_name, sep_replacement='-')
        if guess:
            explicit_group_idx = node.node_idx[:2]
            explicit_group = node.root.node_at(explicit_group_idx)
            for leaf in explicit_group.leaves_containing(self.previous_safe_properties):
                if self.is_leaf_previous(leaf, node):
                    if leaf.root.value[leaf.span[1]] == '-':
                        guess.metadata().confidence = 1
                    else:
                        guess.metadata().confidence = 0.7
                    return guess

            # If previous group last leaf is identified as a safe property,
            # consider the raw value as a groupname
            if len(explicit_group_idx) > 0 and explicit_group_idx[-1] > 0:
                previous_group = explicit_group_idx[:-1] + (explicit_group_idx[-1] - 1,)
                previous_node = node.root.node_at(previous_group)
                for leaf in previous_node.leaves_containing(self.previous_safe_properties):
                    if self.is_leaf_previous(leaf, node):
                        guess = Guess({'releaseGroup': node.clean_value}, confidence=1, input=node.value, span=node.span)
                        if self.validate_group_name(guess):
                            node.guess = guess
                            break

        return None

    def process(self, mtree, options={}):
        SingleNodeGuesser(self.guess_release_group, None, self.log).process(mtree)
