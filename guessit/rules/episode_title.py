#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Episode title
"""
from rebulk import Rebulk, Rule

from .common.formatters import cleanup


class EpisodeTitleFromPosition(Rule):
    """
    Add episode title match in existing matches
    Must run after TitleFromPosition rule.
    """
    def when(self, matches, context):
        filename = matches.markers.named('path', -1)
        start, end = filename.span

        second_hole = matches.holes(start, end+1, formatter=cleanup, predicate=lambda hole: hole.value, index=1)
        return second_hole

    def then(self, matches, when_response, context):
        when_response.name = 'episodeTitle'
        matches.append(when_response)


EPISODE_TITLE = Rebulk().rules(EpisodeTitleFromPosition)
