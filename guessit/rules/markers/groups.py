#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Groups markers (...), [...] and {...}
"""
from __future__ import unicode_literals

from rebulk import Rebulk

GROUPS_MARKER = Rebulk()
GROUPS_MARKER.defaults(name="group", marker=True)

starting = '([{'
ending = ')]}'


def mark_groups(input_string):
    """
    Functional pattern to mark groups (...), [...] and {...}.

    :param input_string:
    :return:
    """
    openings = ([], [], [])
    i = 0

    ret = []
    for char in input_string:
        start_type = starting.find(char)
        if start_type > -1:
            openings[start_type].append(i)

        i += 1

        end_type = ending.find(char)
        if end_type > -1:
            start_index = openings[end_type].pop()
            ret.append((start_index, i))
    return ret


GROUPS_MARKER.functional(mark_groups)
