GuessIt

[![Latest Version](https://img.shields.io/pypi/v/guessit.svg)](https://pypi.python.org/pypi/guessit)
[![LGPLv3 License](https://img.shields.io/badge/license-LGPLv3-blue.svg)]()
[![Codecov](https://img.shields.io/codecov/c/github/guessit-io/guessit)](https://codecov.io/gh/guessit-io/guessit)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/relekang/python-semantic-release)

GuessIt is a python library that extracts as much information as
possible from a video filename.

It has a very powerful matcher that allows to guess properties from a
video using its filename only. This matcher works with both movies and
tv shows episodes.

For example, GuessIt can do the following:

    $ guessit "Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi"
    For: Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi
    GuessIt found: {
        "title": "Treme",
        "season": 1,
        "episode": 3,
        "episode_title": "Right Place, Wrong Time",
        "source": "HDTV",
        "video_codec": "Xvid",
        "release_group": "NoTV",
        "container": "avi",
        "mimetype": "video/x-msvideo",
        "type": "episode"
    }

More information is available at [guessit-io.github.io/guessit](https://guessit-io.github.io/guessit).

JavaScript / TypeScript port
----------------------------

Looking for a JavaScript implementation? [guessit-js](https://github.com/opensubtitles/guessit-js) is a third-party TypeScript/WASM port (maintained by [OpenSubtitles](https://www.opensubtitles.org)) that runs in Node, browsers and WASM with no Python required. It is not affiliated with this project.

Supported languages
-------------------

GuessIt handles two independent notions of "language".

**Season / episode keywords.** Beyond English, GuessIt recognises season and
episode markers written in several languages, in both `keyword number` and
`number keyword` order (e.g. `Temporada 2` and `2ª Temporada`, `Сезон 3` and
`3 сезон`), as well as the compact `T02E22` / `T01XE08` form:

| Language | Season | Episode |
|---|---|---|
| English | `season`, `seasons` | `episode(s)`, `ep`, `eps` |
| French | `saison`, `saisons` | `épisode(s)` |
| Dutch | `seizoen` | `aflevering`, `afl` |
| German | `staffel` (also `2. Staffel`) | `folge` |
| Spanish / Portuguese | `temporada(s)`, `tem`, `temp` (with ordinals `1ª`/`04ª`/`3º`) | `capítulo(s)`, `episodio(s)` |
| Italian | `stagione` | `episodio` |
| Polish | `sezon` | `odcinek` |
| Romanian | `sezonul` | `episodul` |
| Hungarian | `2. évad` | `5. rész` |
| Scandinavian | `säsong`, `sesong`, `sæson` | `avsnitt` |
| Russian | `сезон` (incl. `5-й сезон`, `Сезон №9`) | `серия`, `серии`, `эпизод` |
| Turkish | `sezon` | `bölüm` |
| Japanese / Chinese | `第…季`, `シーズン…`, `…期` | `第…話`, `第…集` |

Episode numbers are also detected for the plain English `episode` spelling
regardless of the title's language. These keyword lists are configurable — see
the [configuration docs](https://guessit-io.github.io/guessit/configuration/).

**Spoken / subtitle language.** The `language` and `subtitle_language`
properties detect the audio and subtitle language from tags such as `VOSTFR`,
`MULTi`, `ITA`, `ENG`, … and resolve them through
[babelfish](https://github.com/Diaoul/babelfish), which covers essentially every
ISO 639 language. Use the `allowed_languages` option to restrict the recognised
set.

Support
-------

This project is hosted on [GitHub](https://github.com/guessit-io/guessit). Feel free to open an issue if you think you have found a bug or something is missing in guessit.

GuessIt relies on [Rebulk](https://github.com/Toilal/rebulk) project for pattern and rules registration.

License
-------

GuessIt is licensed under the [LGPLv3 license](http://www.gnu.org/licenses/lgpl.html).
