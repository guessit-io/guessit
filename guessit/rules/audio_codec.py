#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
audioCodec and audioProfile property
"""
from rebulk import Rebulk
from rebulk.rules import RemoveMatchRule
import regex as re

from .common import dash
from .common.validators import seps_surround

AUDIO_CODEC = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash]).string_defaults(ignore_case=True)
AUDIO_CODEC.defaults(name="audioCodec", validator=seps_surround)

AUDIO_CODEC.regex("MP3", "LAME", r"LAME(?:\d)+-(?:\d)+", value="MP3")
AUDIO_CODEC.regex("DolbyDigital", "DD", value="DD")
AUDIO_CODEC.regex("AAC", value="AAC")
AUDIO_CODEC.regex("AC3", value="AC3")
AUDIO_CODEC.regex("Flac", value="FLAC")
AUDIO_CODEC.regex("DTS", value="DTS")
AUDIO_CODEC.regex("True-HD", value="True-HD")

AUDIO_CODEC.defaults(name="audioProfile", validator=seps_surround)
AUDIO_CODEC.string("HD", value="HD", tags="DTS")
AUDIO_CODEC.regex("HD-MA", value="HDMA", tags="DTS")
AUDIO_CODEC.string("HE", value="HE", tags="AAC")
AUDIO_CODEC.string("LC", value="LC", tags="AAC")
AUDIO_CODEC.string("HQ", value="HQ", tags="AC3")


class AudioProfileRule(RemoveMatchRule):
    """
    Abstract rule to validate audio profiles
    """
    priority = 255

    def __init__(self, codec):
        super(AudioProfileRule, self).__init__()
        self.codec = codec

    def when(self, matches, context):
        profile_list = matches.named('audioProfile', lambda match: self.codec in match.tags)
        ret = []
        for profile in profile_list:
            audio_codec = matches.previous(profile,
                                           lambda match: match.name == 'audioCodec' and match.value == self.codec)
            if not audio_codec:
                audio_codec = matches.next(profile,
                                           lambda match: match.name == 'audioCodec' and match.value == self.codec)
            if not audio_codec:
                ret.append(profile)
        return ret


class DtsRule(AudioProfileRule):
    """
    Rule to validate DTS profile
    """

    def __init__(self):
        super(DtsRule, self).__init__("DTS")


class AacRule(AudioProfileRule):
    """
    Rule to validate AAC profile
    """

    def __init__(self):
        super(AacRule, self).__init__("AAC")


class Ac3Rule(AudioProfileRule):
    """
    Rule to validate AC3 profile
    """

    def __init__(self):
        super(Ac3Rule, self).__init__("AC3")


AUDIO_CODEC.rules(DtsRule, AacRule, Ac3Rule)
