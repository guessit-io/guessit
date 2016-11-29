#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
size property
"""
from rebulk.remodule import re

from rebulk import Rebulk, Rule, RemoveMatch
from ..common.validators import seps_surround
from ..common import dash


def size():
    """
    Builder for rebulk object.
    :return: Created Rebulk object
    :rtype: Rebulk
    """

    def format_size(value):
        return re.sub(r'(?<=\d)[.](?=[^\d])', '', value.upper())

    rebulk = Rebulk().regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])
    rebulk.defaults(name='size', validator=seps_surround)
    rebulk.regex(r'\d+\.?[mgt]b', r'\d+\.\d+[mgt]b', formatter=format_size, tags=['release-group-prefix'])

    return rebulk
