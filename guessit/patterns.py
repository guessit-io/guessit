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


subtitle_exts = [ 'srt', 'idx', 'sub' ]

video_exts = [ 'avi', 'mkv', 'mpg', 'mp4', 'mov', 'ogg', 'ogv', 'wmv' ]

# separator character regexp
sep = r'[][)(}{+ \._-]' # regexp art, hehe :D

# character used to represent a deleted char (when matching groups)
deleted = '_'

# format: [ (regexp, confidence, span_adjust) ]
episode_rexps = [ # ... Season 2 ...
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


weak_episode_rexps = [ # ... 213 ...
                       (sep + r'(?P<episodeNumber>[0-9]{1,3})' + sep, 0.3, (1, -1)),
                       ]



video_rexps = [ # cd number
                (r'cd ?(?P<cdNumber>[0-9])( ?of ?(?P<cdNumberTotal>[0-9]))?', 1.0, (0, 0)),

                # special editions
                (r'edition' + sep + r'(?P<edition>collector)', 1.0, (0, 0)),
                (r'(?P<edition>collector)' + sep + 'edition', 1.0, (0, 0)),
                (r'(?P<edition>special)' + sep + 'edition', 1.0, (0, 0)),
                (r'(?P<edition>criterion)' + sep + 'edition', 1.0, (0, 0)),

                # director's cut
                (r"(?P<edition>director'?s?" + sep + "cut)", 1.0, (0, 0))
                ]

properties = { 'format': [ 'DVDRip', 'HD-DVD', 'HDDVD', 'HDDVDRip', 'BluRay', 'BDRip',
                           'HDRip', 'DVD', 'DVDivX', 'Rip', 'HDTV', 'DVB' ],

               'container': [ 'avi', 'mkv', 'ogv', 'wmv', 'mp4', 'mov' ],

               'screenSize': [ '720p' ],

               'videoCodec': [ 'XviD', 'DivX', 'x264', 'h264', 'Rv10' ],

               'audioCodec': [ 'AC3', 'DTS', 'He-AAC', 'AAC-He', 'AAC' ],

               'releaseGroup': [ 'ESiR', 'WAF', 'SEPTiC', '[XCT]', 'iNT', 'PUKKA',
                                 'CHD', 'ViTE', 'DiAMOND', 'TLF', 'DEiTY', 'FLAiTE',
                                 'MDX', 'GM4F', 'DVL', 'SVD', 'iLUMiNADOS', ' FiNaLe',
                                 'UnSeeN', 'aXXo', 'KLAXXON', 'NoTV' ],

               'website': [ 'tvu.org.ru', 'emule-island.com' ],

               'other': [ '5ch', 'PROPER', 'REPACK', 'LIMITED', 'DualAudio', 'iNTERNAL', 'Audiofixed', 'R5',
                          'complete', 'classic', # not so sure about these ones, could appear in a title
                          'ws', # widescreen
                          'SE', # special edition
                          # TODO: director's cut
                          ],
               }


property_synonyms = { 'DVD': [ 'DVDRip' ],
                      'HD-DVD': [ 'HDDVD', 'HDDVDRip' ],
                      'BluRay': [ 'BDRip' ],
                      'DivX': [ 'DVDivX' ],
                      'h264': [ 'x264' ],
                      'AAC': [ 'He-AAC', 'AAC-He' ],
                      'Special Edition': [ 'Special' ],
                      'Collector Edition': [ 'Collector' ],
                      'Criterion Edition': [ 'Criterion' ]
                      }


reverse_synonyms = {}
for canonical, synonyms in property_synonyms.items():
    for synonym in synonyms:
        reverse_synonyms[synonym.lower()] = canonical

def canonical_form(string):
    return reverse_synonyms.get(string.lower(), string)
