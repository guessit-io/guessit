#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Season/Episode numbering support
"""

from rebulk import Rebulk

import regex as re

EPISODES = Rebulk()

EPISODES.regex(r'(?P<season>\d+)x(?P<episodeNumber>\d+)',
               r'S(?P<season>\d+)[ex](?P<episodeNumber>\d+)',
               formatter={'season': int, 'episodeNumber': int},
               flags=re.IGNORECASE,
               children=True)
