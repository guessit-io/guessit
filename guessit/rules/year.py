#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
year property
"""
from rebulk import Rebulk

from .common.validators import seps_surround

YEAR = Rebulk()
YEAR.defaults(name="year", validator=seps_surround)


def validate_year(match):
    """
    Check if match is a valid year

    :param match:
    :type match:
    :return:
    :rtype:
    """
    return 1920 <= match.value < 2030


YEAR.regex(r"\d{4}", formatter=int, validator=validate_year)
