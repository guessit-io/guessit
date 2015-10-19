#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Comparators
"""
from functools import cmp_to_key


def marker_comparator(matches, markers):
    """
    Builds a comparator that returns markers sorted from the most valuable to the less.

    Take the parts where matches count is higher, then when length is higher, then when position is at left.

    :param matches:
    :type matches:
    :return:
    :rtype:
    """
    def comparator(marker1, marker2):
        """
        The actual comparator function.
        """
        matches_count = len(matches.range(*marker2.span)) - len(matches.range(*marker1.span))
        if matches_count:
            return matches_count
        len_diff = len(marker2) - len(marker1)
        if len_diff:
            return len_diff
        return markers.index(marker2) - markers.index(marker1)
    return comparator


def marker_sorted(markers, matches):
    """
    Sort markers from matches, from the most valuable to the less.

    :param fileparts:
    :type fileparts:
    :param matches:
    :type matches:
    :return:
    :rtype:
    """
    return sorted(markers, key=cmp_to_key(marker_comparator(matches, markers)))
