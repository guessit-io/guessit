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

from guessit.guess import Guess, merge_similar_guesses, merge_all, choose_int, choose_string
from guessit.video import guess_video_filename
from guessit import fileutils, textutils
import re
import logging

log = logging.getLogger("guessit.episode")


def format_episode_guess(guess):
    """Formats all the found values to their natural type.
    For instance, a year would be stored as an int value, ...
    Note that this modifies the dictionary given as input."""
    for prop in [ 'season', 'episodeNumber', 'year' ]:
        try:
            guess[prop] = int(guess[prop])
        except KeyError:
            pass

    return guess


def guess_episode_filename_parts(filename):
    name = fileutils.split_path(filename)
    basename = name[-1]

    result = []

    def guessed(match, confidence = None):
        result.append(format_episode_guess(Guess(match, confidence = confidence)))

    # heuristic 1: try to guess the season & epnumber using S01E02 and 1x02 patterns
    sep = '[ \._-]'
    rexps = [ 'season (?P<season>[0-9]+)',
              '(?P<season>[0-9]+)[x\.](?P<episodeNumber>[0-9]+)',
              '[Ss](?P<season>[0-9]+) ?[Ee](?P<episodeNumber>[0-9]+)'
              ]

    basename_rexps = [ sep + '(?P<episodeNumber>[0-9]+)(?:v[23])?' + sep, # v2 or v3 for some mangas which have multiples rips
                       ]


    for n in name:
        for match in textutils.matchAllRegexp(n, rexps):
            log.debug('Found with confidence 1.0: %s' % match)
            guessed(match, confidence = 1.0)

    for match in textutils.matchAllRegexp(basename, basename_rexps):
        log.debug('Found with confidence 0.4: %s' % match)
        guessed(match, confidence = 0.6)


    # cleanup a bit by removing unlikely eps numbers which are probably numbers in the title
    # or even dates in the filename, etc...
    niceGuess = None
    for guess in list(result):
        if 'episodeNumber' in guess and 'season' in guess:
            niceGuess = guess
        if 'episodeNumber' in guess and 'season' not in guess and guess['episodeNumber'] > 1500:
            log.debug('Removing unlikely %s', guess)
            result.remove(guess)


    # if we have season+epnumber, remove single epnumber guesses
    # TODO: we should do this in a generic merger (eg: that also work for season, etc...)
    #       also: we might lose some information by bluntly removing a match
    if niceGuess:
        for guess in list(result):
            if 'episodeNumber' in guess and 'season' not in guess:
                epnum = guess['episodeNumber']

                # update confidence accordingly
                nconf = niceGuess.confidence('episodeNumber')
                conf = guess.confidence('episodeNumber')

                if niceGuess['episodeNumber'] == epnum:
                    niceGuess.set_confidence('episodeNumber', 1 - (1-nconf)*(1-conf))
                else:
                    niceGuess.set_confidence('episodeNumber', nconf - conf)

                log.debug('Removing %s because %s looks better' % (guess, niceGuess))
                result.remove(guess)



    # heuristic 2: try to guess the serie title from the filename
    for rexp in rexps:
        found = re.compile(rexp, re.IGNORECASE).search(basename)
        if found:
            title = textutils.cleanString(basename[:found.span()[0]])
            log.debug('Found with confidence 0.6: series title = %s' % title)

            guessed({ 'series': title }, confidence = 0.6)


    # heuristic 3: try to guess the serie title from the parent directory!
    #result = query.Episode(allow_incomplete = True)
    if textutils.matchAnyRegexp(name[-2], [ 'season (?P<season>[0-9]+)',
                                           # TODO: need to find a better way to have language packs for regexps
                                           'saison (?P<season>[0-9]+)' ]):
        series = name[-3]
        log.debug('Found with confidence 0.8: series title = %s' % series)
        guessed({ 'series': series }, confidence = 0.8)

    else:
        series = name[-2]
        log.debug('Found with confidence 0.4: series title = %s' % series)
        guessed({ 'series': series }, confidence = 0.4)


    # heuristic 4: add those anyway with very little probability, so that if don't find anything we can still use this
    #result.append((dict(series = 'Unknown', season = 1, episodeNumber = -1), 0.1))

    # post-processing
    # we could already clean a bit the data here by solving it and comparing it to
    # each element we found, eg: remove all md which have an improbable episode number
    # such as 72 if some other valid episode number has been found, etc...

    # if the episode number is higher than 100 and lower than 3000, we assume it is season*100+epnumber
    for guess in [ guess for guess in result if guess.get('episodeNumber', 0) > 100 and guess.get('episodeNumber', 0) < 3000 ]:
        num = guess['episodeNumber']
        # it's the only guess we have, make it look like it's an episode
        # FIXME: maybe we should check if we already have an estimate for the season number?
        guess['season'] = num // 100
        guess['episodeNumber'] = num % 100
        guess.set_confidence('season', guess.confidence('episodeNumber'))


    return result



def guess_episode_filename(filename):
    # guess the video parts of it
    video_info, minidx = guess_video_filename(filename)

    parts = [ video_info ]

    parts += guess_episode_filename_parts(filename)

    # 1- try to sanitize info a little bit more

    # heuristic 1: if there are any series name that look like "blahblah, the", invert it in its correct position
    for part in parts:
        if 'series' not in part:
            continue

        series = part['series']
        lseries = series.lower()

        if lseries[-4:] == ',the':
            part['series'] = 'The ' + series[:-4]

        if lseries[-5:] == ', the':
            part['series'] = 'The ' + series[:-5]


    # 2- try to merge similar information together and give it a higher confidence
    merge_similar_guesses(parts, 'season', choose_int)
    merge_similar_guesses(parts, 'episodeNumber', choose_int)
    merge_similar_guesses(parts, 'series', choose_string)

    return merge_all(parts)

