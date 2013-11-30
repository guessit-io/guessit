#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
# Copyright (c) 2013 Rémi Alvergnat <toilal.dev@gmail.com>
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

from . import compile_pattern, enhance_pattern, sep

from .. import base_text_type
from ..guess import Guess


class _Property:
    """Represents a property configuration."""
    def __init__(self, name, canonical_form, pattern=None, confidence=1.0, span_adjust=(0, 0), enhance=True):
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
        self.compiled = compile_pattern(self.pattern, enhance=enhance)
        self.confidence = confidence
        self.span_adjust = span_adjust

    def __repr__(self):
        return "%s: %s" % (self.name, self.canonical_form)


class PropertiesContainer(object):
    def __init__(self, enhance_patterns=True, canonical_from_pattern=True):
        self._properties = []
        self.enhance_patterns = enhance_patterns
        self.canonical_from_pattern = canonical_from_pattern

    def unregister_property(self, name, *canonical_forms):
        """Unregister a property canonical forms

        If canonical_forms are specified, only those values will be unregistered

        :param name: Property name to unregister
        :type name: string
        :param canonical_forms: Values to unregister
        :type canonical_forms: varargs of string
        """
        _properties = [prop for prop in self._properties if prop.name == name and (not canonical_forms or prop.canonical_form in canonical_forms)]

    def register_property(self, name, canonical_form, *patterns):
        """Register property with defined canonical form and patterns.

        :param name: name of the property (format, screenSize, ...)
        :type name: string
        :param canonical_form: value of the property (DVD, 720p, ...)
        :type canonical_form: string
        :param patterns: regular expression patterns to register for the property canonical_form
        :type patterns: varargs of string
        """
        for pattern in patterns:
            if not canonical_form and self.canonical_from_pattern:
                canonical_form = pattern
            params = {'enhance': self.enhance_patterns}
            if isinstance(pattern, dict):
                params.update(pattern)
                prop = _Property(name, canonical_form, **params)
            elif hasattr(pattern, "__iter__"):
                prop = _Property(name, canonical_form, *pattern, **params)
            else:
                prop = _Property(name, canonical_form, pattern, **params)
            self._properties.append(prop)

    def register_properties(self, name, *canonical_forms):
        """Register properties.

        :param name: name of the property (releaseGroup, ...)
        :type name: string
        :param canonical_forms: values of the property ('ESiR', 'WAF', 'SEPTiC', ...)
        :type canonical_forms: varargs of strings
        """
        for canonical_form in canonical_forms:
            self.register_property(name, None, canonical_form)

    def unregister_all_properties(self):
        """Unregister all defined properties"""
        self._properties.clear()

    def _is_valid(self, string, match, entry_start, entry_end):
        """Make sure our entry is surrounded by separators, or by another entry"""
        span = self._get_span(match)
        start = span[0]
        end = span[1]
        # note: sep is a regexp, but in this case using it as
        # a char sequence achieves the same goal
        sep_start = start <= 0 or string[start - 1] in sep
        sep_end = end >= len(string) or string[end] in sep
        start_by_other = start in entry_end
        end_by_other = end in entry_start
        if (sep_start or start_by_other) and (sep_end or end_by_other):
            return True
        return False

    def _get_span(self, match):
        if match.groups():
            # if groups are defined, take only first group as a result
            return match.start(1), match.end(1)
        else:
            return match.span()

    def find_properties(self, string, name=None):
        """Find all distinct properties for given string, sorted from longer match to shorter match.

        If no capturing group is defined in the property, value will be grabbed from the entire match.

        If one ore more capturing group is defined in the property, first capturing group will be used.

        A found property must be surrounded by separators or another found property to be returned.

        If multiple values are found for the same property, the more confident one will be returned.

        If multiple values are found for the same property and the same confidence, the longer will be returned.

        :param string: input string
        :type string: string

        :param name: name of property to find
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

        for prop in self.get_properties(name):
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

                best_span = self._get_span(best_match)

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
                if not self._is_valid(string, match, entry_start, entry_end):
                    invalid_values.append((prop, match))
            if not invalid_values:
                break
            for prop, match in invalid_values:
                result.pop(prop)
                invalid_span = self._get_span(match)
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
            ret2.append((prop, self._get_span(match)))
        return ret2

    def as_guess(self, found_property, input=None, index=0):
        if found_property:
            prop, span = found_property[index]
            value = prop.canonical_form if prop.canonical_form else input[span[0]:span[1]] if input else None
            guess = Guess({prop.name: value}, confidence=prop.confidence, input=input, span=span, property=prop)
            return guess
        return None

    def compute_canonical_form(self, name, value):
        """Retrieves canonical form of a property given its name and found value.

        :param name: name of the property
        :type name: string
        :param value: found value of the property
        :type value: string

        :return: Canonical form of a property, None otherwise.
        :rtype: string
        """
        if isinstance(value, base_text_type):
            for prop in self.get_properties(name):
                if prop.compiled.match(value):
                    return prop.canonical_form
        return None

    def get_properties(self, name=None, canonical_form=None):
        """Retrieve properties

        :return: Properties
        :rtype: generator
        """
        for prop in self._properties:
            if name is None or prop.name == name and canonical_form is None or prop.canonical_form is None:
                yield prop

    def get_supported_properties(self):
        supported_properties = {}
        for prop in self.get_properties():
            values = supported_properties.get(prop.name)
            if not values:
                values = set()
                supported_properties[prop.name] = values
            values.add(prop.canonical_form if prop.canonical_form else "<any>")
        return supported_properties

    def enhance_property_patterns(self, name):
        """Retrieve enhanced patterns of given property.

        :param name: Property name of patterns to enhance.
        :type name: string

        :return: Enhanced patterns
        :rtype: list of strings

        :deprecated: All property configuration should be done in this module

        :see: :func:`enhance_pattern`
        """
        return [enhance_pattern(prop.pattern) for prop in self.get_properties(name)]
