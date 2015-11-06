#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Season/Episode numbering support
"""
from __future__ import unicode_literals

from collections import defaultdict
import copy

from rebulk import Rebulk, RemoveMatch, Rule, AppendMatch, RenameMatch

import regex as re
from ..common.validators import seps_surround
from ..common import dash, alt_dash
from ..common.numeral import numeral, parse_numeral

EPISODES = Rebulk()
EPISODES.regex_defaults(flags=re.IGNORECASE).string_defaults(ignore_case=True)

# 01x02, 01x02x03x04
EPISODES.regex(r'(?P<season>\d+)x(?P<episodeNumber>\d+)' +
               r'(?:(?P<episodeNumberSeparator>x|-|\+|&)(?P<episodeNumber>\d+))*',
               # S01E02, S01x02, S01E02E03, S01Ex02, S01xE02, SO1Ex02Ex03
               r'S(?P<season>\d+)(?:xE|Ex|E|x)(?P<episodeNumber>\d+)' +
               r'(?:(?P<episodeNumberSeparator>xE|Ex|E|x|-|\+|&)(?P<episodeNumber>\d+))*',
               # S01
               r'S(?P<season>\d+)' +
               r'(?:(?P<seasonSeparator>S|-|\+|&)(?P<season>\d+))*',
               formatter={'season': int, 'episodeNumber': int},
               tags=['SxxExx'],
               children=True,
               private_parent=True,
               conflict_solver=lambda match, other: match
               if match.name in ['season', 'episodeNumber'] and other.name in ['screenSize']
               else '__default__')

# episodeDetails property
for episode_detail in ('Special', 'Bonus', 'Omake', 'Ova', 'Oav', 'Pilot', 'Unaired'):
    EPISODES.string(episode_detail, value=episode_detail, name='episodeDetails')
EPISODES.regex(r'Extras?', name='episodeDetails', value='Extras')

EPISODES.defaults(validate_all=True, validator={'__parent__': seps_surround}, children=True, private_parent=True)

season_words = ['season', 'saison', 'serie', 'seasons', 'saisons', 'series']
episode_words = ['episode', 'episodes', 'ep']
of_words = ['of', 'sur']
all_words = ['All']

EPISODES.regex(r'\L<season_words>@?(?P<season>' + numeral + ')' +
               r'(?:@?\L<of_words>@?(?P<count>' + numeral + '))?' +
               r'(?:@?(?P<seasonSeparator>-)@?(?P<season>\d+))*' +
               r'(?:@?(?P<seasonSeparator>\+|&)@?(?P<season>\d+))*',
               of_words=of_words,
               season_words=season_words,  # Season 1, # Season one
               abbreviations=[alt_dash], formatter={'season': parse_numeral, 'count': parse_numeral})

EPISODES.regex(r'\L<episode_words>-?(?P<episodeNumber>\d+)' +
               r'(?:v(?P<version>\d+))?' +
               r'(?:-?\L<of_words>?-?(?P<count>\d+))?',
               of_words=of_words,
               episode_words=episode_words,  # Episode 4
               abbreviations=[dash], formatter=int)

EPISODES.regex(r'S?(?P<season>\d+)-?(?:xE|Ex|E|x)-?(?P<other>\L<all_words>)',
               tags=['SxxExx'],
               all_words=all_words,
               abbreviations=[dash],
               validator=None,
               formatter={'season': int, 'other': lambda match: 'Complete'})

EPISODES.defaults(validate_all=True, validator={'__parent__': seps_surround}, children=True, private_parent=True)

# 12, 13
EPISODES.regex(r'(?P<episodeNumber>\d{2})' +
               r'(?:v(?P<version>\d+))?' +
               r'(?:(?P<episodeNumberSeparator>[x-])(?P<episodeNumber>\d{2}))*',
               tags=['bonus-conflict', 'weak-movie'], formatter={'episodeNumber': int, 'version': int})

# 012, 013
EPISODES.regex(r'0(?P<episodeNumber>\d{1,2})' +
               r'(?:v(?P<version>\d+))?' +
               r'(?:(?P<episodeNumberSeparator>[x-])0(?P<episodeNumber>\d{1,2}))*',
               tags=['bonus-conflict', 'weak-movie'], formatter={'episodeNumber': int, 'version': int})

# 112, 113
EPISODES.regex(r'(?P<episodeNumber>\d{3,4})' +
               r'(?:v(?P<version>\d+))?' +
               r'(?:(?P<episodeNumberSeparator>[x-])(?P<episodeNumber>\d{3,4}))*',
               tags=['bonus-conflict', 'weak-movie'], formatter={'episodeNumber': int, 'version': int},
               disabled=lambda context: not context.get('episode_prefer_number', False))

# 1, 2, 3
EPISODES.regex(r'(?P<episodeNumber>\d)' +
               r'(?:v(?P<version>\d+))?' +
               r'(?:(?P<episodeNumberSeparator>[x-])(?P<episodeNumber>\d{1,2}))*',
               tags=['bonus-conflict', 'weak-movie'], formatter={'episodeNumber': int, 'version': int},
               disabled=lambda context: not context.get('episode_prefer_number', False))

# e112, e113
EPISODES.regex(r'e(?P<episodeNumber>\d{1,4})' +
               r'(?:v(?P<version>\d+))?' +
               r'(?:(?P<episodeNumberSeparator>e|x|-)(?P<episodeNumber>\d{1,4}))*',
               formatter={'episodeNumber': int, 'version': int})

# ep 112, ep113, ep112, ep113
EPISODES.regex(r'ep-?(?P<episodeNumber>\d{1,4})' +
               r'(?:v(?P<version>\d+))?' +
               r'(?:(?P<episodeNumberSeparator>ep|e|x|-)(?P<episodeNumber>\d{1,4}))*',
               abbreviations=[dash],
               formatter={'episodeNumber': int, 'version': int})

# 102, 0102
EPISODES.regex(r'(?P<season>\d{1,2})(?P<episodeNumber>\d{2})' +
               r'(?:v(?P<version>\d+))?' +
               r'(?:(?P<episodeNumberSeparator>x|-)(?P<episodeNumber>\d{2}))*',
               tags=['bonus-conflict', 'weak-movie', 'weak-duplicate'],
               formatter={'season': int, 'episodeNumber': int, 'version': int},
               conflict_solver=lambda match, other: match if other.name == 'year' else '__default__',
               disabled=lambda context: context.get('episode_prefer_number', False))

EPISODES.regex(r'v(?P<version>\d+)', children=True, private_parent=True, formatter=int)

EPISODES.defaults()

# detached of X count (season/episode)
EPISODES.regex(r'(?P<episodeNumber>\d+)?-?\L<of_words>-?(?P<count>\d+)-?\L<episode_words>?', of_words=of_words,
               episode_words=episode_words, abbreviations=[dash], children=True, private_parent=True, formatter=int)

EPISODES.regex(r'Minisodes?', name='episodeFormat', value="Minisode")

# Harcoded movie to disable weak season/episodes
EPISODES.regex('OSS-?117',
               abbreviations=[dash], name="hardcoded-movies", marker=True,
               conflict_solver=lambda match, other: None)


class CountValidator(Rule):
    """
    Validate count property and rename it
    """
    priority = 64
    consequence = [RemoveMatch, RenameMatch('episodeCount'), RenameMatch('seasonCount')]

    def when(self, matches, context):
        to_remove = []
        episode_count = []
        season_count = []

        for count in matches.named('count'):
            previous = matches.previous(count, lambda match: match.name in ['episodeNumber', 'season'], 0)
            if previous:
                if previous.name == 'episodeNumber':
                    episode_count.append(count)
                elif previous.name == 'season':
                    season_count.append(count)
            else:
                to_remove.append(count)
        return to_remove, episode_count, season_count


class EpisodeNumberSeparatorRange(Rule):
    """
    Remove separator matches and create matches for episoderNumber range.
    """
    priority = 128
    consequence = [RemoveMatch, AppendMatch]

    def when(self, matches, context):
        to_remove = []
        to_append = []
        for separator in matches.named('episodeNumberSeparator'):
            previous_match = matches.previous(separator, lambda match: match.name == 'episodeNumber', 0)
            next_match = matches.next(separator, lambda match: match.name == 'episodeNumber', 0)

            if previous_match and next_match and separator.value == '-':
                for episode_number in range(previous_match.value+1, next_match.value):
                    match = copy.copy(separator)
                    match.name = 'episodeNumber'
                    match.value = episode_number
                    to_append.append(match)
            to_remove.append(separator)
        return to_remove, to_append


class SeasonSeparatorRange(Rule):
    """
    Remove separator matches and create matches for season range.
    """
    priority = 128
    consequence = [RemoveMatch, AppendMatch]

    def when(self, matches, context):
        to_remove = []
        to_append = []
        for separator in matches.named('seasonSeparator'):
            previous_match = matches.previous(separator, lambda match: match.name == 'season', 0)
            next_match = matches.next(separator, lambda match: match.name == 'season', 0)

            if separator.value == '-':
                for episode_number in range(previous_match.value+1, next_match.value):
                    match = copy.copy(separator)
                    match.name = 'season'
                    match.value = episode_number
                    to_append.append(match)
            to_remove.append(separator)
        return to_remove, to_append

EPISODES.rules(EpisodeNumberSeparatorRange, SeasonSeparatorRange)


class RemoveWeakIfMovie(Rule):
    """
    Remove weak-movie tagged matches if it seems to be a movie.
    """
    priority = 64
    consequence = RemoveMatch

    def when(self, matches, context):
        if matches.named('year') or matches.markers.named('hardcoded-movies'):
            return matches.tagged('weak-movie')


class RemoveWeakIfSxxExx(Rule):
    """
    Remove weak-movie tagged matches if SxxExx pattern is matched.
    """
    priority = 64
    consequence = RemoveMatch

    def when(self, matches, context):
        if matches.tagged('SxxExx', lambda match: not match.private):
            return matches.tagged('weak-movie')


class RemoveWeakDuplicate(Rule):
    """
    Remove weak-duplicate tagged matches if duplicate patterns, for example The 100.109
    """
    priority = 64
    consequence = RemoveMatch

    def when(self, matches, context):
        to_remove = []
        for filepart in matches.markers.named('path'):
            patterns = defaultdict(list)
            for match in reversed(matches.range(filepart.start, filepart.end,
                                                predicate=lambda match: 'weak-duplicate' in match.tags)):
                if match.pattern in patterns[match.name]:
                    to_remove.append(match)
                else:
                    patterns[match.name].append(match.pattern)
        return to_remove


class EpisodeDetailValidator(Rule):
    """
    Validate episodeDetails if they are detached or next to season or episodeNumber.
    """
    priority = 64
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []
        for detail in matches.named('episodeDetails'):
            if not seps_surround(detail) \
                    and not matches.previous(detail, lambda match: match.name in ['season', 'episodeNumber']) \
                    and not matches.next(detail, lambda match: match.name in ['season', 'episodeNumber']):
                ret.append(detail)
        return ret


class RemoveDetachedEpisodeNumber(Rule):
    """
    If multiple episodeNumber are found, remove those that are not detached from a range and less than 10.

    Fairy Tail 2 - 16-20, 2 should be removed.
    """
    priority = 64
    consequence = RemoveMatch
    dependency = [RemoveWeakIfSxxExx, RemoveWeakDuplicate]

    def when(self, matches, context):
        ret = []

        episode_numbers = []
        episode_values = set()
        for match in matches.named('episodeNumber', lambda match: not match.private and 'weak-movie' in match.tags):
            if match.value not in episode_values:
                episode_numbers.append(match)
                episode_values.add(match.value)

        episode_numbers = list(sorted(episode_numbers, key=lambda match: match.value))
        if len(episode_numbers) > 1 and \
                        episode_numbers[0].value < 10 and \
                        episode_numbers[1].value - episode_numbers[0].value != 1:
            parent = episode_numbers[0]
            while parent:  # TODO: Add a feature in rebulk to avoid this ...
                ret.append(parent)
                parent = parent.parent
        return ret


class VersionValidator(Rule):
    """
    Validate version if previous match is episodeNumber or if surrounded by separators.
    """
    priority = 64
    dependency = [RemoveWeakIfMovie, RemoveWeakIfSxxExx]
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []
        for version in matches.named('version'):
            episode_number = matches.previous(version, lambda match: match.name == 'episodeNumber', 0)
            if not episode_number and not seps_surround(version.initiator):
                ret.append(version)
        return ret

EPISODES.rules(RemoveWeakIfMovie, RemoveWeakIfSxxExx, RemoveWeakDuplicate, EpisodeDetailValidator,
               RemoveDetachedEpisodeNumber, VersionValidator, CountValidator)
