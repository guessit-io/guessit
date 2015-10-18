#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Release group
"""
import copy

from rebulk import Rebulk, Rule

from .common.formatters import cleanup
from guessit.rules.common import seps

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
    return string

_scene_next = ['extension', 'website']
_scene_previous = ['videoCodec', 'format', 'videoApi', 'audioCodec', 'audioProfile', 'videoProfile', 'audioChannels',
                   'screenSize', 'other']


class SceneReleaseGroup(Rule):
    """
    Add releaseGroup match in existing matches (scene format).

    Something.XViD-ReleaseGroup.mkv
    """
    priority = 5

    def when(self, matches, context):
        filename = matches.markers.named('path', -1)
        start, end = filename.span

        last_hole = matches.holes(start, end + 1, formatter=clean_groupname,
                                  predicate=lambda hole: cleanup(hole.value), index=-1)

        if last_hole:
            next_match = matches.next(last_hole, index=0)
            if not next_match or next_match.name in _scene_next:
                previous_match = matches.previous(last_hole, index=0)
                if not previous_match or previous_match.name in _scene_previous:
                    return last_hole

    def then(self, matches, when_response, context):
        when_response.name = 'releaseGroup'
        matches.append(when_response)


class AnimeReleaseGroup(Rule):
    """
    Add releaseGroup match in existing matches (anime format)
    ...[ReleaseGroup] Something.mkv
    """
    priority = 5

    def when(self, matches, context):
        filename = matches.markers.named('path', -1)

        # pylint:disable=bad-continuation
        group_marker = matches.markers \
            .at_match(filename,
                      lambda marker: marker.name == 'group' and
                                     matches.next(marker, lambda match: match.name == 'title', 0),
                      0)

        if group_marker:
            release_group = copy.copy(group_marker)
            release_group.marker = False
            release_group.raw_start += 1
            release_group.raw_end -= 1
            return release_group

    def then(self, matches, when_response, context):
        when_response.name = 'releaseGroup'
        matches.append(when_response)


RELEASE_GROUP = Rebulk().rules(SceneReleaseGroup, AnimeReleaseGroup)
