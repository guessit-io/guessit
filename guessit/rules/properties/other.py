#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
format property
"""
from __future__ import unicode_literals

import copy

from rebulk import Rebulk, Rule, RemoveMatch
import regex as re

from ..common import dash
from ..common import seps
from ..common.validators import seps_surround
from guessit.rules.common.formatters import raw_cleanup

OTHER = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash]).string_defaults(ignore_case=True)
OTHER.defaults(name="other", validator=seps_surround)

OTHER.regex('Audio-?Fix', 'Audio-?Fixed', value='AudioFix')
OTHER.regex('Sync-?Fix', 'Sync-?Fixed', value='SyncFix')
OTHER.regex('Dual-?Audio', value='DualAudio')
OTHER.regex('ws', 'wide-?screen', value='WideScreen')
OTHER.string('Netflix', 'NF', value='Netflix')

OTHER.string('Real', 'Fix', value='Proper', tags=['has-neighbor-before', 'has-neighbor-after'])
OTHER.string('Proper', 'Repack', 'Rerip', value='Proper')
OTHER.string('Fansub', value='Fansub', tags='has-neighbor')
OTHER.string('Fastsub', value='Fastsub', tags='has-neighbor')

OTHER.regex('(?:Seasons?-)?Complete', value='Complete', tags=['release-group-prefix'],
            validator=lambda match: seps_surround(match) and match.raw.lower().strip(seps) != "complete")
OTHER.string('R5', 'RC', value='R5')
OTHER.regex('Pre-?Air', value='Preair')

for value in ('Screener', 'Remux', '3D', 'HD', 'mHD', 'HDLight', 'HQ', 'DDC', 'HR', 'PAL', 'SECAM', 'NTSC', 'CC', 'LD',
              'MD'):
    OTHER.string(value, value=value)

for value in ('Limited', 'Complete', 'Classic', 'Unrated', 'LiNE', 'Bonus', 'Trailer', 'FINAL'):
    OTHER.string(value, value=value, tags=['has-neighbor', 'release-group-prefix'])

OTHER.string('VO', 'OV', value='OV', tags='has-neighbor')

OTHER.regex('Scr(?:eener)?', value='Screener', validator=None, tags='other.validate.screener')


class ValidateHasNeighbor(Rule):
    """
    Validate tag has-neighbor
    """
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []
        for to_check in matches.range(predicate=lambda match: 'has-neighbor' in match.tags):
            previous_match = matches.previous(to_check, index=0)
            previous_group = matches.markers.previous(to_check, lambda marker: marker.name == 'group', 0)
            if previous_group and (not previous_match or previous_group.end > previous_match.end):
                previous_match = previous_group
            if previous_match and not matches.input_string[previous_match.end:to_check.start].strip(seps):
                break
            next_match = matches.next(to_check, index=0)
            next_group = matches.markers.next(to_check, lambda marker: marker.name == 'group', 0)
            if next_group and (not next_match or next_group.start < next_match.start):
                next_match = next_group
            if next_match and not matches.input_string[to_check.end:next_match.start].strip(seps):
                break
            ret.append(to_check)
        return ret


class ValidateHasNeighborBefore(Rule):
    """
    Validate tag has-neighbor-before that previous match exists.
    """
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []
        for to_check in matches.range(predicate=lambda match: 'has-neighbor-before' in match.tags):
            next_match = matches.next(to_check, index=0)
            next_group = matches.markers.next(to_check, lambda marker: marker.name == 'group', 0)
            if next_group and (not next_match or next_group.start < next_match.start):
                next_match = next_group
            if next_match and not matches.input_string[to_check.end:next_match.start].strip(seps):
                break
            ret.append(to_check)
        return ret


class ValidateHasNeighborAfter(Rule):
    """
    Validate tag has-neighbor-after that next match exists.
    """
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []
        for to_check in matches.range(predicate=lambda match: 'has-neighbor-after' in match.tags):
            previous_match = matches.previous(to_check, index=0)
            previous_group = matches.markers.previous(to_check, lambda marker: marker.name == 'group', 0)
            if previous_group and (not previous_match or previous_group.end > previous_match.end):
                previous_match = previous_group
            if previous_match and not matches.input_string[previous_match.end:to_check.start].strip(seps):
                break
            ret.append(to_check)
        return ret


class ValidateScreenerRule(Rule):
    """
    Validate tag other.validate.screener
    """
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []
        for screener in matches.named('other', lambda match: 'other.validate.screener' in match.tags):
            format_match = matches.previous(screener, lambda match: match.name == 'format', 0)
            if not format_match or matches.input_string[format_match.end:screener.start].strip(seps):
                ret.append(screener)
        return ret


OTHER.rules(ValidateHasNeighbor, ValidateHasNeighborAfter, ValidateHasNeighborBefore, ValidateScreenerRule)


def proper_count(matches):
    """
    Add properCount property
    :param matches:
    :return:
    """
    propers = matches.named('other', lambda match: match.value == 'Proper')
    if propers:
        raws = {}  # Count distinct raw values
        for proper in propers:
            raws[raw_cleanup(proper.raw)] = proper
        proper_count_match = copy.copy(propers[-1])
        proper_count_match.name = 'properCount'
        proper_count_match.value = len(raws)
        matches.append(proper_count_match)


OTHER.post_processor(proper_count)
