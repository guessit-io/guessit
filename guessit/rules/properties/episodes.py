#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Season/Episode numbering support
"""

from rebulk import Rebulk

import regex as re

EPISODES = Rebulk().regex_defaults(flags=re.IGNORECASE)

EPISODES.regex(r'(?P<season>\d+)x(?P<episodeNumber>\d+)',
               r'S(?P<season>\d+)[ex](?P<episodeNumber>\d+)',
               formatter=int,
               children=True,
               private_parent=True,
               conflict_solver=lambda match, other: match
               if match.name in ['season', 'episodeNumber']
               and other.name == 'screenSize'
               else '__default__')
