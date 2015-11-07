#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
screen_size property
"""
from __future__ import unicode_literals

from rebulk import Rebulk, Rule, RemoveMatch
import regex as re

from ..common.validators import seps_surround
from guessit.rules.common import dash

def conflict_solver(match, other):
    """
    Conflict solver for most screen_size.
    """
    if other.name in ['episode', 'season']:
        return '__default__'
    if other.name == 'screen_size' and 'resolution' in other.tags:
        # The chtouile to solve conflict in "720 x 432" string matching both 720p pattern (but it's not 720p ...)
        int_value = _digits_re.findall(match.raw)[-1]
        if other.value.startswith(int_value):
            return match
    return other

SCREEN_SIZE = Rebulk().regex_defaults(flags=re.IGNORECASE)
SCREEN_SIZE.defaults(name="screen_size", validator=seps_surround, conflict_solver=conflict_solver)

SCREEN_SIZE.regex(r"(?:\d{3,}(?:x|\*))?360(?:i|p?x?)", value="360p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:x|\*))?368(?:i|p?x?)", value="368p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:x|\*))?480(?:i|p?x?)", value="480p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:x|\*))?576(?:i|p?x?)", value="576p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:x|\*))?720(?:i|p?x?)", value="720p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:x|\*))?900(?:i|p?x?)", value="900p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:x|\*))?1080i", value="1080i")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:x|\*))?1080p?x?", value="1080p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:x|\*))?2160(?:i|p?x?)", value="4K")


_digits_re = re.compile(r'\d+')

SCREEN_SIZE.defaults(name="screen_size", validator=seps_surround)
SCREEN_SIZE.regex(r'\d{3,}-?(?:x|\*)-?\d{3,}',
                  formatter=lambda value: 'x'.join(_digits_re.findall(value)),
                  abbreviations=[dash],
                  tags=['resolution'],
                  conflict_solver=lambda match, other: '__default__' if other.name == 'screen_size' else other)


class ScreenSizeOnlyOne(Rule):
    """
    Keep a single screen_size pet filepath part.
    """
    consequence = RemoveMatch

    def when(self, matches, context):
        to_remove = []
        for filepart in matches.markers.named('path'):
            screensize = list(reversed(matches.range(filepart.start, filepart.end,
                                                     lambda match: match.name == 'screen_size')))
            if len(screensize) > 1:
                to_remove.extend(screensize[1:])

        return to_remove

SCREEN_SIZE.rules(ScreenSizeOnlyOne)
