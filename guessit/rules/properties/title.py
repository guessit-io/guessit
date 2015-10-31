#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title
"""
from guessit.rules.properties.film import FilmTitleRule
from guessit.rules.properties.language import SubtitlePrefixLanguageRule, SubtitleSuffixLanguageRule, \
    SubtitleExtensionRule
from rebulk import Rebulk, Rule, AppendMatch, RemoveMatch
from rebulk.formatters import formatters

from ..common.formatters import cleanup, reorder_title
from ..common.comparators import marker_sorted
from ..common import seps, title_seps


class TitleFromPosition(Rule):
    """
    Add title match in existing matches
    """
    consequence = [AppendMatch, RemoveMatch]
    dependency = [FilmTitleRule, SubtitlePrefixLanguageRule, SubtitleSuffixLanguageRule, SubtitleExtensionRule]

    @staticmethod
    def ignore_language(match):
        """
        Ignore language included in the possible title (hole)
        """
        return match.name in ['language', 'country']

    @staticmethod
    def check_titles_in_filepart(filepart, matches):  # pylint: disable=too-many-locals
        """
        Find title in filepart (ignoring language)
        """
        start, end = filepart.span

        holes = matches.holes(start, end + 1, formatter=formatters(cleanup, reorder_title),
                              ignore=TitleFromPosition.ignore_language,
                              predicate=lambda hole: hole.value)

        to_remove = []

        for hole in holes:
            # pylint:disable=cell-var-from-loop
            group_markers = matches.markers.named('group')
            hole = hole.crop(group_markers, index=0)

            title_languages = matches.range(hole.start, hole.end, lambda match: match.name == 'language')

            if title_languages:
                to_keep = []

                hole_trailing_languages = matches.chain_before(hole.end, seps,
                                                               predicate=lambda match: match.name == 'language')

                if hole_trailing_languages:
                    # We have one or many language at end of title.
                    # Keep it if other languages exists in the filepart and if not a code
                    other_languages = matches.range(filepart.start, filepart.end,
                                                    lambda match: match.name == 'language'
                                                    and match not in hole_trailing_languages)
                    for hole_trailing_language in hole_trailing_languages:
                        if not other_languages or len(hole_trailing_language) <= 3:
                            hole.end = hole_trailing_language.start
                            to_keep.append(hole_trailing_language)

                hole_starting_languages = matches.chain_after(hole.start, seps,
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
                            hole.start = hole_starting_language.end
                            to_keep.append(hole_starting_language)

                to_remove.extend(title_languages)
                for keep_match in to_keep:
                    to_remove.remove(keep_match)

            if hole and hole.value:
                hole.name = 'title'
                hole.tags = ['title']
                # Split and keep values that can be a title
                titles = hole.split(title_seps, lambda match: match.value)
                for title in titles[1:]:
                    title.name = 'alternativeTitle'
                return titles, to_remove

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
            titles = TitleFromPosition.check_titles_in_filepart(filepart, matches)
            if titles:
                titles, to_remove_c = titles
                ret.extend(titles)
                to_remove.extend(to_remove_c)
                break

        # Add title match in all fileparts containing the year.
        for filepart in years_fileparts:
            titles = TitleFromPosition.check_titles_in_filepart(filepart, matches)
            if titles:
                titles, to_remove_c = titles
                ret.extend(titles)
                to_remove.extend(to_remove_c)

        return ret, to_remove


class PreferTitleWithYear(Rule):
    """
    Prefer title where filepart contains year.
    """
    dependency = TitleFromPosition
    consequence = RemoveMatch

    def when(self, matches, context):
        with_year = []
        titles = matches.named('title')

        for title in titles:
            filepart = matches.markers.at_match(title, lambda marker: marker.name == 'path', 0)
            if filepart:
                year_match = matches.range(filepart.start, filepart.end, lambda match: match.name == 'year', 0)
                if year_match:
                    with_year.append(title)

        if with_year:
            title_values = set([title.value for title in with_year])
        else:
            title_values = set([title.value for title in titles])

        to_remove = []
        for title in titles:
            if title.value not in title_values:
                to_remove.append(title)
        return to_remove


TITLE = Rebulk().rules(TitleFromPosition, PreferTitleWithYear)
