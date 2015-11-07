#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
edition property
"""
from __future__ import unicode_literals

from rebulk import Rebulk
import regex as re

from ..common import dash
from ..common.validators import seps_surround

EDITION = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash]).string_defaults(ignore_case=True)
EDITION.defaults(name='edition', validator=seps_surround)

EDITION.regex('collector', 'collector-edition', 'edition-collector', value='Collector Edition')
EDITION.regex('special-edition', 'edition-special', value='Special Edition',
              conflict_solver=lambda match, other: other
              if other.name == 'episode_details' and other.value == 'Special'
              else '__default__')
EDITION.regex('criterion-edition', 'edition-criterion', value='Criterion Edition')
EDITION.regex('deluxe', 'deluxe-edition', 'edition-deluxe', value='Deluxe Edition')
EDITION.regex('director\'?s?-cut', 'director\'?s?-cut-edition', 'edition-director\'?s?-cut', value='Director\'s cut')
