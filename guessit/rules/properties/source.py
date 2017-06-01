#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
source property
"""
from rebulk.remodule import re

from rebulk import Rebulk, RemoveMatch, Rule

from ..common import dash
from ..common.validators import seps_before, seps_after


def source():
    """
    Builder for rebulk object.
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash], private_parent=True, children=True)
    rebulk.defaults(name='source', tags=['video-codec-prefix', 'streaming_service.suffix'])

    rip_prefix = '(?P<other>Rip)-?'
    rip_suffix = '-?(?P<other>Rip)'
    rip_optional_suffix = '(?:' + rip_suffix + ')?'

    def build_source_pattern(*patterns, **kwargs):
        """Helper pattern to build source pattern."""
        prefix_format = kwargs.get('prefix') or ''
        suffix_format = kwargs.get('suffix') or ''

        string_format = prefix_format + '({0})' + suffix_format
        return [string_format.format(pattern) for pattern in patterns]

    def demote_other(match, other):  # pylint: disable=unused-argument
        """Default conflict solver with 'other' property."""
        return other if other.name == 'other' else '__default__'

    rebulk.regex(*build_source_pattern('VHS', suffix=rip_optional_suffix),
                 value={'source': 'VHS', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('CAM', suffix=rip_optional_suffix),
                 value={'source': 'Camera', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('HD-?CAM', suffix=rip_optional_suffix),
                 value={'source': 'HD Camera', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TELESYNC', 'TS', suffix=rip_optional_suffix),
                 value={'source': 'Telesync', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('HD-?TELESYNC', 'HD-?TS', suffix=rip_optional_suffix),
                 value={'source': 'HD Telesync', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('WORKPRINT', 'WP'), value='Workprint')
    rebulk.regex(*build_source_pattern('TELECINE', 'TC', suffix=rip_optional_suffix),
                 value={'source': 'Telecine', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('HD-?TELECINE', 'HD-?TC', suffix=rip_optional_suffix),
                 value={'source': 'HD Telecine', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('PPV', suffix=rip_optional_suffix),
                 value={'source': 'Pay-per-view', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('SD-?TV', suffix=rip_optional_suffix),
                 value={'source': 'TV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TV', suffix=rip_suffix),  # TV is too common to allow matching
                 value={'source': 'TV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TV', 'SD-?TV', prefix=rip_prefix),
                 value={'source': 'TV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TV-?(?=Dub)'), value='TV')
    rebulk.regex(*build_source_pattern('DVB', 'PD-?TV', suffix=rip_optional_suffix),
                 value={'source': 'Digital TV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('DVD', suffix=rip_optional_suffix),
                 value={'source': 'DVD', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('VIDEO-?TS', 'DVD-?R(?:$|(?!E))',  # 'DVD-?R(?:$|^E)' => DVD-Real ...
                                       'DVD-?9', 'DVD-?5'), value='DVD')

    rebulk.regex(*build_source_pattern('HD-?TV', suffix=rip_optional_suffix), conflict_solver=demote_other,
                 value={'source': 'HDTV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TV-?HD', suffix=rip_suffix), conflict_solver=demote_other,
                 value={'source': 'HDTV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('TV', suffix='-?(?P<other>Rip-?HD)'), conflict_solver=demote_other,
                 value={'source': 'HDTV', 'other': 'Rip'})

    rebulk.regex(*build_source_pattern('VOD', suffix=rip_optional_suffix),
                 value={'source': 'Video on Demand', 'other': 'Rip'})

    rebulk.regex(*build_source_pattern('WEB', 'WEB-?DL', suffix=rip_suffix),
                 value={'source': 'Web', 'other': 'Rip'})
    # WEBCap is a synonym to WEBRip, mostly used by non english
    rebulk.regex(*build_source_pattern('WEB-?(?P<another>Cap)', suffix=rip_optional_suffix),
                 value={'source': 'Web', 'other': 'Rip', 'another': 'Rip'})
    rebulk.regex(*build_source_pattern('WEB-?DL', 'WEB-?HD', 'WEB', 'DL-?WEB', 'DL(?=-?Mux)'),
                 value={'source': 'Web'})

    rebulk.regex(*build_source_pattern('HD-?DVD', suffix=rip_optional_suffix),
                 value={'source': 'HD-DVD', 'other': 'Rip'})

    rebulk.regex(*build_source_pattern('Blu-?ray', 'BD', 'BD[59]', 'BD25', 'BD50', suffix=rip_optional_suffix),
                 value={'source': 'Blu-ray', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('(?P<another>BR)-?(?=Scr(?:eener)?)', '(?P<another>BR)-?(?=Mux)'),  # BRRip
                 value={'source': 'Blu-ray', 'another': 'ReEncoded'})
    rebulk.regex(*build_source_pattern('(?P<another>BR)', suffix=rip_suffix),  # BRRip
                 value={'source': 'Blu-ray', 'other': 'Rip', 'another': 'ReEncoded'})

    rebulk.regex(*build_source_pattern('AHDTV'), value='Analogue HDTV')
    rebulk.regex(*build_source_pattern('UHD-?TV', suffix=rip_optional_suffix), conflict_solver=demote_other,
                 value={'source': 'Ultra HDTV', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('UHD', suffix=rip_suffix), conflict_solver=demote_other,
                 value={'source': 'Ultra HDTV', 'other': 'Rip'})

    rebulk.regex(*build_source_pattern('DSR', 'DTH', suffix=rip_optional_suffix),
                 value={'source': 'Satellite', 'other': 'Rip'})
    rebulk.regex(*build_source_pattern('DSR?', 'SAT', suffix=rip_suffix),
                 value={'source': 'Satellite', 'other': 'Rip'})

    rebulk.rules(ValidateSource)

    return rebulk


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
