#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Release group
"""
import copy
from guessit.rules.common.validators import int_coercable
from guessit.rules.properties.title import TitleFromPosition

from rebulk import Rebulk, Rule, AppendMatch

from ..common.formatters import cleanup
from ..common import seps
from ..common.comparators import marker_sorted

forbidden_groupnames = ['rip', 'by', 'for', 'par', 'pour', 'bonus']

groupname_seps = ''.join([c for c in seps if c not in '[]{}()'])


def clean_groupname(string):
    """
    Removes and strip separators from input_string
    :param input_string:
    :type input_string:
    :return:
    :rtype:
    """
    string = string.strip(groupname_seps)
    for forbidden in forbidden_groupnames:
        if string.lower().startswith(forbidden):
            string = string[len(forbidden):]
            string = string.strip(groupname_seps)
        if string.lower().endswith(forbidden):
            string = string[:len(forbidden)]
            string = string.strip(groupname_seps)
    return string


_scene_previous = ['videoCodec', 'format', 'videoApi', 'audioCodec', 'audioProfile', 'videoProfile', 'audioChannels',
                   'screenSize']


class SceneReleaseGroup(Rule):
    """
    Add releaseGroup match in existing matches (scene format).

    Something.XViD-ReleaseGroup.mkv
    """
    dependency = TitleFromPosition
    consequence = AppendMatch

    def when(self, matches, context):
        ret = []

        for filepart in marker_sorted(matches.markers.named('path'), matches):
            start, end = filepart.span

            last_hole = matches.holes(start, end + 1, formatter=clean_groupname,
                                      predicate=lambda hole: cleanup(hole.value), index=-1)

            if last_hole:
                previous_match = matches.previous(last_hole, index=0)
                if previous_match and previous_match.name in _scene_previous and \
                        not matches.input_string[previous_match.end:last_hole.start].strip(seps)\
                        and not int_coercable(last_hole.value.strip(seps)):
                    last_hole.name = 'releaseGroup'
                    last_hole.tags = ['scene']
                    ret.append(last_hole)
        return ret


class AnimeReleaseGroup(Rule):
    """
    Add releaseGroup match in existing matches (anime format)
    ...[ReleaseGroup] Something.mkv
    """
    dependency = [SceneReleaseGroup, TitleFromPosition]
    consequence = AppendMatch

    def when(self, matches, context):
        ret = []

        # If a scene releaseGroup is found, ignore this kind of releaseGroup rule.
        if matches.named('releaseGroup', lambda match: 'scene' in match.tags):
            return ret

        for filepart in marker_sorted(matches.markers.named('path'), matches):

            # pylint:disable=bad-continuation
            empty_group_marker = matches.markers \
                .range(filepart.start, filepart.end, lambda marker: marker.name == 'group'
                       and not matches.range(marker.start, marker.end)
                       and not int_coercable(marker.value.strip(seps)), 0)

            if empty_group_marker:
                release_group = copy.copy(empty_group_marker)
                release_group.marker = False
                release_group.raw_start += 1
                release_group.raw_end -= 1
                release_group.name = 'releaseGroup'
                ret.append(release_group)
        return ret


RELEASE_GROUP = Rebulk().rules(SceneReleaseGroup, AnimeReleaseGroup)
