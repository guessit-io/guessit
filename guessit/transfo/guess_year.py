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
from guessit.date import search_year


class GuessYear(Transformer):
    def __init__(self):
        Transformer.__init__(self, -160)

    def supported_properties(self):
        return ['year']

    def guess_year(self, string):
        year, span = search_year(string)
        if year:
            return {'year': year}, span
        else:
            return None, None

    def second_pass_options(self, mtree):
        year_nodes = mtree.leaves_containing('year')
        if len(year_nodes) > 1:
            return None, {'skip_nodes': year_nodes[:len(year_nodes) - 1]}
        return None, None

    def process(self, mtree, *args, **kwargs):
        SingleNodeGuesser(self.guess_year, 1.0, self.log, *args, **kwargs).process(mtree)
