#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title
"""
from rebulk import Rebulk, AppendMatchRule, RemoveMatchRule

from ..common.formatters import cleanup
from ..common.comparators import marker_sorted


class TitleFromPosition(AppendMatchRule):
    """
    Add title match in existing matches
    """
    priority = 10

    @staticmethod
    def check_title_in_filepart(filepart, matches):
        """
        Find title in filepart
        """
        start, end = filepart.span

        first_hole = matches.holes(start, end + 1, formatter=cleanup, predicate=lambda hole: hole.value, index=0)
        if first_hole:
            group_markers = matches.markers.named('group')
            title = first_hole.crop(group_markers, index=0)
            if title:
                return title

    def when(self, matches, context):
        fileparts = list(marker_sorted(matches.markers.named('path'), matches))

        # Priorize fileparts containing the year
        years_fileparts = []
        for filepart in fileparts:
            year_match = matches.range(filepart.start, filepart.end, lambda match: match.name == 'year', 0)
            if year_match:
                years_fileparts.append(filepart)

        ret = []
        for filepart in fileparts:
            try:
                years_fileparts.remove(filepart)
            except ValueError:
                pass
            title = TitleFromPosition.check_title_in_filepart(filepart, matches)
            if title:
                ret.append(title)
                title.name = 'title'
                break

        # Add title match in all fileparts containing the year.
        for filepart in years_fileparts:
            title = TitleFromPosition.check_title_in_filepart(filepart, matches)
            if title:
                ret.append(title)
                title.name = 'title'

        return ret


class PreferTitleWithYear(RemoveMatchRule):
    """
    Prefer title where filepart contains year.
    """
    priority = -255

    def when(self, matches, context):
        with_year = []
        without_year = []

        for title in matches.named('title'):
            filepart = matches.markers.at_match(title, lambda marker: marker.name == 'path', 0)
            if filepart:
                year_match = matches.range(filepart.start, filepart.end, lambda match: match.name == 'year', 0)
                if year_match:
                    with_year.append(title)
                else:
                    without_year.append(title)

        if with_year:
            return without_year


TITLE = Rebulk().rules(TitleFromPosition, PreferTitleWithYear)
