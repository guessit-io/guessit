#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2012 Nicolas Wack <wackou@gmail.com>
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
from guessit import Guess
from guessit.transfo import SingleNodeGuesser
from guessit.patterns.properties import find_properties, get_properties
import logging

log = logging.getLogger(__name__)


def guess_properties(string):
    found = find_properties(string)
    if found:
        prop, span = found[0]
        guess = Guess(confidence=prop.confidence)
        guess[prop.name] = prop.canonical_form
        return guess, span
    return None, None


supported_properties = {}
for prop in get_properties():
    values = supported_properties.get(prop.name)
    if not values:
        values = set()
        supported_properties[prop.name] = values
    values.add(prop.canonical_form)


priority = 35


def process(mtree):
    SingleNodeGuesser(guess_properties, 1.0, log).process(mtree)
