#!/usr/bin/env python
"""
other property
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rebulk import POST_PROCESS, AppendMatch, Rebulk, RemoveMatch, RenameMatch, Rule
from rebulk.match import Match
from rebulk.remodule import re

from ...config import load_config_patterns
from ...reutils import build_or_pattern
from ...rules.common.formatters import raw_cleanup
from ..common import dash, seps
from ..common.pattern import is_disabled
from ..common.validators import and_, seps_after, seps_before, seps_surround

if TYPE_CHECKING:
    from collections.abc import Iterable

    from rebulk.match import Matches


def other(config: dict[str, Any]) -> Rebulk:
    """
    Builder for rebulk object.

    :param config: rule configuration
    :type config: dict
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk(disabled=lambda context: is_disabled(context, "other"))
    rebulk = rebulk.regex_defaults(flags=re.IGNORECASE, abbreviations=[dash]).string_defaults(ignore_case=True)
    rebulk.defaults(name="other", validator=seps_surround)

    load_config_patterns(rebulk, config.get("other"))

    rebulk.rules(
        RenameAnotherToOther,
        ValidateHasNeighbor,
        ValidateHasNeighborAfter,
        ValidateHasNeighborBefore,
        ValidateScreenerRule,
        ValidateMuxRule,
        ValidateHardcodedSubs,
        ValidateStreamingServiceNeighbor,
        ValidateAtEnd,
        ValidateReal,
        ProperCountRule,
    )

    return rebulk


def complete_words(rebulk: Rebulk, season_words: Iterable[str], complete_article_words: Iterable[str]) -> None:
    """
    Custom pattern to find complete seasons from words.
    """
    season_words_pattern = build_or_pattern(season_words)
    complete_article_words_pattern = build_or_pattern(complete_article_words)

    def validate_complete(match: Match) -> bool:
        """
        Make sure season word is are defined.
        :param match:
        :type match:
        :return:
        :rtype:
        """
        children = match.children
        return not (not children.named("completeWordsBefore") and not children.named("completeWordsAfter"))

    rebulk.regex(
        "(?P<completeArticle>"
        + complete_article_words_pattern
        + "-)?"
        + "(?P<completeWordsBefore>"
        + season_words_pattern
        + "-)?"
        + "Complete"
        + "(?P<completeWordsAfter>-"
        + season_words_pattern
        + ")?",
        private_names=["completeArticle", "completeWordsBefore", "completeWordsAfter"],
        value={"other": "Complete"},
        tags=["release-group-prefix"],
        validator={"__parent__": and_(seps_surround, validate_complete)},
    )


class ProperCountRule(Rule):
    """
    Add proper_count property
    """

    priority = POST_PROCESS

    consequence = AppendMatch

    properties = {"proper_count": [None]}

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        propers = matches.named("other", lambda match: match.value == "Proper")
        if propers:
            raws: dict[str, Match] = {}  # Count distinct raw values
            for proper in propers:
                raws[raw_cleanup(proper.raw or "")] = proper

            value = 0
            start: int | None = None
            end: int | None = None

            proper_count_matches: list[Match] = []

            for proper in raws.values():
                if not start or start > proper.start:
                    start = proper.start
                if not end or end < proper.end:
                    end = proper.end
                proper_count = proper.children.named("proper_count", 0)
                if proper_count:
                    value += int(proper_count.value)
                elif "real" in proper.tags:
                    value += 2
                else:
                    value += 1

            assert start is not None
            assert end is not None
            proper_count_match = Match(name="proper_count", start=start, end=end, input_string=matches.input_string)
            proper_count_match.value = value
            proper_count_matches.append(proper_count_match)

            return proper_count_matches
        return None


class RenameAnotherToOther(Rule):
    """
    Rename `another` properties to `other`
    """

    priority = 32
    consequence = RenameMatch("other")

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        return matches.named("another")


class ValidateHasNeighbor(Rule):
    """
    Validate tag has-neighbor
    """

    consequence = RemoveMatch
    priority = 64

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        ret: list[Match] = []
        for to_check in matches.range(predicate=lambda match: "has-neighbor" in match.tags):
            previous_match = matches.previous(to_check, index=0)
            previous_group = matches.markers.previous(to_check, lambda marker: marker.name == "group", 0)
            if previous_group and (not previous_match or previous_group.end > previous_match.end):
                previous_match = previous_group
            if previous_match and not (matches.input_string or "")[previous_match.end : to_check.start].strip(seps):
                break
            next_match = matches.next(to_check, index=0)
            next_group = matches.markers.next(to_check, lambda marker: marker.name == "group", 0)
            if next_group and (not next_match or next_group.start < next_match.start):
                next_match = next_group
            if next_match and not (matches.input_string or "")[to_check.end : next_match.start].strip(seps):
                break
            ret.append(to_check)
        return ret


class ValidateHasNeighborBefore(Rule):
    """
    Validate tag has-neighbor-before that previous match exists.
    """

    consequence = RemoveMatch
    priority = 64

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        ret: list[Match] = []
        for to_check in matches.range(predicate=lambda match: "has-neighbor-before" in match.tags):
            next_match = matches.next(to_check, index=0)
            next_group = matches.markers.next(to_check, lambda marker: marker.name == "group", 0)
            if next_group and (not next_match or next_group.start < next_match.start):
                next_match = next_group
            if next_match and not (matches.input_string or "")[to_check.end : next_match.start].strip(seps):
                break
            ret.append(to_check)
        return ret


class ValidateHasNeighborAfter(Rule):
    """
    Validate tag has-neighbor-after that next match exists.
    """

    consequence = RemoveMatch
    priority = 64

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        ret: list[Match] = []
        for to_check in matches.range(predicate=lambda match: "has-neighbor-after" in match.tags):
            previous_match = matches.previous(to_check, index=0)
            previous_group = matches.markers.previous(to_check, lambda marker: marker.name == "group", 0)
            if previous_group and (not previous_match or previous_group.end > previous_match.end):
                previous_match = previous_group
            if previous_match and not (matches.input_string or "")[previous_match.end : to_check.start].strip(seps):
                break
            ret.append(to_check)
        return ret


class ValidateScreenerRule(Rule):
    """
    Validate tag other.validate.screener
    """

    consequence = RemoveMatch
    priority = 64

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        ret: list[Match] = []
        for screener in matches.named("other", lambda match: "other.validate.screener" in match.tags):
            source_match = matches.previous(screener, lambda match: match.initiator.name == "source", 0)
            if not source_match or (matches.input_string or "")[source_match.end : screener.start].strip(seps):
                ret.append(screener)
        return ret


class ValidateMuxRule(Rule):
    """
    Validate tag other.validate.mux
    """

    consequence = RemoveMatch
    priority = 64

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        ret: list[Match] = []
        for mux in matches.named("other", lambda match: "other.validate.mux" in match.tags):
            source_match = matches.previous(mux, lambda match: match.initiator.name == "source", 0)
            if not source_match:
                ret.append(mux)
        return ret


class ValidateHardcodedSubs(Rule):
    """Validate HC matches."""

    priority = 32
    consequence = RemoveMatch

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        to_remove: list[Match] = []
        for hc_match in matches.named("other", predicate=lambda match: match.value == "Hardcoded Subtitles"):
            next_match = matches.next(hc_match, predicate=lambda match: match.name == "subtitle_language", index=0)
            if next_match and not matches.holes(
                hc_match.end, next_match.start, predicate=lambda match: match.value.strip(seps)
            ):
                continue

            previous_match = matches.previous(
                hc_match, predicate=lambda match: match.name == "subtitle_language", index=0
            )
            if previous_match and not matches.holes(
                previous_match.end, hc_match.start, predicate=lambda match: match.value.strip(seps)
            ):
                continue

            to_remove.append(hc_match)

        return to_remove


class ValidateStreamingServiceNeighbor(Rule):
    """Validate streaming service's neighbors."""

    priority = 32
    consequence = RemoveMatch

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        to_remove: list[Match] = []
        for match in matches.named(
            "other",
            predicate=lambda m: (
                m.initiator.name != "source"
                and ("streaming_service.prefix" in m.tags or "streaming_service.suffix" in m.tags)
            ),
        ):
            match = match.initiator
            if not seps_after(match):
                if "streaming_service.prefix" in match.tags:
                    next_match = matches.next(match, lambda m: m.name == "streaming_service", 0)
                    if next_match and not matches.holes(
                        match.end, next_match.start, predicate=lambda m: m.value.strip(seps)
                    ):
                        continue
                if match.children:
                    to_remove.extend(match.children)
                to_remove.append(match)

            elif not seps_before(match):
                if "streaming_service.suffix" in match.tags:
                    previous_match = matches.previous(match, lambda m: m.name == "streaming_service", 0)
                    if previous_match and not matches.holes(
                        previous_match.end, match.start, predicate=lambda m: m.value.strip(seps)
                    ):
                        continue

                if match.children:
                    to_remove.extend(match.children)
                to_remove.append(match)

        return to_remove


class ValidateAtEnd(Rule):
    """Validate other which should occur at the end of a filepart."""

    priority = 32
    consequence = RemoveMatch

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        to_remove: list[Match] = []
        for filepart in matches.markers.named("path"):
            for match in matches.range(
                filepart.start, filepart.end, predicate=lambda m: m.name == "other" and "at-end" in m.tags
            ):
                if matches.holes(match.end, filepart.end, predicate=lambda m: m.value.strip(seps)) or matches.range(
                    match.end, filepart.end, predicate=lambda m: m.name not in ("other", "container")
                ):
                    to_remove.append(match)

        return to_remove


class ValidateReal(Rule):
    """
    Validate Real
    """

    consequence = RemoveMatch
    priority = 64

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        ret: list[Match] = []
        for filepart in matches.markers.named("path"):
            for match in matches.range(filepart.start, filepart.end, lambda m: m.name == "other" and "real" in m.tags):
                if not matches.range(filepart.start, match.start):
                    ret.append(match)

        return ret
