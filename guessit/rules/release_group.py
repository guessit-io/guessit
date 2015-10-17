#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Release group
"""
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


class SceneReleaseGroup(Rule):
    """
    Add title match in existing matches
    """
    priority = 5

    def when(self, matches, context):
        filename = matches.markers.named('path', -1)
        start, end = filename.span

        first_hole = matches.holes(start, end+1, formatter=clean_groupname,
                                   predicate=lambda hole: cleanup(hole.value), index=-1)
        return first_hole

    def then(self, matches, when_response, context):
        when_response.name = 'releaseGroup'
        matches.append(when_response)


RELEASE_GROUP = Rebulk().rules(SceneReleaseGroup)
