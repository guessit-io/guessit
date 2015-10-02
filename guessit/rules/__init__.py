#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Rebulk configuration for guessit
"""

from rebulk import Rebulk

from .episodes import EPISODES

REBULK = Rebulk()
REBULK.rebulk(EPISODES)

