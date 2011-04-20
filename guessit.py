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

from guessit import slogging, episode, movie
import sys
import logging


if __name__ == '__main__':
    slogging.setupLogging()
    logging.getLogger('guessit').setLevel(logging.DEBUG)

    if True:
        testeps = [ 'Series/Californication/Season 2/Californication.2x05.Vaginatown.HDTV.XviD-0TV.[tvu.org.ru].avi',
                    'Series/dexter/Dexter.5x02.Hello,.Bandit.ENG.-.sub.FR.HDTV.XviD-AlFleNi-TeaM.[tvu.org.ru].avi',
                    'Series/Treme/Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.[tvu.org.ru].avi',
                    'Series/Duckman/Duckman - 101 (01) - 20021107 - I, Duckman.avi',
                    'Series/Duckman/Duckman - S1E13 Joking The Chicken (unedited).avi',
                    'Series/Simpsons/The_simpsons_s13e18_-_i_am_furious_yellow.mpg',
                    'Series/Simpsons/Saison 12 Français/Simpsons,.The.12x08.A.Bas.Le.Sergent.Skinner.FR.[tvu.org.ru].avi',
                    'Series/Dr._Slump_-_002_DVB-Rip_Catalan_by_kelf.avi',
                    'Series/Kaamelott/Kaamelott - Livre V - Second Volet - HD 704x396 Xvid 2 pass - Son 5.1 - TntRip by Slurm.avi'
                    ]

        for f in testeps:
            print '-'*80
            print 'For:', f
            result = episode.guess_episode_filename(f).to_json()
            print 'Found:', result


    if False:
        testmovies = [ 'Movies/Fear and Loathing in Las Vegas (1998)/Fear.and.Loathing.in.Las.Vegas.720p.HDDVD.DTS.x264-ESiR.mkv',
                       'Movies/El Dia de la Bestia (1995)/El.dia.de.la.bestia.DVDrip.Spanish.DivX.by.Artik[SEDG].avi',
                       'Movies/Blade Runner (1982)/Blade.Runner.(1982).(Director\'s.Cut).CD1.DVDRip.XviD.AC3-WAF.avi',
                       'Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv',
                       'Movies/Sin City (BluRay) (2005)/Sin.City.2005.BDRip.720p.x264.AC3-SEPTiC.mkv',
                       'Movies/Borat (2006)/Borat.(2006).R5.PROPER.REPACK.DVDRip.XviD-PUKKA.avi', # FIXME: PROPER and R5 get overwritten
                       '[XCT].Le.Prestige.(The.Prestige).DVDRip.[x264.HP.He-Aac.{Fr-Eng}.St{Fr-Eng}.Chaps].mkv', # FIXME: title gets overwritten
                       'Battle Royale (2000)/Battle.Royale.(Batoru.Rowaiaru).(2000).(Special.Edition).CD1of2.DVDRiP.XviD-[ZeaL].avi'
                       ]

        for f in testmovies:
            print '-'*80
            print 'For:', f
            result = movie.guess_movie_filename(f).to_json()
            print 'Found:', result
