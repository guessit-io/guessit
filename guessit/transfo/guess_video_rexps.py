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
from guessit.patterns import _psep
from guessit.patterns.containers import PropertiesContainer


class GuessVideoRexps(Transformer):
    def __init__(self):
        Transformer.__init__(self, 25)

        self.container = PropertiesContainer(canonical_from_pattern=False)

        self.container.register_property('cdNumber', None, 'cd' + _psep + '(?P<cdNumber>[0-9])(?:' + _psep + 'of' + _psep + '(?P<cdNumberTotal>[0-9]))?', confidence=1.0, enhance=False, global_span=True)
        self.container.register_property('cdNumberTotal', None, '([1-9])' + _psep + 'cds?', confidence=0.9, enhance=False)

        self.container.register_property('edition', 'Collector Edition', 'collector', 'collector-edition', 'edition-collector')

        self.container.register_property('edition', 'Special Edition', 'special', 'special-edition', 'edition-special')

        self.container.register_property('edition', 'Criterion Edition', 'criterion', 'criterion-edition', 'edition-criterion')

        self.container.register_property('edition', 'Deluxe Edition', 'deluxe', 'cdeluxe-edition', 'edition-deluxe')

        self.container.register_property('edition', 'Director\'s cut', 'director\'?s?-cut', 'director\'?s?-cut-edition', 'edition-director\'?s?-cut')

        self.container.register_property('bonusNumber', None, 'x([0-9]{1,2})', enhance=False, global_span=True)

        self.container.register_property('filmNumber', None, 'f([0-9]{1,2})', enhance=False, global_span=True)

    def supported_properties(self):
        return self.container.get_supported_properties()

    def guess_video_rexps(self, string):
        found = self.container.find_properties(string)
        return self.container.as_guess(found, string)

    def process(self, mtree):
        SingleNodeGuesser(self.guess_video_rexps, None, self.log).process(mtree)
