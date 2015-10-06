#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Validators
"""

from rebulk.validators import chars_before, chars_after, chars_surround

from . import seps

from functools import partial


seps_before = partial(chars_before, seps)
seps_after = partial(chars_after, seps)
seps_surround = partial(chars_surround, seps)
