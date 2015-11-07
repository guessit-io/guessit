#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bonus support
"""
from __future__ import unicode_literals

import regex as re
from guessit.rules.properties.title import TitleFromPosition
from rebulk import Rebulk, AppendMatch, Rule

from ..common.formatters import cleanup
from ..common.validators import seps_surround

BONUS = Rebulk().regex_defaults(flags=re.IGNORECASE)


BONUS.regex(r'x(\d+)', name='bonus', private_parent=True, children=True, formatter=int,
            validator={'__parent__': lambda match: seps_surround},
            conflict_solver=lambda match, conflicting: match
            if conflicting.name in ['video_codec', 'episode'] and 'bonus-conflict' not in conflicting.tags
            else '__default__')


class BonusTitleRule(Rule):
    """
    Find bonus title after bonus.
    """
    dependency = TitleFromPosition
    consequence = AppendMatch

    def when(self, matches, context):
        bonus_number = matches.named('bonus', lambda match: not match.private, index=0)
        if bonus_number:
            filepath = matches.markers.at_match(bonus_number, lambda marker: marker.name == 'path', 0)
            hole = matches.holes(bonus_number.end, filepath.end + 1, formatter=cleanup, index=0)
            if hole and hole.value:
                hole.name = 'bonus_title'
                return hole


BONUS.rules(BonusTitleRule)
