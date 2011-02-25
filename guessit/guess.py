#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2011 Nicolas Wack <wackou@gmail.com>
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

import json
import logging

log = logging.getLogger("guessit.guess")


class Guess(dict):
    def __init__(self, *args, **kwargs):
        try:
            confidence = kwargs.pop('confidence')
        except KeyError:
            confidence = 0

        dict.__init__(self, *args, **kwargs)

        self._confidence = {}
        for prop in self:
            self._confidence[prop] = confidence

    def to_json(self):
        parts = json.dumps(self, indent = 4).split('\n')
        for i, p in enumerate(parts):
            if p[:5] != '    "':
                continue

            prop = p.split('"')[1]
            parts[i] = ('    [%.2f] ' % self._confidence.get(prop, -1)) + p[5:]

        return '\n'.join(parts)

    def confidence(self, prop):
        return self._confidence[prop]

    def set_confidence(self, prop, value):
        self._confidence[prop] = value

    def update(self, other):
        dict.update(self, other)
        if isinstance(other, Guess):
            for prop in other:
                self._confidence[prop] = other.confidence(prop)



def merge_similar_guesses(guesses, prop, choose):
    """Take a list of guesses and merge those which have the same properties,
    increasing or decreasing the confidence depending on whether their values
    are similar."""

    similar = [ guess for guess in guesses if prop in guess ]
    if len(similar) < 2:
        # nothing to merge
        return

    if len(similar) > 2:
        log.warning('merge too complex to be dealt with at the moment, bailing out...')
        return

    g1, g2 = similar

    if len(set(g1) & set(g2)) > 1:
        log.warning('both guesses to be merged have more than one property in common, bailing out...')
        return

    # merge all props of s2 into s1, updating the confidence for the considered property
    v1, v2 = g1[prop], g2[prop]
    c1, c2 = g1.confidence(prop), g2.confidence(prop)

    new_value, new_confidence = choose((v1, c1), (v2, c2))
    if new_confidence >= c1:
        log.debug("Updating matching property '%s' with confidence %.2f" % (prop, new_confidence))
    else:
        log.debug("Updating non-matching property '%s' with confidence %.2f" % (prop, new_confidence))

    g2[prop] = new_value
    g2.set_confidence(prop, new_confidence)

    g1.update(g2)
    guesses.remove(g2)


def merge_all(guesses):
    """Merges all the guesses in a single result and returns it."""
    result = guesses[0]

    for g in guesses[1:]:
        if set(result) & set(g):
            log.warning('overwriting properties %s in merged result...' % (set(result) & set(g)))
        result.update(g)

    return result

