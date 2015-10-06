#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
audioCodec property
"""
from rebulk import Rebulk

from .common import dash
from .common.validators import seps_surround

import regex as re

AUDIO_CODEC = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])
AUDIO_CODEC.defaults(name="audioCodec", validator=seps_surround)

AUDIO_CODEC.regex("MP3", "LAME", r"LAME(?:\d)+-(?:\d)+", value="MP3")
AUDIO_CODEC.regex("DolbyDigital", "DD", value="DD")
AUDIO_CODEC.regex("AAC", value="AAC")
AUDIO_CODEC.regex("AC3", value="AC3")
AUDIO_CODEC.regex("Flac", value="FLAC")
AUDIO_CODEC.regex("DTS", value="DTS")  # TODO: LeftValidator
AUDIO_CODEC.regex("True-HD", value="True-HD")
