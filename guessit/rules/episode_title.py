#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Episode title
"""
from rebulk import Rebulk, AppendMatchRule

from .common.formatters import cleanup


class EpisodeTitleFromPosition(AppendMatchRule):
    """
    Add episode title match in existing matches
    Must run after TitleFromPosition rule.
    """
    priority = 10

    def when(self, matches, context):
        filename = matches.markers.named('path', -1)
        start, end = filename.span

        second_hole = matches.holes(start, end+1, formatter=cleanup, predicate=lambda hole: hole.value, index=1)
        if second_hole:
            episode = matches.previous(second_hole, lambda previous: previous.name in ['episodeNumber', 'season'], 0)
            if episode:
                second_hole.name = 'episodeTitle'
                return second_hole


EPISODE_TITLE = Rebulk().rules(EpisodeTitleFromPosition)
