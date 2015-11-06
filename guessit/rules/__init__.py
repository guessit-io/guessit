#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rebulk configuration for guessit
"""
from __future__ import unicode_literals

from rebulk import Rebulk

from .markers.path import PATH_MARKER
from .markers.groups import GROUPS_MARKER

from .properties.episodes import EPISODES
from .properties.container import CONTAINER
from .properties.format import FORMAT
from .properties.video_codec import VIDEO_CODEC
from .properties.audio_codec import AUDIO_CODEC
from .properties.screen_size import SCREEN_SIZE
from .properties.website import WEBSITE
from .properties.date import DATE
from .properties.title import TITLE
from .properties.episode_title import EPISODE_TITLE
from .properties.language import LANGUAGE
from .properties.country import COUNTRY
from .properties.release_group import RELEASE_GROUP
from .properties.other import OTHER
from .properties.edition import EDITION
from .properties.cds import CDS
from .properties.bonus import BONUS
from .properties.film import FILM
from .properties.part import PART
from .properties.crc import CRC

from .processors import PROCESSORS

REBULK = Rebulk()

REBULK.rebulk(PATH_MARKER)
REBULK.rebulk(GROUPS_MARKER)

REBULK.rebulk(EPISODES)
REBULK.rebulk(CONTAINER)
REBULK.rebulk(FORMAT)
REBULK.rebulk(VIDEO_CODEC)
REBULK.rebulk(AUDIO_CODEC)
REBULK.rebulk(SCREEN_SIZE)
REBULK.rebulk(WEBSITE)
REBULK.rebulk(DATE)
REBULK.rebulk(TITLE)
REBULK.rebulk(EPISODE_TITLE)
REBULK.rebulk(LANGUAGE)
REBULK.rebulk(COUNTRY)
REBULK.rebulk(RELEASE_GROUP)
REBULK.rebulk(OTHER)
REBULK.rebulk(EDITION)
REBULK.rebulk(CDS)
REBULK.rebulk(BONUS)
REBULK.rebulk(FILM)
REBULK.rebulk(PART)
REBULK.rebulk(CRC)

REBULK.rebulk(PROCESSORS)
