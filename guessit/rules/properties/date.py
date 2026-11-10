#!/usr/bin/env python
"""
date, week and year properties
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from rebulk import Rebulk, RemoveMatch, Rule

from ...reutils import build_or_pattern
from ..common import dash, seps
from ..common.date import search_date, valid_week, valid_year
from ..common.pattern import is_disabled
from ..common.validators import and_, seps_surround

if TYPE_CHECKING:
    from rebulk.match import Match, Matches


def date(config: dict[str, Any]) -> Rebulk:
    """
    Builder for rebulk object.

    :param config: rule configuration
    :type config: dict
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk().defaults(validator=seps_surround)

    rebulk.regex(
        r"\d{4}",
        name="year",
        formatter=int,
        disabled=lambda context: is_disabled(context, "year"),
        conflict_solver=lambda match, other: (
            other if other.name in ("episode", "season") and len(other.raw) < len(match.raw) else "__default__"
        ),
        validator=lambda match: seps_surround(match) and valid_year(match.value),
    )

    rebulk.chain(
        tags=["year-range"],
        flags=re.IGNORECASE,
        children=True,
        private_parent=True,
        validate_all=True,
        validator={"__parent__": and_(seps_surround, _is_ascending_year_range), "year": _is_valid_year_match},
        formatter={"year": int},
        conflict_solver=lambda match, other: (
            other if other.name in ("episode", "season") and len(other.raw) <= len(match.raw) else "__default__"
        ),
        disabled=lambda context: is_disabled(context, "year"),
    ).defaults(tags=["year-range"], validator=None, private_parent=True).regex(r"(?P<year>\d{4})").regex(
        _year_range_separator_pattern(config["year_range_separators"]) + r"(?P<year>\d{4})"
    )

    rebulk.regex(
        build_or_pattern(config["week_words"]) + r"-?(\d{1,2})",
        name="week",
        formatter=int,
        children=True,
        flags=re.IGNORECASE,
        abbreviations=[dash],
        conflict_solver=lambda match, other: (
            other if other.name in ("episode", "season") and len(other.raw) < len(match.raw) else "__default__"
        ),
        validator=lambda match: seps_surround(match) and valid_week(match.value),
    )

    def date_functional(string: str, context: dict[str, Any]) -> tuple[int, int, dict[str, Any]] | None:
        """
        Search for date in the string and retrieves match

        :param string:
        :return:
        """

        ret = search_date(
            string, context.get("date_year_first"), context.get("date_day_first"), context.get("type") == "movie"
        )
        if ret:
            return ret[0], ret[1], {"value": ret[2]}
        return None

    rebulk.functional(
        date_functional,
        name="date",
        properties={"date": [None]},
        disabled=lambda context: is_disabled(context, "date"),
        conflict_solver=lambda match, other: other if other.name in ("episode", "season", "crc32") else "__default__",
    )

    rebulk.rules(
        KeepMarkedYearInFilepart,
        AbsorbWeekdayPrefix(config["weekday_words"]),
        PreferLeadingYearAsEpisodeTitle,
    )

    return rebulk


def _year_range_separator_pattern(separators: list[str]) -> str:
    word_separators = [separator for separator in separators if separator.isalpha()]
    symbol_separators = [separator for separator in separators if not separator.isalpha()]
    padding = "[ ._]"
    alternatives = []
    if symbol_separators:
        alternatives.append(padding + "*" + build_or_pattern(symbol_separators, escape=True) + padding + "*")
    if word_separators:
        alternatives.append(padding + "+" + build_or_pattern(word_separators, escape=True) + padding + "+")
    return "(?:" + "|".join(alternatives) + ")"


def _is_valid_year_match(match: Match) -> bool:
    return valid_year(int(match.value))


def _is_ascending_year_range(match: Match) -> bool:
    years = [int(year.value) for year in match.children.named("year")]
    return len(years) == 2 and years[0] < years[1]


class AbsorbWeekdayPrefix(Rule):
    """
    Absorb a weekday word glued to a date into the ``date`` match (upstream #794).

    ``A.Place.in.the.Sun.S2025E01.Thu.2.Jan.2025.Mar.Menor.Spain...`` parses ``2 Jan 2025`` as the
    air date but the leading "Thu" is the broadcast weekday, not the title. The interior date splits
    the title hole in two, so ``EpisodeTitleFromPosition`` fills the first hole ("Thu") and drops the
    real title after the date ("Mar Menor Spain"). Growing the date span to cover the adjacent weekday
    removes that first hole, so the title after the date is reclaimed instead.

    Only a weekday directly preceding the date (separators only between, and not already claimed by
    another match) is absorbed; the parsed date value is unchanged.
    """

    consequence = RemoveMatch

    def __init__(self, weekday_words: list[str]) -> None:
        super().__init__()
        seps_class = "[" + re.escape(seps) + "]"
        self.weekday_re = re.compile(
            r"(?:^|" + seps_class + r")(" + build_or_pattern(weekday_words) + r")" + seps_class + r"*$",
            re.IGNORECASE,
        )

    def enabled(self, context: dict[str, Any] | None) -> bool:
        return not is_disabled(context, "date")

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        input_string = matches.input_string or ""
        ret: list[tuple[Match, int]] = []
        for date_match in matches.named("date"):
            filepart = matches.markers.at_match(date_match, lambda m: m.name == "path", 0)
            lower = filepart.start if filepart else 0
            weekday = self.weekday_re.search(input_string[lower : date_match.start])
            if not weekday:
                continue
            new_start = lower + weekday.start(1)
            # Only absorb a free weekday word; never swallow a token already claimed by a match.
            if matches.range(new_start, date_match.start, predicate=lambda m: not m.private):
                continue
            ret.append((date_match, new_start))
        return ret

    def then(self, matches: Matches, when_response: Any, context: dict[str, Any] | None) -> None:
        for date_match, new_start in when_response:
            matches.remove(date_match)
            date_match.start = new_start
            matches.append(date_match)


class KeepMarkedYearInFilepart(Rule):
    """
    Keep first years marked with [](){} in filepart, or if no year is marked, ensure it won't override titles.

    The two years of a ``YYYY-YYYY`` range count as a single year: they are kept or removed together,
    and a range is never released to the title.
    """

    priority = 64
    consequence = RemoveMatch

    def enabled(self, context: dict[str, Any] | None) -> bool:
        return not is_disabled(context, "year")

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        ret: list[Match] = []
        if len(matches.named("year")) > 1:
            for filepart in matches.markers.named("path"):
                years = matches.range(filepart.start, filepart.end, lambda match: match.name == "year")
                range_spans = {year.span for year in years if "year-range" in year.tags}
                duplicates = [year for year in years if "year-range" not in year.tags and year.span in range_spans]
                ret.extend(duplicates)
                units = _year_units([year for year in years if year not in duplicates])
                if len(units) > 1:
                    group_units: list[list[Match]] = []
                    ungroup_units: list[list[Match]] = []
                    for unit in units:
                        if any(matches.markers.at_match(year, lambda marker: marker.name == "group") for year in unit):
                            group_units.append(unit)
                        else:
                            ungroup_units.append(unit)
                    if group_units and ungroup_units:
                        ret.extend(year for unit in ungroup_units + group_units[1:] for year in unit)
                    elif not group_units:
                        first_unit_is_range = len(ungroup_units[0]) > 1
                        kept = 1 if first_unit_is_range else 2
                        if not first_unit_is_range:
                            ret.extend(ungroup_units[0])  # Keep first year for title.
                        ret.extend(year for unit in ungroup_units[kept:] for year in unit)
        return ret


def _year_units(years: list[Match]) -> list[list[Match]]:
    units: list[list[Match]] = []
    ranges: dict[int, list[Match]] = {}
    for year in years:
        chain = _root_parent(year) if "year-range" in year.tags else None
        if chain is None:
            units.append([year])
        elif id(chain) in ranges:
            ranges[id(chain)].append(year)
        else:
            ranges[id(chain)] = [year]
            units.append(ranges[id(chain)])
    return units


def _root_parent(match: Match) -> Match | None:
    root = match.parent
    while root is not None and root.parent is not None:
        root = root.parent
    return root


class PreferLeadingYearAsEpisodeTitle(Rule):
    """Prefer a lone leading year-range number as the title of episode files.

    A filename like 1923.S01E01.mkv is an episode of a show titled "1923":
    with an episode marker present, a lone number leading the filepart is
    more likely the title than the year. 1883 and 24 already parse that way
    only because they fall outside the year range. Release the year match so
    the title rules can pick the number up.
    """

    priority = 32  # After the year rules (64), before the title rules (0).
    consequence = RemoveMatch

    def enabled(self, context: dict[str, Any] | None) -> bool:
        # with date parsing excluded, a leading number followed by 2-digit
        # groups is more likely a date's year component than a title
        return (
            not is_disabled(context, "year") and not is_disabled(context, "date") and not is_disabled(context, "title")
        )

    def when(self, matches: Matches, context: dict[str, Any] | None) -> list[Match]:
        to_remove: list[Match] = []
        for filepart in matches.markers.named("path"):
            years = matches.range(filepart.start, filepart.end, lambda match: match.name == "year")
            if len(years) != 1:
                continue
            year = years[0]
            if year.start != filepart.start:
                continue
            episode_markers = matches.range(
                filepart.start, filepart.end, lambda match: match.name in ("episode", "season")
            )
            if not episode_markers:
                continue
            first_marker = min(episode_markers, key=lambda match: match.start)
            if first_marker.start <= year.end:
                continue
            # allow the leading part of the episode marker's own token
            # (e.g. the 'S' of S01E01), which no match covers by itself
            input_string = matches.input_string or ""
            token_start = first_marker.start
            while token_start > year.end and input_string[token_start - 1] not in seps:
                token_start -= 1
            # the year must be the only content before the episode token
            if any(match is not year for match in matches.range(filepart.start, token_start)):
                continue
            if any(char not in seps for char in input_string[year.end : token_start]):
                continue
            to_remove.append(year)
        return to_remove
