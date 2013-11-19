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

_properties = {}
_properties_compiled = {}

_dash = '-'
_psep = '[-. _]?'


def compile_pattern(pattern):
    return re.compile(enhance_pattern(pattern), re.IGNORECASE)


def enhance_pattern(pattern):
    """
    Enhance pattern to match more equivalent values.

    @param pattern: string considered as a regexp.

    '-' are replaced by ([ \.-_]), which matches more types of separators (or none)
    """
    return pattern.replace(_dash, _psep)


def enhance_property_patterns(name):
    """
    Get the enhanced patterns of given property.

    @param name: property name of patterns to enhance.

    @see enhance_pattern(pattern)
    """
    return [enhance_pattern(p) for patterns in _properties[name].values() for p in patterns]


def unregister_property(name, *property_canonical_forms):
    """
    Unregister a property canonical forms

    If property_canonical_forms are specified, only those values will be unregistered

    @param name: property name to unregister
    @param property_canonical_forms: canonical_forms to unregister
    """
    prop_canonical_forms = _properties.get(name)

    if not prop_canonical_forms is None:
        if property_canonical_forms:
            for canonical_form in property_canonical_forms:
                if canonical_form in prop_canonical_forms:
                    del prop_canonical_forms[canonical_form]

                if not prop_canonical_forms:
                    del _properties[name]
        else:
            del _properties[name]

    rexps = _properties_compiled.get(name)
    if not rexps is None:
        if property_canonical_forms:
            for canonical_form in property_canonical_forms:
                if canonical_form in rexps:
                    del rexps[canonical_form]

                if not rexps:
                    del _properties_compiled[name]
        else:
            del _properties_compiled[name]


def register_property(name, canonical_form, *patterns):
    """
    Register property with defined canonical form and multiple patterns.

    @param name: name of the property (format, screenSize, ...)
    @param canonical_form: value of the property (DVD, 720p, ...)
    @param patterns: regular expression patterns to register for the property canonical_form

    @note: simpler patterns need to be at the end of the list to not shadow more
    complete ones, eg: 'AAC' needs to come after 'He-AAC'
    ie: from most specific to less specific
    """
    global _properties
    prop_canonical_forms = _properties.get(name)

    if prop_canonical_forms is None:
        prop_canonical_forms = {}
        _properties[name] = prop_canonical_forms
    prop_patterns = prop_canonical_forms.get(canonical_form)

    if prop_patterns is None:
        prop_patterns = []
        prop_canonical_forms[canonical_form] = prop_patterns

    for pattern in patterns:
        prop_patterns.append(pattern)

    rexps = _properties_compiled.get(name)
    if rexps is None:
        rexps = {}
        _properties_compiled[name] = rexps

    property_patterns = None
    if not canonical_form in rexps:
        property_patterns = []
        rexps[canonical_form] = property_patterns
    else:
        property_patterns = rexps[canonical_form]
    for pattern in patterns:
        property_patterns.append(compile_pattern(pattern))


def register_properties(name, *canonical_forms):
    """
    Registry properties.

    @param name: name of the property (releaseGroup, ...)
    @param canonical_forms: values of the property ('ESiR', 'WAF', 'SEPTiC', ...)
    """
    for canonical_form in canonical_forms:
        register_property(name, canonical_form, canonical_form)


def clear_properties():
    """
    Unregister all defined properties
    """
    _properties.clear()
    _properties_compiled.clear()


def find_properties(string):
    """
    Find properties for given string.

    A property must always be surrounded by separators to be returned.

    @return: list of tuple (property_name, canonical_form, start, end)
    """
    result = []
    for property_name, props in _properties_compiled.items():
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
                    if ((start > 0 and string[start - 1] not in sep) or
                        (end < len(string) and string[end] not in sep)):
                        continue

                    result.append((property_name, canonical_form, start, end))
    return result


def compute_canonical_form(property_name, value):
    """
    @return: Canonical form of a property given its name if it is a valid one, None otherwise.
    """
    if isinstance(value, base_text_type):
        for canonical_form, rexps in _properties_compiled[property_name].items():
            for rexp in rexps:
                if rexp.match(value):
                    return canonical_form
    return None

register_property('format', 'DVD', 'DVD', 'DVD-Rip', 'VIDEO-TS', 'DVDivX')
register_property('format', 'HD-DVD', 'HD-(?:DVD)?-Rip', 'HD-DVD')
register_property('format', 'BluRay', 'Blu-ray', 'B[DR]Rip')
register_property('format', 'HDTV', 'HD-TV')
register_property('format', 'DVB', 'DVB-Rip', 'DVB', 'PD-TV')
register_property('format', 'WEBRip', 'WEB-Rip')
register_property('format', 'Screener', 'DVD-SCR', 'Screener')
register_property('format', 'VHS', 'VHS')
register_property('format', 'WEB-DL', 'WEB-DL')

register_property('is3D', True, '3D')

register_property('screenSize', '360p', '(?:\d{3,}(?:\\|\/|x|\*))?360(?:i|p?x?)')
register_property('screenSize', '368p', '(?:\d{3,}(?:\\|\/|x|\*))?368(?:i|p?x?)')
register_property('screenSize', '480p', '(?:\d{3,}(?:\\|\/|x|\*))?480(?:i|p?x?)')
register_property('screenSize', '576p', '(?:\d{3,}(?:\\|\/|x|\*))?576(?:i|p?x?)')
register_property('screenSize', '720p', '(?:\d{3,}(?:\\|\/|x|\*))?720(?:i|p?x?)')
register_property('screenSize', '1080i', '(?:\d{3,}(?:\\|\/|x|\*))?1080i(?:i|p?x?)')
register_property('screenSize', '1080p', '(?:\d{3,}(?:\\|\/|x|\*))?1080(?:i|p?x?)')
register_property('screenSize', '4K', '(?:\d{3,}(?:\\|\/|x|\*))?2160(?:i|p?x?)')

register_property('videoCodec', 'XviD', 'Xvid')
register_property('videoCodec', 'DivX', 'DVDivX', 'DivX')
register_property('videoCodec', 'h264', '[hx]-264')
register_property('videoCodec', 'Rv10', 'Rv10')
register_property('videoCodec', 'Mpeg2', 'Mpeg2')

# has nothing to do here (or on filenames for that matter), but some
# releases use it and it helps to identify release groups, so we adapt
register_property('videoApi', 'DXVA', 'DXVA')

register_property('audioCodec', 'AC3', 'AC3')
register_property('audioCodec', 'DTS', 'DTS')
register_property('audioCodec', 'AAC', 'He-AAC', 'AAC-He', 'AAC')

register_property('audioChannels', '5.1', r'5\.1', 'DD5[._ ]1', '5ch')

register_property('episodeFormat', 'Minisode', r'Minisodes?')

register_properties('releaseGroup', 'ESiR', 'WAF', 'SEPTiC', r'\[XCT\]', 'iNT', 'PUKKA',
                                  'CHD', 'ViTE', 'TLF', 'FLAiTE',
                                  'MDX', 'GM4F', 'DVL', 'SVD', 'iLUMiNADOS',
                                  'aXXo', 'KLAXXON', 'NoTV', 'ZeaL', 'LOL',
                                  'CtrlHD', 'POD', 'WiKi', 'IMMERSE', 'FQM',
                                  '2HD', 'CTU', 'HALCYON', 'EbP', 'SiTV',
                                  'HDBRiSe', 'AlFleNi-TeaM', 'EVOLVE', '0TV',
                                  'TLA', 'NTB', 'ASAP', 'MOMENTUM', 'FoV', 'D-Z0N3',
                                  'TrollHD', 'ECI'
                                  )

register_properties('weakReleaseGroup', 'DEiTY', 'FiNaLe', 'UnSeeN', 'KiNGS', 'CLUE', 'DIMENSION',
                                      'SAiNTS', 'ARROW', 'EuReKA', 'SiNNERS', 'DiRTY', 'REWARD',
                                      'REPTiLE',
                                      )

register_properties('other', 'PROPER', 'REPACK', 'LIMITED', 'DualAudio', 'Audiofixed', 'R5',
                           'complete', 'classic',  # not so sure about these ones, could appear in a title
                           'ws')
