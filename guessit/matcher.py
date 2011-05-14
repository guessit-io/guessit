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
from guessit.patterns import sep, deleted, episodes_rexps, weak_episodes_rexps, properties, canonical_form
from guessit.textutils import find_first_level_groups, split_on_groups, blank_region
from guessit.fileutils import split_path_components
import datetime
import os.path
import re
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


# TODO: subs

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

    def update_found(string, span, span_adjust = (0,0)):
        span = (span[0] + span_adjust[0],
                span[1] + span_adjust[1])
        regions.append(span)
        return blank_region(string, span)

    # try to find dates first, as they are very specific
    date, span = search_date(current)
    if date:
        guessed({ 'date': date }, confidence = 1.0)
        current = update_found(current, span)

    # specific regexps (ie: season X episode, ...)
    for rexp, confidence, span_adjust in episodes_rexps:
        match = re.search(rexp, current, re.IGNORECASE)
        if match:
            metadata = match.groupdict()
            guessed(metadata, confidence = confidence)
            current = update_found(current, match.span(), span_adjust)

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
            guessed(metadata, confidence = 1.0)
            current = update_found(current, match.span(), span_adjust = (1, -1))


    # common well-defined words
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

                guessed({ prop: canonical_form(value) }, confidence = confidence)
                current = update_found(current, (pos, end))
                clow = current.lower()

    # weak guesses for episode number, only run it if we don't have an estimate already
    if not any('episodeNumber' in match for match in result):
        for rexp, confidence, span_adjust in weak_episodes_rexps:
            match = re.search(rexp, current, re.IGNORECASE)
            if match:
                metadata = match.groupdict()
                guessed(metadata, confidence = confidence)
                current = update_found(current, match.span(), span_adjust)

    # try to find languages now
    language, span, confidence = search_language(current)
    while language:
        # is it a subtitle language?
        if 'sub' in textutils.clean_string(current[:span[0]]).split(' '):
            guessed({ 'subtitleLanguage': language }, confidence = confidence)
        else:
            guessed({ 'language': language }, confidence = confidence)
        current = update_found(current, span)
        #print 'current', current
        language, span, confidence = search_language(current)


    # remove our sentinels now and ajust spans accordingly
    assert(current[0] == ' ' and current[-1] == ' ')
    current = current[1:-1]
    regions = [ (start-1, end-1) for start, end in regions ]

    # split into '-' separated subgroups (with required separator chars
    # around the dash)
    didx = current.find('-')
    while didx > 0:
        regions.append((didx, didx))
        didx = current.find('-', didx+1)

    grps = split_on_groups(current, regions)

    return zip(split_on_groups(string, regions),
               split_on_groups(current, regions))


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
        guessed({ 'extension':  fileext}, confidence = 1.0)

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

        # TODO: some processing steps here such as
        # - if we matched a language in a file with a sub extension and that the group
        #   is the last group of the filename, it is probably the language of the subtitle
        # - try to guess series and episode title with what we have left, such as
        #   - series title would be the group before s01e01
        #   - ep title would be the group just after s01e01
        #   - etc...

        # re-append the extension now
        match_tree.append([[(fileext,deleted*len(fileext))]])

        self.parts = result
        self.match_tree = match_tree

    def print_match_tree(self):
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
                   ]

        def add_char(pidx, eidx, gidx, remaining):
            nr = len(remaining)
            m_tree[0] = m_tree[0] + str(pidx) * nr
            m_tree[1] = m_tree[1] + str(eidx) * nr
            m_tree[2] = m_tree[2] + str(gidx) * nr
            m_tree[3] = m_tree[3] + remaining

        for pidx, pathpart in enumerate(self.match_tree):
            for eidx, explicit_group in enumerate(pathpart):
                for gidx, (group, remaining) in enumerate(explicit_group):
                    add_char(pidx, eidx, gidx, remaining)
            if pidx < len(self.match_tree) - 2:
                add_char(' ', ' ', ' ', '/')
            elif pidx == len(self.match_tree) - 2:
                add_char(' ', ' ', ' ', '.')

        return '\n'.join(m_tree)

    def leftover(self):
        """Return the list of string groups that could not be matched to anything."""
        leftover = []
        for pathpart in self.match_tree:
            for explicit_group in pathpart:
                for group, remaining in explicit_group:
                    leftover.append(remaining)

        leftover = [ textutils.clean_string(l) for l in leftover ]
        leftover = filter(bool, leftover)

        return leftover


    def matched(self):
        parts = self.parts

        # 2- try to merge similar information together and give it a higher confidence
        merge_similar_guesses(parts, 'season', choose_int)
        merge_similar_guesses(parts, 'episodeNumber', choose_int)
        merge_similar_guesses(parts, 'series', choose_string)

        #for p in parts:
        #    print p.to_json()

        result = merge_all(parts)
        #print result, parts
        log.debug('Final result: ' + result.to_json())

        leftover = self.leftover()
        print 'Leftover from guessing: %s' % leftover
        log.debug('Leftover from guessing: %s' % leftover)

        return result
