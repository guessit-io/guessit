#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title
"""
from rebulk import Rebulk, Rule

from .common.formatters import cleanup


class TitleFromPosition(Rule):
    """
    Add title match in existing matches
    """
    priority = 10

    def when(self, matches, context):
        filename = matches.markers.named('path', -1)
        start, end = filename.span

        first_hole = matches.holes(start, end+1, formatter=cleanup, predicate=lambda hole: hole.value, index=0)
        if first_hole:
            group_markers = matches.markers.named('group')
            title = first_hole.crop(group_markers, index=0)

            return title

    def then(self, matches, when_response, context):
        when_response.name = 'title'
        matches.append(when_response)


TITLE = Rebulk().rules(TitleFromPosition)
