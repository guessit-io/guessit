#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title
"""
from rebulk import Rebulk, RemoveMatchRule, AppendRemoveMatchRule
from rebulk.formatters import formatters

from ..common.formatters import cleanup, reorder_title
from ..common.comparators import marker_sorted
from ..common import seps
from rebulk.rules import AppendRemoveMatchRule


class TitleFromPosition(AppendRemoveMatchRule):
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
    def check_title_in_filepart(filepart, matches):  # pylint: disable=too-many-locals
        """
        Find title in filepart (ignoring language)
        """
        start, end = filepart.span

        first_hole = matches.holes(start, end + 1, formatter=formatters(cleanup, reorder_title),
                                   ignore=TitleFromPosition.ignore_language,
                                   predicate=lambda hole: hole.value, index=0)

        to_remove = []

        if first_hole:
            title_languages = matches.range(first_hole.start, first_hole.end, lambda match: match.name == 'language')

            if title_languages:
                to_keep = []

                hole_trailing_languages = matches.chain_before(first_hole.end, seps,
                                                               predicate=lambda match: match.name == 'language')

                if hole_trailing_languages:
                    # We have one or many language at end of title.
                    # Keep it if other languages exists in the filepart and if note a code
                    other_languages = matches.range(filepart.start, filepart.end,
                                                    lambda match: match.name == 'language'
                                                    and match not in hole_trailing_languages)
                    for hole_trailing_language in hole_trailing_languages:
                        if not other_languages or len(hole_trailing_language) <= 3:
                            first_hole.end = hole_trailing_language.start
                            to_keep.append(hole_trailing_language)

                hole_starting_languages = matches.chain_after(first_hole.start, seps,
                                                              predicate=lambda match: match.name == 'language' and
                                                              match not in to_keep)

                if hole_starting_languages:
                    # We have one or many language at start of title.
                    # Keep it if other languages exists in the filepart and if not a code.
                    other_languages = matches.range(filepart.start, filepart.end,
                                                    lambda match: match.name == 'language'
                                                    and match not in hole_starting_languages)

                    for hole_starting_language in hole_starting_languages:
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


class PreferTitleWithYear(RemoveMatchRule):
    """
    Prefer title where filepart contains year.
    """
    priority = -255

    def when(self, matches, context):
        to_keep = []
        to_remove = []

        for title in matches.named('title'):
            filepart = matches.markers.at_match(title, lambda marker: marker.name == 'path', 0)
            if filepart:
                year_match = matches.range(filepart.start, filepart.end, lambda match: match.name == 'year', 0)
                if year_match:
                    to_keep.append(title)
                else:
                    to_remove.append(title)

        if to_keep:
            title_values = set([title.value for title in to_keep])
            if len(title_values) > 1:
                # We have distinct values for title with year. Keep only values from most valuable filepart.
                fileparts = marker_sorted(matches.markers.named('path'), matches)
                best_title = None
                for filepart in fileparts:
                    best_title = matches.range(filepart.start, filepart.end, lambda match: match.name == 'title', 0)
                    if best_title:
                        break
                for title in to_keep:
                    if title.value != best_title.value:
                        to_remove.append(title)
                        to_keep.remove(title)
            return to_remove


TITLE = Rebulk().rules(TitleFromPosition, PreferTitleWithYear)
