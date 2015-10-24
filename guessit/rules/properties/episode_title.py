#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Episode title
"""
from rebulk import Rebulk, AppendMatchRule

from ..common.formatters import cleanup, reorder_title, chain


class EpisodeTitleFromPosition(AppendMatchRule):
    """
    Add episode title match in existing matches
    Must run after TitleFromPosition rule.
    """
    priority = 9  # Just after main title

    def when(self, matches, context):
        filename = matches.markers.named('path', -1)
        start, end = filename.span

        holes = matches.holes(start, end + 1, formatter=chain(cleanup, reorder_title),
                              predicate=lambda hole: hole.value)

        for hole in holes:
            episode = matches.previous(hole,
                                       lambda previous: previous.name in ['episodeNumber', 'season', 'date'], 0)
            if episode:
                group_markers = matches.markers.named('group')
                title = hole.crop(group_markers, index=0)

                if title and title.value:
                    title.name = 'episodeTitle'
                    return title


EPISODE_TITLE = Rebulk().rules(EpisodeTitleFromPosition)
