#!/usr/bin/env python
"""
Lexical-coherence scoring for title candidates.

A cheap, deterministic proxy for "does this run of words read as a real title phrase"
(not a grammatical parse): a multilingual function-word backbone plus an alphabetic ratio.
Used to arbitrate which candidate segment becomes the primary title.
"""

from __future__ import annotations

from rebulk.remodule import re

# Closed multilingual set of function words (en / fr / es / it / de) that signal a real
# language phrase rather than a bag of tokens. Romaji particles are intentionally excluded:
# they collide with release tokens and the arbiter is scoped to Latin-language phrases.
FUNCTION_WORDS = frozenset(
    {
        # en
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "in",
        "on",
        "at",
        "for",
        "from",
        "by",
        "with",
        "into",
        "onto",
        "no",
        # fr
        "le",
        "la",
        "les",
        "un",
        "une",
        "de",
        "du",
        "des",
        "et",
        "ou",
        "dans",
        "sur",
        "pour",
        "par",
        "avec",
        # es
        "el",
        "los",
        "las",
        "y",
        "en",
        "con",
        "por",
        "para",
        "del",
        # it
        "il",
        "lo",
        "gli",
        "i",
        "uno",
        "una",
        "di",
        "da",
        "della",
        "delle",
        "dei",
        # de
        "der",
        "die",
        "das",
        "und",
        "oder",
        "von",
        "zu",
        "mit",
        "im",
    }
)

_WORD_SPLIT = re.compile(r"[^0-9a-zà-ÿ]+", re.IGNORECASE)


def _words(text: str) -> list[str]:
    return [word for word in _WORD_SPLIT.split(text.lower()) if word]


def title_cohesion(text: str) -> float:
    """
    Score how much ``text`` reads as a language phrase (higher = more title-like).

    Combines the fraction of function words (phrase backbone) with the fraction of
    alphabetic (non-numeric) words. Returns 0.0 for empty / non-word input.

    A language phrase outscores a release-site host:

    >>> title_cohesion("The Wheel of Time") > title_cohesion("www Tamilblasters party")
    True
    >>> title_cohesion("")
    0.0
    """
    words = _words(text)
    if not words:
        return 0.0
    function = sum(1 for word in words if word in FUNCTION_WORDS)
    alphabetic = sum(1 for word in words if not word.isdigit())
    return function / len(words) + alphabetic / len(words)
