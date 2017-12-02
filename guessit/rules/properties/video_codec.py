#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
video_codec and video_profile property
"""
from rebulk.remodule import re

from rebulk import Rebulk, Rule, RemoveMatch

from ..common import dash
from ..common.validators import seps_after, seps_before, seps_surround


def video_codec():
    """
    Builder for rebulk object.
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash]).string_defaults(ignore_case=True)
    rebulk.defaults(name="video_codec", tags=['source-suffix', 'streaming_service.suffix'])

    rebulk.regex(r'Rv\d{2}', value='RealVideo')
    rebulk.regex('Mpeg2', value='MPEG-2')
    rebulk.regex("DVDivX", "DivX", value="DivX")
    rebulk.regex('XviD', value='Xvid')
    rebulk.regex('VC-?1', value='VC-1')
    rebulk.regex('[hx]-?264(?:-?AVC(?:HD)?)?(?:-?SC)?', 'MPEG-?4(?:-?AVC(?:HD)?)', 'AVC(?:HD)?(?:-?SC)?', value='H.264')
    rebulk.regex('[hx]-?265(?:-?HEVC)?', 'HEVC', value='H.265')
    rebulk.regex('(?P<video_codec>hevc)(?P<color_depth>10)', value={'video_codec': 'H.265', 'color_depth': '10-bit'},
                 tags=['video-codec-suffix'], children=True)

    # http://blog.mediacoderhq.com/h264-profiles-and-levels/
    # http://fr.wikipedia.org/wiki/H.264
    rebulk.defaults(name="video_profile", validator=seps_surround)

    rebulk.string('BP', value='Baseline', tags='video_profile.rule')
    rebulk.string('XP', 'EP', value='Extended', tags='video_profile.rule')
    rebulk.string('MP', value='Main', tags='video_profile.rule')
    rebulk.string('HP', 'HiP', value='High', tags='video_profile.rule')
    rebulk.regex('Hi422P', value='High 4:2:2')
    rebulk.regex('Hi444PP', value='High 4:4:4 Predictive')
    rebulk.regex('Hi10P?', value='High 10')  # no profile validation is required

    rebulk.string('DXVA', value='DXVA', name='video_api')

    rebulk.defaults(name='color_depth', validator=seps_surround)
    rebulk.regex('12.?bits?', value='12-bit')
    rebulk.regex('10.?bits?', 'YUV420P10', 'Hi10P?', value='10-bit')
    rebulk.regex('8.?bits?', value='8-bit')

    rebulk.rules(ValidateVideoCodec, VideoProfileRule)

    return rebulk


class ValidateVideoCodec(Rule):
    """
    Validate video_codec with source property or separated
    """
    priority = 64
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []
        for codec in matches.named('video_codec'):
            if not seps_before(codec) and \
                    not matches.at_index(codec.start - 1, lambda match: 'video-codec-prefix' in match.tags):
                ret.append(codec)
                continue
            if not seps_after(codec) and \
                    not matches.at_index(codec.end + 1, lambda match: 'video-codec-suffix' in match.tags):
                ret.append(codec)
                continue
        return ret


class VideoProfileRule(Rule):
    """
    Rule to validate video_profile
    """
    consequence = RemoveMatch

    def when(self, matches, context):
        profile_list = matches.named('video_profile', lambda match: 'video_profile.rule' in match.tags)
        ret = []
        for profile in profile_list:
            codec = matches.previous(profile, lambda match: match.name == 'video_codec')
            if not codec:
                codec = matches.next(profile, lambda match: match.name == 'video_codec')
            if not codec:
                ret.append(profile)
        return ret
