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

from guessit.transfo import SingleNodeGuesser
from guessit.patterns import properties, sep
import logging

log = logging.getLogger("guessit.transfo.guess_properties")


DEPENDS = []
PROVIDES = []


def guess_properties(string):
    low = string.lower()
    for prop, values in properties.items():
        for value in values:
            pos = low.find(value.lower())
            if pos != -1:
                end = pos + len(value)
                # make sure our word is always surrounded by separators
                if ((pos > 0 and low[pos-1] not in sep) or
                    (end < len(low) and low[end] not in sep)):
                    # note: sep is a regexp, but in this case using it as
                    #       a sequence achieves the same goal
                    continue
                return { prop: value }, (pos, end)

    return None, None


def process(mtree):
    SingleNodeGuesser(guess_properties, 1.0, log).process(mtree)
