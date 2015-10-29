#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Season/Episode numbering support
"""

from rebulk import Rebulk, RemoveMatch, Rule

import regex as re
from ..common.validators import seps_surround
from guessit.rules.common import dash
from ..common.numeral import numeral, parse_numeral

EPISODES = Rebulk()
EPISODES.regex_defaults(flags=re.IGNORECASE)

# 01x02, 01x02x03x04
EPISODES.regex(r'(?P<season>\d+)x(?P<episodeNumber>\d+)(?:(?:x|-|&)(?P<episodeNumber>\d+))*',
               # S01E02, S01x02, S01E02E03, S01Ex02, S01xE02, SO1Ex02Ex03
               r'S(?P<season>\d+)(?:xE|Ex|E|x)(?P<episodeNumber>\d+)(?:(?:xE|Ex|E|x|-|&)(?P<episodeNumber>\d+))*',
               # S01
               r'S(?P<season>\d+)(?:(?:S|-|&)(?P<season>\d+))*',
               formatter=int,
               tags=['SxxExx'],
               children=True,
               private_parent=True,
               conflict_solver=lambda match, other: match
               if match.name in ['season', 'episodeNumber']
               and other.name in ['screenSize']
               else '__default__')

# episodeDetails property
for episode_detail in ('Special', 'Bonus', 'Omake', 'Ova', 'Oav', 'Pilot', 'Unaired'):
    EPISODES.string(episode_detail, name='episodeDetails')
EPISODES.regex(r'Extras?', name='episodeDetails', value='Extras')

EPISODES.defaults(validate_all=True, validator={'__parent__': seps_surround}, children=True, private_parent=True)

season_words = ['season', 'saison', 'serie', 'seasons', 'saisons', 'series']
episode_words = ['episode', 'episodes']

EPISODES.regex(r'\L<season_words>-?(?P<season>' + numeral + ')', season_words=season_words,  # Season 1, # Season one
               abbreviations=[dash], formatter=parse_numeral)
EPISODES.regex(r'\L<episode_words>-?(?P<episodeNumber>\d+)', episode_words=episode_words,  # Episode 4
               abbreviations=[dash], formatter=int)

# 12, 13
EPISODES.regex(r'(?P<episodeNumber>\d{2})(?:[x-](<?P<episodeNumber>\d{2}))*',
               tags=['bonus-conflict', 'weak-movie'], formatter=int)

# 012, 013
EPISODES.regex(r'0(?P<episodeNumber>\d{1,2})(?:[x-]0(<?P<episodeNumber>\d{1,2}))*',
               tags=['bonus-conflict', 'weak-movie'], formatter=int)

# 112, 113
EPISODES.regex(r'(?P<episodeNumber>\d{3,4})(?:[x-](<?P<episodeNumber>\d{3,4}))*',
               tags=['bonus-conflict', 'weak-movie'], formatter=int,
               disabled=lambda context: not context.get('episode_prefer_number', False))

# e112, e113
EPISODES.regex(r'e(?P<episodeNumber>\d{1,4})(?:(?:e|x|-)(?P<episodeNumber>\d{1,4}))*',
               formatter=int)

# ep 112, ep113, ep112, ep113
EPISODES.regex(r'ep-?(?P<episodeNumber>\d{1,4})(?:(?:ep|e|x|-)(?P<episodeNumber>\d{1,4}))*',
               abbreviations=[dash],
               formatter=int)

# 102, 0102
EPISODES.regex(r'(?P<season>\d{1,2})(?P<episodeNumber>\d{2})(?:(?:x|-)(?P<episodeNumber>\d{2}))*',
               tags=['bonus-conflict', 'weak-movie'],
               formatter=int,
               conflict_solver=lambda match, other: match if other.name == 'year' else '__default__',
               disabled=lambda context: context.get('episode_prefer_number', False))

EPISODES.defaults()

EPISODES.regex(r'Minisodes?', name='episodeFormat', value="Minisode")

# Harcoded movie to disable weak season/episodes
EPISODES.regex('OSS-?117',
               abbreviations=[dash], name="hardcoded-movies", marker=True,
               conflict_solver=lambda match, other: None)



class RemoveWeakIfMovie(Rule):
    """
    Remove weak-movie tagged matches if it seems to be a movie.
    """
    priority = 550
    consequence = RemoveMatch

    def when(self, matches, context):
        if matches.named('year') or matches.markers.named('hardcoded-movies'):
            return matches.tagged('weak-movie')


class RemoveWeakIfSxxExx(Rule):
    """
    Remove weak-movie tagged matches if SxxExx pattern is matched.
    """
    priority = 550
    consequence = RemoveMatch

    def when(self, matches, context):
        if matches.tagged('SxxExx'):
            return matches.tagged('weak-movie')


class EpisodeDetailValidator(Rule):
    """
    Validate episodeDetails if they are detached or next to season or episodeNumber.
    """
    priority = 2048
    consequence = RemoveMatch

    def when(self, matches, context):
        ret = []
        for detail in matches.named('episodeDetails'):
            if not seps_surround(detail) \
                    and not matches.previous(detail, lambda match: match.name in ['season', 'episodeNumber']) \
                    and not matches.next(detail, lambda match: match.name in ['season', 'episodeNumber']):
                ret.append(detail)
        return ret

EPISODES.rules(RemoveWeakIfMovie, RemoveWeakIfSxxExx, EpisodeDetailValidator)
