#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
video_codec and video_profile property
"""
from __future__ import unicode_literals

from rebulk import Rebulk, Rule, RemoveMatch
import regex as re

from ..common import dash
from ..common.validators import seps_surround

VIDEO_CODEC = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash]).string_defaults(ignore_case=True)
VIDEO_CODEC.defaults(name="video_codec", validator=seps_surround)

VIDEO_CODEC.regex(r"Rv\d{2}", value="Real")
VIDEO_CODEC.regex("Mpeg2", value="Mpeg2")
VIDEO_CODEC.regex("DVDivX", "DivX", value="DivX")
VIDEO_CODEC.regex("XviD", value="XviD")
VIDEO_CODEC.regex("[hx]-?264(?:-?AVC)?", "MPEG-?4(?:-?AVC)", value="h264")
VIDEO_CODEC.regex("[hx]-?265(?:-?HEVC)?", "HEVC", value="h265")

# http://blog.mediacoderhq.com/h264-profiles-and-levels/
# http://fr.wikipedia.org/wiki/H.264
VIDEO_CODEC.defaults(name="video_profile", validator=seps_surround)

VIDEO_CODEC.regex('10.?bit', 'Hi10P', value='10bit')
VIDEO_CODEC.regex('8.?bit', value='8bit')

VIDEO_CODEC.string('BP', value='BP', tags='video_profile.rule')
VIDEO_CODEC.string('XP', 'EP', value='XP', tags='video_profile.rule')
VIDEO_CODEC.string('MP', value='MP', tags='video_profile.rule')
VIDEO_CODEC.string('HP', 'HiP', value='HP', tags='video_profile.rule')
VIDEO_CODEC.regex('Hi422P', value='Hi422P', tags='video_profile.rule')
VIDEO_CODEC.regex('Hi444PP', value='Hi444PP', tags='video_profile.rule')

VIDEO_CODEC.string('DXVA', value='DXVA', name='video_api')


class VideoProfileRule(Rule):
    """
    Rule to validate video_profile
    """
    consequence = RemoveMatch

    def when(self, matches, context):
        profile_list = matches.named('video_profile', lambda match: 'video_profile.rule' in match.tags)
        ret = []
        for profile in profile_list:
            video_codec = matches.previous(profile,
                                           lambda match: match.name == 'video_codec')
            if not video_codec:
                video_codec = matches.next(profile,
                                           lambda match: match.name == 'video_codec')
            if not video_codec:
                ret.append(profile)
        return ret


VIDEO_CODEC.rules(VideoProfileRule)
