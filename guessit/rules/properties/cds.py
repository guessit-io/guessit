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

CDS.regex(r'cd-?(?P<cdNumber>\d+)(?:-?of-?(?P<cdNumberTotal>\d+))?',
          validator={'cdNumber': lambda match: match.value > 0, 'cdNumberTotal': lambda match: match.value > 0},
          formatter={'cdNumber': int, 'cdNumberTotal': int},
          children=True,
          private_parent=True)
CDS.regex(r'(?P<cdNumberTotal>\d+)-?cds?',
          validator={'cdNumber': lambda match: match.value > 0, 'cdNumberTotal': lambda match: match.value > 0},
          formatter={'cdNumberTotal': int},
          children=True,
          private_parent=True)
