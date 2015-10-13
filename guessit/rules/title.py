#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title
"""
from rebulk import Rebulk

from .common.formatters import cleanup


def title_from_position(matches):
    """
    Add title match in existing matches

    :param matches:
    :param context:
    :return:
    """
    filename = matches.markers.named('path', lambda marker: 'last' in marker.tags, 0)
    start, end = filename.span

    first_hole = matches.holes(start, end+1, formatter=cleanup, predicate=lambda hole: hole.value, index=0)
    if first_hole:
        first_hole.name = 'title'
        matches.append(first_hole)


TITLE = Rebulk().post_processor(title_from_position)
