#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2011 Nicolas Wack <wackou@gmail.com>
# Copyright (c) 2011 Ricard Marxer <ricardmp@gmail.com>
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

from __future__ import unicode_literals

from . import sep
from guessit import base_text_type
import re

prop_multi = { 'format': { 'DVD': [ 'DVD', 'DVD-Rip', 'VIDEO-TS', 'DVDivX' ],
                           'HD-DVD': [ 'HD-(?:DVD)?-Rip', 'HD-DVD' ],
                           'BluRay': [ 'Blu-ray', 'B[DR]Rip' ],
                           'HDTV': [ 'HD-TV' ],
                           'DVB': [ 'DVB-Rip', 'DVB', 'PD-TV' ],
                           'WEBRip': [ 'WEB-Rip' ],
                           'Screener': [ 'DVD-SCR', 'Screener' ],
                           'VHS': [ 'VHS' ],
                           'WEB-DL': [ 'WEB-DL' ] },

               'is3D': { True: [ '3D' ] },

               'screenSize': { '360p': [ '(?:\d{3,}(?:\\|\/|x|\*))?360(?:i|p?x?)' ],
                               '368p': [ '(?:\d{3,}(?:\\|\/|x|\*))?368(?:i|p?x?)' ],
                               '480p': [ '(?:\d{3,}(?:\\|\/|x|\*))?480(?:i|p?x?)' ],
                               '576p': [ '(?:\d{3,}(?:\\|\/|x|\*))?576(?:i|p?x?)' ],
                               '720p': [ '(?:\d{3,}(?:\\|\/|x|\*))?720(?:i|p?x?)' ],
                               '1080i': [ '(?:\d{3,}(?:\\|\/|x|\*))?1080i' ],
                               '1080p': [ '(?:\d{3,}(?:\\|\/|x|\*))?1080(?:\z|[^i])p?x?' ],
                               '4K': [ '(?:\d{3,}(?:\\|\/|x|\*))?2160(?:\z|[^i])p?x?'] },

               'videoCodec': { 'XviD': [ 'Xvid' ],
                               'DivX': [ 'DVDivX', 'DivX' ],
                               'h264': [ '[hx]-264' ],
                               'Rv10': [ 'Rv10' ],
                               'Mpeg2': [ 'Mpeg2' ] },

               # has nothing to do here (or on filenames for that matter), but some
               # releases use it and it helps to identify release groups, so we adapt
               'videoApi': {  'DXVA': [ 'DXVA' ] },

               'audioCodec': { 'AC3': [ 'AC3' ],
                               'DTS': [ 'DTS' ],
                               'AAC': [ 'He-AAC', 'AAC-He', 'AAC' ] },

               'audioChannels': { '5.1': [ r'5\.1', 'DD5[._ ]1', '5ch' ] },

               'episodeFormat': { 'Minisode': [ 'Minisodes?' ] }

               }

# prop_single dict of { property_name: [ canonical_form ] }
prop_single = { 'releaseGroup': [ 'ESiR', 'WAF', 'SEPTiC', r'\[XCT\]', 'iNT', 'PUKKA',
                                  'CHD', 'ViTE', 'TLF', 'FLAiTE',
                                  'MDX', 'GM4F', 'DVL', 'SVD', 'iLUMiNADOS',
                                  'aXXo', 'KLAXXON', 'NoTV', 'ZeaL', 'LOL',
                                  'CtrlHD', 'POD', 'WiKi','IMMERSE', 'FQM',
                                  '2HD',  'CTU', 'HALCYON', 'EbP', 'SiTV',
                                  'HDBRiSe', 'AlFleNi-TeaM', 'EVOLVE', '0TV',
                                  'TLA', 'NTB', 'ASAP', 'MOMENTUM', 'FoV', 'D-Z0N3',
                                  'TrollHD', 'ECI'
                                  ],

                # potentially confusing release group names (they are words)
                'weakReleaseGroup': [ 'DEiTY', 'FiNaLe', 'UnSeeN', 'KiNGS', 'CLUE', 'DIMENSION',
                                      'SAiNTS', 'ARROW', 'EuReKA', 'SiNNERS', 'DiRTY', 'REWARD',
                                      'REPTiLE',
                                      ],

                'other': [ 'PROPER', 'REPACK', 'LIMITED', 'DualAudio', 'Audiofixed', 'R5',
                           'complete', 'classic', # not so sure about these ones, could appear in a title
                           'ws' ] # widescreen
                }

__dash = '-'
__psep = '[-. _]?'

def compile_pattern(pattern):
    return re.compile(enhance_pattern(pattern), re.IGNORECASE)

def enhance_pattern(pattern):
    """
    Enhance pattern to match more equivalent values.
    
    @param pattern: string considered as a regexp.
    
    '-' are replaced by ([ \.-_]), which matches more types of separators (or none)
    """
    return pattern.replace(__dash, __psep)

def enhance_property_patterns(name):
    """
    Get the enhanced pattern of given property.
    
    @param name: property name of patterns to enhance. 
    
    @see enhance_pattern(pattern)
    """
    return [ enhance_pattern(p) for patterns in prop_multi[name].values() for p in patterns  ]

def unregister_property_patterns(name, canonical_form):
    """
    Unregister a property pattern canonical_form
    """
    prop_canonical_forms = prop_multi.get(name)
    
    if not prop_canonical_forms is None:
        prop_patterns = prop_canonical_forms.get(canonical_form)
        
        if not prop_patterns is None:
            del prop_canonical_forms[canonical_form]
        
        if not prop_canonical_forms:
            del prop_multi[name]

def register_property_pattern(name, canonical_form, *patterns):
    """
    Register a property pattern canonical_form
    
    @param name: name of the property (format, screenSize, ...)
    @param canonical_form: value of the property (DVD, 720p, ...)
    @param patterns: regular expression patterns to register for the property canonical_form
    
    @note: simpler patterns need to be at the end of the list to not shadow more
    complete ones, eg: 'AAC' needs to come after 'He-AAC'
    ie: from most specific to less specific
    """
    global prop_multi
    
    prop_canonical_forms = prop_multi.get(name)
    
    if prop_canonical_forms is None:
        prop_canonical_forms = {}
        prop_multi[name] = prop_canonical_forms
    prop_patterns = prop_canonical_forms.get(canonical_form)
    
    if prop_patterns is None:
        prop_patterns = []
        prop_canonical_forms[canonical_form] = prop_patterns
    
    for pattern in patterns:
        prop_patterns.append(pattern)
        
__properties_rexps = None

def compile_all():
    """
    After changing patterns in this file, this method should be called before trying to guess anything.
    
    It compiles defined properties (prop_multi & prop_single) into patterns.__properties_rexps
    
    @return __properties_rexps dict of { property_name: { canonical_form: [ rexp ] } }
    containing the rexps compiled from both prop_multi and prop_single
    """
    global __properties_rexps
    __properties_rexps = dict((type_, dict((canonical_form,
                                         [ compile_pattern(pattern) for pattern in patterns ])
                                        for canonical_form, patterns in props.items()))
                            for type_, props in prop_multi.items())

    __properties_rexps.update(dict((type_, dict((canonical_form, [ compile_pattern(canonical_form) ])
                                             for canonical_form in props))
                                 for type_, props in prop_single.items()))

    return __properties_rexps

compile_all()

def find_properties(string):
    """
    Find properties for given string.
    
    A property must always be surrounded by separators to be returned.
    
    @return: list of tuple (property_name, canonical_form, start, end)
    """
    result = []
    for property_name, props in __properties_rexps.items():
        # FIXME: this should be done in a more flexible way...
        if property_name in ['weakReleaseGroup']:
            continue

        for canonical_form, rexps in props.items():
            for value_rexp in rexps:
                match = value_rexp.search(string)
                if match:
                    start, end = match.span()
                    # make sure our word is always surrounded by separators
                    # note: sep is a regexp, but in this case using it as
                    #       a char sequence achieves the same goal
                    if ((start > 0 and string[start-1] not in sep) or
                        (end < len(string) and string[end] not in sep)):
                        continue

                    result.append((property_name, canonical_form, start, end))
    return result

def compute_canonical_form(property_name, value):
    """
    @return: Canonical form of a property given its name if it is a valid one, None otherwise.
    """
    if isinstance(value, base_text_type):
        for canonical_form, rexps in __properties_rexps[property_name].items():
            for rexp in rexps:
                if rexp.match(value):
                    return canonical_form
    return None