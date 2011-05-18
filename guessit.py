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

from guessit import slogging, guess_file_info
from guessit.textutils import to_utf8
from optparse import OptionParser
import sys
import logging


def detect_filename(filename, filetype, info = ['filename']):
    if isinstance(filename, str):
        filename = filename.decode('utf-8')

    print 'For:', to_utf8(filename)
    print 'GuessIt found:', guess_file_info(filename, filetype, info).nice_string()


def run_demo(episodes = True, movies = True):
    # NOTE: tests should not be added here but rather in the test/ folder
    #       this is just intended as a quick example
    if episodes:
        testeps = [ u'Series/Californication/Season 2/Californication.2x05.Vaginatown.HDTV.XviD-0TV.[tvu.org.ru].avi',
                    u'Series/dexter/Dexter.5x02.Hello,.Bandit.ENG.-.sub.FR.HDTV.XviD-AlFleNi-TeaM.[tvu.org.ru].avi',
                    u'Series/Treme/Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.[tvu.org.ru].avi',
                    u'Series/Duckman/Duckman - 101 (01) - 20021107 - I, Duckman.avi',
                    u'Series/Duckman/Duckman - S1E13 Joking The Chicken (unedited).avi',
                    u'Series/Simpsons/The_simpsons_s13e18_-_i_am_furious_yellow.mpg',
                    u'Series/Simpsons/Saison 12 Français/Simpsons,.The.12x08.A.Bas.Le.Sergent.Skinner.FR.[tvu.org.ru].avi',
                    u'Series/Dr._Slump_-_002_DVB-Rip_Catalan_by_kelf.avi',
                    u'Series/Kaamelott/Kaamelott - Livre V - Second Volet - HD 704x396 Xvid 2 pass - Son 5.1 - TntRip by Slurm.avi'
                    ]

        for f in testeps:
            print '-'*80
            detect_filename(f, filetype = 'episode')


    if movies:
        testmovies = [ u'Movies/Fear and Loathing in Las Vegas (1998)/Fear.and.Loathing.in.Las.Vegas.720p.HDDVD.DTS.x264-ESiR.mkv',
                       u'Movies/El Dia de la Bestia (1995)/El.dia.de.la.bestia.DVDrip.Spanish.DivX.by.Artik[SEDG].avi',
                       u'Movies/Blade Runner (1982)/Blade.Runner.(1982).(Director\'s.Cut).CD1.DVDRip.XviD.AC3-WAF.avi',
                       u'Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv',
                       u'Movies/Sin City (BluRay) (2005)/Sin.City.2005.BDRip.720p.x264.AC3-SEPTiC.mkv',
                       u'Movies/Borat (2006)/Borat.(2006).R5.PROPER.REPACK.DVDRip.XviD-PUKKA.avi', # FIXME: PROPER and R5 get overwritten
                       u'[XCT].Le.Prestige.(The.Prestige).DVDRip.[x264.HP.He-Aac.{Fr-Eng}.St{Fr-Eng}.Chaps].mkv', # FIXME: title gets overwritten
                       u'Battle Royale (2000)/Battle.Royale.(Batoru.Rowaiaru).(2000).(Special.Edition).CD1of2.DVDRiP.XviD-[ZeaL].avi',
                       u'Movies/Brazil (1985)/Brazil_Criterion_Edition_(1985).CD2.English.srt',
                       u'Movies/Persepolis (2007)/[XCT] Persepolis [H264+Aac-128(Fr-Eng)+ST(Fr-Eng)+Ind].mkv',
                       u'Movies/Toy Story (1995)/Toy Story [HDTV 720p English-Spanish].mkv',
                       u'Movies/Pirates of the Caribbean: The Curse of the Black Pearl (2003)/Pirates.Of.The.Carribean.DC.2003.iNT.DVDRip.XviD.AC3-NDRT.CD1.avi',
                       u'Movies/Office Space (1999)/Office.Space.[Dual-DVDRip].[Spanish-English].[XviD-AC3-AC3].[by.Oswald].avi',
                       u'Movies/The NeverEnding Story (1984)/The.NeverEnding.Story.1.1984.DVDRip.AC3.Xvid-Monteque.avi',
                       u'Movies/Juno (2007)/Juno KLAXXON.avi',
                       u'Movies/Chat noir, chat blanc (1998)/Chat noir, Chat blanc - Emir Kusturica (VO - VF - sub FR - Chapters).mkv',
                       u'Movies/Wild Zero (2000)/Wild.Zero.DVDivX-EPiC.srt',
                       u'Movies/El Bosque Animado (1987)/El.Bosque.Animado.[Jose.Luis.Cuerda.1987].[Xvid-Dvdrip-720x432].avi',
                       u'testsmewt_bugs/movies/Baraka_Edition_Collector.avi'
                       ]

        for f in testmovies:
            print '-'*80
            detect_filename(f, filetype = 'movie')


if __name__ == '__main__':
    slogging.setupLogging()

    parser = OptionParser(usage = 'usage: %prog [options] file1 [file2...]')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
                      help = 'display debug output')
    parser.add_option('-i', '--info', dest = 'info', default = 'filename',
                      help = 'the desired information type: filename, hash_mpc or a hash from python\'s '
                             'hashlib module, such as hash_md5, hash_sha1, ...; or a list of any of '
                             'them, comma-separated')
    parser.add_option('-t', '--type', dest = 'filetype', default = 'autodetect',
                      help = 'the suggested file type: movie, episode or autodetect')
    parser.add_option('-d', '--demo', action='store_true', dest='demo', default=False,
                      help = 'run a few builtin tests instead of analyzing a file')

    options, args = parser.parse_args()
    if options.verbose:
        logging.getLogger('guessit').setLevel(logging.DEBUG)

    if options.demo:
        run_demo(episodes = True, movies = True)
    else:
        if args:
            for filename in args:
                detect_filename(filename, filetype = options.filetype, info = options.info.split(','))

        else:
            parser.print_help()
