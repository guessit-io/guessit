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

EPISODES = Rebulk()
EPISODES.regex_defaults(flags=re.IGNORECASE)

EPISODES.regex(r'(?P<season>\d+)x(?P<episodeNumber>\d+)',  # 01x02
               r'S(?P<season>\d+)[ex](?P<episodeNumber>\d+)',  # S01E02, S01x02
               r'S(?P<season>\d+)xe(?P<episodeNumber>\d+)',  # S01Ex02
               r'S(?P<season>\d{1,2})',  # S01
               formatter=int,
               tags=['SxxExx'],
               children=True,
               private_parent=True,
               conflict_solver=lambda match, other: match
               if match.name in ['season', 'episodeNumber']
               and other.name == 'screenSize'
               else '__default__')

# episodeDetails property
for episode_detail in ('Special', 'Bonus', 'Omake', 'Ova', 'Oav', 'Pilot', 'Unaired'):
    EPISODES.string(episode_detail, name='episodeDetails')
EPISODES.regex(r'Extras?', name='episodeDetails', value='Extras')

EPISODES.defaults(validate_all=True, validator={'__parent__': seps_surround}, children=True, private_parent=True)

season_words = ['season', 'saison', 'serie', 'seasons', 'saisons', 'series']
episode_words = ['episode', 'episodes']

EPISODES.regex(r'\L<season_words>-(?P<season>' + numeral + ')', season_words=season_words,  # Season 1, # Season one
               abbreviations=[dash], formatter=parse_numeral)
EPISODES.regex(r'\L<episode_words>-(?P<episodeNumber>\d+)', episode_words=episode_words,  # Episode 4
               abbreviations=[dash], formatter=int)

season_markers = ['s']
episode_markers = ['e', 'ep']


no_zero_validator = {'__parent__': seps_surround,
                     'season': lambda match: match.value > 0, 'episodeNumber': lambda match: match.value > 0}

EPISODES.regex(r'(?P<episodeNumber>\d{2})', tags=['bonus-conflict', 'weak-movie'], formatter=int)  # 12
EPISODES.regex(r'0(?P<episodeNumber>\d{1,2})', tags=['bonus-conflict', 'weak-movie'], formatter=int)  # 02, 012
EPISODES.regex(r'(?P<episodeNumber>\d{3,4})', tags=['bonus-conflict', 'weak-movie'], formatter=int,  # 112, 113
               validator=no_zero_validator,
               disabled=lambda context: not context.get('episode_prefer_number', False))

EPISODES.regex(r'\L<episode_markers>-(?P<episodeNumber>\d{2})',  # ep 12, e 12
               formatter=int, abbreviations=[dash], episode_markers=episode_markers)
EPISODES.regex(r'\L<episode_markers>-0(?P<episodeNumber>\d{1,2})',  # ep 02, ep 012, e 02, e 012
               formatter=int, abbreviations=[dash], episode_markers=episode_markers)
EPISODES.regex(r'\L<episode_markers>-(?P<episodeNumber>\d{3,4})', # ep 112, ep 113, e 112, e 113
               formatter=int, abbreviations=[dash], episode_markers=episode_markers)

EPISODES.regex(r'(?P<season>\d{1})(?P<episodeNumber>\d{2})', tags=['bonus-conflict', 'weak-movie'],  # 102
               formatter=int,
               validator=no_zero_validator,
               disabled=lambda context: context.get('episode_prefer_number', False))
EPISODES.regex(r'(?P<season>\d{2})(?P<episodeNumber>\d{2})', tags=['bonus-conflict', 'weak-movie'],  # 0102
               formatter=int,
               validator=no_zero_validator,
               conflict_solver=lambda match, other: match if other.name == 'year' else '__default__',
               disabled=lambda context: context.get('episode_prefer_number', False))

EPISODES.defaults()

EPISODES.regex(r'Minisodes?', name='episodeFormat', value="Minisode")

# Harcoded movie to disable weak season/episodes
EPISODES.regex('OSS-117',
               abbreviations=[dash], name="hardcoded-movies", marker=True,
               conflict_solver=lambda match, other: None)



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


class EpisodeDetailValidator(RemoveMatchRule):
    """
    Validate rules if they are detached or next to season or episodeNumber.
    """
    priority = 2048

    def when(self, matches, context):
        ret = []
        for detail in matches.named('episodeDetails'):
            if not seps_surround(detail) \
                    and not matches.previous(detail, lambda match: match.name in ['season', 'episodeNumber']) \
                    and not matches.next(detail, lambda match: match.name in ['season', 'episodeNumber']):
                ret.append(detail)
        return ret

EPISODES.rules(RemoveWeakIfMovie, RemoveWeakIfSxxExx, EpisodeDetailValidator)
