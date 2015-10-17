#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Release group
"""
from rebulk import Rebulk, Rule

from .common.formatters import strip


class SceneReleaseGroup(Rule):
    """
    Add title match in existing matches
    """
    priority = 5

    def when(self, matches, context):
        filename = matches.markers.named('path', -1)
        start, end = filename.span

        first_hole = matches.holes(start, end+1, formatter=strip, predicate=lambda hole: hole.value, index=-1)
        return first_hole

    def then(self, matches, when_response, context):
        when_response.name = 'releaseGroup'
        matches.append(when_response)


RELEASE_GROUP = Rebulk().rules(SceneReleaseGroup)
