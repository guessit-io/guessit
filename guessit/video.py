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

from guessit.guess import Guess, merge_append_guesses, merge_all
from guessit import language, fileutils, textutils
import os.path
import re
import logging

log = logging.getLogger('guessit.video')



def format_video_guess(guess):
    """Formats all the found values to their natural type.
    For instance, a year would be stored as an int value, ...
    Note that this modifies the dictionary given as input."""
    for prop in [ 'year' ]:
        try:
            guess[prop] = int(guess[prop])
        except KeyError:
            pass

    for prop in [ 'language', 'subtitleLanguage' ]:
        try:
            guess[prop] = language._language_map[guess[prop].lower()]
        except KeyError:
            pass

    return guess


def valid_year(year):
    try:
        import datetime
        maxyear = datetime.datetime.now().year+5
        return int(year) > 1920 and int(year) < maxyear
    except ValueError:
        return False




def guess_video_filename_parts(filename):
    filename = os.path.basename(filename)
    result = []

    def guessed(match, confidence = None):
        result.append(format_video_guess(Guess(match, confidence = confidence)))


    # DVDRip.Xvid-$(grpname)
    grpnames = [ '\.Xvid-(?P<releaseGroup>.*?)\.',
                 '\.DivX-(?P<releaseGroup>.*?)\.',
                 '\.DVDivX-(?P<releaseGroup>.*?)\.',
                 ]
    editions = [ '(?P<edition>(special|unrated|criterion).edition)',
                 '(?P<edition>director\\\\?\'s.cut)',
                 '(?P<edition>edition.collector)'
                 ]
    audio = [ '(?P<audioChannels>5\.1)' ]

    specific = grpnames + editions + audio

    matches, smin = textutils.matchAllRegexpMinIndex(filename, specific)
    for match in textutils.matchAllRegexp(filename, specific):
        if 'edition' in match:
            match['edition'] = textutils.cleanString(match['edition'])

        log.debug('Found with confidence 1.0: %s' % match)
        guessed(match, confidence = 1.0)
        for key, value in match.items():
            filename = filename.replace(value, '')


    # remove punctuation for looser matching now
    seps = [ ' ', '-', '.', '_' ]
    for sep in seps:
        filename = filename.replace(sep, ' ')

    # TODO: replace this with a getMetadataGroups function that splits on parentheses/braces/brackets
    remove = [ '[', ']', '(', ')', '{', '}' ]
    for rem in remove:
        filename = filename.replace(rem, ' ')

    name = filename.split(' ')


    properties = { 'format': [ 'DVDRip', 'HDDVD', 'HDDVDRip', 'BDRip', 'R5', 'HDRip', 'DVD', 'Rip', 'HDTV' ],
                   'container': [ 'avi', 'mkv', 'ogv', 'wmv', 'mp4', 'mov' ],
                   'screenSize': [ '720p' ],
                   'videoCodec': [ 'XviD', 'DivX', 'x264', 'Rv10' ],
                   'audioCodec': [ 'AC3', 'DTS', 'He-AAC', 'AAC-He', 'AAC' ],
                   'language': [ 'vo', 'vf' ] + [ lang for langs in language._reverse_language_map.values() for lang in langs ],
                   'releaseGroup': [ 'ESiR', 'WAF', 'SEPTiC', '[XCT]', 'iNT', 'PUKKA', 'CHD', 'ViTE', 'DiAMOND', 'TLF',
                                     'DEiTY', 'FLAiTE', 'MDX', 'GM4F', 'DVL', 'SVD', 'iLUMiNADOS', ' FiNaLe', 'UnSeeN',
                                     'aXXo', 'KLAXXON' ],
                   'other': [ '5ch', 'PROPER', 'REPACK', 'LIMITED', 'DualAudio', 'iNTERNAL', 'Audiofixed',
                              'classic', # not so sure about this one, could appear in a title
                              'ws', # widescreen
                              'SE', # special edition
                              # TODO: director's cut
                              ],
                   }

    # ensure they're all lowercase
    for prop, value in properties.items():
        properties[prop] = [ s.lower() for s in value ]


    # to try to guess what part of the filename is the movie title, we only keep as
    # possible title the first characters of the filename up to the leftmost metadata
    # element we found, no more
    minIdx = len(name)

    # get specific properties
    for prop, value in properties.items():
        for part in name:
            if part.lower() in value:
                log.debug('Found with confidence 1.0: %s' % { prop: part })
                guessed({ prop: part }, confidence = 1.0)
                minIdx = min(minIdx, name.index(part))


    # get year
    for part in name:
        year = textutils.stripBrackets(part)
        if valid_year(year):
            year = int(year)
            log.debug('Found with confidence 0.9: %s' % { 'year': year })
            guessed({ 'year': year }, confidence = 0.9)
            minIdx = min(minIdx, name.index(part))

    # remove ripper name
    # FIXME: fails with movies such as "down by law", etc...
    for by, who in zip(name[:-1], name[1:]):
        if by.lower() == 'by':
            log.debug('Found with confidence 0.4: %s' % { 'ripper': who })
            guessed({ 'ripper': who }, confidence = 0.4)
            minIdx = min(minIdx, name.index(by))

    # subtitles
    # TODO: only finds the first one, need to check whether there are many of them
    for sub, lang in zip(name[:-1], name[1:]):
        if sub.lower() == 'sub':
            log.debug('Found with confidence 0.7: %s' % { 'subtitleLanguage': lang })
            guessed({ 'subtitleLanguage': lang }, confidence = 0.7)
            minIdx = min(minIdx, name.index(sub))

    # get CD number (if any)
    cdrexp = re.compile('[Cc][Dd]([0-9]+)')
    for part in name:
        try:
            cdnumber = int(cdrexp.search(part).groups()[0])
            log.debug('Found with confidence 1.0: %s' % { 'cdNumber': cdnumber })
            guessed({ 'cdNumber': cdnumber }, confidence = 1.0)
            minIdx = min(minIdx, name.index(part))
        except AttributeError:
            pass

    name = ' '.join(name[:minIdx])
    minIdx = len(name)

    # TODO: generic website url guesser
    websites = [ 'sharethefiles.com', 'tvu.org.ru' ]
    websites = [ '(?P<website>%s)' % w.replace('.', ' ') for w in websites ] # dots have been previously converted to spaces
    # TODO: maybe we can add more patterns here?
    rexps = websites

    matched = textutils.matchAllRegexp(name, rexps)
    for match in matched:
        log.debug('Found with confidence 1.0: %s' % match)
        guessed(match, confidence = 1.0)
        for key, value in match.items():
            minIdx = min(minIdx, name.find(value))


    minIdx = min(minIdx, smin)

    return result, minIdx


def guess_video_filename(filename):
    """Return the guessed information about the video file, as well the idx in
    the filename string starting with which we found something."""
    parts, idx = guess_video_filename_parts(filename)

    merge_append_guesses(parts, 'language')
    merge_append_guesses(parts, 'subtitleLanguage')

    return merge_all(parts), idx
