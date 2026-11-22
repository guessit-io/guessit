#!/usr/bin/env python
"""
API functions that can be used by external software
"""

from __future__ import annotations

import os
import threading
import traceback
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING, Any, NamedTuple, cast

from rebulk.introspector import introspect

from .__version__ import __version__
from .options import load_config, merge_options, parse_options
from .rules import rebulk_builder
from .schema_builder import build_json_schema, overlay_config_enums
from .schema_generated import GUESSIT_SCHEMA

if TYPE_CHECKING:
    from collections.abc import Callable, Hashable

    from rebulk import Rebulk


class GuessitException(Exception):
    """
    Exception raised when guessit fails to perform a guess because of an internal error.
    """

    def __init__(self, string: Any, options: Any) -> None:
        super().__init__(
            "An internal error has occurred in guessit.\n"
            "===================== Guessit Exception Report =====================\n"
            f"version={__version__}\n"
            f"string={string!s}\n"
            f"options={options!s}\n"
            "--------------------------------------------------------------------\n"
            f"{traceback.format_exc()}"
            "--------------------------------------------------------------------\n"
            "Please report at "
            "https://github.com/guessit-io/guessit/issues.\n"
            "===================================================================="
        )

        self.string = string
        self.options = options


def configure(options: Any = None, rules_builder: Callable[..., Rebulk] | None = None, force: bool = False) -> None:
    """
    Load configuration files and initialize rebulk rules if required.

    :param options:
    :type options: dict
    :param rules_builder:
    :type rules_builder:
    :param force:
    :type force: bool
    :return:
    """
    default_api.configure(options, rules_builder=rules_builder, force=force)


def reset() -> None:
    """
    Reset api internal state.
    """
    default_api.reset()


def guessit(string: str | Path | bytes, options: Any = None) -> dict[str, Any]:
    """
    Retrieves all matches from string as a dict
    :param string: the filename or release name
    :type string: str
    :param options:
    :type options: str|dict
    :return:
    :rtype:
    """
    return default_api.guessit(string, options)


def properties(options: Any = None) -> dict[str, Any]:
    """
    Retrieves all properties with possible values that can be guessed
    :param options:
    :type options: str|dict
    :return:
    :rtype:
    """
    return default_api.properties(options)


def schema(options: Any = None) -> dict[str, Any]:
    """
    Retrieve the property schema (type, cardinality and enums) for the effective configuration
    :param options:
    :type options: str|dict
    :return:
    :rtype: dict
    """
    return default_api.schema(options)


def json_schema(options: Any = None) -> dict[str, Any]:
    """
    Retrieve the draft-07 JSON Schema of the output for the effective configuration
    :param options:
    :type options: str|dict
    :return:
    :rtype: dict
    """
    return default_api.json_schema(options)


def suggested_expected(titles: Any, options: Any = None) -> list[Any]:
    """
    Return a list of suggested titles to be used as `expected_title` based on the list of titles
    :param titles: the filename or release name
    :type titles: list|set|dict
    :param options:
    :type options: str|dict
    :return:
    :rtype: list of str
    """
    return default_api.suggested_expected(titles, options)


def _complete_properties(ordered: dict[str, Any]) -> dict[str, Any]:
    """Make ``properties()`` code-complete against :data:`GUESSIT_SCHEMA`.

    Value-constrained properties advertise their full declared enum (unioned with
    whatever introspection found); every other schema property is guaranteed to be
    present, with ``[None]`` marking a free/computed value.
    """
    for name, spec in GUESSIT_SCHEMA.items():
        current = ordered.get(name) or []
        enum = spec.get("enum")
        if enum:
            # Union, deduplicating scalars while preserving any compound values
            # already present (e.g. edition's ['Ultimate', 'Collector']).
            merged = list(current)
            seen = {value for value in current if not isinstance(value, list)}
            for value in enum:
                if value not in seen:
                    merged.append(value)
                    seen.add(value)
            ordered[name] = sorted(merged, key=str)
        elif not current:
            ordered[name] = [None]
    # Newly added keys are appended; re-sort so the key order stays alphabetical
    # (the contract introspection already followed before completion).
    return dict(sorted(ordered.items(), key=lambda item: str(item[0])))


class _Configured(NamedTuple):
    """What a call runs with: the rule set and the effective options built for its options."""

    config: dict[str, Any]
    advanced_config: Any
    rebulk: Rebulk
    options: dict[str, Any]


def _freeze(value: Any) -> Hashable:
    """Hashable form of sanitized options, equal for equal options. Raises TypeError if a value can't be hashed."""
    if isinstance(value, dict):
        return dict, frozenset((key, _freeze(item)) for key, item in value.items())
    if isinstance(value, (set, frozenset)):
        return frozenset, frozenset(_freeze(item) for item in value)
    if isinstance(value, (list, tuple)):
        return type(value), tuple(_freeze(item) for item in value)
    hash(value)
    return cast("Hashable", value)


class GuessItApi:
    """
    An api class that can be configured with custom Rebulk configuration.

    The effective options of the last ``configured_cache_size`` option sets are kept, along with their rule
    set; option sets whose ``advanced_config`` differs each need their own rule set, and only the last
    ``rule_set_cache_size`` rule sets are kept. Setting either size to 0 disables the cache.
    """

    configured_cache_size = 16
    rule_set_cache_size = 2

    def __init__(self) -> None:
        """Default constructor."""
        self._lock = threading.Lock()
        self._clear_state()

    def _clear_state(self) -> None:
        self.rebulk: Rebulk | None = None
        self.config: dict[str, Any] | None = None
        self.load_config_options: Any = None
        self.advanced_config: Any = None
        self.effective_options: dict[str, Any] | None = None
        self.effective_options_input: Any = None
        self._configured: dict[Hashable, _Configured] = {}

    def _evict(self) -> None:
        while len(self._configured) > max(self.configured_cache_size, 0):
            del self._configured[next(iter(self._configured))]
        last_use = {id(configured.rebulk): index for index, configured in enumerate(self._configured.values())}
        while len(last_use) > max(self.rule_set_cache_size, 0):
            oldest = min(last_use, key=last_use.__getitem__)
            del last_use[oldest]
            self._configured = {
                key: configured for key, configured in self._configured.items() if id(configured.rebulk) != oldest
            }

    def reset(self) -> None:
        """
        Reset api internal state.
        """
        with self._lock:
            self._clear_state()

    @classmethod
    def _fix_encoding(cls, value: Any) -> Any:
        if isinstance(value, list):
            return [cls._fix_encoding(item) for item in value]
        if isinstance(value, dict):
            return {cls._fix_encoding(k): cls._fix_encoding(v) for k, v in value.items()}
        if isinstance(value, bytes):
            return value.decode("ascii")
        return value

    @classmethod
    def _has_same_properties(cls, dic1: dict[str, Any], dic2: dict[str, Any], values: list[str]) -> bool:
        return all(dic1.get(value) == dic2.get(value) for value in values)

    def configure(
        self,
        options: Any = None,
        rules_builder: Callable[..., Rebulk] | None = None,
        force: bool = False,
        sanitize_options: bool = True,
    ) -> dict[str, Any]:
        """
        Load configuration files and initialize rebulk rules if required.

        :param options:
        :type options: str|dict
        :param rules_builder:
        :type rules_builder:
        :param force:
        :type force: bool
        :param sanitize_options:
        :type force: bool
        :return:
        :rtype: dict
        """
        return self._configure(options, rules_builder, force, sanitize_options).config

    def _configure(
        self,
        options: Any = None,
        rules_builder: Callable[..., Rebulk] | None = None,
        force: bool = False,
        sanitize_options: bool = True,
    ) -> _Configured:
        # A cached rule set was built by whichever builder was in use then, so an explicit builder bypasses the cache.
        use_cache = rules_builder is None
        if not rules_builder:
            rules_builder = rebulk_builder

        if sanitize_options:
            options = parse_options(options, True)
            options = self._fix_encoding(options)

        key: Hashable | None
        try:
            key = _freeze(options)
        except TypeError:
            key = None

        with self._lock:
            config_reloaded = (
                self.config is None
                or self.load_config_options is None
                or force
                or not self._has_same_properties(
                    self.load_config_options, options, ["config", "no_user_config", "no_default_config"]
                )
            )
            if config_reloaded:
                config = load_config(options)
                config = self._fix_encoding(config)
                self.load_config_options = options
                self._configured.clear()
            else:
                assert self.config is not None
                config = self.config

            # merge_options deep-copies its first argument, so building the effective options is costly:
            # keep them per option set, along with the rule set they were built for.
            cached = self._configured.pop(key, None) if key is not None else None
            configured = cached if use_cache else None
            if configured is None:
                advanced_config = merge_options(config.get("advanced_config"), options.get("advanced_config"))
                if force or not self.rebulk or not self.advanced_config or self.advanced_config != advanced_config:
                    self.advanced_config = deepcopy(advanced_config)
                    self.rebulk = rules_builder(advanced_config)
                assert self.rebulk is not None
                configured = _Configured(config, self.advanced_config, self.rebulk, merge_options(config, options))
            if key is not None:
                self._configured[key] = configured
                self._evict()

            self.config = config
            self.advanced_config = configured.advanced_config
            self.rebulk = configured.rebulk
            self.effective_options = configured.options
            self.effective_options_input = options
            return configured

    def guessit(self, string: str | Path | bytes, options: Any = None) -> dict[str, Any]:
        """
        Retrieves all matches from string as a dict
        :param string: the filename or release name
        :type string: str|Path
        :param options:
        :type options: str|dict
        :return:
        :rtype:
        """
        if string is None:
            # A bare None is almost always an accidental call (e.g. a missing filename); fail with a
            # clear message instead of the cryptic internal error report wrapped by GuessitException.
            raise TypeError("guessit() requires a filename string, got None")
        if isinstance(string, Path):
            try:
                # Handle path-like object
                string = os.fspath(string)
            except AttributeError:
                string = str(string)

        try:
            options = parse_options(options, True)
            options = self._fix_encoding(options)
            configured = self._configure(options, sanitize_options=False)
            options = configured.options
            result_decode = False
            result_encode = False

            if isinstance(string, bytes):
                string = string.decode("ascii")
                result_encode = True

            matches = configured.rebulk.matches(string, options)
            if result_decode:
                for match in matches:
                    if isinstance(match.value, bytes):
                        match.value = match.value.decode("utf-8")
            if result_encode:
                for match in matches:
                    if isinstance(match.value, str):
                        match.value = match.value.encode("ascii")
            matches_dict = matches.to_dict(
                options.get("advanced", False), options.get("single_value", False), options.get("enforce_list", False)
            )
            output_input_string = options.get("output_input_string", False)
            if output_input_string:
                matches_dict["input_string"] = matches.input_string
            # rebulk 6 types MatchesDict keys as ``str | None``; every guessit
            # property (and ``input_string``) is named, so the keys are always ``str``.
            return cast("dict[str, Any]", matches_dict)
        except Exception as err:
            raise GuessitException(string, options) from err

    def properties(self, options: Any = None) -> dict[str, Any]:
        """
        Grab properties and values that can be generated.
        :param options:
        :type options:
        :return:
        :rtype:
        """
        options = parse_options(options, True)
        options = self._fix_encoding(options)
        configured = self._configure(options, sanitize_options=False)
        rebulk = configured.rebulk
        unordered = introspect(rebulk, configured.options).properties
        ordered = OrderedDict()
        for k in sorted(unordered.keys(), key=str):
            ordered[k] = sorted(unordered[k], key=str)
        if hasattr(rebulk, "customize_properties"):
            ordered = rebulk.customize_properties(ordered)
        return _complete_properties(ordered)

    def schema(self, options: Any = None) -> dict[str, Any]:
        """
        Grab the property schema (type, cardinality and enums) for the effective configuration.

        The type and cardinality of every property are configuration invariants, taken from the
        frozen :data:`GUESSIT_SCHEMA`; only the closed-vocabulary enums depend on the configuration
        and are overlaid from :meth:`properties`. With no options this returns a copy of
        :data:`GUESSIT_SCHEMA`.

        :param options:
        :type options: str|dict
        :return:
        :rtype: dict
        """
        if options is None:
            return deepcopy(GUESSIT_SCHEMA)
        return overlay_config_enums(GUESSIT_SCHEMA, self.properties(options))

    def json_schema(self, options: Any = None) -> dict[str, Any]:
        """
        Grab the draft-07 JSON Schema of the output for the effective configuration.

        With no options this equals the committed ``guessit/data/output-schema.json``.

        :param options:
        :type options: str|dict
        :return:
        :rtype: dict
        """
        return build_json_schema(self.schema(options))

    def suggested_expected(self, titles: Any, options: Any = None) -> list[Any]:
        """
        Return a list of suggested titles to be used as `expected_title` based on the list of titles
        :param titles: the filename or release name
        :type titles: list|set|dict
        :param options:
        :type options: str|dict
        :return:
        :rtype: list of str
        """
        suggested: list[Any] = []
        for title in titles:
            guess = self.guessit(title, options)
            if len(guess) != 2 or "title" not in guess:
                suggested.append(title)

        return suggested


default_api = GuessItApi()
