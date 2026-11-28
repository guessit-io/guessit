#!/usr/bin/env python
"""
language_variant property

Refines :mod:`language` for release tags that tell regional or original-version
variants apart (French ``VFF``, ``VFQ``, ``VOF``, ...).

The vocabulary is data, not code: every variant and its facets live in
``advanced_config.language_variant``. A variant token yields both the
``language_variant`` property and the ``language`` facet's language on the same
span, so the audio language keeps being reported exactly as before.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import babelfish
from rebulk import AppendMatch, Rebulk, Rule
from rebulk.match import Match

from ..common.pattern import is_disabled
from ..common.validators import seps_surround

if TYPE_CHECKING:
    from rebulk.match import Matches


def language_variant(config: dict[str, Any]) -> Rebulk:
    """
    Builder for rebulk object.

    :param config: rule configuration
    :type config: dict
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk(disabled=lambda context: is_disabled(context, "language_variant"))

    for variant, variant_config in config.items():
        if variant.startswith("_"):
            continue
        tokens = variant_config.get("tokens")
        if not tokens:
            continue
        rebulk.string(
            *tokens,
            name="language_variant",
            value=variant,
            ignore_case=True,
            validator=seps_surround,
            tags=["language-variant"],
        )

    rebulk.rules(LanguageVariantLanguageRule(config))

    return rebulk


class LanguageVariantLanguageRule(Rule):
    """Add the ``language`` facet of every ``language_variant`` match on the same span."""

    consequence = AppendMatch
    priority = 64

    properties = {"language": [None]}

    def __init__(self, config: dict[str, Any]) -> None:
        """Constructor."""
        super().__init__()
        self.variants = config

    def enabled(self, context: dict[str, Any] | None) -> bool:
        return not is_disabled(context, "language_variant") and not is_disabled(context, "language")

    def when(self, matches: Matches, context: dict[str, Any] | None) -> Any:
        allowed_languages = self._allowed_languages(context)
        to_append: list[Match] = []
        for match in matches.named("language_variant"):
            variant_config = self.variants.get(match.value)
            if not variant_config:
                continue
            facet = variant_config.get("language")
            if not facet:
                continue
            try:
                language = babelfish.Language.fromguessit(facet)
            except babelfish.Error:
                continue
            if allowed_languages and not (
                language.alpha3.lower() in allowed_languages
                or (language.alpha2 and language.alpha2.lower() in allowed_languages)
                or (language.name and language.name.lower() in allowed_languages)
            ):
                continue
            already_found = any(
                other.start == match.start and other.end == match.end for other in matches.named("language")
            )
            if already_found:
                continue
            to_append.append(
                Match(
                    match.start,
                    match.end,
                    name="language",
                    value=language,
                    input_string=matches.input_string,
                )
            )
        return to_append

    @staticmethod
    def _allowed_languages(context: dict[str, Any] | None) -> set[str]:
        """Languages the caller allows, lowercased."""
        if not context:
            return set()
        return {str(language).lower() for language in context.get("allowed_languages") or []}
