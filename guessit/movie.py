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

from guessit.guess import Guess, merge_similar_guesses, merge_all, choose_string
from guessit.video import guess_video_filename
from guessit import fileutils, textutils
import re
import logging

log = logging.getLogger('guessit.movie')


def format_movie_guess(guess):
    """Formats all the found values to their natural type.
    For instance, a year would be stored as an int value, ...
    Note that this modifies the dictionary given as input."""
    for prop in [ 'year' ]:
        try:
            guess[prop] = int(guess[prop])
        except KeyError:
            pass

    return guess


def valid_year(year):
    try:
        return int(year) > 1920 and int(year) < 2015
    except ValueError:
        return False


def guess_XCT(filename):
    result = Guess()

    if not '[XCT]' in filename:
        return filename, []

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

        # FIXME: this is a hack here, it should be more generic (ie: done once, not everywhere)
        from guessit.video import _language_map
        result['subtitleLanguage'] = [ _language_map[lang.lower()] for lang in result['subtitleLanguage'] ]


        # find audio
        audio = textutils.matchRegexp(mdstr, 'aac[0-9\.-]*[{\(](?P<audio>.*?)[}\)]')['audio']
        log.debug('Found XCT audio with confidence 1.0: %s' % audio.split('-'))
        mdstr.replace(audio, '')
        result.set('language', audio.split('-'), confidence = 1.0)

        # FIXME: this is a hack here, it should be more generic (ie: done once, not everywhere)
        result['language'] = [ _language_map[lang.lower()] for lang in result['language'] ]

        # find year: if we found it, then the english title of the movie is either what's inside
        # the parentheses before the year, or everything before the year
        s = filename
        for c in '()[]':
            s = s.replace(c, ' ')
        title = textutils.cleanString(s[:-3]) # to remove the extension if still left
        log.debug('Found XCT title with confidence 0.6: %s' % title)
        result.set('title', title, confidence = 0.6)

        years = [ m['year'] for m in textutils.multipleMatchRegexp(filename, '(?P<year>[0-9]{4})') if valid_year(m['year']) ]
        if len(years) == 1:
            title = filename[:filename.index(years[0])].replace('.', ' ')
            log.debug('Found XCT title with confidence 0.8: %s' % title)
            result.set('title', title, confidence = 0.8)
        elif len(years) >= 2:
            log.warning('Ambiguous filename: possible years are ' + ', '.join(years))

        try:
            title = textutils.matchRegexp(title, '\((?P<title>.*?)\)')['title'].replace('.', ' ')
            log.debug('Found XCT title with confidence 0.9: %s' % title)
            result.set('title', title, confidence = 0.9)
        except:
            pass

        result['title'] = title

    finally:
        return filename, [ result ]



def guess_movie_filename_parts(filename):
    import os.path
    filename = os.path.basename(filename)
    result = []

    # first apply specific methods which are very strict but have a very high confidence
    filename, result = guess_XCT(filename)

    def guessed(match, confidence = None):
        result.append(format_movie_guess(Guess(match, confidence = confidence)))

    # then guess the video parts of it
    video_info, minidx = guess_video_filename(filename)


    result.append(video_info)

    # last chance on the full name: try some popular movie regexps
    name = textutils.cleanString(filename)


    # FIXME: this won't work with "2001 a space odyssey" for instance, where sth is incorrectly detected
    minidx = min(minidx, textutils.find_any(filename, '-()[]'))
    title = textutils.cleanString(filename[:minidx])

    # NOTE: unneeded now as the previous operation already took care of parentheses...
    # small heuristic: if the title ends with something between parenthese, it might either be:
    #  - the translation of the movie title in another language
    #  - some actors
    #  - some part of the title when it is long and has 2 names, one subset of the other
    # in any case, we might be better off removing it
    #p1, p2 = title.find('('), title.find(')')
    #if 0 < p1 < p2:
    #    title = (title[:p1] + title[p2+1:]).strip()

    # return final name as a (weak) guess for the movie title
    log.debug('Found with confidence 0.3: %s' % { 'title': title })
    guessed({ 'title': title }, confidence = 0.3)

    return result



def guess_movie_filename(filename):
    log.debug('Trying to guess info for movie: ' + filename)

    parts = guess_movie_filename_parts(filename)

    merge_similar_guesses(parts, 'title', choose_string)

    result = merge_all(parts)
    log.debug('Final result: ' + result.to_json())

    return result
