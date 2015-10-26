#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Processors
"""
from collections import defaultdict
from rebulk import Rebulk

from .common.comparators import marker_sorted


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
    to_remove = []
    for filepart in fileparts:
        current_filepart_values = defaultdict(list)

        filepart_matches = matches.range(filepart.start, filepart.end)

        current_filepart_names = set()
        for match in filepart_matches:
            current_filepart_names.add(match.name)
            if match.name in previous_fileparts_names:
                if match.value not in current_filepart_values[match.name]:
                    to_remove.append(match)
            else:
                if match.value not in current_filepart_values[match.name]:
                    current_filepart_values[match.name].append(match.value)

        previous_fileparts_names.update(current_filepart_names)

    for match in to_remove:
        matches.remove(match)


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


PROCESSORS = Rebulk().processor(enlarge_group_matches).post_processor(remove_ambiguous)
