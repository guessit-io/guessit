#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
format property
"""
from __future__ import unicode_literals

from rebulk import Rebulk, RemoveMatch, Rule
import regex as re

from ..common import dash
from ..common.validators import seps_before, seps_after

FORMAT = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])
FORMAT.defaults(name="format")

FORMAT.regex("VHS", "VHS-?Rip", value="VHS")
FORMAT.regex("CAM", "CAM-?Rip", "HD-?CAM", value="Cam")
FORMAT.regex("TELESYNC", "TS", "HD-?TS", value="Telesync")
FORMAT.regex("WORKPRINT", "WP", value="Workprint")
FORMAT.regex("TELECINE", "TC", value="Telecine")
FORMAT.regex("PPV", "PPV-?Rip", value="PPV")  # Pay Per View
FORMAT.regex("SD-?TV", "SD-?TV-?Rip", "Rip-?SD-?TV", "TV-?Rip",
             "Rip-?TV", value="TV")  # TV is too common to allow matching
FORMAT.regex("DVB-?Rip", "DVB", "PD-?TV", value="DVB")
FORMAT.regex("DVD", "DVD-?Rip", "VIDEO-?TS", "DVD-?R(?:$|(?!E))",  # "DVD-?R(?:$|^E)" => DVD-Real ...
             "DVD-?9", "DVD-?5", value="DVD")

FORMAT.regex("HD-?TV", "TV-?RIP-?HD", "HD-?TV-?RIP", "HD-?RIP", value="HDTV")
FORMAT.regex("VOD", "VOD-?Rip", value="VOD")
FORMAT.regex("WEB-?Rip", value="WEBRip")
FORMAT.regex("WEB-?DL", "WEB-?HD", "WEB", value="WEB-DL")
FORMAT.regex("HD-?DVD-?Rip", "HD-?DVD", value="HD-DVD")
FORMAT.regex("Blu-?ray(?:-?Rip)?", "B[DR]", "B[DR]-?Rip", "BD[59]", "BD25", "BD50", value="BluRay")


class ValidateFormat(Rule):
    """
    Validate format with screener property or separated.
    """
    priority = 64
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []
        for format_match in matches.named('format'):
            if not seps_before(format_match) and \
                    not matches.range(format_match.start - 1, format_match.start - 2,
                                      lambda match: match.name == 'other' and match.value == 'Screener'):
                ret.append(format_match)
                continue
            if not seps_after(format_match) and \
                    not matches.range(format_match.end, format_match.end + 1,
                                      lambda match: match.name == 'other' and match.value == 'Screener'):
                ret.append(format_match)
                continue
        return ret


FORMAT.rules(ValidateFormat)
