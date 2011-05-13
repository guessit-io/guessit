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
import datetime
import os.path
import re
import logging

log = logging.getLogger("guessit.matcher")



def split_path_components(filename):
    """Returns the filename split into [ dir*, basename, ext ]."""
    result = fileutils.split_path(filename)
    basename = result.pop(-1)
    return result + list(os.path.splitext(basename))


def find_first_level_groups_span(string, enclosing):
    """Return a list of pairs (start, end) for the groups delimited by the given
    enclosing characters.
    This does not return nested groups, ie: '(ab(c)(d))' will return a single group
    containing the whole string.

    >>> find_first_level_group_span('abcd', '()')
    []

    >>> find_first_level_group_span('abc(de)fgh', '()')
    [(3, 6)]

    >>> find_first_level_group_span('(ab(c)(d))', '()')
    [(0, 9)]

    >>> find_first_level_group_span('ab[c]de[f]gh(i)', '[]')
    [(2, 4), (7, 9)]
    """
    opening, closing = enclosing
    depth = [] # depth is a stack of indices where we opened a group
    result = []
    for i, c, in enumerate(string):
        if c == opening:
            depth.append(i)
        elif c == closing:
            try:
                start = depth.pop()
                end = i
                if not depth:
                    # we emptied our stack, so we have a 1st level group
                    result.append((start, end))
            except IndexError:
                # we closed a group which was not opened before
                pass

    return result


def split_on_groups(string, groups, exclude_splitter = False):
    if not groups:
        return [ string ]

    boundaries = reduce(lambda l, x: l + list(x), groups, [])
    if boundaries[0] != 0:
        boundaries.insert(0, -1)
    if boundaries[-1] != len(string)-1:
        boundaries.append(len(string))

    offset = 1 if exclude_splitter else 0
    groups = [ string[start+offset:end] for start, end in zip(boundaries[:-1], boundaries[1:]) ]

    return filter(bool, groups) # return only non-empty groups


def find_first_level_groups(string, enclosing):
    """Return a list of groups that could be split because of explicit grouping.
    The groups are delimited by the given enclosing characters.

    This does not return nested groups, ie: '(ab(c)(d))' will return a single group
    containing the whole string.

    >>> find_first_level_group('', '()')
    ['']

    >>> find_first_level_group('abcd', '()')
    ['abcd']

    >>> find_first_level_group('abc(de)fgh', '()')
    ['abc', 'de', 'fgh']

    >>> find_first_level_group('(ab(c)(d))', '()')
    ['ab(c)(d)']

    >>> find_first_level_group('ab[c]de[f]gh(i)', '[]')
    ['ab', 'c', 'de', 'f', 'gh(i)']

    >>> find_first_level_group('()[]()', '()')
    ['', '[]', '']

    """
    groups = find_first_level_groups_span(string, enclosing)

    return split_on_groups(string, groups, exclude_splitter = True)


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




sep = r'[][)( \._-]' # regexp art, hehe :D

# format: [ (regexp, confidence, span_adjust) ]
episodes_rexps = [ # ... Season 2 ...
                   (r'season (?P<season>[0-9]+)', 1.0, (0, 0)),
                   (r'saison (?P<season>[0-9]+)', 1.0, (0, 0)),

                   # ... s02e13 ...
                   (r'[Ss](?P<season>[0-9]{1,2}).{,3}[EeXx](?P<episodeNumber>[0-9]{1,2})[^0-9]', 1.0, (0, -1)),

                   # ... 2x13 ...
                   (r'[^0-9](?P<season>[0-9]{1,2})[x\.](?P<episodeNumber>[0-9]{2})[^0-9]', 0.8, (1, -1)),

                   # ... s02 ...
                   (sep + r's(?P<season>[0-9]{1,2})' + sep, 0.6, (0, 0)),

                   # v2 or v3 for some mangas which have multiples rips
                   (sep + r'(?P<episodeNumber>[0-9]{1,3})v[23]' + sep, 0.6, (0, 0)),
                   ]

weak_episodes_rexps = [ # ... 213 ...
                        (sep + r'(?P<episodeNumber>[0-9]{1,3})' + sep, 0.3, (1, -1)),
                        ]





properties = { 'format': [ 'DVDRip', 'HD-DVD', 'HDDVD', 'HDDVDRip', 'BluRay', 'BDRip',
                           'R5', 'HDRip', 'DVD', 'Rip', 'HDTV', 'DVB' ],

               'container': [ 'avi', 'mkv', 'ogv', 'wmv', 'mp4', 'mov' ],

               'screenSize': [ '720p' ],

               'videoCodec': [ 'XviD', 'DivX', 'x264', 'Rv10' ],

               'audioCodec': [ 'AC3', 'DTS', 'He-AAC', 'AAC-He', 'AAC' ],

               'releaseGroup': [ 'ESiR', 'WAF', 'SEPTiC', '[XCT]', 'iNT', 'PUKKA',
                                 'CHD', 'ViTE', 'DiAMOND', 'TLF', 'DEiTY', 'FLAiTE',
                                 'MDX', 'GM4F', 'DVL', 'SVD', 'iLUMiNADOS', ' FiNaLe',
                                 'UnSeeN', 'aXXo', 'KLAXXON', 'NoTV' ],

               'website': [ 'tvu.org.ru', 'emule-island.com' ],

               'other': [ '5ch', 'PROPER', 'REPACK', 'LIMITED', 'DualAudio', 'iNTERNAL', 'Audiofixed',
                          'complete', 'classic', # not so sure about these ones, could appear in a title
                          'ws', # widescreen
                          'SE', # special edition
                          # TODO: director's cut
                          ],
               }

property_synonyms = { 'DVD': [ 'DVDRip' ],
                      'HD-DVD': [ 'HDDVD', 'HDDVDRip' ],
                      'BluRay': [ 'BDRip' ],
                      'DivX': [ 'DVDivX' ]
                      }


reverse_synonyms = {}
for canonical, synonyms in property_synonyms.items():
    for synonym in synonyms:
        reverse_synonyms[synonym.lower()] = canonical

def canonical_form(string):
    return reverse_synonyms.get(string.lower(), string)

# TODO: language, subs

def blank_region(string, region):
    deleted = '_'
    return string[:region[0]] + deleted * (region[1]-region[0]) + string[region[1]:]


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

        guessed({ 'extension': match_tree.pop(-1)[1:] }, confidence = 1.0)

        print match_tree

        # 2- split each of those into explicit groups, if any
        #   be careful, as this might split some regexps with more confidence such as Alfleni-Team, or [XCT]
        #     or split a date such as (14-01-2008)
        match_tree = [ split_explicit_groups(part) for part in match_tree ]

        # 3- try to match information in decreasing order of confidence and
        #    blank the matching group in the string if we found something
        for pathpart in match_tree:
            for gidx, explicit_group in enumerate(pathpart):
                # add sentinels so we can match a separator char at either end of
                # our groups, even when they are at the beginning or end of the string
                # we will adjust the span accordingly later
                current = ' ' + explicit_group + ' '

                regions = [] # list of (start, end) of matched regions

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
                    print 'current', current

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
                        print 'GOULOU RELEASE GROUP', current
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
                    print 'current', current
                    language, span, confidence = search_language(current)



                # remove our sentinels now
                assert(current[0] == ' ' and current[-1] == ' ')
                current = current[1:-1]
                regions = [ (start-1, end-1) for start, end in regions ]

                print 'remaining = "%s"' % current.encode('utf8')
                pathpart[gidx] = (explicit_group, current, regions)

        self.parts = result
        self.match_tree = match_tree

        self.matched()


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
        leftover = []
        for pathpart in self.match_tree:
            for group, remaining, regions in pathpart:
                leftover.append(split_on_groups(remaining, regions))

        print leftover
        leftover = [ textutils.clean_string(t) for l in leftover for s in l for t in s.split('-') ]
        leftover = filter(bool, leftover)

        log.debug('Leftover from guessing: %s' % leftover)

        return result
