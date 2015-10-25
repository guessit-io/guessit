#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Season/Episode numbering support
"""

from rebulk import Rebulk, RemoveMatchRule

import regex as re
from ..common.validators import seps_surround
from guessit.rules.common import dash
from ..common.numeral import numeral, parse_numeral

EPISODES = Rebulk().defaults(validate_all=True, validator={'__parent__': seps_surround})
EPISODES.regex_defaults(flags=re.IGNORECASE, children=True)

EPISODES.regex(r'(?P<season>\d+)x(?P<episodeNumber>\d+)',  # 01x02
               r'S(?P<season>\d+)[ex](?P<episodeNumber>\d+)',  # S01E02, S01x02
               r'S(?P<season>\d+)xe(?P<episodeNumber>\d+)',  # S01Ex02
               formatter=int,
               private_parent=True,
               tags=['SxxExx'],
               conflict_solver=lambda match, other: match
               if match.name in ['season', 'episodeNumber']
               and other.name == 'screenSize'
               else '__default__')

season_words = ['season', 'saison', 'serie', 'seasons', 'saisons', 'series']
episode_words = ['episode', 'episodes']

EPISODES.regex(r'\L<season_words>-(?P<season>' + numeral + ')', season_words=season_words,  # Season 1, # Season one
               abbreviations=[dash], formatter=parse_numeral)

season_markers = ['s']
episode_markers = ['e', 'ep']


no_zero_validator = {'__parent__': seps_surround,
                     'season': lambda match: match.value > 0, 'episodeNumber': lambda match: match.value > 0}

EPISODES.regex(r'(?P<episodeNumber>\d{2})', tags=['bonus-conflict', 'weak-movie'], formatter=int)  # 12
EPISODES.regex(r'0(?P<episodeNumber>\d{1,2})', tags=['bonus-conflict', 'weak-movie'], formatter=int)  # 02, 012
EPISODES.regex(r'(?P<episodeNumber>\d{3,4})', tags=['bonus-conflict', 'weak-movie'], formatter=int,  # 112, 113
               validator=no_zero_validator,
               disabled=lambda context: not context.get('episode_prefer_number', False))

EPISODES.regex(r'(?P<season>\d{1})(?P<episodeNumber>\d{2})', tags=['bonus-conflict', 'weak-movie'],  # 102
               formatter=int,
               validator=no_zero_validator,
               disabled=lambda context: context.get('episode_prefer_number', False))
EPISODES.regex(r'(?P<season>\d{2})(?P<episodeNumber>\d{2})', tags=['bonus-conflict', 'weak-movie'],  # 0102
               formatter=int,
               validator=no_zero_validator,
               conflict_solver=lambda match, other: match if other.name == 'year' else '__default__',
               disabled=lambda context: context.get('episode_prefer_number', False))

# Harcoded movie to disable weak season/episodes
EPISODES.regex('OSS-117',
               abbreviations=[dash], name="hardcoded-movies", marker=True,
               conflict_solver=lambda match, other: None, children=False)


class RemoveWeakIfMovie(RemoveMatchRule):
    """
    Remove weak-movie tagged matches if it seems to be a movie.
    """
    priority = 550

    def when(self, matches, context):
        if matches.named('year') or matches.markers.named('hardcoded-movies'):
            return matches.tagged('weak-movie')


class RemoveWeakIfSxxExx(RemoveMatchRule):
    """
    Remove weak-movie tagged matches if SxxExx pattern is matched.
    """
    priority = 550

    def when(self, matches, context):
        if matches.tagged('SxxExx'):
            return matches.tagged('weak-movie')

EPISODES.rules(RemoveWeakIfMovie, RemoveWeakIfSxxExx)

