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
from guessit.transfo import SingleNodeGuesser, format_guess
from guessit.patterns import sep
from guessit.patterns.numeral import numeral, digital_numeral, parse_numeral
import re


class GuessEpisodesRexps(Transformer):
    def __init__(self):
        Transformer.__init__(self, 20)

        # format: [ (regexp, confidence, span_adjust) ]
        self.episode_rexps = [  # ... Season 2 ...
                          (r'(?:season|saison)\s+(?P<season>%s)' % (numeral,), 1.0, (0, 0)),

                          # ... s02e13 ...
                          (r's(?P<season>' + digital_numeral + ')[^0-9]?(?P<episodeNumber>(?:-?[e-]' + digital_numeral + ')+)[^0-9]', 1.0, (0, -1)),

                          # ... 2x13 ...
                          (r'[^0-9](?P<season>' + digital_numeral + ')[^0-9 .-]?(?P<episodeNumber>(?:-?x' + digital_numeral + ')+)[^0-9]', 1.0, (1, -1)),

                          # ... s02 ...
                          # (sep + r's(?P<season>[0-9]{1,2})' + sep, 0.6, (1, -1)),
                          (r's(?P<season>' + digital_numeral + ')[^0-9]', 0.6, (0, -1)),

                          # v2 or v3 for some mangas which have multiples rips
                          (r'(?P<episodeNumber>' + digital_numeral + ')v[23]' + sep, 0.6, (0, 0)),

                          # ... ep 23 ...
                          ('(?:ep|episode)' + sep + r'(?P<episodeNumber>' + numeral + ')[^0-9]', 0.7, (0, -1)),

                          # ... e13 ... for a mini-series without a season number
                          (sep + r'e(?P<episodeNumber>' + digital_numeral + ')' + sep, 0.6, (1, -1))

                  ]

    def supported_properties(self):
        return ['episodeNumber', 'bonusNumber', 'season']

    def number_list(self, s):
        l = [ parse_numeral(n) for n in re.findall(numeral, s) ]

        if len(l) == 2:
            # it is an episode interval, return all numbers in between
            return list(range(l[0], l[1] + 1))

        return l

    def guess_episodes_rexps(self, string):
        for rexp, confidence, span_adjust in self.episode_rexps:
            match = re.search(rexp, string, re.IGNORECASE)
            if match:
                span = (match.start() + span_adjust[0],
                        match.end() + span_adjust[1])
                guess = Guess(match.groupdict(), confidence=confidence, input=string, span=span)


                # decide whether we have only a single episode number or an
                # episode list
                if guess.get('episodeNumber'):
                    eplist = self.number_list(guess['episodeNumber'])
                    guess.set('episodeNumber', eplist[0], confidence=confidence, input=string, span=span)

                    if len(eplist) > 1:
                        guess.set('episodeList', eplist, confidence=confidence, input=string, span=span)

                if guess.get('bonusNumber'):
                    eplist = self.number_list(guess['bonusNumber'])
                    guess.set('bonusNumber', eplist[0], confidence=confidence, input=string, span=span)


                guess = format_guess(guess)
                return guess, span

        return None, None

    def should_process(self, matcher):
        return matcher.match_tree.guess['type'] in ('episode', 'episodesubtitle', 'episodeinfo')

    def process(self, mtree):
        SingleNodeGuesser(self.guess_episodes_rexps, None, self.log).process(mtree)
