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

log = logging.getLogger("guessit.matcher")



def split_explicit_groups(string):
    """return the string split into explicit groups, that is, those either
    between parenthese, square brackets or curly braces, and those separated
    by a dash."""
    result = find_first_level_groups(string, '()')
    result = reduce(lambda l, x: l + find_first_level_groups(x, '[]'), result, [])
    result = reduce(lambda l, x: l + find_first_level_groups(x, '{}'), result, [])
    # do not do this at this moment, it is not strong enough and can break other
    # patterns, such as dates, etc...
    #result = reduce(lambda l, x: l + x.split('-'), result, [])

    return result


def format_episode_guess(guess):
    """Format all the found values to their natural type.
    For instance, a year would be stored as an int value, etc...

    Note that this modifies the dictionary given as input.
    """

    for prop in [ 'season', 'episodeNumber', 'year' ]:
        try:
            guess[prop] = int(guess[prop])
        except KeyError:
            pass

    return guess

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

# TODO: subs

def find_group(tree, prop):
    """Find the list of groups that resulted in a guess that contains the
    asked property."""
    result = []
    for pidx, pathpart in enumerate(tree):
        for eidx, explicit_group in enumerate(pathpart):
            for gidx, (group, remaining, guess) in enumerate(explicit_group):
                if guess and prop in guess:
                    result.append((pidx, eidx, gidx))
    return result

def guess_groups(string, result):
    # add sentinels so we can match a separator char at either end of
    # our groups, even when they are at the beginning or end of the string
    # we will adjust the span accordingly later
    current = ' ' + string + ' '

    regions = [] # list of (start, end) of matched regions

    def guessed(match_dict, confidence):
        guess = format_episode_guess(Guess(match_dict, confidence = confidence))
        result.append(guess)
        log.debug('Found with confidence %.2f: %s' % (confidence, guess))
        return guess

    def update_found(string, guess, span, span_adjust = (0,0)):
        span = (span[0] + span_adjust[0],
                span[1] + span_adjust[1])
        regions.append((span, guess))
        return blank_region(string, span)

    # try to find dates first, as they are very specific
    date, span = search_date(current)
    if date:
        guess = guessed({ 'date': date }, confidence = 1.0)
        current = update_found(current, guess, span)

    # specific regexps (ie: season X episode, ...)
    for rexp, confidence, span_adjust in episodes_rexps:
        match = re.search(rexp, current, re.IGNORECASE)
        if match:
            metadata = match.groupdict()
            guess = guessed(metadata, confidence = confidence)
            current = update_found(current, guess, match.span(), span_adjust)

    # release groups have certain constraints, cannot be included in the previous general regexps
    group_names = [ sep + r'(Xvid)-(?P<releaseGroup>.*?)[ \.]',
                    sep + r'(DivX)-(?P<releaseGroup>.*?)[ \.]',
                    sep + r'(DVDivX)-(?P<releaseGroup>.*?)[ \.]',
                    ]
    for rexp in group_names:
        match = re.search(rexp, current, re.IGNORECASE)
        if match:
            metadata = match.groupdict()
            metadata.update({ 'videoCodec': canonical_form(match.group(1)) })
            guess = guessed(metadata, confidence = 1.0)
            current = update_found(current, guess, match.span(), span_adjust = (1, -1))


    # common well-defined words and regexps
    clow = current.lower()
    confidence = 1.0 # for all of them
    for prop, values in properties.items():
        for value in values:
            pos = clow.find(value.lower())
            if pos != -1:
                end = pos + len(value)
                # make sure our word is always surrounded by separators
                if clow[pos-1] not in sep or clow[end] not in sep:
                    # note: sep is a regexp, but in this case using it as
                    #       a sequence achieves the same goal
                    continue

                guess = guessed({ prop: canonical_form(value) }, confidence = confidence)
                current = update_found(current, guess, (pos, end))
                clow = current.lower()

    # weak guesses for episode number, only run it if we don't have an estimate already
    if not any('episodeNumber' in match for match in result):
        for rexp, _, span_adjust in weak_episodes_rexps:
            match = re.search(rexp, current, re.IGNORECASE)
            if match:
                metadata = match.groupdict()
                epnum = int(metadata['episodeNumber'])
                if epnum > 100:
                    guess = guessed({ 'season': epnum // 100,
                                      'episodeNumber': epnum % 100 }, confidence = 0.6)
                else:
                    guess = guessed(metadata, confidence = 0.3)
                current = update_found(current, guess, match.span(), span_adjust)

    # try to find languages now
    language, span, confidence = search_language(current)
    while language:
        # is it a subtitle language?
        if 'sub' in clean_string(current[:span[0]]).split(' '):
            guess = guessed({ 'subtitleLanguage': language }, confidence = confidence)
        else:
            guess = guessed({ 'language': language }, confidence = confidence)
        current = update_found(current, guess, span)
        #print 'current', current
        language, span, confidence = search_language(current)


    # remove our sentinels now and ajust spans accordingly
    assert(current[0] == ' ' and current[-1] == ' ')
    current = current[1:-1]
    regions = [ ((start-1, end-1), guess) for (start, end), guess in regions ]

    # split into '-' separated subgroups (with required separator chars
    # around the dash)
    didx = current.find('-')
    while didx > 0:
        regions.append(((didx, didx), None))
        didx = current.find('-', didx+1)

    # cut our final groups, and rematch the guesses to the group that created
    # id, None if it is a leftover group
    region_spans = [ span for span, guess in regions ]
    string_groups = split_on_groups(string, region_spans)
    remaining_groups = split_on_groups(current, region_spans)
    guesses = []

    pos = 0
    for group in string_groups:
        found = False
        for span, guess in regions:
            if span[0] == pos:
                guesses.append(guess)
                found = True
        if not found:
            guesses.append(None)

        pos += len(group)

    return  zip(string_groups,
                remaining_groups,
                guesses)

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



class IterativeMatcher(object):
    def __init__(self, filename):
        if not isinstance(filename, unicode):
            log.debug('WARNING: given filename to matcher is not unicode...')

        match_tree = []
        result = [] # list of found metadata

        def guessed(match_dict, confidence):
            guess = format_episode_guess(Guess(match_dict, confidence = confidence))
            result.append(guess)
            log.debug('Found with confidence %.2f: %s' % (confidence, guess))
            return guess

        # 1- first split our path into dirs + basename + ext
        match_tree = split_path_components(filename)

        fileext = match_tree.pop(-1)[1:].lower()
        if fileext in subtitle_exts:
            extguess = guessed({ 'type': 'subtitle',
                                 'container': fileext }, confidence = 1.0)
        elif fileext in video_exts:
            extguess = guessed({ 'container': fileext }, confidence = 1.0)
        else:
            extguess = guessed({ 'extension':  fileext}, confidence = 1.0)

        # TODO: depending on the extension, we could already grab some info and maybe specialized
        #       guessers, eg: a lang parser for idx files, an automatic detection of the language
        #       for srt files, a video metadata extractor for avi, mkv, ...

        # 2- split each of those into explicit groups, if any
        #   be careful, as this might split some regexps with more confidence such as Alfleni-Team, or [XCT]
        #     or split a date such as (14-01-2008)
        match_tree = [ split_explicit_groups(part) for part in match_tree ]

        # 3- try to match information in decreasing order of confidence and
        #    blank the matching group in the string if we found something
        for pathpart in match_tree:
            for gidx, explicit_group in enumerate(pathpart):
                pathpart[gidx] = guess_groups(explicit_group, result)

        # 4- try to identify the remaining unknown groups by looking at their position
        #    relative to other known elements

        eps = find_group(match_tree, 'episodeNumber')
        #print tree_to_string(match_tree).encode('utf-8')
        #print filename.encode('utf-8')
        #print 'Found groups', eps
        if eps:
            pidx, eidx, gidx = eps[0]

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


        # TODO: some processing steps here such as
        # - if we matched a language in a file with a sub extension and that the group
        #   is the last group of the filename, it is probably the language of the subtitle

        # re-append the extension now
        #print '*'*100
        #print 'extguess', extguess
        match_tree.append([[(fileext, deleted*len(fileext), extguess)]])

        self.parts = result
        self.match_tree = match_tree
        print self.print_match_tree().encode('utf-8')
        print filename.encode('utf-8')

    def print_match_tree(self):
        """TODO: rename me"""
        return tree_to_string(self.match_tree)


    def matched(self):
        # we need to make a copy here, as the merge functions work in place and
        # calling them on the match tree would modify it
        parts = copy.deepcopy(self.parts)

        # 2- try to merge similar information together and give it a higher confidence
        merge_similar_guesses(parts, 'season', choose_int)
        merge_similar_guesses(parts, 'episodeNumber', choose_int)
        merge_similar_guesses(parts, 'series', choose_string)

        #for p in parts:
        #    print p.to_json()

        result = merge_all(parts, append = ['language', 'subtitleLanguage'])
        #print result, parts
        log.debug('Final result: ' + result.to_json())

        return result
