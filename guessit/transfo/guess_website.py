#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
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

from __future__ import unicode_literals
from guessit.plugins import Transformer

from guessit.patterns.website import container
from guessit.transfo import SingleNodeGuesser


class GuessWebsite(Transformer):
    def __init__(self):
        Transformer.__init__(self, 45)

    def guess_website(self, string):
        found = container.find_properties(string, 'website')
        return container.as_guess(found, string)

    def process(self, mtree):
        SingleNodeGuesser(self.guess_website, 1.0, self.log).process(mtree)
