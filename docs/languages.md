# Supported languages

GuessIt handles two independent notions of "language".

## Season / episode keywords

Beyond English, GuessIt recognises season and episode markers written in
several languages, in both `keyword number` and `number keyword` order
(e.g. `Temporada 2` and `2ª Temporada`, `Сезон 3` and `3 сезон`), as well as
the compact `T02E22` / `T01XE08` form:

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
the [configuration docs](configuration.md).

## Spoken / subtitle language

The `language` and `subtitle_language` properties detect the audio and subtitle
language from tags such as `VOSTFR`, `MULTi`, `ITA`, `ENG`, … and resolve them
through [babelfish](https://github.com/Diaoul/babelfish), which covers
essentially every ISO 639 language. Use the `allowed_languages` option to
restrict the recognised set.
