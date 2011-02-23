#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ntpath
import re
import textutils
import json
import logging

log = logging.getLogger("pygoo")

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

# let's be a nicely behaving library
h = NullHandler()
log.addHandler(h)



def split_path(path):
    """Splits the given path into the list of folders and the filename (or the
    last folder if you gave it a folder path.

    If the given path was an absolute path, the first element will always be:
     - the '/' root folder on Unix systems
     - the drive letter on Windows systems (eg: r'C:\')

    >>> split_path('/usr/bin/smewt')
    ['/', 'usr', 'bin', 'smewt']

    >>> split_path('relative_path/to/my_folder/')
    ['relative_path', 'to', 'my_folder']

    >>> split_path(r'C:\Program Files\Smewt\smewt.exe')
    ['C:\\\\', 'Program Files', 'Smewt', 'smewt.exe']

    >>> split_path(r'Documents and Settings\User\config\')
    ['Documents and Settings', 'User', 'config']

    """
    result = []
    while True:
        head, tail = ntpath.split(path)

        # on Unix systems, the root folder is '/'
        if head == '/' and tail == '':
            return [ '/' ] + result

        # on Windows, the root folder is a drive letter (eg: 'C:\')
        if len(head) == 3 and head[1:] == ':\\' and tail == '':
            return [ head ] + result

        if head == '' and tail == '':
            return result

        # we just split a directory ending with '/', so tail is empty
        if not tail:
            path = head
            continue

        result = [ tail ] + result
        path = head


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

class Guess(dict):
    def __init__(self, *args, **kwargs):
        try:
            confidence = kwargs.pop('confidence')
        except KeyError:
            confidence = 0

        dict.__init__(self, *args, **kwargs)

        self._confidence = {}
        for prop in self:
            self._confidence[prop] = confidence

    def to_json(self):
        parts = json.dumps(self, indent = 4).split('\n')
        for i, p in enumerate(parts):
            if p[:5] != '    "':
                continue

            prop = p.split('"')[1]
            parts[i] = ('    [%.2f] ' % self._confidence.get(prop, -1)) + p[5:]

        return '\n'.join(parts)

    def confidence(self, prop):
        return self._confidence[prop]

    def set_confidence(self, prop, value):
        self._confidence[prop] = value


def guess_episode_filename_parts(filename):
    name = split_path(filename)
    basename = name[-1]

    result = []

    # heuristic 1: try to guess the season & epnumber using S01E02 and 1x02 patterns
    sep = '[ \._-]'
    rexps = [ 'season (?P<season>[0-9]+)',
              sep + '(?P<episodeNumber>[0-9]+)(?:v[23])?' + sep, # v2 or v3 for some mangas which have multiples rips
              '(?P<season>[0-9]+)[x\.](?P<episodeNumber>[0-9]+)',
              '[Ss](?P<season>[0-9]+) ?[Ee](?P<episodeNumber>[0-9]+)'
              ]

    for n in name:
        for match in textutils.matchAllRegexp(n, rexps):
            log.debug('Found with confidence 1.0: %s' % match)
            #ep = query.Episode(confidence = 1.0, allow_incomplete = True, **match)
            #media.append('matches', ep)
            result.append(format_episode_guess(Guess(match, confidence = 1.0)))

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

            result.append(Guess(series = title, confidence = 0.6))


    # heuristic 3: try to guess the serie title from the parent directory!
    #result = query.Episode(allow_incomplete = True)
    if textutils.matchAnyRegexp(name[-2], [ 'season (?P<season>[0-9]+)',
                                           # TODO: need to find a better way to have language packs for regexps
                                           'saison (?P<season>[0-9]+)' ]):
        series = name[-3]
        log.debug('Found with confidence 0.8: series title = %s' % series)
        result.append(Guess(series = series, confidence = 0.8))

    else:
        series = name[-2]
        log.debug('Found with confidence 0.4: series title = %s' % series)
        result.append(Guess(series = series, confidence = 0.4))


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
    parts = guess_episode_filename_parts(filename)

    return parts

    # 1- try to sanitize info a little bit more

    # heuristic 1: if there are any series name that look like "blahblah, the", invert it in its correct position
    for part, confidence in parts:
        if 'series' not in part:
            continue

        series = part['series']
        lseries = series.lower()

        if lseries[-4:] == ',the':
            part['series'] = 'The ' + series[:-4]

        if lseries[-5:] == ', the':
            part['series'] = 'The ' + series[:-5]


    # 2- try to merge similar information together and give it a higher confidence

    return parts


if __name__ == '__main__':
    testfiles = [ '/data/Series/Californication/Season 2/Californication.2x05.Vaginatown.HDTV.XviD-0TV.[tvu.org.ru].avi',
                  '/data/Series/dexter/Dexter.5x02.Hello,.Bandit.ENG.-.sub.FR.HDTV.XviD-AlFleNi-TeaM.[tvu.org.ru].avi',
                  '/data/Series/Treme/Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.[tvu.org.ru].avi',
                  '/data/Series/Duckman/Duckman - 101 (01) - 20021107 - I, Duckman.avi',
                  '/data/Series/Duckman/Duckman - S1E13 Joking The Chicken (unedited).avi',
                  '/data/Series/Simpsons/The_simpsons_s13e18_-_i_am_furious_yellow.mpg',
                  '/data/Series/Simpsons/Saison 12 Français/Simpsons,.The.12x08.A.Bas.Le.Sergent.Skinner.FR.[tvu.org.ru].avi'
                  ]

    import json
    import slogging

    slogging.setupLogging()
    log.setLevel(logging.DEBUG)

    for f in testfiles:
        print '-'*80
        print 'For:', f
        print 'Found:'
        for guess in guess_episode_filename(f):
            #print 'Confidence:', confidence, json.dumps(g, indent = 4)
            print guess.to_json()
