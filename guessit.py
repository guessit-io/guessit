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

from guessit import slogging, episode
import sys
import logging


if __name__ == '__main__':
    testfiles = [ '/data/Series/Californication/Season 2/Californication.2x05.Vaginatown.HDTV.XviD-0TV.[tvu.org.ru].avi',
                  '/data/Series/dexter/Dexter.5x02.Hello,.Bandit.ENG.-.sub.FR.HDTV.XviD-AlFleNi-TeaM.[tvu.org.ru].avi',
                  '/data/Series/Treme/Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.[tvu.org.ru].avi',
                  '/data/Series/Duckman/Duckman - 101 (01) - 20021107 - I, Duckman.avi',
                  '/data/Series/Duckman/Duckman - S1E13 Joking The Chicken (unedited).avi',
                  '/data/Series/Simpsons/The_simpsons_s13e18_-_i_am_furious_yellow.mpg',
                  '/data/Series/Simpsons/Saison 12 Français/Simpsons,.The.12x08.A.Bas.Le.Sergent.Skinner.FR.[tvu.org.ru].avi'
                  ]

    slogging.setupLogging()
    logging.getLogger('guessit').setLevel(logging.DEBUG)

    for f in testfiles:
        print '-'*80
        print 'For:', f
        result = episode.guess_episode_filename(f).to_json()
        print 'Found:', result
        #for guess in guess_episode_filename(f):
        #    #print 'Confidence:', confidence, json.dumps(g, indent = 4)
        #    print guess.to_json()
