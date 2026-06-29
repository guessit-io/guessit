#!/usr/bin/env python
"""Tests for the typed Key registry (guessit.rules.common.keys)."""

from typing import Any

from rebulk import Key

from ..api import guessit
from ..rules.common import keys as keys_module
from ..schema import GUESSIT_SCHEMA

#: Registry key names that are internal match names, renamed before output and
#: therefore absent from GUESSIT_SCHEMA. ``bit_rate`` becomes ``audio_bit_rate`` /
#: ``video_bit_rate`` (see ``BitRateTypeRule``).
_INTERNAL_NAMES = {"bit_rate"}


def _registry() -> list[Key[Any]]:
    return [value for value in vars(keys_module).values() if isinstance(value, Key)]


def test_registry_keys_are_well_formed() -> None:
    registry = _registry()
    assert registry, "the Key registry should not be empty"
    for key in registry:
        assert key.name, f"{key!r} has an empty name"
        assert isinstance(key.value_type, type), f"{key.name} value_type must be a type"
        assert callable(key.converter), f"{key.name} converter must be callable"


def test_registry_key_names_are_unique() -> None:
    names = [key.name for key in _registry()]
    assert len(names) == len(set(names)), f"duplicate key names: {names}"


def test_emitted_key_names_exist_in_schema() -> None:
    for key in _registry():
        if key.name in _INTERNAL_NAMES:
            continue
        assert key.name in GUESSIT_SCHEMA, f"key {key.name!r} is not an emitted property"


def test_registry_formatter_applies_end_to_end() -> None:
    # A config-driven property whose formatter now comes from the registry Key
    # (film -> int via FILM.converter) must still yield the typed value.
    assert guessit("James_Bond-f21-Casino_Royale.mkv").get("film") == 21
