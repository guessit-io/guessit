#!/usr/bin/env python
"""
Generate the machine-readable property schema and JSON Schema.

Source of truth (self-contained — no guessit-js needed):
  - guessit.api.properties()      → authoritative enum lists (declared values)
  - guessit/test/**/*.yml inputs  → runtime type + cardinality (array/scalar)

Outputs (committed):
  - guessit/schema.py             → GUESSIT_SCHEMA (typed dict) + PropertySchema
  - guessit/data/output-schema.json → JSON Schema (draft-07) of the output

Run:  uv run python scripts/gen_schema.py
Keep the outputs in sync; a test asserts they don't drift.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import babelfish
import yaml

from guessit import api
from guessit.rules.common.quantity import BitRate, FrameRate, Size
from guessit.yamlutils import OrderedDictYAMLLoader

ROOT = Path(__file__).resolve().parent.parent
TEST_DIR = ROOT / "guessit" / "test"
SCHEMA_PY = ROOT / "guessit" / "schema.py"
OUTPUT_SCHEMA_JSON = ROOT / "guessit" / "data" / "output-schema.json"

# Closed-vocabulary properties: these expose an `enum`. Everything else is free
# text / numeric / structured and gets a type only. (Mirrors guessit-js.)
#
# `mimetype` is deliberately NOT constrained: it is computed by the stdlib
# `mimetypes.guess_type`, whose vocabulary depends on the Python version and the
# host's mime database (/etc/mime.types). Pinning its enum would make the schema
# environment-specific and the drift test fail across the CI Python matrix.
VALUE_CONSTRAINED = {
    "source", "screen_size", "video_codec", "audio_codec", "audio_channels",
    "audio_profile", "video_profile", "video_api", "color_depth", "container",
    "other", "edition", "type", "scan_type", "streaming_service",
    "episode_format",
}  # fmt: skip

# Properties rendered as a language/country object (or its string code).
LANGUAGE_PROPS = {"language", "subtitle_language", "country"}

_TOKEN_PREFIX = re.compile(r"^[ +-]+")


def _base_type(value: Any) -> str:
    """Map a runtime value to a schema base type."""
    if isinstance(value, babelfish.Language | babelfish.Country):
        return "Language"
    if isinstance(value, bool):  # before int — bool is a subclass of int
        return "boolean"
    if isinstance(value, int | float):
        return "number"
    if isinstance(value, Size | BitRate | FrameRate):
        return "string"  # quantities render as strings
    if isinstance(value, str):
        return "string"
    if isinstance(value, dict):
        return "object"
    return "string"


def _corpus_inputs() -> list[str]:
    """All input strings from the YAML corpus, token prefixes stripped."""
    inputs: list[str] = []
    for path in sorted(TEST_DIR.rglob("*.yml")) + sorted(TEST_DIR.rglob("*.yaml")):
        with open(path, encoding="utf-8") as stream:
            data = yaml.load(stream, OrderedDictYAMLLoader)
        if not isinstance(data, dict):
            continue
        for key in data:
            text = key if isinstance(key, str) else str(key)
            inputs.append(_TOKEN_PREFIX.sub("", text))
    return inputs


def _collect_runtime() -> tuple[dict[str, set[str]], set[str], set[str], dict[str, set[Any]]]:
    """Run the corpus and aggregate per-property base types, cardinality and values."""
    types: dict[str, set[str]] = defaultdict(set)
    array: set[str] = set()
    scalar: set[str] = set()
    values: dict[str, set[Any]] = defaultdict(set)

    def record(name: str, item: Any) -> None:
        types[name].add(_base_type(item))
        if name in VALUE_CONSTRAINED and isinstance(item, str | int) and not isinstance(item, bool):
            values[name].add(item)

    for string in _corpus_inputs():
        try:
            guess = api.guessit(string)
        except Exception:  # a single bad input must not abort generation
            continue
        for name, value in guess.items():
            if isinstance(value, list):
                array.add(name)
                for item in value:
                    record(name, item)
            else:
                scalar.add(name)
                record(name, value)
    return types, array, scalar, values


def build_schema() -> dict[str, dict[str, Any]]:
    """Build the GUESSIT_SCHEMA mapping."""
    declared = api.properties()  # authoritative declared values (code-complete enum source)
    types, array, scalar, observed = _collect_runtime()

    schema: dict[str, dict[str, Any]] = {}
    for name in sorted(set(declared) | set(types)):
        # enum = declared (code-complete, e.g. source "Workprint") union corpus-observed
        # (e.g. every screen_size resolution) — only for closed-vocabulary properties.
        enum: list[Any] = []
        if name in VALUE_CONSTRAINED:
            decl: set[Any] = set()
            for value in declared.get(name, []):
                if value is None:
                    continue
                if isinstance(value, list):  # compound declared value, e.g. ['Ultimate', 'Collector']
                    decl.update(value)
                else:
                    decl.add(value)
            enum = sorted(decl | observed.get(name, set()), key=str)

        base = sorted(types.get(name, set()))
        if name in LANGUAGE_PROPS:
            base = ["Language"]
        elif not base:  # never emitted by the corpus → fall back to a plausible type
            base = (
                ["number"] if all(isinstance(v, int) and not isinstance(v, bool) for v in enum) and enum else ["string"]
            )

        entry: dict[str, Any] = {
            "type": base,
            "array": name in array,
            "scalar": name in scalar or name not in array,
        }
        if enum:
            entry["enum"] = enum
        schema[name] = entry
    return schema


def render_schema_py(schema: dict[str, dict[str, Any]]) -> str:
    """Render guessit/schema.py (Python literal; `ruff format` prettifies it)."""
    body = repr(schema)
    return (
        "#!/usr/bin/env python\n"
        '"""Machine-readable schema of every property guessit can emit.\n\n'
        "AUTO-GENERATED by scripts/gen_schema.py — do not edit by hand.\n"
        "Regenerate: uv run python scripts/gen_schema.py\n"
        '"""\n\n'
        "from __future__ import annotations\n\n"
        "from typing import Literal, TypedDict\n\n"
        'PropertyType = Literal["string", "number", "boolean", "Language", "object"]\n\n\n'
        "class PropertySchema(TypedDict, total=False):\n"
        '    """Description of a single property guessit can emit."""\n\n'
        "    type: list[PropertyType]\n"
        "    array: bool\n"
        "    scalar: bool\n"
        "    enum: list[str | int]\n\n\n"
        f"GUESSIT_SCHEMA: dict[str, PropertySchema] = {body}\n"
    )


def build_json_schema(schema: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Build the draft-07 JSON Schema from GUESSIT_SCHEMA."""
    language_def = {
        "type": ["object", "string"],
        "description": "A language or country: a string code, or an object.",
        "properties": {
            "name": {"type": "string"},
            "alpha3": {"type": "string"},
            "alpha2": {"type": "string"},
            "country": {"type": ["string", "null"]},
            "script": {"type": ["string", "null"]},
        },
    }
    json_base = {"string": "string", "number": "number", "boolean": "boolean", "object": "object"}

    def base_fragment(spec: dict[str, Any]) -> dict[str, Any]:
        if "Language" in spec["type"]:
            return {"$ref": "#/definitions/Language"}
        frag: dict[str, Any] = {"type": [json_base[t] for t in spec["type"]]}
        if len(frag["type"]) == 1:
            frag["type"] = frag["type"][0]
        if spec.get("enum"):
            frag["enum"] = list(spec["enum"])
        return frag

    properties: dict[str, Any] = {}
    for name, spec in schema.items():
        base = base_fragment(spec)
        if spec["array"] and spec["scalar"]:
            properties[name] = {"oneOf": [base, {"type": "array", "items": base}]}
        elif spec["array"]:
            properties[name] = {"type": "array", "items": base}
        else:
            properties[name] = base

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": "https://github.com/guessit-io/guessit/output-schema.json",
        "title": "guessit output",
        "description": "Metadata extracted from a release name. Every property is optional; "
        "presence depends on the input. Generated by scripts/gen_schema.py.",
        "type": "object",
        "definitions": {"Language": language_def},
        "properties": properties,
        "additionalProperties": True,
    }


def main() -> None:
    schema = build_schema()
    SCHEMA_PY.write_text(render_schema_py(schema), encoding="utf-8")
    OUTPUT_SCHEMA_JSON.write_text(
        json.dumps(build_json_schema(schema), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {SCHEMA_PY.relative_to(ROOT)} and {OUTPUT_SCHEMA_JSON.relative_to(ROOT)} ({len(schema)} properties)")


if __name__ == "__main__":
    main()
