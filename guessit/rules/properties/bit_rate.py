#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
video_bit_rate and audio_bit_rate properties
"""
import re

from rebulk import Rebulk
from rebulk.rules import Rule, RenameMatch

from ..common import dash, seps
from ..common.quantity import BitRate
from ..common.validators import seps_surround


def bit_rate():
    """
    Builder for rebulk object.
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])
    rebulk.defaults(name='audio_bit_rate', validator=seps_surround)
    rebulk.regex(r'\d+-?[kmg]bps', r'\d+\.\d+-?[kmg]bps',
                 conflict_solver=(
                     lambda match, other: match
                     if other.name == 'audio_channels' and 'weak-audio_channels' not in other.tags
                     else other
                 ),
                 formatter=BitRate.fromstring, tags=['release-group-prefix'])

    rebulk.rules(BitRateTypeRule)

    return rebulk


class BitRateTypeRule(Rule):
    """
    Convert audio bit rate guess into video bit rate.
    """
    consequence = RenameMatch('video_bit_rate')

    def when(self, matches, context):
        for match in matches.named('audio_bit_rate'):
            previous = matches.previous(match, index=0,
                                        predicate=lambda m: m.name in ('source', 'screen_size', 'video_codec'))
            if previous and not matches.holes(previous.end, match.start, predicate=lambda m: m.value.strip(seps)):
                yield match
