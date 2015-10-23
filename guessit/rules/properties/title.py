#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title
"""
from rebulk import Rebulk, AppendMatchRule, RemoveMatchRule

from ..common.formatters import cleanup
from ..common.comparators import marker_sorted
from ..common import seps


class TitleFromPosition(AppendMatchRule):
    """
    Add title match in existing matches
    """
    priority = 10

    @staticmethod
    def ignore_language(match):
        """
        Ignore language included in the possible title (hole)
        """
        return match.name == 'language'

    @staticmethod
    def check_title_in_filepart(filepart, matches):
        """
        Find title in filepart (ignoring language)
        """
        start, end = filepart.span

        first_hole = matches.holes(start, end + 1, formatter=cleanup, ignore=TitleFromPosition.ignore_language,
                                   predicate=lambda hole: hole.value, index=0)

        to_remove = []

        if first_hole:
            title_languages = matches.range(first_hole.start, first_hole.end, lambda match: match.name == 'language')

            if title_languages:
                to_keep = []

                hole_trailing_language = title_languages[-1]

                if hole_trailing_language and \
                        not matches.input_string[hole_trailing_language.end:first_hole.end].strip(seps):
                    # We have a language at end of title.
                    # Keep it if other languages exists in the filepart and if note a code
                    other_languages = matches.range(filepart.start, filepart.end,
                                                    lambda match: match.name == 'language'
                                                    and match != hole_trailing_language)
                    if not other_languages or len(hole_trailing_language) <= 3:
                        first_hole.end = hole_trailing_language.start
                        to_keep.append(hole_trailing_language)

                hole_starting_language = title_languages[0]
                if hole_starting_language and hole_starting_language not in to_keep and \
                        not matches.input_string[first_hole.start:hole_starting_language.start].strip(seps):
                    # We have a language at start of title.
                    # Keep it if other languages exists in the filepart and if not a code.
                    other_languages = matches.range(filepart.start, filepart.end,
                                                    lambda match: match.name == 'language'
                                                    and match != hole_starting_language)

                    if not other_languages or len(hole_starting_language) <= 3:
                        first_hole.start = hole_starting_language.end
                        to_keep.append(hole_starting_language)

                to_remove.extend(title_languages)
                for keep_match in to_keep:
                    to_remove.remove(keep_match)

            group_markers = matches.markers.named('group')
            title = first_hole.crop(group_markers, index=0)

            if title and title.value:
                return title, to_remove
        return None, None

    def when(self, matches, context):
        fileparts = list(marker_sorted(matches.markers.named('path'), matches))

        to_remove = []

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
            title, to_remove_c = TitleFromPosition.check_title_in_filepart(filepart, matches)
            if title:
                ret.append(title)
                title.name = 'title'
                to_remove.extend(to_remove_c)
                break

        # Add title match in all fileparts containing the year.
        for filepart in years_fileparts:
            title, to_remove_c = TitleFromPosition.check_title_in_filepart(filepart, matches)
            if title:
                ret.append(title)
                title.name = 'title'
                to_remove.extend(to_remove_c)

        return ret, to_remove

    def then(self, matches, when_response, context):
        titles, to_remove = when_response
        super(TitleFromPosition, self).then(matches, titles, context)
        for to_remove in when_response[1]:
            matches.remove(to_remove)


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
