#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Film support
"""
import regex as re
from rebulk import Rebulk, AppendMatch, Rule

from ..common.formatters import cleanup

FILM = Rebulk().regex_defaults(flags=re.IGNORECASE)

FILM.regex(r'f(\d+)', name='filmNumber', private_parent=True, children=True, formatter=int)


class FilmTitleRule(Rule):
    """
    Abstract rule to validate audio profiles
    """
    priority = 15  # Must be before title guessing
    consequence = AppendMatch

    def when(self, matches, context):
        bonus_number = matches.named('filmNumber', lambda match: not match.private, index=0)
        if bonus_number:
            filepath = matches.markers.at_match(bonus_number, lambda marker: marker.name == 'path', 0)
            hole = matches.holes(filepath.start, bonus_number.start + 1, formatter=cleanup, index=0)
            if hole and hole.value:
                hole.name = 'filmSeries'
                return hole


FILM.rules(FilmTitleRule)
