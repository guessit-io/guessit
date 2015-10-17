#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Processors
"""
from rebulk import Rebulk
from rebulk.match import Match


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


def reserve_groups_characters(matches):
    """
    Add dummy matches for groups markers than contains matches, to avoid [] {} and () characters to be used ...
    :param matches:
    :type matches:
    :return:
    :rtype:
    """
    for group in matches.markers.named('group'):
        if matches.range(group.start, group.end):
            matches.append(Match(group.start, group.start + 1, value=matches.input_string[group.start:group.start + 1],
                                 input_string=matches.input_string, private=True))
            matches.append(Match(group.end-1, group.end, value=matches.input_string[group.end-1:group.end],
                                 input_string=matches.input_string, private=True))


PROCESSORS = Rebulk().processor(prefer_last_path, reserve_groups_characters)
