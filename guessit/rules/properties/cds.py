#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cd properties
"""
from __future__ import unicode_literals

from rebulk import Rebulk
import regex as re

from ..common import dash

CDS = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])

CDS.regex(r'cd-?(?P<cd>\d+)(?:-?of-?(?P<cd_count>\d+))?',
          validator={'cd': lambda match: match.value > 0, 'cd_count': lambda match: match.value > 0},
          formatter={'cd': int, 'cd_count': int},
          children=True,
          private_parent=True)
CDS.regex(r'(?P<cd_count>\d+)-?cds?',
          validator={'cd': lambda match: match.value > 0, 'cd_count': lambda match: match.value > 0},
          formatter={'cd_count': int},
          children=True,
          private_parent=True)
