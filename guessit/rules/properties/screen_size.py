#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
screenSize property
"""
from rebulk import Rebulk
import regex as re

from ..common.validators import seps_surround
from guessit.rules.common import dash

SCREEN_SIZE = Rebulk().regex_defaults(flags=re.IGNORECASE)
SCREEN_SIZE.defaults(name="screenSize", validator=seps_surround)

SCREEN_SIZE.regex(r"(?:\d{3,}(?:\\|\/|x|\*))?360(?:i|p?x?)", value="360p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:\\|\/|x|\*))?368(?:i|p?x?)", value="368p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:\\|\/|x|\*))?480(?:i|p?x?)", value="480p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:\\|\/|x|\*))?576(?:i|p?x?)", value="576p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:\\|\/|x|\*))?720(?:i|p?x?)", value="720p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:\\|\/|x|\*))?900(?:i|p?x?)", value="900p")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:\\|\/|x|\*))?1080i", value="1080i")
SCREEN_SIZE.regex(r"(?:\d{3,}(?:\\|\/|x|\*))?1080p?x?", value="1080p")
SCREEN_SIZE.regex(r"(?:\d{3,4}(?:\\|\/|x|\*))?2160(?:i|p?x?)", value="4K")


_digits_re = re.compile(r'\d+')


SCREEN_SIZE.regex(r'\d{3,4}-?[x\*]-?\d{3,4}', abbreviations=[dash],
                  formatter=lambda value: 'x'.join(_digits_re.findall(value)),
                  conflict_solver=lambda match, other: match if other.name == 'screenSize' else other)

# TODO: implement validators from guessit 1
# validator=ChainedValidator(DefaultValidator(), OnlyOneValidator()))
