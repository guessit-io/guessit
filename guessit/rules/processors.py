#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Processors
"""
from rebulk import Rebulk


def prefer_last_path(matches):
    """
    If multiple match are found, keep the one in filename part.

    :param matches:
    :param context:
    :return:
    """
    filename = matches.markers.named('path', -1)
    for name in matches.names:
        named_list = matches.named(name)
        if len(named_list) > 1:
            keep_list = []
            for named in named_list:
                marker = matches.markers.at_match(named, lambda marker: marker is filename, 0)
                if marker:
                    keep_list.append(named)
            if keep_list:
                for named in named_list:
                    if named not in keep_list:
                        matches.remove(named)


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

PROCESSORS = Rebulk().processor(prefer_last_path, enlarge_group_matches)
