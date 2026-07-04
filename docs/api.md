# API and options

GuessIt can be used from the command line or as a Python library. Both accept
the same set of options — on the command line as flags, in Python as a dict (or
a CLI-style string).

## Command line

```bash
$ guessit "Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi"
```

Useful flags:

- `--json` / `-j`, `--yaml` / `-y` — structured output.
- `--advanced` / `-a` — include each match's raw span and position.
- `--show-property <name>` / `-P` — print a single property value.
- `--input-file <path>` / `-f` — read filenames from a UTF-8 text file.
- `--properties` / `-p`, `--values` / `-V` — list what GuessIt can detect (see
  [Discovering properties and values](#discovering-properties-and-values)).
- `--schema`, `--json-schema` — print the property schema, or its
  [JSON Schema](https://json-schema.org/) (draft-07), for the effective
  configuration. Both honour `--json` / `--yaml` and reflect `--config`.

Run `guessit --help` for the complete list.

## Python API

### `guessit(string, options=None)`

Parse a filename or release name and return a `MatchesDict` — an ordered dict of
the detected properties:

```python
>>> from guessit import guessit
>>> guessit('Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi')
MatchesDict({'title': 'Treme', 'season': 1, 'episode': 3, 'episode_title': 'Right Place, Wrong Time', 'source': 'HDTV', 'video_codec': 'Xvid', 'release_group': 'NoTV', 'container': 'avi', 'mimetype': 'video/x-msvideo', 'type': 'episode'})

```

A property whose value is a list keeps every match; `enforce_list` (below) forces
every property to a list for uniform handling.

### Passing options

The second argument accepts either a dict or a command-line-style string. These
are equivalent:

```python
guessit('Movie.2020.1080p.mkv', {'type': 'movie', 'excludes': ['screen_size']})
guessit('Movie.2020.1080p.mkv', '--type movie --excludes screen_size')
```

Options coming from configuration files are merged with the ones passed here;
see [Configuration](configuration.md) for the merge rules and the `pristine`
override.

### `GuessItApi`

`guessit()` delegates to a shared default instance. Building your own instance
lets you parse many names while reusing the compiled configuration: pass the
same options on each call and the instance skips rebuilding the rules when the
options are unchanged.

```python
from guessit import GuessItApi

api = GuessItApi()
options = {'expected_title': ['The 100']}
api.guessit('The 100', options)
api.guessit('The 100 S01E01', options)  # reuses the cached configuration
```

### Discovering properties and values

Several mechanisms expose what GuessIt can emit:

- `properties(options=None)` — a dict mapping every property to the list of
  values it can produce (empty list for free-form values).
- `schema(options=None)` — a mapping of each property to its type, cardinality
  and (for closed vocabularies) allowed values.
- `json_schema(options=None)` — the same information as a
  [JSON Schema](https://json-schema.org/) (draft-07).
- `guessit.GUESSIT_SCHEMA` — the frozen schema for the default configuration
  (what `schema()` returns with no options); `guessit/data/output-schema.json`
  is its JSON Schema counterpart.
- On the command line, `guessit -p` lists the properties, `guessit -V` lists
  their possible values, and `guessit --schema` / `guessit --json-schema` print
  the two schema forms.

For example:

```python
>>> from guessit import properties
>>> 'Blu-ray' in properties()['source']
True

```

`schema()` and `json_schema()` are **configuration-aware**: a property's type and
cardinality are configuration invariants (taken from the frozen `GUESSIT_SCHEMA`),
but the closed-vocabulary enums reflect the configuration you pass, so a custom
`advanced_config` value shows up in the returned schema:

```python
>>> from guessit import schema
>>> options = {'advanced_config': {'streaming_service': {'MyOwnTV': 'myowntv'}}}
>>> 'MyOwnTV' in schema(options)['streaming_service']['enum']
True

```

`GUESSIT_SCHEMA`, `properties()`, `schema()`, `json_schema()` and
`suggested_expected()` are all exported from the top-level `guessit` package (and
are also available as methods on `GuessItApi`).

### `suggested_expected(titles)`

Given an iterable of known titles, return the subset that GuessIt would
mis-parse into extra properties — good candidates to feed back as
`expected_title`:

```python
>>> from guessit import suggested_expected
>>> suggested_expected(['OSS 117', 'The 100', 'Normal Movie Title'])
['The 100']

```

Here `The 100` is otherwise read as season 1 / episode 0; declaring it as an
expected title fixes the guess:

```python
guessit('The 100', {'expected_title': ['The 100']})
# -> title 'The 100', type 'movie'
```

## Options reference

Command-line flags map to dict keys by replacing `-` with `_` (e.g.
`--allowed-languages` → `allowed_languages`). Options that take several values
can be repeated on the command line and are lists in the dict form.

### Naming

- **`type`** (`-t`) — force the file type, `movie` or `episode`, instead of
  guessing it.
- **`name_only`** (`-n`) — treat the whole string as a name, so `/` and `\` are
  ordinary separators rather than path boundaries.
- **`date_year_first`** (`-Y`) / **`date_day_first`** (`-D`) — disambiguate a
  short date by fixing whether the leading digits are the year or the day.
- **`episode_prefer_number`** (`-E`) — parse `serie.213.avi` as episode 213
  rather than season 2 / episode 13.
- **`expected_title`** (`-T`) — titles that must be parsed verbatim, protecting
  titles that would otherwise be split into properties (see
  [`suggested_expected`](#suggested_expectedtitles)).
- **`expected_group`** (`-G`) — release-group names to always recognise.
- **`allowed_languages`** (`-L`) / **`allowed_countries`** (`-C`) — restrict the
  recognised languages / countries (see [Languages](languages.md)).
- **`includes`** / **`excludes`** — restrict detection to, or skip, the named
  properties.

### Output shaping

- **`single_value`** (`-s`) — keep only the first value found for each property.
- **`enforce_list`** (`-l`) — wrap every value in a list, even single ones.
- **`output_input_string`** (`-i`) — add the original `input_string` to the
  result.

### Configuration

- **`config`** (`-c`), **`no_user_config`**, **`no_default_config`** — control
  which configuration files are loaded. See [Configuration](configuration.md).
