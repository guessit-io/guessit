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

from guessit.guess import Guess, merge_similar_guesses, merge_all
from guessit import fileutils, textutils
import re
import logging

log = logging.getLogger('guessit.movie')


def valid_year(year):
    try:
        return int(year) > 1920 and int(year) < 2015
    except ValueError:
        return False


def guess_XCT(filename):
    result = Guess()

    if not '[XCT]' in filename:
        return filename, result

    filename = filename.replace('[XCT]', '')

    try:
        # find metadata
        mdstr = textutils.matchRegexp(filename, '\[(?P<mdstr>.*?)\]')['mdstr']
        filename = filename.replace(mdstr, '')

        # find subs
        subs = textutils.matchRegexp(mdstr, 'St[{\(](?P<subs>.*?)[}\)]')['subs']
        log.debug('Found XCT subs with confidence 1.0: %s' % subs.split('-'))
        mdstr.replace(subs, '')
        result.set('subtitleLanguage', subs.split('-'), confidence = 1.0)

        # find audio
        audio = textutils.matchRegexp(mdstr, 'aac[0-9\.-]*[{\(](?P<audio>.*?)[}\)]')['audio']
        log.debug('Found XCT audio with confidence 1.0: %s' % audio.split('-'))
        mdstr.replace(audio, '')
        result.set('language', audio.split('-'), confidence = 1.0)

        # find year: if we found it, then the english title of the movie is either what's inside
        # the parentheses before the year, or everything before the year
        title = filename
        log.debug('Found XCT title with confidence 0.6: %s' % title)
        result.set('title', title, confidence = 0.6)

        years = [ m['year'] for m in textutils.multipleMatchRegexp(filename, '(?P<year>[0-9]{4})') if valid_year(m['year']) ]
        if len(years) == 1:
            title = filename[:filename.index(years[0])]
            log.debug('Found XCT title with confidence 0.8: %s' % title)
            result.set('title', title, confidence = 0.8)
        elif len(years) >= 2:
            log.warning('Ambiguous filename: possible years are ' + ', '.join(years))

        try:
            title = textutils.matchRegexp(title, '\((?P<title>.*?)\)')['title']
            log.debug('Found XCT title with confidence 0.9: %s' % title)
            result.set('title', title, confidence = 0.9)
        except:
            pass

        result['title'] = title

    finally:
        return filename, result


'''
def VideoFilename(filename):
    parts = textutils.cleanString(filename).split()

    found = {} # dictionary of identified named properties to their index in the parts list

    # heuristic 1: find VO, sub FR, etc...
    for i, part in enumerate(parts):
        if matchRegexp(part, [ 'VO', 'VF' ]):
            found = { ('audio', 'VO'): i }

    # heuristic 2: match video size
    #rexp('...x...') with x > 200  # eg: (720, 480) -> property format = 16/9, etc...

    # we consider the name to be what's left at the beginning, before any other identified part
    # (other possibility: look at the remaining zones in parts which are not covered by any identified props, look for the first one, or the biggest one)
    name = ' '.join(parts[:min(found.values())])
'''

def guess_movie_filename(filename):
    import os.path
    filename = os.path.basename(filename)
    result = Guess()

    # TODO: fix those cases

    # first apply specific methods which are very strict but have a very high confidence
    filename, result = guess_XCT(filename)

    # DVDRip.Xvid-$(grpname)
    grpnames = [ '\.Xvid-(?P<releaseGroup>.*?)\.',
                 '\.DivX-(?P<releaseGroup>.*?)\.'
                 ]
    editions = [ '(?P<edition>(special|unrated|criterion).edition)'
                 ]
    audio = [ '(?P<audioChannels>5\.1)' ]

    specific = grpnames + editions + audio
    for match in textutils.matchAllRegexp(filename, specific):
        log.debug('Found with confidence 1.0: %s' % match)
        result.update(match, confidence = 1.0)
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


    properties = { 'format': [ 'DVDRip', 'HDDVD', 'HDDVDRip', 'BDRip', 'R5', 'HDRip', 'DVD', 'Rip' ],
                   'container': [ 'avi', 'mkv', 'ogv', 'wmv', 'mp4', 'mov' ],
                   'screenSize': [ '720p' ],
                   'videoCodec': [ 'XviD', 'DivX', 'x264', 'Rv10' ],
                   'audioCodec': [ 'AC3', 'DTS', 'He-AAC', 'AAC-He', 'AAC' ],
                   'language': [ 'english', 'eng',
                                 'spanish', 'esp',
                                 'french', 'fr',
                                 'italian', # no 'it', too common a word in english
                                 'vo', 'vf'
                                 ],
                   'releaseGroup': [ 'ESiR', 'WAF', 'SEPTiC', '[XCT]', 'iNT', 'PUKKA', 'CHD', 'ViTE', 'DiAMOND', 'TLF',
                                     'DEiTY', 'FLAiTE', 'MDX', 'GM4F', 'DVL', 'SVD', 'iLUMiNADOS', ' FiNaLe', 'UnSeeN' ],
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
                log.debug('Found with confidence 1.0: %s' % ({ prop: part },))
                result.set(prop, part, confidence = 1.0)
                minIdx = min(minIdx, name.index(part))


    # get year
    for part in name:
        year = textutils.stripBrackets(part)
        if valid_year(year):
            log.debug('Found with confidence 0.9: %s' % ({ 'year': int(year) },))
            result.set('year', int(year), confidence = 0.9)
            minIdx = min(minIdx, name.index(part))

    # remove ripper name
    # FIXME: fails with movies such as "down by law", etc...
    for by, who in zip(name[:-1], name[1:]):
        if by.lower() == 'by':
            log.debug('Found with confidence 0.4: %s' % ({ 'ripper': who },))
            result.set('ripper', who, confidence = 0.4)
            minIdx = min(minIdx, name.index(by))

    # subtitles
    # TODO: only finds the first one, need to check whether there are many of them
    for sub, lang in zip(name[:-1], name[1:]):
        if sub.lower() == 'sub':
            log.debug('Found with confidence 0.7: %s' % ({ 'subtitleLanguage': lang },))
            result.set('subtitleLanguage', lang, confidence = 0.7)
            minIdx = min(minIdx, name.index(sub))

    # get CD number (if any)
    cdrexp = re.compile('[Cc][Dd]([0-9]+)')
    for part in name:
        try:
            cdnumber = int(cdrexp.search(part).groups()[0])
            log.debug('Found with confidence 1.0: %s' % ({ 'cdnumber': cdnumber },))
            result.set('cdNumber', cdnumber, confidence = 1.0)
            minIdx = min(minIdx, name.index(part))
        except AttributeError:
            pass

    name = ' '.join(name[:minIdx])
    minIdx = len(name)

    # last chance on the full name: try some popular regexps
    general = [ '(?P<dircut>director\'s cut)',
                '(?P<edition>edition collector)' ]
    websites = [ 'sharethefiles.com', 'tvu.org.ru' ]
    websites = [ '(?P<website>%s)' % w.replace('.', ' ') for w in websites ] # dots have been previously converted to spaces
    rexps = general + websites

    matched = textutils.matchAllRegexp(name, rexps)
    for match in matched:
        log.debug('Found with confidence 1.0: %s' % match)
        result.update(match, confidence = 1.0)
        for key, value in match.items():
            minIdx = min(minIdx, name.find(value))

    # FIXME: this won't work with "2001 a space odyssey" for instance, where sth it incorrectly detected
    name = name[:minIdx].strip()

    # try website names
    # TODO: generic website url guesser
    websites = [ 'sharethefiles.com' ]


    # return final name as a (weak) guess for the movie title
    log.debug('Found with confidence 0.3: %s' % {'title': name})
    result.set('title', name, confidence = 0.3)

    return result

