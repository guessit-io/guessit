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
    def is_ignored(match):
        """
        Ignore matches when scanning for title (hole)
        """
        return match.name in ['language', 'country']

    @staticmethod
    def should_keep(match, to_keep, matches, filepart, hole):
        """
        Check if this match should be accepted when ending or starting a hole.
        :param match:
        :type match:
        :param to_keep:
        :type to_keep: list[Match]
        :param matches:
        :type matches: Matches
        :param hole: the filepart match
        :type hole: Match
        :param hole: the hole match
        :type hole: Match
        :return:
        :rtype:
        """
        # Keep language if other languages exists in the filepart and if not a code.
        if match.name == 'language' and len(match) <= 3:
            return True

        outside_matches = filepart.crop(hole)
        other_languages = []
        for outside in outside_matches:
            other_languages.extend(matches.range(outside.start, outside.end,
                                                 lambda c_match: c_match.name == match.name and c_match not in to_keep))

        if not other_languages:
            return True

        return False

    @staticmethod
    def check_titles_in_filepart(filepart, matches):  # pylint: disable=too-many-locals
        """
        Find title in filepart (ignoring language)
        """
        start, end = filepart.span

        holes = matches.holes(start, end + 1, formatter=formatters(cleanup, reorder_title),
                              ignore=TitleFromPosition.is_ignored,
                              predicate=lambda hole: hole.value)

        for hole in holes:
            # pylint:disable=cell-var-from-loop

            to_remove = []
            to_keep = []

            ignored_matches = matches.range(hole.start, hole.end, TitleFromPosition.is_ignored)

            if ignored_matches:
                for ignored_match in reversed(ignored_matches):
                    # pylint:disable=undefined-loop-variable
                    trailing = matches.chain_before(hole.end, seps, predicate=lambda match: match == ignored_match)
                    if trailing and TitleFromPosition.should_keep(ignored_match, to_keep, matches, filepart, hole):
                        to_keep.append(ignored_match)
                        hole.end = ignored_match.start

                for ignored_match in ignored_matches:
                    if ignored_match not in to_keep:
                        starting = matches.chain_after(hole.start, seps, predicate=lambda match: match == ignored_match)
                        if starting and TitleFromPosition.should_keep(ignored_match, to_keep, matches, filepart, hole):
                            to_keep.append(ignored_match)
                            hole.start = ignored_match.end

            to_remove.extend(ignored_matches)
            for keep_match in to_keep:
                to_remove.remove(keep_match)

            group_markers = matches.markers.named('group')
            hole = hole.crop(group_markers, index=0)

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
