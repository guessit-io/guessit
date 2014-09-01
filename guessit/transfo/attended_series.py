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
from guessit.containers import PropertiesContainer
from guessit.matcher import GuessFinder

from guessit.plugins.transformers import Transformer
from guessit.textutils import find_first_level_groups
from guessit.patterns import group_delimiters
from functools import reduce
import re


class AttendedSeries(Transformer):
    def __init__(self):
        Transformer.__init__(self, 230)

    def should_process(self, mtree, options=None):
        return options and options.get('attended_series')

    def attended_series(self, string, node=None, options=None):
        container = PropertiesContainer(enhance=True, canonical_from_pattern=False)

        for attended_serie in options.get('attended_series'):
            if attended_serie.startswith('re:'):
                attended_serie = attended_serie[3:]
                attended_serie = attended_serie.replace(' ', '-')
                container.register_property('series', attended_serie, enhance=True)
            else:
                attended_serie = re.escape(attended_serie)
                container.register_property('series', attended_serie, enhance=False)

        found = container.find_properties(string, node, options)
        return container.as_guess(found, string)

    def supported_properties(self):
        return ['series']

    def process(self, mtree, options=None):
        GuessFinder(self.attended_series, None, self.log, options).process_nodes(mtree.unidentified_leaves())
