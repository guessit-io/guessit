#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Part support
"""
import regex as re
from rebulk import Rebulk

from ..common import dash
from ..common.numeral import numeral, parse_numeral

PART = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])

prefixes = ['pt', 'part']

PART.regex(r'\L<prefixes>-(' + numeral + r')(?:$|[^\d])', prefixes=prefixes,
           name='part', private_parent=True, children=True, formatter=parse_numeral)
