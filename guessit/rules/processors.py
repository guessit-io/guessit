#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Processors
"""
from rebulk import Rebulk

from .common.comparators import marker_sorted


def prefer_last_path(matches):
    """
    If multiple match are found with same name, keep the one in the most valuable filepart.
    Also keep others match with same value than those in most valuable filepart.

    :param matches:
    :param context:
    :return:
    """
    filepart = marker_sorted(matches.markers.named('path'), matches)[0]
    for name in matches.names:
        name_matches = matches.named(name)
        if len(name_matches) > 1:
            keep_list = []
            keep_values = []
            for name_match in name_matches:
                marker = matches.markers.at_match(name_match, lambda marker: marker is filepart, 0)
                if marker:
                    keep_list.append(name_match)
                    keep_values.append(name_match.value)

            for name_match in name_matches:
                if name_match not in keep_list and name_match.value in keep_values:
                    keep_list.append(name_match)

            if keep_list:
                for name_match in name_matches:
                    if name_match not in keep_list:
                        matches.remove(name_match)


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


PROCESSORS = Rebulk().processor(enlarge_group_matches).post_processor(prefer_last_path)
