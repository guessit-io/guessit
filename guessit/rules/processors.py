#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Processors
"""
from __future__ import unicode_literals

from collections import defaultdict
import copy
from rebulk import Rebulk

from .common.formatters import strip
from .common.comparators import marker_sorted
from .common.date import valid_year

from .properties.type import type_processor
from .properties.mimetype import mimetype_processor

import six


def remove_ambiguous(matches):
    """
    If multiple match are found with same name and different values, keep the one in the most valuable filepart.
    Also keep others match with same name and values than those kept ones.

    :param matches:
    :param context:
    :return:
    """
    fileparts = marker_sorted(matches.markers.named('path'), matches)

    previous_fileparts_names = set()
    values = defaultdict(list)

    to_remove = []
    for filepart in fileparts:
        filepart_matches = matches.range(filepart.start, filepart.end)

        filepart_names = set()
        for match in filepart_matches:
            filepart_names.add(match.name)
            if match.name in previous_fileparts_names:
                if match.value not in values[match.name]:
                    to_remove.append(match)
            else:
                if match.value not in values[match.name]:
                    values[match.name].append(match.value)

        previous_fileparts_names.update(filepart_names)

    for match in to_remove:
        matches.remove(match)


def country_in_title(matches):
    """
    If country and title are found, append country value to title as 2-letter code
    :param matches:
    :type matches:
    :return:
    :rtype:
    """
    country = matches.named('country', index=0)
    titles = matches.named('title')
    if country and titles:
        for title in titles:
            title.value += ' (%s)' % country.value


def _preferred_string(value1, value2):  # pylint:disable=too-many-return-statements
    """
    Retrieves preferred title from both values.
    :param value1:
    :type value1: str
    :param value2:
    :type value2: str
    :return: The preferred title
    :rtype: str
    """
    if value1 and not value2:
        return value1
    if value2 and not value1:
        return value2
    if value1 == value2:
        return value1
    if value1.istitle() and not value2.istitle():
        return value1
    if value2.istitle() and not value1.istitle():
        return value2
    if value1[0].isupper() and not value1[0].isupper():
        return value1
    if value2[0].isupper() and not value1[0].isupper():
        return value2
    return value1


def equivalent_holes(matches):
    """
    Creates equivalent matches for holes that have same values than existing (case insensitive)
    :param matches:
    :type matches:
    :return:
    :rtype:
    """
    new_matches = []

    for filepath in marker_sorted(matches.markers.named('path'), matches):
        holes = matches.holes(start=filepath.start, end=filepath.end, formatter=strip)
        for name in matches.names:
            for hole in list(holes):
                for current_match in matches.named(name):
                    if isinstance(current_match.value, six.string_types) and \
                                    hole.value.lower() == current_match.value.lower():
                        new_value = _preferred_string(hole.value, current_match.value)
                        if hole.value != new_value:
                            hole.value = new_value
                        if current_match.value != new_value:
                            current_match.value = new_value
                        hole.name = name
                        hole.tags = ['equivalent']
                        new_matches.append(hole)
                        if hole in holes:
                            holes.remove(hole)

    for new_match in new_matches:
        matches.append(new_match)


def season_year(matches):
    """
    If a season is a valid year and no year was found, create an match with year.
    :param matches:
    :type matches:
    :return:
    :rtype:
    """
    if not matches.named('year'):
        for season in matches.named('season'):
            if valid_year(season.value):
                year = copy.copy(season)
                year.name = 'year'
                matches.append(year)


def enlarge_group_matches(matches):
    """
    Enlarge matches that are starting and/or ending group to include brackets in their span.
    :param matches:
    :type matches:
    :return:
    :rtype:
    """
    for group in matches.markers.named('group'):
        for match in matches.starting(group.start + 1):
            matches.remove(match)
            match.start -= 1
            match.raw_start += 1
            matches.append(match)

        for match in matches.ending(group.end - 1):
            matches.remove(match)
            match.end += 1
            match.raw_end -= 1
            matches.append(match)


PROCESSORS = Rebulk().processor(enlarge_group_matches).post_processor(equivalent_holes, remove_ambiguous,
                                                                      country_in_title, season_year, mimetype_processor,
                                                                      type_processor)
