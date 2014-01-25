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

from guessit import Guess
from guessit.transfo import SingleNodeGuesser
from guessit.patterns import sep
import re


class GuessWeakEpisodesRexps(Transformer):
    def __init__(self):
        Transformer.__init__(self, 15)

        self.weak_episode_rexps = [  # ... 213 or 0106 ...
                       (sep + r'(?P<episodeNumber>[0-9]{2,4})' + sep, (1, -1))
                       ]

    def supported_properties(self):
        return ['episodeNumber', 'season']

    def guess_weak_episodes_rexps(self, string, node):
        if 'episodeNumber' in node.root.info:
            return None, None

        for rexp, span_adjust in self.weak_episode_rexps:
            match = re.search(rexp, string, re.IGNORECASE)
            if match:
                metadata = match.groupdict()
                span = (match.start() + span_adjust[0],
                        match.end() + span_adjust[1])

                epnum = int(metadata['episodeNumber'])
                if epnum > 100:
                    season, epnum = epnum // 100, epnum % 100
                    # episodes which have a season > 50 are most likely errors
                    # (Simpson is at 25!)
                    if season > 50:
                        continue
                    return Guess({'season': season, 'episodeNumber': epnum}, confidence=0.6, input=string, span=span)
                else:
                    return Guess(metadata, confidence=0.3, input=string, span=span)

        return None, None

    guess_weak_episodes_rexps.use_node = True

    def should_process(self, matcher):
        return matcher.match_tree.guess['type'] in ('episode', 'episodesubtitle', 'episodeinfo')

    def process(self, mtree):
        SingleNodeGuesser(self.guess_weak_episodes_rexps, 0.6, self.log).process(mtree)
