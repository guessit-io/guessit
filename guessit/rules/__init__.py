#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rebulk configuration for guessit
"""

from rebulk import Rebulk

from .episodes import EPISODES
from .format import FORMAT
from .video_codec import VIDEO_CODEC
from .audio_codec import AUDIO_CODEC
from .screen_size import SCREEN_SIZE
from .website import WEBSITE
from .year import YEAR

REBULK = Rebulk()

REBULK.rebulk(EPISODES)
REBULK.rebulk(FORMAT)
REBULK.rebulk(VIDEO_CODEC)
REBULK.rebulk(AUDIO_CODEC)
REBULK.rebulk(SCREEN_SIZE)
REBULK.rebulk(WEBSITE)
REBULK.rebulk(YEAR)
