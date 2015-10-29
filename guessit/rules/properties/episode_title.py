#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Episode title
"""
from collections import defaultdict
from guessit.rules.common import seps, title_seps
from rebulk import Rebulk, Rule, AppendMatch, RenameMatch
from rebulk.formatters import formatters

from ..common.formatters import cleanup, reorder_title


class EpisodeTitleFromPosition(Rule):
    """
    Add episode title match in existing matches
    Must run after TitleFromPosition rule.
    """
    priority = 8  # Just after main title
    consequence = AppendMatch

    def when(self, matches, context):
        if matches.named('episodeTitle'):
            return

        filename = matches.markers.named('path', -1)
        start, end = filename.span

        holes = matches.holes(start, end + 1, formatter=formatters(cleanup, reorder_title),
                              predicate=lambda hole: hole.value)

        for hole in holes:
            episode = matches.previous(hole,
                                       lambda previous: previous.name in
                                       ['episodeNumber', 'episodeDetails', 'season', 'date'],
                                       0)
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
    priority = 7  # Just after main title
    consequence = RenameMatch

    def when(self, matches, context):
        if matches.named('episodeTitle'):
            return

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


class TitleToEpisodeTitle(Rule):
    """
    If multiple different title are found, convert the one following episode number to episodeTitle.
    """
    priority = 9  # Just after main title

    def when(self, matches, context):
        titles = matches.named('title')

        if len(titles) < 2:
            return

        title_groups = defaultdict(list)
        for title in titles:
            title_groups[title.value].append(title)

        episode_titles = []
        main_titles = []
        for title in titles:
            if matches.previous(title, lambda match: match.name == 'episodeNumber'):
                episode_titles.append(title)
            else:
                main_titles.append(title)

        if episode_titles:
            return episode_titles

    def then(self, matches, when_response, context):
        for episode_title in when_response:
            matches.remove(episode_title)
            episode_title.name = 'episodeTitle'
            matches.append(episode_title)


class Filepart3EpisodeTitle(Rule):
    """
    If we have at least 3 filepart structured like this:

    Serie name/SO1/E01-episodeTitle.mkv
    AAAAAAAAAA/BBB/CCCCCCCCCCCCCCCCCCCC

    If CCCC contains episodeNumber and BBB contains seasonNumber
    Then title is to be found in AAAA.
    """
    priority = 11  # Before main title rule
    consequence = AppendMatch('title')

    def when(self, matches, context):
        fileparts = matches.markers.named('path')
        if len(fileparts) < 3:
            return

        filename = fileparts[-1]
        directory = fileparts[-2]
        subdirectory = fileparts[-3]

        episode_number = matches.range(filename.start, filename.end, lambda match: match.name == 'episodeNumber', 0)
        if episode_number:
            season = matches.range(directory.start, directory.end, lambda match: match.name == 'season', 0)

            if season:
                hole = matches.holes(subdirectory.start, subdirectory.end,
                                     formatter=cleanup, seps=title_seps, predicate=lambda match: match.value, index=0)
                if hole:
                    return hole


class Filepart2EpisodeTitle(Rule):
    """
    If we have at least 2 filepart structured like this:

    Serie name SO1/E01-episodeTitle.mkv
    AAAAAAAAAAAAA/BBBBBBBBBBBBBBBBBBBBB

    If BBBB contains episodeNumber and AAA contains a hole followed by seasonNumber
    Then title is to be found in AAAA.
    """
    priority = 11  # Before main title rule
    consequence = AppendMatch('title')

    def when(self, matches, context):
        fileparts = matches.markers.named('path')
        if len(fileparts) < 2:
            return

        filename = fileparts[-1]
        directory = fileparts[-2]

        episode_number = matches.range(filename.start, filename.end, lambda match: match.name == 'episodeNumber', 0)
        if episode_number:
            season = matches.range(directory.start, directory.end, lambda match: match.name == 'season', 0)
            if season:
                hole = matches.holes(directory.start, directory.end, formatter=cleanup, seps=title_seps,
                                     predicate=lambda match: match.value, index=0)
                if hole:
                    return hole


EPISODE_TITLE = Rebulk().rules(EpisodeTitleFromPosition,
                               AlternativeTitleReplace,
                               TitleToEpisodeTitle,
                               Filepart3EpisodeTitle,
                               Filepart2EpisodeTitle)
