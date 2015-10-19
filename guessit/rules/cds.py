#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cd properties
"""
from rebulk import Rebulk
import regex as re

from .common import dash

CDS = Rebulk().regex_defaults(flags=re.IGNORECASE)

CDS.regex('cd' + dash[1] + '(?P<cdNumber>[0-9])(?:' + dash[1] + 'of' + dash[1] + '(?P<cdNumberTotal>[0-9]))?',
          formatter={'cdNumber': int, 'cdNumberTotal': int}, every=True, private_parent=True)
CDS.regex('([1-9])' + dash[1] + 'cds?', name='cdNumberTotal', formatter=int)
