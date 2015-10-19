#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rebulk configuration for guessit
"""

from rebulk import Rebulk

from .episodes import EPISODES
from .extension import EXTENSION
from .format import FORMAT
from .video_codec import VIDEO_CODEC
from .audio_codec import AUDIO_CODEC
from .screen_size import SCREEN_SIZE
from .website import WEBSITE
from .year import YEAR
from .title import TITLE
from .episode_title import EPISODE_TITLE
from .markers.path import PATH_MARKER
from .markers.groups import GROUPS_MARKER
from .language import LANGUAGE
from .processors import PROCESSORS
from .release_group import RELEASE_GROUP
from .other import OTHER
from .edition import EDITION


REBULK = Rebulk()

REBULK.rebulk(EPISODES)
REBULK.rebulk(EXTENSION)
REBULK.rebulk(FORMAT)
REBULK.rebulk(VIDEO_CODEC)
REBULK.rebulk(AUDIO_CODEC)
REBULK.rebulk(SCREEN_SIZE)
REBULK.rebulk(WEBSITE)
REBULK.rebulk(YEAR)
REBULK.rebulk(TITLE)
REBULK.rebulk(EPISODE_TITLE)
REBULK.rebulk(LANGUAGE)
REBULK.rebulk(RELEASE_GROUP)
REBULK.rebulk(OTHER)
REBULK.rebulk(EDITION)

REBULK.rebulk(PATH_MARKER)
REBULK.rebulk(GROUPS_MARKER)
REBULK.rebulk(PROCESSORS)
