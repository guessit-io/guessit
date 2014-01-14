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

from __future__ import absolute_import, division, print_function, unicode_literals

from . import compile_pattern, enhance_pattern, sep

from .. import base_text_type
from ..guess import Guess


class _Property:
    """Represents a property configuration."""
    def __init__(self, name, canonical_form, pattern=None, confidence=1.0, enhance=True, global_span=False, weak=False):
        """
        :param name: Name of the property (format, screenSize, ...)
        :type name: string
        :param canonical_form: Unique value of the property (DVD, 720p, ...)
        :type canonical_form: string
        :param pattern: Regexp pattern
        :type pattern: string
        :param confidence: confidence
        :type confidence: float
        :param enhance: enhance the pattern
        :type enhance: boolean
        :param global_span: if True, the whole match span will used to create the Guess.
                            Else, the span from the capturing groups will be used.
        :type global_span: boolean
        :param weak: if True, the match property is weak and could be part of the title
        :type weak: boolean
        """
        self.name = name
        self.canonical_form = canonical_form
        if not pattern is None:
            self.pattern = pattern
        else:
            self.pattern = canonical_form
        self.compiled = compile_pattern(self.pattern, enhance=enhance)
        self.confidence = confidence
        self.global_span = global_span
        self.weak = weak

    def __repr__(self):
        return "%s: %s" % (self.name, self.canonical_form)


class PropertiesContainer(object):
    def __init__(self, enhance_patterns=True, canonical_from_pattern=True):
        self._properties = []
        self._eqs = {}
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

    def register_property(self, name, canonical_form, *patterns, **property_params):
        """Register property with defined canonical form and patterns.

        :param name: name of the property (format, screenSize, ...)
        :type name: string
        :param canonical_form: value of the property (DVD, 720p, ...)
        :type canonical_form: string
        :param patterns: regular expression patterns to register for the property canonical_form
        :type patterns: varargs of string
        """
        properties = []
        for pattern in patterns:
            if not canonical_form and self.canonical_from_pattern:
                canonical_form = pattern
            params = {'enhance': self.enhance_patterns}
            params.update(property_params)
            if isinstance(pattern, dict):
                params.update(pattern)
                prop = _Property(name, canonical_form, **params)
            else:
                prop = _Property(name, canonical_form, pattern, **params)
            self._properties.append(prop)
            properties.append(prop)
        return properties

    def register_properties(self, name, *canonical_forms, **property_params):
        """Register properties.

        :param name: name of the property (releaseGroup, ...)
        :type name: string
        :param canonical_forms: values of the property ('ESiR', 'WAF', 'SEPTiC', ...)
        :type canonical_forms: varargs of strings
        """
        properties = []
        for canonical_form in canonical_forms:
            properties.extend(self.register_property(name, None, canonical_form, **property_params))
        return properties

    def unregister_all_properties(self):
        """Unregister all defined properties"""
        self._properties.clear()

    def _is_valid(self, string, match, entry_start, entry_end):
        """Make sure our entry is surrounded by separators, or by another entry"""
        span = match.span()
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

    def _get_match_groups(self, prop, match):
        """
        Retrieves groups from match

        :return: list of group names
        """
        if match.groupdict():
            # if groups are defined, take only first group as a result
            results = []
            for k in match.groupdict().keys():
                span = match.span(k)
                if span[0] > -1:
                    results.append(k)
            return results
        else:
            if match.groups():
                return [1]
            else:
                return [None]

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
        :rtype: list of tuples (:class:`_Property`, match, list of tuples (property_name, tuple(value_start, value_end)))

        :see: `_Property`
        :see: `register_property`
        :see: `register_properties`
        """
        result = {}

        entry_start = {}
        entry_end = {}

        entries = []

        ret = []

        if not string.strip():
            return ret

        # search all properties
        for prop in self.get_properties(name):
            match = prop.compiled.search(string)
            if match:
                entry = prop, match
                entries.append(entry)

        # compute entries start and ends
        for prop, match in entries:
            span = match.span()
            start = span[0]
            end = span[1]

            if start not in entry_start:
                entry_start[start] = [prop]
            else:
                entry_start[start].append(prop)

            if end not in entry_end:
                entry_end[end] = [prop]
            else:
                entry_end[end].append(prop)

        # remove invalid values
        while True:
            invalid_entries = []
            for entry in entries:
                prop, match = entry
                if not self._is_valid(string, match, entry_start, entry_end):
                    invalid_entries.append(entry)
            if not invalid_entries:
                break
            for entry in invalid_entries:
                prop, match = entry
                entries.remove(entry)
                invalid_span = match.span()
                start = invalid_span[0]
                end = invalid_span[1]
                entry_start[start].remove(prop)
                if not entry_start.get(start):
                    del entry_start[start]
                entry_end[end].remove(prop)
                if not entry_end.get(end):
                    del entry_end[end]

        # keep only best match if multiple values where found
        entries_dict = {}
        for entry in entries:
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

        for prop, match in result.items():
            ret.append((prop, match))

        def _sorting(x):
            _, x_match = x
            x_start, x_end = x_match.span()
            return (x_start - x_end)

        ret.sort(key=_sorting)

        ret2 = []
        for prop, match in ret:
            groups = self._get_match_groups(prop, match)
            ret2.append((prop, match, groups))
        return ret2

    def as_guess(self, found_properties, input=None, filter=None, sep_replacement=None, *args, **kwargs):
        if filter is None:
            filter = lambda property, *args, **kwargs: True
        for property in found_properties:
            prop, match, property_results = property
            property_name = self._effective_prop_name(prop.name)
            guess = Guess(confidence=prop.confidence, input=input, span=match.span(), prop=property_name, weak=prop.weak)
            span_start, span_end = match.span()
            for group_name in property_results:
                if isinstance(group_name, int):
                    if group_name == 1:
                        span_start = match.span(group_name)[0]
                    span_end = match.span(group_name)[1]
                value = self._effective_prop_value(prop, input, match.span(group_name) if group_name else match.span(), sep_replacement)
                name = self._effective_prop_name(group_name if isinstance(group_name, base_text_type) else property_name)
                guess[name] = value
                if group_name:
                    guess.metadata(prop).span = match.span(group_name)
            guess.metadata().span = match.span() if prop.global_span else (span_start, span_end)
            if filter(guess):
                return guess
        return None

    def _effective_prop_value(self, prop, input=None, span=None, sep_replacement=None):
        if prop.canonical_form:
            return prop.canonical_form
        if input is None:
            return None
        value = input
        if not span is None:
            value = value[span[0]:span[1]]
        value = input[span[0]:span[1]] if input else None
        if sep_replacement:
            for sep_char in sep:
                value = value.replace(sep_char, sep_replacement)
        return value

    def _effective_prop_name(self, name):
        return name if not name in self._eqs else self._eqs[name]

    def register_equivalent(self, name, equivalent_name):
        self._eqs[equivalent_name] = name

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
            if (name is None or prop.name == name) and (canonical_form is None or prop.canonical_form == canonical_form):
                yield prop

    def get_supported_properties(self):
        supported_properties = {}
        for prop in self.get_properties():
            name = self._effective_prop_name(prop.name)
            values = supported_properties.get(name)
            if not values:
                values = set()
                supported_properties[name] = values
            if prop.canonical_form:
                values.add(prop.canonical_form)
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
