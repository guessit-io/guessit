#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
videoCodec property
"""
from rebulk import Rebulk

from .common import dash
from .common.validators import seps_surround

import regex as re

VIDEO_CODEC = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])
VIDEO_CODEC.defaults(name="videoCodec", validator=seps_surround)

VIDEO_CODEC.regex(r"Rv\d{2}", value="Real")
VIDEO_CODEC.regex("Mpeg2", value="Mpeg2")
VIDEO_CODEC.regex("DVDivX", "DivX", value="DivX")
VIDEO_CODEC.regex("XviD", value="XviD")
VIDEO_CODEC.regex("[hx]-264(?:-AVC)?", "MPEG-4(?:-AVC)", value="h264")
VIDEO_CODEC.regex("[hx]-265(?:-HEVC)?", "HEVC", value="h265")
