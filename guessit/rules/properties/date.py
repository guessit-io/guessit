#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Date and year
"""
from rebulk import Rebulk

from ..common.date import search_date, valid_year
from ..common.validators import seps_surround

DATE = Rebulk()

DATE = Rebulk()
DATE.defaults(validator=seps_surround)

DATE.regex(r"\d{4}", name="year", formatter=int,
           validator=lambda match: seps_surround(match) and valid_year(match.value))


def date(string, context):
    """
    Search for date in the string and retrieves match

    :param string:
    :return:
    """

    ret = search_date(string, context.get('date_year_first'), context.get('date_day_first'))
    if ret:
        return ret[0], ret[1], {'value': ret[2]}


DATE.functional(date, name="date")
