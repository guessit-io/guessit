#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
audio_codec and audio_profile property
"""
from __future__ import unicode_literals

from rebulk import Rebulk, Rule, RemoveMatch
import regex as re

from ..common import dash
from ..common.validators import seps_before, seps_after

AUDIO_CODEC = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash]).string_defaults(ignore_case=True)
AUDIO_CODEC.defaults(name="audio_codec")

AUDIO_CODEC.regex("MP3", "LAME", r"LAME(?:\d)+-?(?:\d)+", value="MP3")
AUDIO_CODEC.regex("DolbyDigital", "DD", value="DolbyDigital")
AUDIO_CODEC.regex("AAC", value="AAC")
AUDIO_CODEC.regex("AC3", value="AC3")
AUDIO_CODEC.regex("Flac", value="FLAC")
AUDIO_CODEC.regex("DTS", value="DTS")
AUDIO_CODEC.regex("True-?HD", value="True-HD")

AUDIO_CODEC.defaults(name="audio_profile")
AUDIO_CODEC.string("HD", value="HD", tags="DTS")
AUDIO_CODEC.regex("HD-?MA", value="HDMA", tags="DTS")
AUDIO_CODEC.string("HE", value="HE", tags="AAC")
AUDIO_CODEC.string("LC", value="LC", tags="AAC")
AUDIO_CODEC.string("HQ", value="HQ", tags="AC3")

AUDIO_CODEC.defaults(name="audio_channels")
AUDIO_CODEC.regex(r'(7[\W_]1)(?:[^\d]|$)', value='7.1', children=True)
AUDIO_CODEC.regex(r'(5[\W_]1)(?:[^\d]|$)', value='5.1', children=True)
AUDIO_CODEC.regex(r'(2[\W_]0)(?:[^\d]|$)', value='2.0', children=True)
AUDIO_CODEC.string('7ch', '8ch', value='7.1')
AUDIO_CODEC.string('5ch', '6ch', value='5.1')
AUDIO_CODEC.string('2ch', 'stereo', value='2.0')
AUDIO_CODEC.string('1ch', 'mono', value='1.0')

audio_properties = ['audio_codec', 'audio_profile', 'audio_channels']


class AudioValidatorRule(Rule):
    """
    Remove audio properties if not surrounded by separators and not next each others
    """
    priority = 64
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []

        audio_list = matches.range(predicate=lambda match: match.name in audio_properties)
        for audio in audio_list:
            if not seps_before(audio):
                valid_before = matches.range(audio.start-1, audio.start, lambda match: match.name in audio_properties)
                if not valid_before:
                    ret.append(audio)
                    continue
            if not seps_after(audio):
                valid_after = matches.range(audio.end, audio.end+1,
                                            lambda match: match.name in audio_properties)
                if not valid_after:
                    ret.append(audio)
                    continue

        return ret


class AudioProfileRule(Rule):
    """
    Abstract rule to validate audio profiles
    """
    priority = 64
    dependency = AudioValidatorRule
    consequence = RemoveMatch

    def __init__(self, codec):
        super(AudioProfileRule, self).__init__()
        self.codec = codec

    def when(self, matches, context):
        profile_list = matches.named('audio_profile', lambda match: self.codec in match.tags)
        ret = []
        for profile in profile_list:
            audio_codec = matches.previous(profile,
                                           lambda match: match.name == 'audio_codec' and match.value == self.codec)
            if not audio_codec:
                audio_codec = matches.next(profile,
                                           lambda match: match.name == 'audio_codec' and match.value == self.codec)
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


AUDIO_CODEC.rules(DtsRule, AacRule, Ac3Rule, AudioValidatorRule)


class HqConflictRule(Rule):
    """
    Solve conflict between HQ from other property and from audio_profile.
    """

    dependency = [DtsRule, AacRule, Ac3Rule]
    consequence = RemoveMatch

    def when(self, matches, context):
        hq_audio = matches.named('audio_profile', lambda match: match.value == 'HQ')
        hq_audio_spans = [match.span for match in hq_audio]
        hq_other = matches.named('other', lambda match: match.span in hq_audio_spans)

        if hq_other:
            return hq_other

AUDIO_CODEC.rules(HqConflictRule)
