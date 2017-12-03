#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
screen_size property
"""
from rebulk.match import Match
from rebulk.remodule import re

from rebulk import Rebulk, Rule, RemoveMatch, AppendMatch

from ..common.pattern import is_enabled
from ..common.validators import seps_surround
from ..common import dash, seps
from ...reutils import build_or_pattern

interlaced = frozenset({'360', '480', '576', '900', '1080'})
progressive = frozenset(interlaced | {'368', '720', '2160', '4320'})


def screen_size():
    """
    Builder for rebulk object.
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk(disabled=lambda context: not is_enabled(context, 'screen_size'))
    rebulk = rebulk.string_defaults(ignore_case=True).regex_defaults(flags=re.IGNORECASE)

    rebulk.defaults(name='screen_size', validator=seps_surround, abbreviations=[dash], private_children=True)

    res_pattern = r'(?:(?P<width>\d{3,4})(?:x|\*))?'
    rebulk.regex(res_pattern + build_or_pattern(interlaced, name='height') + r'(?P<scan_type>i)(?:24|30|50|60|120)?')
    rebulk.regex(res_pattern + build_or_pattern(progressive, name='height') + r'(?P<scan_type>p)(?:24|30|50|60|120)?')
    rebulk.regex(res_pattern + build_or_pattern(progressive, name='height') + r'(?P<scan_type>p)?(?:hd)')
    rebulk.regex(res_pattern + build_or_pattern(progressive, name='height') + r'(?P<scan_type>p)?x?')
    rebulk.string('4k', value='2160p')
    rebulk.regex(r'(?P<width>\d{3,4})-?(?:x|\*)-?(?P<height>\d{3,4})',
                 conflict_solver=lambda match, other: '__default__' if other.name == 'screen_size' else other)

    rebulk.rules(PostProcessScreenSize(progressive), ScreenSizeOnlyOne, RemoveScreenSizeConflicts)

    return rebulk


class PostProcessScreenSize(Rule):
    """
    Process the screen size calculating the aspect ratio if available.

    Convert to a standard notation (720p, 1080p, etc) when it's a standard resolution and
    aspect ratio is valid or not available.

    It also creates an aspect_ratio match when available.
    """
    consequence = AppendMatch

    def __init__(self, standard_heights, min_ar=1.333, max_ar=1.898):
        super(PostProcessScreenSize, self).__init__()
        self.standard_heights = standard_heights
        self.min_ar = min_ar
        self.max_ar = max_ar

    def when(self, matches, context):
        to_append = []
        for match in matches.named('screen_size'):
            values = match.children.to_dict()
            if 'height' not in values:
                continue

            scan_type = (values.get('scan_type') or 'p').lower()
            height = values['height']
            if 'width' not in values:
                match.value = '{0}{1}'.format(height, scan_type)
                continue

            width = values['width']
            calculated_ar = float(width) / float(height)

            aspect_ratio = Match(match.start, match.end, input_string=match.input_string,
                                 name='aspect_ratio', value=round(calculated_ar, 3))
            to_append.append(aspect_ratio)
            if height in self.standard_heights and self.min_ar < calculated_ar < self.max_ar:
                match.value = '{0}{1}'.format(height, scan_type)
            else:
                match.value = '{0}x{1}'.format(width, height)

        return to_append


class ScreenSizeOnlyOne(Rule):
    """
    Keep a single screen_size per filepath part.
    """
    consequence = RemoveMatch

    def when(self, matches, context):
        to_remove = []
        for filepart in matches.markers.named('path'):
            screensize = list(reversed(matches.range(filepart.start, filepart.end,
                                                     lambda match: match.name == 'screen_size')))
            if len(screensize) > 1 and len(set((match.value for match in screensize))) > 1:
                to_remove.extend(screensize[1:])

        return to_remove


class RemoveScreenSizeConflicts(Rule):
    """
    Remove season and episode matches which conflicts with screen_size match.
    """
    consequence = RemoveMatch

    def when(self, matches, context):
        to_remove = []
        for filepart in matches.markers.named('path'):
            screensize = matches.range(filepart.start, filepart.end, lambda match: match.name == 'screen_size', 0)
            if not screensize:
                continue

            conflicts = matches.conflicting(screensize, lambda match: match.name in ('season', 'episode'))
            if not conflicts:
                continue

            video_profile = matches.range(screensize.end, filepart.end, lambda match: match.name == 'video_profile', 0)
            if video_profile and not matches.holes(screensize.end, video_profile.start,
                                                   predicate=lambda h: h.value and h.value.strip(seps)):
                to_remove.extend(conflicts)

            previous = matches.previous(screensize, index=0, predicate=(
                lambda m: m.name in ('date', 'source', 'other', 'streaming_service')))
            if previous and not matches.holes(previous.end, screensize.start,
                                              predicate=lambda h: h.value and h.value.strip(seps)):
                to_remove.extend(conflicts)

        return to_remove
