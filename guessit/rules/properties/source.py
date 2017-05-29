#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
source property
"""
from rebulk.remodule import re

from rebulk import Rebulk, RemoveMatch, RenameMatch, Rule

from ..common import dash
from ..common.validators import seps_before, seps_after


def source():
    """
    Builder for rebulk object.
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash], children=True)
    rebulk.defaults(name='source', tags=['video-codec-prefix', 'streaming_service.suffix'])

    rip_prefix = '(?P<other>Rip)-?'
    rip_suffix = '-?(?P<other>Rip)'
    rip_optional_suffix = '(?:' + rip_suffix + ')?'

    def build_source_pattern(*patterns, **kwargs):
        """Build source pattern keeping the legacy format property."""
        source_format = '((?P<format>{0}))'
        prefix_format = kwargs.get('prefix') or ''
        suffix_format = kwargs.get('suffix') or ''

        string_format = prefix_format + source_format + suffix_format
        return [string_format.format(pattern) for pattern in patterns]

    def demote_other(match, other):  # pylint: disable=unused-argument
        """Default conflict solver with 'other' property."""
        return other if other.name == 'other' else '__default__'

    rebulk.regex(*build_source_pattern('VHS', suffix=rip_optional_suffix),
                 value={'format': 'VHS', 'source': 'VHS', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('CAM', 'HD-?CAM', suffix=rip_optional_suffix),
                 value={'format': 'Cam', 'source': 'Camera', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TELESYNC', 'TS', 'HD-?TS', suffix=rip_optional_suffix),
                 value={'format': 'Telesync', 'source': 'Telesync', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('WORKPRINT', 'WP'), value='Workprint')
    rebulk.regex(*build_source_pattern('TELECINE', 'TC', suffix=rip_optional_suffix),
                 value={'format': 'Telecine', 'source': 'Telecine', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('PPV', suffix=rip_optional_suffix),  # Pay Per View
                 value={'format': 'PPV', 'source': 'PPV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('SD-?TV', suffix=rip_optional_suffix),
                 value={'format': 'TV', 'source': 'TV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TV', suffix=rip_suffix),  # TV is too common to allow matching
                 value={'format': 'TV', 'source': 'TV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TV', 'SD-?TV', prefix=rip_prefix),
                 value={'format': 'TV', 'source': 'TV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TV-?(?=Dub)'), value='TV')
    rebulk.regex(*build_source_pattern('DVB', 'PD-?TV', suffix=rip_optional_suffix),
                 value={'format': 'DVB', 'source': 'Digital TV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('DVD', suffix=rip_optional_suffix),
                 value={'format': 'DVD', 'source': 'DVD', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('VIDEO-?TS', 'DVD-?R(?:$|(?!E))',  # 'DVD-?R(?:$|^E)' => DVD-Real ...
                                       'DVD-?9', 'DVD-?5'), value={'format': 'DVD', 'source': 'DVD'})

    rebulk.regex(*build_source_pattern('HD-?TV', suffix=rip_optional_suffix), conflict_solver=demote_other,
                 value={'format': 'HDTV', 'source': 'HDTV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('HD', suffix=rip_suffix), conflict_solver=demote_other,
                 value={'format': 'HDTV', 'source': 'HDTV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TV-?HD', suffix=rip_suffix), conflict_solver=demote_other,
                 value={'format': 'HDTV', 'source': 'HDTV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TV', suffix='-?(?P<other>Rip-?HD)'), conflict_solver=demote_other,
                 value={'format': 'HDTV', 'source': 'HDTV', 'other': 'Rip'})

    rebulk.regex(*build_source_pattern('VOD', suffix=rip_optional_suffix),
                 value={'format': 'VOD', 'source': 'Video on Demand', 'other': 'Rip'})

    rebulk.regex(*build_source_pattern('WEB', 'WEB-?DL', suffix=rip_suffix),
                 value={'format': 'WEBRip', 'source': 'WEB', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('WEB-?(?P<another>Cap)', suffix=rip_optional_suffix),
                 value={'format': 'WEBRip', 'source': 'WEB', 'other': 'Rip', 'another': 'Capped'})
    rebulk.regex(*build_source_pattern('WEB-?DL', 'WEB-?HD', 'WEB', 'DL-?WEB', 'DL(?=-?Mux)'),
                 value={'format': 'WEB-DL', 'source': 'WEB'})

    rebulk.regex(*build_source_pattern('HD-?DVD', suffix=rip_optional_suffix),
                 value={'format': 'HD-DVD', 'source': 'HD-DVD', 'other': 'Rip'})

    rebulk.regex(*build_source_pattern('Blu-?ray', 'BD', 'BD[59]', 'BD25', 'BD50', suffix=rip_optional_suffix),
                 value={'format': 'BluRay', 'source': 'BluRay', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('(?P<another>BR)-?(?=Scr(?:eener)?)', '(?P<another>BR)-?(?=Mux)'),  # BRRip
                 value={'format': 'BluRay', 'source': 'BluRay', 'another': 'ReEncoded'})
    rebulk.regex(*build_source_pattern('(?P<another>BR)', suffix=rip_suffix),  # BRRip
                 value={'format': 'BluRay', 'source': 'BluRay', 'other': 'Rip', 'another': 'ReEncoded'})

    rebulk.regex(*build_source_pattern('AHDTV'), value={'format': 'AHDTV', 'source': 'Analogue HDTV'})
    rebulk.regex(*build_source_pattern('UHD-?TV', suffix=rip_optional_suffix), conflict_solver=demote_other,
                 value={'format': 'UHDTV', 'source': 'Ultra HDTV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('UHD', suffix=rip_suffix), conflict_solver=demote_other,
                 value={'format': 'UHDTV', 'source': 'Ultra HDTV', 'other': 'Rip'})

    rebulk.regex(*build_source_pattern('HD-?TC', suffix=rip_optional_suffix),
                 value={'format': 'HDTC', 'source': 'HD Telecine', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('DSR', 'DTH', suffix=rip_optional_suffix),
                 value={'format': 'SATRip', 'source': 'Satellite', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('DSR?', 'SAT', suffix=rip_suffix),
                 value={'format': 'SATRip', 'source': 'Satellite', 'other': 'Rip'})

    rebulk.rules(RenameAdditionalSourceMatches, ValidateSource)

    return rebulk


class RenameAdditionalSourceMatches(Rule):
    """
    Rename the additional children matches generated by `source` rules to `other`
    """
    priority = 64
    consequence = RenameMatch('other')

    def when(self, matches, context):
        return matches.named('another')


class ValidateSource(Rule):
    """
    Validate source with screener property, with video_codec property or separated
    """
    priority = 64
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []
        for match in matches.named('source'):
            match = match.initiator
            if not seps_before(match) and \
                    not matches.range(match.start - 1, match.start - 2,
                                      lambda match: 'source-prefix' in match.tags):
                if match.children:
                    ret.extend(match.children)
                ret.append(match)
                continue
            if not seps_after(match) and \
                    not matches.range(match.end, match.end + 1,
                                      lambda match: 'source-suffix' in match.tags):
                if match.children:
                    ret.extend(match.children)
                ret.append(match)
                continue
        return ret
