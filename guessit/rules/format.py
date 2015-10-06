#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
format property
"""
from rebulk import Rebulk

from .common import dash

import regex as re
from .common.validators import seps_surround

FORMAT = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])
FORMAT.defaults(name="format", validator=seps_surround)

FORMAT.regex("VHS", "VHS-Rip", value="VHS")
FORMAT.regex("CAM", "CAM-Rip", "HD-CAM", value="Cam")
FORMAT.regex("TELESYNC", "TS", "HD-TS", value="Telesync")
FORMAT.regex("WORKPRINT", "WP", value="Workprint")
FORMAT.regex("TELECINE", "TC", value="Telecine")
FORMAT.regex("PPV", "PPV-Rip", value="PPV")  # Pay Per View
FORMAT.regex("SD-TV", "SD-TV-Rip", "Rip-SD-TV", "TV-Rip", "Rip-TV", value="TV")  # TV is too common to allow matching
FORMAT.regex("DVB-Rip", "DVB", "PD-TV", value="DVB")
FORMAT.regex("DVD", "DVD-Rip", "VIDEO-TS", "DVD-R", "DVD-9", "DVD-5", value="DVD")
FORMAT.regex("HD-TV", "TV-RIP-HD", "HD-TV-RIP", "HD-RIP", value="HDTV")
FORMAT.regex("VOD", "VOD-Rip", value="VOD")
FORMAT.regex("WEB-Rip", value="WEBRip")
FORMAT.regex("WEB-DL", "WEB-HD", "WEB", value="WEB-DL")
FORMAT.regex("HD-DVD-Rip", "HD-DVD", value="HD-DVD")
FORMAT.regex("Blu-ray(?:-Rip)?", "B[DR]", "B[DR]-Rip", "BD[59]", "BD25", "BD50", value="BluRay")
