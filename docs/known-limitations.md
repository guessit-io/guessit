# Known limitations

GuessIt extracts metadata from a filename using **structural pattern matching only** — it has no
catalogue, no network lookup and no per-title knowledge. A few filename shapes are genuinely
ambiguous to a structural parser: the same characters can legitimately be either a real title /
episode-title word or a property value, and no local signal reliably tells them apart.

This page documents those cases as a deliberate record. Each one was investigated and closed as
**Won't fix** — not because it is wrong to want the better result, but because every attempted fix
either required external knowledge guessit does not have, or regressed a larger, well-anchored set
of real-world filenames. They are kept here so the history is not lost and so the tool can evolve if
a safe solution is ever found.

!!! note
    If you control the input, the ambiguity usually disappears with one extra token (an explicit
    release year, an `SxxExx` marker, …) or with the `expected_title` / `type` options. The examples
    below are the *bare* forms where guessit has nothing else to go on.

## A title or episode-title word consumed as a property

A token that is genuinely part of the (episode) title also happens to be a recognised
`other` / `proper` / `edition` / … keyword. When that word sits **inside a multi-word title**, the
property match wins and truncates the title.

The narrow, unambiguous variant — a title made of a **single leading article** (`The`) followed by
the keyword — *is* handled (`The.Convert.2024` → title `The Convert`; `Chapter.19.The.Convert` →
episode_title `The Convert`, see `ExtendLoneArticleTitle`). The general mid-title case is not.

### #743 — `Convert` in a multi-word episode title

```text
The.Mandalorian.S03E03.Chapter.19.The.Convert.2160p.WEB-DL.DDP5.1.HEVC-Group
  episode_title: "Chapter 19 The"   other: "Converted"      (wrong)
  wanted -> episode_title: "Chapter 19 The Convert"  (no other)
```

### #746 — `Real` in an episode title

```text
Schmigadoon.S02E04.Something.Real.1080p.ATVP.WEB-DL.DDP5.1.H.264-NOGRP
  episode_title: "Something"   other: "Proper"             (wrong)
  wanted -> episode_title: "Something Real"  (no other)
```

**Root cause.** `Converted` (`CONVERT`) and `Real`/`Proper` are `has-neighbor` `other` keywords. With
a neighbour present they match wherever they appear, including mid-title.

**Why Won't fix.** A broadening that merged such words back into the title was tried and **reverted
(PR #838)** because it broke legitimate detection. The behaviour is now locked by regression anchors
(`episodes.yml`): `Game.of.Thrones.S01E09.Baelor.The.Real.1080p` must stay `other: Proper`, and
`Better.Call.Saul.S04E10.Winner.The.Internal.1080p` must stay `other: Internal`. Capitalisation does
not discriminate either: the corpus *wants* lower-case `hdtv.real.proper` to be `Proper`, so an
"upper-case `REAL` only" rule would regress those.

**A future fix** would need to weigh "is this word a release tag here?" against the surrounding
title shape with much more context than a single neighbour — most reliably with title knowledge
guessit does not hold.

## A number misread as a season / episode

Bare numbers next to an episode are the hardest class. `S01E02` followed by a number can be a
multi-episode range (`S01E01.02.03`) or an episode title starting with a digit (`S01E02.3 Kings`);
a 4-digit number can be a year, an absolute episode, or — structurally — a `season+episode` split.
Guessit resolves these with consecutiveness / position heuristics that are correct for the bulk of
the corpus but wrong for the cases below.

### #752 — leading digit of an episode title joined as a range

```text
Show.Name.1969.S01E02.3.Kings.1080p.DDP5.1.H.264
  episode: [2, 3]   episode_title: "Kings"                 (wrong)
  wanted -> episode: 2   episode_title: "3 Kings"
```

The `SxxExx` chain extends across a weak `.` separator to the **consecutive** number `3`
(gap ≤ `max_range_gap + 1`). With a non-consecutive digit it already does the right thing —
`S01E02.5.Kings` → episode `2`, episode_title `5 Kings`. Telling `S01E02.3.Kings` (title) apart from
`S01E02.03` (range) needs to know `Kings` is a title, which is the same ambiguity as #743/#746.

### #744 — episode title made of numbers and hyphens

```text
Ted.Lasso.S03E03.4-5-1.1080p.ATVP.WEB-DL.DDP5.1.H.264-Group
  episode: [3, 4, 5]   episode_title: "1"                  (wrong)
  wanted -> episode: 3   episode_title: "4-5-1"
```

`4-5` is read as an episode range (`-` is a range separator) joined to `E03`. There is no structural
signal that `4-5-1` is a title (a football formation) rather than a range.

### #747 — single-digit leading episode number (anime)

```text
5. Nanatsu no Taizai - The Seven Deadly Sins [1080 Hi10p AAC][kuchikirukia].mkv
  title: "5 Nanatsu no Taizai"   type: movie               (wrong)
  wanted -> episode: 5   title: "Nanatsu no Taizai"
```

A **two-digit** leading number works (`22. Nanatsu …` → episode `22`); a bare **single** digit is
deliberately not treated as an episode (the single-digit weak pattern requires a `vN` version
suffix). Enabling a bare leading single digit as an episode would mis-read a large number of real
titles that legitimately start with a digit.

### #772 — a folder's episode range overrides the file's episode

```text
[Erai-raws] Great Teacher Onizuka - 01~43 [480p][Multiple Subtitle]/[Erai-raws] Great Teacher Onizuka - 11 [480p].mkv
  episode: [1, 43]                                          (wrong)
  wanted -> episode: 11
```

The folder's `01~43` (a season-pack range) and the file's `11` are both *weak* episodes (no
`SxxExx`). The filename's `11` is dropped because the folder filepart carries more matches overall
and is treated as the more authoritative part. Making the filename win on a weak-vs-weak tie breaks
the opposite, equally valid anchor where a more complete parent `SxxExx` must override a sample clip
in a subdirectory (`Westworld.S02E03…/sample/Westworld.S01E01.sample.mkv` → `S02E03`).

### #774 — a future year in the title read as season/episode

```text
Blade Runner 2049.HDRip.XviD.AC3-EVO.avi
  season: 20   episode: 49   title: "Blade Runner"         (wrong)
  wanted -> title: "Blade Runner 2049"   (year 2017, from the real release)
```

`2049` is part of the **title**. It is not a valid year (`valid_year` accepts `1900 ≤ y < 2035`) and
structurally matches a `season+episode` split (`20`/`49`). When the real release year is present the
result is correct (`Blade.Runner.2049.2017…` → title `Blade Runner 2049`); without it there is no
local signal that `2049` is title text. As the reporter notes, disambiguating this reliably needs an
external database (e.g. IMDb).

### #373 — a title starting with `NxN`

```text
3x3 Eyes (1991)/Season 2/3x3 Eyes - 2x01 - Descent.mkv
  season: 3   episode: [3, 1]   title: "Eyes"             (wrong)
  wanted -> title: "3x3 Eyes"   season: 2   episode: 1
```

The leading `3x3` of the title *3×3 Eyes* is byte-for-byte a `season x episode` marker. Nothing
local says it is title text rather than `S03E03`.

### #533 — a bare trailing number

```text
One Piece - 720
  season: 7   episode: 20                                 (one reading)
  wanted -> episode: 720  *or*  screen_size: 720p  (depending on intent)
```

A trailing `720` is simultaneously a plausible `720p` resolution, an absolute episode `720`, and a
`7x20` season/episode. guessit picks one (`7x20`); the choice is anchored by a fixture but cannot be
"correct" for every release. Add the missing `p` (`720p`) or an `Exx` marker to disambiguate.

### #693 — a bare resolution or duration number read as season/episode

```text
Gladiator.EXTENDED.2000.720.BrRip.264.YIFY   -> season: 7   episode: 20    (wrong)
Gladiator.EXTENDED.2000.1080.BrRip.264.YIFY  -> season: 10  episode: 80    (wrong)
Aliens DVD Silver Box Set 131 Min            -> season: 1   episode: 31    (wrong)
  wanted -> no season/episode (these are movies)
```

The same shape as #533: a bare `720` / `1080` (resolution without the `p`) or a stray duration
(`131 Min`) is structurally a `season+episode` split (`7x20`, `10x80`, `1x31`). Nothing local marks
them as a resolution or a runtime. The related **frame-rate** form *is* handled — `Gladiator 23.976
FPS` correctly yields `frame_rate: 23.976fps` because the `FPS` suffix disambiguates it.

An adjacent **video codec** does disambiguate it, and is handled since #933:
`Les.Profs.2013.FRENCH.AC3.1080.x264-Ox` yields `screen_size: 1080p` + `video_codec: H.264`. The
cases above have no such neighbour — `BrRip.264` is a stray number, not an `x264` codec token.

### #637 — a one-letter title followed by a number

```text
E.60.2020.02.16.Remembering.Coach.Alto.720p.ESPN.WEB-DL.AAC2.0.H.264-KiMCHi.mkv
  title: "E"   episode: 60                                 (wrong)
  wanted -> title: "E 60"   (the show "E:60", with no episode)
```

The show *E:60* is released as `E.60` (the `:` is illegal in filenames). A single-letter token
followed by a one/two-digit number is byte-for-byte a `title + episode` shape; there is no local
signal that `E 60` is the whole title rather than episode `60` of a show called `E`.

## Anime titles containing a ` - ` separator

```text
[HorribleSubs] Garo - Vanishing Line - 01 [1080p].mkv
  title: "Garo"   alternative_title: "Vanishing Line"     (#524, #670)
  wanted -> title: "Garo - Vanishing Line"   episode: 1
```

` - ` is guessit's title / alternative-title separator, but many anime *names* contain a literal
` - ` (`Garo - Vanishing Line`, `Uma Musume - Pretty Derby`). There is no structural way to tell a
name-internal dash from a real title/alt-title boundary, so the name is split. These are anchored by
fixtures as the accepted behaviour.

### #690 — `Season N - M` read as a season range

```text
[Golumpa] Re ZERO -Starting Life in Another World- Season 2 - 15 [CR-Dub 1080p x264].mkv
  season: [2, 3, …, 15]                                    (wrong)
  wanted -> season: 2   episode: 15
```

`Season N - M` is read as the season range `N`→`M`. This is **not** safely fixable because the very
same shape is a legitimate season *pack* elsewhere in the corpus — `Coupling Season 1 - 4 Complete
DVDRip/…` is anchored as season `1`→`4`. Nothing structural distinguishes "season 2, episode 15"
from "seasons 2 through 15"; the dashes inside the *Re:ZERO* title only make the ambiguity more
visible. Use an explicit `SxxExx` (`S02E15`) to disambiguate.

## A leading language / country code consumed from the title

```text
HI.SCORE.GIRL.II.S01E01-E09.Blu-ray.MKV.h264.1080p.FLAC2.0-SonicBoom
  language: hi   title: "SCORE GIRL II"                    (#660, wrong)
  wanted -> title: "HI SCORE GIRL II"   (the show "High Score Girl")
```

`HI` is the ISO-639 code for Hindi, and it sits where a language tag legitimately can. The show
*HI SCORE GIRL* (stylised *High Score Girl*) opens with that exact token, so the language match eats
the first title word. This is the same class as the `Us` / country case (#739): a short token that
is simultaneously a valid code and a real title word, with no local signal to tell them apart. The
`expected_title` option (`HI SCORE GIRL`) resolves it at call time.

## Release group boundaries

The release group is the trailing token after the final dash, disambiguated from titles and
properties heuristically. A few shapes defeat the heuristic.

### #530 — a group name placed *before* the title

```text
avchd-modern.family.s02e01.720p.bluray.x264.mkv
  title: "modern family"                                  (no release_group)
  wanted -> release_group: "avchd"
```

A handful of scene groups prefix their name to the filename. guessit only looks for the group at the
**end**; a leading `avchd-` is indistinguishable from a title word without an explicit per-group
allow-list (which the project deliberately does not maintain).

### #356 — episode-title words swallowed by a greedy release group

```text
National.Geographic.Documentaries.S2016E15.720p.HDTV.x264.Mammoth.Back.from.the.Dead-DHD.mkv
  release_group: "Mammoth.Back.from.the.Dead-DHD"         (wrong)
  wanted -> episode_title: "Mammoth Back from the Dead"   release_group: "DHD"
```

Text between the video codec and the trailing `-DHD` has no marker telling guessit where the episode
title ends and the release group begins, so the whole run is taken as the group.

### #236 / #248 — an indexer suffix kept in the release group

```text
Hannibal.S03E13.720p.HDTV.x264-KILLERS[rarbg]   -> release_group: "KILLERS[rarbg]"
Some.Show.S01E01.720p.HDTV.x264-UAV[rartv]      -> release_group: "UAV[rartv]"
```

The bracketed indexer tag (`[rarbg]`, `[rartv]`) is **kept by design** — guessit cannot know whether
brackets after the group are an indexer stamp or part of the group's actual name, and stripping them
unconditionally would corrupt groups that legitimately use brackets. This is anchored by fixtures
(`SADPANDA[rarbg]`, `BTW[rartv]`, …); downstream consumers that need the bare group should strip a
known indexer suffix themselves.

### #496 — a `www`-prefixed website

```text
The.Path_.2x10.HDTV_.XviD_.www_.DivxTotaL.com_.avi
  website: "DivxTotaL.com"   release_group: "www"         (wrong)
  wanted -> website: "www.DivxTotaL.com"   (no release_group)
```

The `www` is split from the website it belongs to and left dangling as a release group.

## Title text is normalised, never rewritten

```text
The Devils Backbone (2001).avi
  title: "The Devils Backbone"                            (no apostrophe)
  wanted -> title: "The Devil's Backbone"   (#508)
```

guessit cleans separators and casing but never edits the **words** of a title — it has no dictionary
or catalogue, so it cannot restore a missing apostrophe, fix a typo, or expand an abbreviation. The
returned title is faithful to the filename's characters; correcting orthography is a job for a
downstream lookup against a real title database.

## A date-shaped title read as a date

```text
19-2.2014.S03E01.GERMAN.720p.HDTV.x264-ACED
  date: 2014-02-19   title: (none)                        (#494)
  wanted -> title: "19-2"   year: 2014
```

The show *19-2* produces `19-2.2014`, which is a valid `DD-M.YYYY` date. A title that is itself a
date-like number is structurally indistinguishable from an actual date; date detection wins.

## How these could be revisited

Most of the cases above share one root: they need to know whether an ambiguous token is *content*
(title / episode title) or *metadata*. Promising directions, none of them free:

- **User hints** — `expected_title`, `type=movie|episode`, or a future "release year is before N"
  hint already resolve several of these at call time.
- **A title corpus / optional lookup** — an opt-in catalogue would settle #743, #746, #752 and #774
  directly, at the cost of guessit's "no network, no data" promise.
- **Smarter title-shape scoring** — weighing a property match against the surrounding title context
  (word count, capitalisation, neighbours on both sides) rather than a single neighbour, validated
  against the full YAML corpus to avoid re-introducing the PR #838 regressions.
- **Configurable scene-group lists** — an opt-in allow-list of prefix groups (#530) or indexer
  suffixes (#236, #248) would let consumers tighten release-group detection without changing the
  default heuristics.

Contributions exploring these are welcome — please validate against the entire `guessit/test/*.yml`
corpus, since the regression anchors there are what make these cases hard.
