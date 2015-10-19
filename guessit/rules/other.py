#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
format property
"""
import copy
from rebulk import Rebulk, RemoveMatchRule

from .common import dash

import regex as re
from .common import seps
from .common.validators import seps_surround

OTHER = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash]).string_defaults(ignore_case=True)
OTHER.defaults(name="other", validator=seps_surround)

OTHER.regex('Audio-Fix', 'Audio-Fixed', value='AudioFix')
OTHER.regex('Sync-Fix', 'Sync-Fixed', value='SyncFix')
OTHER.regex('Dual-Audio', value='DualAudio')
OTHER.regex('ws', 'wide-screen', value='WideScreen')
OTHER.string('Netflix', 'NF', value='Netflix')

OTHER.string('Real', 'Fix', value='Proper', tags='other.has-neighbor')
OTHER.string('Proper', 'Repack', 'Rerip', value='Proper')
OTHER.string('Fansub', value='Fansub', tags='other.has-neighbor')
OTHER.string('Fastsub', value='Fastsub', tags='other.has-neighbor')

OTHER.regex('(?:Seasons?-)?Complete', value='Complete',
            validator=lambda match: seps_surround(match) and match.raw.lower().strip(seps) != "complete")
OTHER.string('R5', 'RC', value='R5')
OTHER.regex('Pre-Air', value='Preair')

for value in ('Screener', 'Remux', '3D', 'HD', 'mHD', 'HDLight', 'HQ', 'DDC', 'HR', 'PAL', 'SECAM', 'NTSC', 'CC', 'LD',
              'MD'):
    OTHER.string(value, value=value)

for value in ('Limited', 'Complete', 'Classic', 'Unrated', 'LiNE', 'Bonus', 'Trailer'):
    OTHER.string(value, value=value, tags='other.has-neighbor')

OTHER.regex('Scr(?:eener)?', value='Screener', validator=None, tags='other.validate.screener')


class ValidateHasNeighbor(RemoveMatchRule):
    """
    Validate tag other.has-neighbor
    """
    priority = 255

    def when(self, matches, context):
        ret = []
        for to_check in matches.range(predicate=lambda match: 'other.has-neighbor' in match.tags):
            previous_match = matches.previous(to_check, index=0)
            if previous_match and not matches.input_string[previous_match.end:to_check.start].strip(seps):
                break
            next_match = matches.next(to_check, index=0)
            if next_match and not matches.input_string[to_check.end:next_match.start].strip(seps):
                break
            ret.append(to_check)
        return ret


class ValidateScreenerRule(RemoveMatchRule):
    """
    Validate tag other.validate.screener
    """
    priority = 255

    def when(self, matches, context):
        ret = []
        for screener in matches.named('other', lambda match: 'other.validate.screener' in match.tags):
            format_match = matches.previous(screener, lambda match: match.name == 'format', 0)
            if not format_match or matches.input_string[format_match.end:screener.start].strip(seps):
                ret.append(screener)
        return ret

OTHER.rules(ValidateHasNeighbor, ValidateScreenerRule)


def proper_count(matches):
    """
    Add properCount property
    :param matches:
    :return:
    """
    propers = matches.named('other', lambda match: match.value == 'Proper')
    if propers:
        proper_count_match = copy.copy(propers[-1])
        proper_count_match.name = 'properCount'
        proper_count_match.value = len(propers)
        matches.append(proper_count_match)

OTHER.post_processor(proper_count)

