#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2011 Nicolas Wack <wackou@gmail.com>
#
# GuessIt is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessIt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from guessit import fileutils, textutils
from guessit.guess import Guess, merge_similar_guesses, merge_all, choose_int, choose_string
from guessit.date import search_date
from guessit.language import search_language
from guessit.patterns import video_exts, subtitle_exts, sep, deleted, episodes_rexps, weak_episodes_rexps, properties, canonical_form
from guessit.textutils import find_first_level_groups, split_on_groups, blank_region, clean_string
from guessit.fileutils import split_path_components
import datetime
import os.path
import re
import copy
import logging

log = logging.getLogger("guessit.matchtree")




def tree_to_string(tree):
    """
    000000 11111 22222222222222222222222222222222222222222222222222222222222222
    000000 00000 00000000000000000000000000000000000000000000000000111111111111
    000000 00000 00000011112222222222222222222222222333345555555556011111111112
    Series/Treme/Treme.____.Right.Place,.Wrong.Time.____._________.____________
    Series/Treme/Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.[tvu.org.ru].avi
    """
    m_tree = [ '', # path level index
               '', # explicit group index
               '', # matched regexp and dash-separated
               '', # groups leftover that couldn't be matched
               '', # meaning conveyed: E = episodenumber, S = season, ...
               ]

    def add_char(pidx, eidx, gidx, remaining, meaning = None):
        nr = len(remaining)
        m_tree[0] = m_tree[0] + str(pidx) * nr
        m_tree[1] = m_tree[1] + str(eidx) * nr
        m_tree[2] = m_tree[2] + str(gidx) * nr
        m_tree[3] = m_tree[3] + remaining
        m_tree[4] = m_tree[4] + str(meaning or ' ') * nr

    def meaning(result):
        mmap = { 'episodeNumber': 'E',
                 'season': 'S',
                 'extension': 'e',
                 'format': 'f',
                 'language': 'l',
                 'videoCodec': 'v',
                 'website': 'w',
                 'container': 'c',
                 'series': 'T',
                 'title': 't'
                 }

        if result is None:
            return ' '

        for prop, l in mmap.items():
            if prop in result:
                return l

        return 'x'

    for pidx, pathpart in enumerate(tree):
        for eidx, explicit_group in enumerate(pathpart):
            for gidx, (group, remaining, result) in enumerate(explicit_group):
                add_char(pidx, eidx, gidx, remaining, meaning(result))

        # special conditions for the path separator
        if pidx < len(tree) - 2:
            add_char(' ', ' ', ' ', '/')
        elif pidx == len(tree) - 2:
            add_char(' ', ' ', ' ', '.')

    return '\n'.join(m_tree)



def iterate_groups(match_tree):
    """Iterate over all the groups in a match_tree and return them as pairs
    of (group_pos, group) where:
     - group_pos = (pidx, eidx, gidx)
     - group = (string, remaining, guess)
    """
    for pidx, pathpart in enumerate(match_tree):
        for eidx, explicit_group in enumerate(pathpart):
            for gidx, group in enumerate(explicit_group):
                yield (pidx, eidx, gidx), group


def find_group(match_tree, prop):
    """Find the list of groups that resulted in a guess that contains the
    asked property."""
    result = []
    for gpos, (string, remaining, guess) in iterate_groups(match_tree):
        if guess and prop in guess:
            result.append(gpos)
    return result

def get_group(match_tree, gpos):
    pidx, eidx, gidx = gpos
    return match_tree[pidx][eidx][gidx]


def leftover_valid_groups(match_tree, valid = lambda s: len(s) > 3):
    """Return the list of valid string groups (eg: len(s) > 3) that could not be
    matched to anything as a list of pairs (cleaned_str, group_pos)."""
    leftover = []
    for gpos, (group, remaining, guess) in iterate_groups(match_tree):
        if not guess:
            clean_str = clean_string(remaining)
            if valid(clean_str):
                leftover.append((clean_str, gpos))

    return leftover


def match_from_epnum_position(match_tree, epnum_pos, guessed):
    """guessed is a callback function to call with the guessed group."""
    pidx, eidx, gidx = epnum_pos

    def update_found(leftover, group_pos, guess):
        pidx, eidx, gidx = group_pos
        group = match_tree[pidx][eidx][gidx]
        match_tree[pidx][eidx][gidx] = (group[0],
                                        deleted * len(group[0]),
                                        guess)
        return [ g for g in leftover if g[1] != group_pos ]

    # a few helper functions to be able to filter using high-level semantics
    def same_pgroup_before(group):
        _, (ppidx, eeidx, ggidx) = group
        return ppidx == pidx and (eeidx, ggidx) < (eidx, gidx)

    def same_pgroup_after(group):
        _, (ppidx, eeidx, ggidx) = group
        return ppidx == pidx and (eeidx, ggidx) > (eidx, gidx)

    def same_egroup_before(group):
        _, (ppidx, eeidx, ggidx) = group
        return ppidx == pidx and eeidx == eidx and ggidx < gidx

    def same_egroup_after(group):
        _, (ppidx, eeidx, ggidx) = group
        return ppidx == pidx and eeidx == eidx and ggidx > gidx

    leftover = leftover_valid_groups(match_tree)

    # if we only have 1 valid group before the episodeNumber, then it's probably the series name
    series_candidates = filter(same_pgroup_before, leftover)
    if len(series_candidates) == 1:
        guess = guessed({ 'series': series_candidates[0][0] }, confidence = 0.7)
        leftover = update_found(leftover, series_candidates[0][1], guess)

    # only 1 group after (in the same explicit group) and it's probably the episode title
    title_candidates = filter(same_egroup_after, leftover)
    if len(title_candidates) == 1:
        guess = guessed({ 'title': title_candidates[0][0] }, confidence = 0.5)
        leftover = update_found(leftover, title_candidates[0][1], guess)

    # epnumber is the first group and there are only 2 after it in same path group
    #  -> season title - episode title
    already_has_title = (find_group(match_tree, 'title') != [])

    title_candidates = filter(same_pgroup_after, leftover)
    if (not already_has_title and                    # no title
        not filter(same_pgroup_before, leftover) and # no groups before
        len(title_candidates) == 2):                 # only 2 groups after

        guess = guessed({ 'series': title_candidates[0][0] }, confidence = 0.4)
        leftover = update_found(leftover, title_candidates[0][1], guess)
        guess = guessed({ 'title': title_candidates[1][0] }, confidence = 0.4)
        leftover = update_found(leftover, title_candidates[1][1], guess)


    # if we only have 1 remaining valid group in the pathpart before the filename,
    # then it's probably the series name
    series_candidates = [ group for group in leftover if group[1][0] == pidx-1 ]
    if len(series_candidates) == 1:
        guess = guessed({ 'series': series_candidates[0][0] }, confidence = 0.7)
        leftover = update_found(leftover, series_candidates[0][1], guess)

    return match_tree



