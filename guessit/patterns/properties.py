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

_properties = []

_dash = '-'
_psep = '[\W_]?'


class _Property:
    """Represents a property configuration."""
    def __init__(self, name, canonical_form, pattern=None, confidence=1.0, span_adjust=(0, 0)):
        """
        :param name: Name of the property (format, screenSize, ...)
        :type name: string
        :param canonical_form: Unique value of the property (DVD, 720p, ...)
        :type canonical_form: string
        :param pattern: Regexp pattern
        :type pattern: string
        :param confidence: confidence
        :type confidence: float
        :param span_adjust: offset to apply to found span
        :type span_adjust: tuple (int start, int end)
        """
        self.name = name
        self.canonical_form = canonical_form
        if not pattern is None:
            self.pattern = pattern
        else:
            self.pattern = canonical_form
        self.compiled = compile_pattern(self.pattern)
        self.confidence = confidence
        self.span_adjust = span_adjust

    def __repr__(self):
        return "%s: %s" % (self.name, self.canonical_form)


def compile_pattern(pattern):
    """Compile and enhance a pattern

    :param pattern: Pattern to compile (regexp).
    :type pattern: string

    :return: The compiled pattern
    :rtype: regular expression object
    """
    return re.compile(enhance_pattern(pattern), re.IGNORECASE)


def enhance_pattern(pattern):
    """Enhance pattern to match more equivalent values.

    '-' are replaced by '[\W_]?', which matches more types of separators (or none)

    :param pattern: Pattern to enhance (regexp).
    :type pattern: string

    :return: The enhanced pattern
    :rtype: string
    """
    return pattern.replace(_dash, _psep)


def enhance_property_patterns(name):
    """Retrieve enhanced patterns of given property.

    :param name: Property name of patterns to enhance.
    :type name: string

    :return: Enhanced patterns
    :rtype: list of strings

    :deprecated: All property configuration should be done in this module

    :see: :func:`enhance_pattern`
    """
    return [enhance_pattern(prop.pattern) for prop in get_properties(name)]


def unregister_property(name, *canonical_forms):
    """Unregister a property canonical forms

    If canonical_forms are specified, only those values will be unregistered

    :param name: Property name to unregister
    :type name: string
    :param canonical_forms: Values to unregister
    :type canonical_forms: varargs of string
    """
    _properties = [prop for prop in _properties if prop.name == name and (not canonical_forms or prop.canonical_form in canonical_forms)]


def register_property(name, canonical_form, *patterns):
    """Register property with defined canonical form and patterns.

    :param name: name of the property (format, screenSize, ...)
    :type name: string
    :param canonical_form: value of the property (DVD, 720p, ...)
    :type canonical_form: string
    :param patterns: regular expression patterns to register for the property canonical_form
    :type patterns: varargs of string
    """
    for pattern in patterns:
        if isinstance(pattern, dict):
            prop = _Property(name, canonical_form, **pattern)
        elif hasattr(pattern, "__iter__"):
            prop = _Property(name, canonical_form, *pattern)
        else:
            prop = _Property(name, canonical_form, pattern)
        _properties.append(prop)


def register_properties(name, *canonical_forms):
    """Registry properties.

    :param name: name of the property (releaseGroup, ...)
    :type name: string
    :param canonical_forms: values of the property ('ESiR', 'WAF', 'SEPTiC', ...)
    :type canonical_forms: varargs of strings
    """
    for canonical_form in canonical_forms:
        register_property(name, canonical_form, canonical_form)


def unregister_all_properties():
    """Unregister all defined properties"""
    _properties.clear()


def _is_valid(string, match, entry_start, entry_end):
    """Make sure our entry is surrounded by separators, or by another entry"""
    span = _get_span(match)
    start = span[0]
    end = span[1]
    # note: sep is a regexp, but in this case using it as
    #a char sequence achieves the same goal
    sep_start = start <= 0 or string[start - 1] in sep
    sep_end = end >= len(string) or string[end] in sep
    start_by_other = start in entry_end
    end_by_other = end in entry_start
    if (sep_start or start_by_other) and (sep_end or end_by_other):
        return True
    return False


def _get_span(match):
    if match.groups():
        # if groups are defined, take only first group as a result
        return match.start(1), match.end(1)
    else:
        return match.span()


def find_properties(string):
    """Find all distinct properties for given string, sorted from longer match to shorter match.

    If no capturing group is defined in the property, value will be grabbed from the entire match.

    If one ore more capturing group is defined in the property, first capturing group will be used.

    A found property must be surrounded by separators or another found property to be returned.

    If multiple values are found for the same property, the more confident one will be returned.

    If multiple values are found for the same property and the same confidence, the longer will be returned.

    :param string: input string
    :type string: string

    :return: found properties
    :rtype: list of tuples (:class:`_Property`, tuple(start, end))

    :see: `_Property`
    :see: `register_property`
    :see: `register_properties`
    """
    result = {}

    entry_start = {}
    entry_end = {}

    entries = []
    entries_dict = {}

    for prop in get_properties():
        # FIXME: this should be done in a more flexible way...
        if prop.name in ['weakReleaseGroup']:
            continue

        match = prop.compiled.search(string)
        if match:
            entry = prop, match
            entries.append(entry)
            if not prop.name in entries_dict:
                entries_dict[prop.name] = []
            entries_dict[prop.name].append(entry)

    if entries_dict:
        for entries in entries_dict.values():
            best_prop, best_match = None, None
            if len(entries) == 1:
                best_prop, best_match = entries[0]
            else:
                for prop, match in entries:
                    if match.groups():
                        # if groups are defined, take only first group as a result
                        start, end = match.start(1), match.end(1)
                    else:
                        start, end = match.span()
                    if not best_prop or \
                    best_prop.confidence < best_prop.confidence or \
                    best_prop.confidence == best_prop.confidence and \
                    best_match.span()[1] - best_match.span()[0] < match.span()[1] - match.span()[0]:
                        best_prop, best_match = prop, match

            result[best_prop] = best_match

            best_span = _get_span(best_match)

            start = best_span[0]
            end = best_span[1]

            if start not in entry_start:
                entry_start[start] = [best_prop]
            else:
                entry_start[start].append(best_prop)

            if end not in entry_end:
                entry_end[end] = [best_prop]
            else:
                entry_end[end].append(best_prop)

    while True:
        invalid_values = []
        for prop, match in result.items():
            if not _is_valid(string, match, entry_start, entry_end):
                invalid_values.append((prop, match))
        if not invalid_values:
            break
        for prop, match in invalid_values:
            result.pop(prop)
            invalid_span = _get_span(match)
            start = invalid_span[0]
            end = invalid_span[1]
            entry_start[start].remove(prop)
            if not entry_start.get(start):
                del entry_start[start]
            entry_end[end].remove(prop)
            if not entry_end.get(end):
                del entry_end[end]

    ret = []
    for prop, match in result.items():
        ret.append((prop, match))

    def _sorting(x):
        _, x_match = x
        x_start, x_end = x_match.span()
        return (x_start - x_end)

    ret.sort(key=_sorting)

    ret2 = []
    for prop, match in ret:
        ret2.append((prop, _get_span(match)))
    return ret2


def compute_canonical_form(name, value):
    """Retrieves canonical form of a property given its name and found value.

    :param name: name of the property
    :type name: string
    :param value: found value of the property
    :type value: string

    :return: Canonical form of a property, None otherwise.
    :rtype: string
    """
    if isinstance(value, base_text_type):
        for prop in get_properties(name):
            if prop.compiled.match(value):
                return prop.canonical_form
    return None


def get_properties(name=None, canonical_form=None):
    """Retrieve properties

    :return: Properties
    :rtype: generator
    """
    for prop in _properties:
        if name is None or prop.name == name and canonical_form is None or prop.canonical_form is None:
            yield prop


register_property('format', 'DVD', 'DVD', 'DVD-Rip', 'VIDEO-TS', 'DVDivX')
register_property('format', 'HD-DVD', 'HD-(?:DVD)?-Rip', 'HD-DVD')
register_property('format', 'BluRay', 'Blu-ray', 'B[DR]Rip')
register_property('format', 'HDTV', 'HD-TV')
register_property('format', 'DVB', 'DVB-Rip', 'DVB', 'PD-TV')
register_property('format', 'WEBRip', 'WEB-Rip')
register_property('format', 'VHS', 'VHS')
register_property('format', 'WEB-DL', 'WEB-DL')

for prop in get_properties('format'):
    register_property('isScreener', True, prop.pattern + '(-?Scr(?:eener)?)')
register_property('isScreener', True, 'Screener')

register_property('is3D', True, '3D')

register_property('isFinalEpisode', True, 'final')

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
                                  'TrollHD', 'ECI', 'MARINE-FORD'
                                  )

register_properties('weakReleaseGroup', 'DEiTY', 'FiNaLe', 'UnSeeN', 'KiNGS', 'CLUE', 'DIMENSION',
                                      'SAiNTS', 'ARROW', 'EuReKA', 'SiNNERS', 'DiRTY', 'REWARD',
                                      'REPTiLE',
                                      )

register_properties('other', 'PROPER', 'REPACK', 'LIMITED', 'DualAudio', 'Audiofixed', 'R5',
                           'complete', 'classic',  # not so sure about these ones, could appear in a title
                           'ws')
