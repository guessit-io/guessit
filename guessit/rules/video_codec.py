#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
videoCodec and videoProfile property
"""
from rebulk import Rebulk, RemoveMatchRule
import regex as re

from .common import dash
from .common.validators import seps_surround

VIDEO_CODEC = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash]).string_defaults(ignore_case=True)
VIDEO_CODEC.defaults(name="videoCodec", validator=seps_surround)

VIDEO_CODEC.regex(r"Rv\d{2}", value="Real")
VIDEO_CODEC.regex("Mpeg2", value="Mpeg2")
VIDEO_CODEC.regex("DVDivX", "DivX", value="DivX")
VIDEO_CODEC.regex("XviD", value="XviD")
VIDEO_CODEC.regex("[hx]-264(?:-AVC)?", "MPEG-4(?:-AVC)", value="h264")
VIDEO_CODEC.regex("[hx]-265(?:-HEVC)?", "HEVC", value="h265")

# http://blog.mediacoderhq.com/h264-profiles-and-levels/
# http://fr.wikipedia.org/wiki/H.264
VIDEO_CODEC.defaults(name="videoProfile", validator=seps_surround)

VIDEO_CODEC.regex('10.?bit', 'Hi10P', value='10bit')
VIDEO_CODEC.regex('8.?bit', value='8bit')

VIDEO_CODEC.string('BP', value='BP', tags='videoProfile.rule')
VIDEO_CODEC.string('XP', 'EP', value='XP', tags='videoProfile.rule')
VIDEO_CODEC.string('MP', value='MP', tags='videoProfile.rule')
VIDEO_CODEC.string('HP', 'HiP', value='HP', tags='videoProfile.rule')
VIDEO_CODEC.regex('Hi422P', value='Hi422P', tags='videoProfile.rule')
VIDEO_CODEC.regex('Hi444PP', value='Hi444PP', tags='videoProfile.rule')


class VideoProfileRule(RemoveMatchRule):
    """
    Rule to validate videoProfile
    """
    priority = 255

    def when(self, matches, context):
        profile_list = matches.named('videoProfile', lambda match: 'videoProfile.rule' in match.tags)
        ret = []
        for profile in profile_list:
            video_codec = matches.previous(profile,
                                           lambda match: match.name == 'videoCodec')
            if not video_codec:
                video_codec = matches.next(profile,
                                           lambda match: match.name == 'videoCodec')
            if not video_codec:
                ret.append(profile)
        return ret


VIDEO_CODEC.rules(VideoProfileRule)
