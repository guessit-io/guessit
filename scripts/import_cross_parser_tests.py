#!/usr/bin/env python
"""Import labelled release names from other (permissively-licensed) parsers.

This fetches the test fixtures of several MIT/MPL-2.0 release-name parsers,
translates each labelled entry into the guessit vocabulary (see
``cross_parser_mapping``), and vendors the result as JSON under
``guessit/test/cross_parser/`` together with an attribution NOTICE.

It then runs guessit over every imported entry and writes a *baseline* manifest
of the fields that currently disagree, so ``test_cross_parser.py`` can tolerate
existing divergences and fail only on regressions.

Run manually (like ``scripts/gen_schema.py``); the suite never needs the network:

    uv run python scripts/import_cross_parser_tests.py

Add ``--no-baseline`` to refresh only the datasets, or ``--source NAME`` to limit.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cross_parser_mapping as cm

if TYPE_CHECKING:
    from collections.abc import Callable

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "guessit" / "test" / "cross_parser"
SCHEMA_PATH = ROOT / "guessit" / "data" / "output-schema.json"

# --- common tooling: declarative per-source spec ------------------------------
#
# Every source is described the same way: where to fetch it, how its raw payload
# is shaped (``loader``), and a flat list of ``FieldRule``s mapping an external
# label key to a guessit field through a named value-mapper. One engine
# (``load_entries`` + ``assemble``) drives all of them, so adding a source means
# adding a declarative ``SourceSpec`` here — no bespoke adapter code.


@dataclass(frozen=True)
class FieldRule:
    """Map one external label key onto a guessit field via a named mapper kind."""

    field: str  # guessit field to emit
    key: str  # key in the external label dict
    kind: str  # mapper kind, see make_mappers()


@dataclass(frozen=True)
class SourceSpec:
    name: str
    license: str
    homepage: str
    url: str
    loader: str  # 'json_dict' | 'json_list' | 'aligned' | 'ptt'
    fields: tuple[FieldRule, ...]
    type_rule: Callable[[dict[str, Any]], str | None]
    name_key: str | None = None  # json_list: key holding the release name
    label_key: str | None = None  # json_list: nested label key (None = item itself)


def _type_movie_tvshow(label: dict[str, Any]) -> str | None:
    return {"movie": "movie", "tvshow": "episode"}.get(label.get("type"))


def _type_ismovie(label: dict[str, Any]) -> str | None:
    return "movie" if label.get("ismovie") else "episode"


def _type_ptn(label: dict[str, Any]) -> str | None:
    return "episode" if ("season" in label or "episode" in label) else "movie"


def _type_ptt(label: dict[str, Any]) -> str | None:
    # Only PTT's test_main.py records are complete enough to infer type from the
    # absence of season/episode; partial single-field entries must not guess.
    if not label.get("_complete"):
        return None
    return "episode" if (label.get("seasons") or label.get("episodes")) else "movie"


def _type_anime(label: dict[str, Any]) -> str | None:
    # presence, not truthiness: episode_number 0 (episode zero / specials) is valid
    return "episode" if label.get("episode_number") is not None else None


# Shared field rules reused by the parse-torrent-name family (go-ptn, ptn).
_PTN_FAMILY_FIELDS: tuple[FieldRule, ...] = (
    FieldRule("title", "title", "title"),
    FieldRule("year", "year", "year"),
    FieldRule("season", "season", "se"),
    FieldRule("episode", "episode", "se"),
    FieldRule("screen_size", "resolution", "screen_size"),
    FieldRule("video_codec", "codec", "video_codec"),
    FieldRule("source", "quality", "source"),
    FieldRule("audio_codec", "audio", "audio_codec"),
)

SOURCES: dict[str, SourceSpec] = {
    "thcolin": SourceSpec(
        name="thcolin",
        license="MIT",
        homepage="https://github.com/thcolin/scene-release-parser-php",
        url="https://raw.githubusercontent.com/thcolin/scene-release-parser-php/master/utils/releases.json",
        loader="json_dict",
        type_rule=_type_movie_tvshow,
        fields=(
            FieldRule("title", "title", "title"),
            FieldRule("year", "year", "year"),
            FieldRule("season", "season", "se"),
            FieldRule("episode", "episode", "se"),
            FieldRule("screen_size", "resolution", "screen_size"),
            FieldRule("video_codec", "encoding", "video_codec"),
            FieldRule("source", "source", "source"),
        ),
    ),
    "go-ptn": SourceSpec(
        name="go-ptn",
        license="MIT",
        homepage="https://github.com/razsteinmetz/go-ptn",
        url="https://raw.githubusercontent.com/razsteinmetz/go-ptn/master/testdata.json",
        loader="json_list",
        name_key="fname",
        label_key="wanted",
        type_rule=_type_ismovie,
        fields=_PTN_FAMILY_FIELDS,
    ),
    "ptn": SourceSpec(
        name="ptn",
        license="MIT",
        homepage="https://github.com/divijbindlish/parse-torrent-name",
        url="https://raw.githubusercontent.com/divijbindlish/parse-torrent-name/master/tests/files/",
        loader="aligned",
        type_rule=_type_ptn,
        fields=_PTN_FAMILY_FIELDS,
    ),
    "ptt": SourceSpec(
        name="ptt",
        license="MIT",
        homepage="https://github.com/dreulavelle/PTT",
        url="https://raw.githubusercontent.com/dreulavelle/PTT/main/tests/",
        loader="ptt",
        type_rule=_type_ptt,
        fields=(
            FieldRule("title", "title", "title"),
            FieldRule("year", "year", "year"),
            FieldRule("season", "seasons", "se"),
            FieldRule("episode", "episodes", "se"),
            FieldRule("screen_size", "resolution", "screen_size"),
            FieldRule("video_codec", "codec", "video_codec"),
            FieldRule("source", "quality", "source"),
            FieldRule("audio_codec", "audio", "audio_codec"),
        ),
    ),
    "anitomy": SourceSpec(
        name="anitomy",
        license="MPL-2.0",
        homepage="https://github.com/erengy/anitomy",
        url="https://raw.githubusercontent.com/erengy/anitomy/master/test/data.json",
        loader="json_list",
        name_key="file_name",
        type_rule=_type_anime,
        fields=(
            FieldRule("title", "anime_title", "title"),
            FieldRule("year", "anime_year", "year"),
            FieldRule("episode", "episode_number", "se"),
            FieldRule("screen_size", "video_resolution", "screen_size"),
            FieldRule("video_codec", "video_term", "video_codec"),
            FieldRule("audio_codec", "audio_term", "audio_codec"),
        ),
    ),
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "guessit-cross-parser-import"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def load_screen_sizes() -> set[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    prop = schema["properties"]["screen_size"]
    enum = prop.get("enum") or prop.get("items", {}).get("enum") or []
    return set(enum)


# --- common engine: mappers, assembler, loaders ------------------------------


def make_mappers(screen_sizes: set[str]) -> dict[str, Callable[[Any], Any]]:
    """Named value-mappers shared by every source (see ``FieldRule.kind``)."""

    def title(value: Any) -> Any:
        text = str(value).strip()
        return text or None

    def year(value: Any) -> Any:
        n = cm.map_int(value)
        return n if n is not None and 1900 <= n <= 2100 else None

    return {
        "title": title,
        "year": year,
        "se": cm.map_season_episode,
        "screen_size": lambda v: cm.map_screen_size(v, screen_sizes),
        "video_codec": cm.map_video_codec,
        "source": cm.map_source,
        "audio_codec": cm.map_audio_codec,
    }


def assemble(label: dict[str, Any], spec: SourceSpec, mappers: dict[str, Callable[[Any], Any]]) -> dict[str, Any]:
    """Turn one external label dict into a guessit ``expected`` dict via the spec."""
    expected: dict[str, Any] = {}
    for rule in spec.fields:
        raw = label.get(rule.key)
        if raw is None:
            continue
        value = mappers[rule.kind](raw)
        if value is not None and value != "":
            expected[rule.field] = value
    type_ = spec.type_rule(label)
    if type_ in ("movie", "episode"):
        expected["type"] = type_
    return expected


def _ptt_tuples(text: str) -> list[tuple[Any, ...]]:
    """Yield literal tuples from every ``parametrize`` list in a PTT test file."""
    tree = ast.parse(text)
    tuples: list[tuple[Any, ...]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.List):
            continue
        for elt in node.elts:
            if not (isinstance(elt, ast.Tuple) and elt.elts and isinstance(elt.elts[0], ast.Constant)):
                continue
            try:
                value = tuple(ast.literal_eval(e) for e in elt.elts)
            except (ValueError, SyntaxError):
                continue
            if isinstance(value[0], str):
                tuples.append(value)
    return tuples


# PTT spreads its fixtures across files. The per-field files carry raw values in
# the SAME external vocabulary as test_main.py, so we fold them into one label
# dict per release (test_main wins) and let the common assembler map them.
PTT_FIELD_FILES: dict[str, tuple[str, int]] = {
    "test_title.py": ("title", 1),
    "test_year.py": ("year", 1),
    "test_season.py": ("seasons", 1),
    "test_episodes.py": ("episodes", 1),
    "test_resolution.py": ("resolution", 1),
    "test_codec.py": ("codec", 1),
    "test_quality.py": ("quality", 1),
}


def _load_ptt(spec: SourceSpec) -> list[tuple[str, dict[str, Any]]]:
    merged: dict[str, dict[str, Any]] = {}
    for value in _ptt_tuples(fetch(spec.url + "test_main.py").decode("utf-8")):
        if len(value) == 2 and isinstance(value[1], dict):
            name, label = value
            target = merged.setdefault(name, {})
            target["_complete"] = True  # came from test_main.py — type is inferable
            for key, raw in label.items():
                target.setdefault(key, raw)
    for filename, (key, index) in PTT_FIELD_FILES.items():
        try:
            text = fetch(spec.url + filename).decode("utf-8")
        except Exception as exc:  # a missing fixture file is non-fatal
            print(f"    (skip {filename}: {exc})", file=sys.stderr)
            continue
        for value in _ptt_tuples(text):
            if len(value) > index:
                merged.setdefault(value[0], {}).setdefault(key, value[index])
    return list(merged.items())


def load_entries(spec: SourceSpec) -> list[tuple[str, dict[str, Any]]]:
    """Fetch a source and normalise its payload to ``(release_name, label_dict)``."""
    if spec.loader == "json_dict":
        data = json.loads(fetch(spec.url))
        return list(data.items())
    if spec.loader == "json_list":
        data = json.loads(fetch(spec.url))
        out = []
        for item in data:
            name = item.get(spec.name_key)
            label = item.get(spec.label_key) if spec.label_key else item
            if name and isinstance(label, dict):
                out.append((name, label))
        return out
    if spec.loader == "aligned":
        names = json.loads(fetch(spec.url + "input.json"))
        labels = json.loads(fetch(spec.url + "output.json"))
        return list(zip(names, labels, strict=False))
    if spec.loader == "ptt":
        return _load_ptt(spec)
    raise ValueError(f"unknown loader {spec.loader!r}")


def import_source(name: str, mappers: dict[str, Callable[[Any], Any]]) -> int:
    spec = SOURCES[name]
    print(f"  fetching {name} ({spec.license}) ...", flush=True)
    payload = []
    for release, label in load_entries(spec):
        if not isinstance(label, dict):
            continue
        expected = assemble(label, spec, mappers)
        if expected:  # keep every entry carrying at least one mapped field
            payload.append({"release_name": release, "expected": expected})
    doc = {
        "_source": spec.name,
        "_license": spec.license,
        "_homepage": spec.homepage,
        "_url": spec.url,
        "_note": "Generated by scripts/import_cross_parser_tests.py — do not edit by hand.",
        "entries": payload,
    }
    out_path = DATA_DIR / f"{name}.json"
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"    -> {len(payload)} entries written to {out_path.relative_to(ROOT)}")
    return len(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=sorted(SOURCES), help="import only this source")
    parser.add_argument("--no-baseline", action="store_true", help="skip baseline regeneration")
    parser.add_argument(
        "--baseline-only", action="store_true", help="regenerate baseline from the vendored data, without fetching"
    )
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not args.baseline_only:
        mappers = make_mappers(load_screen_sizes())  # screen sizes are fixed for the whole run
        names = [args.source] if args.source else list(SOURCES)
        print("Importing datasets:")
        total = 0
        for name in names:
            try:
                total += import_source(name, mappers)
            except Exception as exc:
                print(f"    !! {name} failed: {exc}", file=sys.stderr)
        print(f"Total: {total} entries across {len(names)} source(s).")

    if not args.no_baseline:
        print("Regenerating baseline (running guessit over the dataset) ...")
        regenerate_baseline()


def regenerate_baseline() -> None:
    """Run guessit over every imported entry; record current field disagreements.

    The manifest is structured as ``{parser: {release_name: [diverging_field,
    ...]}}``. Uses the same comparator as the test (``guessit.test._cross_parser``)
    so the baseline and the assertions can never drift apart.
    """
    sys.path.insert(0, str(ROOT))
    from guessit import guessit
    from guessit.test._cross_parser import field_matches, iter_cases

    disagreements: dict[str, dict[str, list[str]]] = {}
    total = ok = 0
    for source, name, expected in iter_cases():  # same enumeration the test uses
        total += 1
        try:
            result = guessit(name)
        except Exception:
            disagreements.setdefault(source, {})[name] = ["<exception>"]
            continue
        bad = [f for f, exp in expected.items() if not field_matches(result, f, exp)]
        if bad:
            disagreements.setdefault(source, {})[name] = bad
        else:
            ok += 1
    baseline_path = DATA_DIR / "baseline.json"
    baseline_path.write_text(json.dumps(disagreements, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n_dis = sum(len(fields) for by_name in disagreements.values() for fields in by_name.values())
    print(f"  baseline: {ok}/{total} entries fully agree; {n_dis} field disagreements recorded.")


if __name__ == "__main__":
    main()
