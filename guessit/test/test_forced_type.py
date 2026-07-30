#!/usr/bin/env python
"""Consistency of the forced ``type`` modes (#939).

Forcing the type guessit already infers must be a no-op: ``guessit(name, {"type": t})`` has to
return exactly ``guessit(name)`` whenever the latter yields ``type: t``. The whole yaml corpus is
swept, so any new divergence shows up here even though the corpus itself barely exercises the
forced modes.
"""

from __future__ import annotations

import os

import pytest
import yaml

from .. import guessit
from ..yamlutils import OrderedDictYAMLLoader
from . import test_yml

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Names whose forced-type result still differs from the inferred one. Each is a lone digit that
# only the forced-episode patterns pick up — inside a release group, a path segment or a duplicate
# marker — and pushes out a property. Tracked by #939; entries must be removed as they get fixed.
KNOWN_DIVERGENCES = frozenset(
    {
        "series/Freaks And Geeks/Season 1/Episode 4 - Kim Kelly Is My Friend-eng(1).srt",
        "/Volumes/data-1/Series/Futurama/Season 3/Futurama_-_S03_DVD_Bonus_-_Deleted_Scenes_Part_3.ogm",
        "[t.3.3.d]_Mikakunin_de_Shinkoukei_-_12_[720p][5DDC1352].mkv",
        "[7.1.7.8.5] Foo Bar - 11 (H.264) [5235532D].mkv",
        "[GroupName].Show.Name.-.02.5.(Special).[BD.1080p]",
        "Thumping.Spike.2.E01.DF.WEBRip.720p-DRAMATV.mp4",
        "La Casa di Carta Stagione 2 Episodio 5",
        "GTTV.E3.All.Access.Live.Day.1.Xbox.Showcase.Preshow.HDTV.x264-SYS",
    }
)


def corpus_names() -> list[str]:
    """Every input string of the yaml corpus, minus the entries pinned to their own options."""
    names: list[str] = []
    for filename, _ in zip(*test_yml.files_and_ids(), strict=False):
        with open(os.path.join(__location__, filename), encoding="utf-8") as infile:
            data = yaml.load(infile, OrderedDictYAMLLoader)
        for string, expected in data.items():
            if string == "__default__" or (isinstance(expected, dict) and "options" in expected):
                continue
            match = test_yml.TestYml.options_re.match(str(string))
            name = match.group(2) if match else str(string)
            if name:
                names.append(test_yml.TestYml.fix_encoding(name))
    return sorted(set(names))


def test_forcing_the_inferred_type_is_a_no_op() -> None:
    names = corpus_names()
    divergences = {}
    for name in names:
        inferred = guessit(name)
        guessed_type = inferred.get("type")
        if guessed_type not in ("movie", "episode"):
            continue
        forced = guessit(name, {"type": guessed_type})
        if dict(forced) != dict(inferred):
            divergences[name] = (dict(inferred), dict(forced))

    unexpected = {name: diff for name, diff in divergences.items() if name not in KNOWN_DIVERGENCES}
    assert not unexpected, "forcing the inferred type changed the result:\n" + "\n".join(
        f"  {name}\n    inferred={inferred}\n    forced  ={forced}" for name, (inferred, forced) in unexpected.items()
    )

    scanned = set(names)
    stale = {name for name in KNOWN_DIVERGENCES if name in scanned and name not in divergences}
    assert not stale, f"these names no longer diverge, drop them from KNOWN_DIVERGENCES: {sorted(stale)}"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        # A year in the part keeps the leading number of the title out of the episode reading,
        # whatever the requested type (#939).
        ("12.Angry.Men.1957.mkv", {"title": "12 Angry Men", "year": 1957}),
        ("Movies/21 (2008)/21.(2008).DVDRip.x264.AC3-FtS.mkv", {"title": "21", "year": 2008, "release_group": "FtS"}),
        # An explicit episode marker is still numbered, year or not.
        (
            "Mastercook Italia - Stagione 6 (2016) 720p Episodio 13 spyro.mkv",
            {"season": 6, "episode": 13, "year": 2016},
        ),
    ],
)
def test_forced_episode_keeps_year_anchored_properties(name: str, expected: dict[str, object]) -> None:
    result = guessit(name, {"type": "episode"})
    for prop, value in expected.items():
        assert result.get(prop) == value, f"{prop}: {result.get(prop)!r} != {value!r} in {dict(result)}"


def test_forced_episode_ignores_an_episode_word_from_another_filepart() -> None:
    """A parent directory named "Episode" must not vouch for a number in the file below it."""
    result = guessit("Series/Episode/12.Angry.Men.1957.mkv", {"type": "episode"})
    assert result.get("title") == "12 Angry Men"
    assert result.get("year") == 1957
