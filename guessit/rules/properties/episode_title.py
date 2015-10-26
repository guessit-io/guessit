#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Episode title
"""
from guessit.rules.common import seps
from rebulk import Rebulk, AppendMatchRule, Rule
from rebulk.formatters import formatters

from ..common.formatters import cleanup, reorder_title


class EpisodeTitleFromPosition(AppendMatchRule):
    """
    Add episode title match in existing matches
    Must run after TitleFromPosition rule.
    """
    priority = 9  # Just after main title

    def when(self, matches, context):
        filename = matches.markers.named('path', -1)
        start, end = filename.span

        holes = matches.holes(start, end + 1, formatter=formatters(cleanup, reorder_title),
                              predicate=lambda hole: hole.value)

        for hole in holes:
            episode = matches.previous(hole,
                                       lambda previous: previous.name in ['episodeNumber', 'season', 'date'], 0)
            if episode:
                group_markers = matches.markers.named('group')
                title = hole.crop(group_markers, index=0)

                if title and title.value:
                    title.name = 'episodeTitle'
                    title.tags = ['title']
                    return title


class AlternativeTitleReplace(Rule):
    """
    If alternateTitle was found and title is next to episodeNumber, season or date, replace it with episodeTitle.
    """
    priority = 9  # Just after main title

    def when(self, matches, context):
        alternative_title = matches.range(predicate=lambda match: match.name == 'alternativeTitle', index=0)
        if alternative_title:
            main_title = matches.chain_before(alternative_title.start, seps=seps,
                                              predicate=lambda match: 'title' in match.tags, index=0)
            if main_title:
                episode = matches.previous(main_title,
                                           lambda previous: previous.name in ['episodeNumber', 'season', 'date'], 0)
                if episode:
                    return alternative_title

    def then(self, matches, when_response, context):
        matches.remove(when_response)
        when_response.name = 'episodeTitle'
        matches.append(when_response)


EPISODE_TITLE = Rebulk().rules(EpisodeTitleFromPosition, AlternativeTitleReplace)
