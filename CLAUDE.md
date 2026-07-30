# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

GuessIt is a Python library that extracts metadata (title, season, episode, codec, release group, etc.) from video filenames using pattern matching. It uses the **Rebulk** library as its rule engine.

## Common Commands

This project uses **uv** for packaging, dependencies, and builds (PEP 621 `pyproject.toml` + `uv.lock`, hatchling backend). There is no `setup.py` or `requirements.txt`. Multi-version testing uses `tox` (with `tox-uv`, see `tox.ini`).

```bash
# Create the dev environment (virtualenv + dev/test dependencies, from uv.lock)
uv sync

# Run all tests (includes doctests)
uv run pytest

# Run a single test file
uv run pytest guessit/test/test_api.py

# Run a single test by name
uv run pytest -k test_default

# Run only the YAML-driven matcher tests
uv run pytest guessit/test/test_yml.py

# Run the opt-in cross-parser tests (excluded from the default run)
uv run pytest -m cross_parser
# Re-import / refresh the cross-parser datasets + baseline (needs network; run rarely)
uv run python scripts/import_cross_parser_tests.py

# Lint (ruff, config in pyproject.toml [tool.ruff])
uv run ruff check guessit
# Auto-fix lint issues
uv run ruff check guessit --fix
# Format
uv run ruff format
# Type-check (mypy strict, config in pyproject.toml [tool.mypy])
uv run mypy

# Install the git hooks (pre-commit: ruff check + format + mypy; commit-msg: commitizen)
uv run pre-commit install
# Run all file hooks manually (what the CI `pre-commit` job runs)
uv run pre-commit run --all-files

# Run tests on a specific Python version
uv run --python 3.11 pytest
# Run the full multi-version test matrix locally (tox-uv)
uv run tox
# ... or a single environment
uv run tox -e py312

# Build the sdist + wheel
uv build

# Regenerate the property schema (guessit/schema_generated.py + guessit/data/output-schema.json)
uv run python scripts/gen_schema.py

# CLI usage (use --json / --yaml for structured output)
uv run guessit "Treme.1x03.HDTV.XviD-NoTV.avi"
```

The pytest config lives in `pyproject.toml` (`[tool.pytest.ini_options]`) and enables `--doctest-modules` and `--doctest-glob='*.rst'`, so docstring examples and `.rst` docs are executed as part of the suite — keep them accurate when editing.

## Architecture

### Rule Engine (Rebulk-based)

The core parsing is built on **Rebulk**, a declarative pattern matching library. Each media property (episodes, codec, language, etc.) has its own rule module under `guessit/rules/properties/`, exposing a factory function that takes a config dict and returns a configured `Rebulk` instance. All rules are composed together in `guessit/rules/__init__.py:rebulk_builder()`.

**Rule ordering matters.** `rebulk_builder()` registers properties in a deliberate sequence, and later rules can post-process or override earlier matches. When adding a property, create a module under `rules/properties/`, then import and register it in `rebulk_builder()` at the right position. `rules/processors.py` and `rules/markers/` (path, groups) handle cross-cutting post-processing of the match set; `rules/common/` holds shared validators/formatters.

### API Layers

- **Public API** (`guessit/__init__.py`): `guessit()`, `properties()`, `schema()`, `json_schema()`, `suggested_expected()`
- **GuessItApi class** (`guessit/api.py`): Core implementation, manages Rebulk configuration and execution
- **CLI** (`guessit/__main__.py`): Command-line interface, supports JSON/YAML output

### Property schema

`guessit/schema_generated.py` (`GUESSIT_SCHEMA`) and `guessit/data/output-schema.json` (JSON Schema draft-07) are the machine-readable description of every property guessit can emit — type, cardinality, and closed-vocabulary enums. **Both are generated** by `scripts/gen_schema.py` from `api.properties()` + the YAML corpus; never hand-edit them. They describe the **default configuration**. The public accessors `schema(options)` / `json_schema(options)` (in `api.py`, exported from `guessit`) build a **configuration-aware** schema on top of that frozen base: type/cardinality come from `GUESSIT_SCHEMA`, enums are overlaid from `properties(options)` (see `guessit/schema_builder.py`). The bare `guessit.GUESSIT_SCHEMA` constant is still exported but **deprecated** in favour of `schema()`. `GuessItApi.properties()` uses the schema to stay code-complete (advertises every property and its full enum). `test_schema.py` fails if the committed files drift from the generator.

### Configuration

- Default config: `guessit/config/options.json`
- Users can customize via `--config` CLI flag or programmatic `options` dict
- Options are merged: default → user config → programmatic options
- **All tokens and word lists must live in the configuration** (`options.json`, under
  `advanced_config.<property>`), never hard-coded in a rule module. A rule reads its lists from
  the `config` dict its builder receives; this keeps every vocabulary user-overridable. When
  adding a feature that needs keywords/stop-words/function-words, add them to `advanced_config`
  and thread them through the property builder — do not inline a `frozenset`/list literal.
- **Do not base rules on letter case.** Guessit is case-insensitive by design (patterns match
  regardless of case), so a rule must not use casing as a discriminator (`re.match(r"^[A-Z]...")`,
  `.isupper()`, etc.). Real release names come in Title-Case, lowercase and UPPERCASE alike;
  keying on case makes a rule silently miss the other spellings. Prefer a structural signal
  (position relative to an anchor, separators, neighbouring matches, a config tag). Rare, clearly
  justified exceptions may exist, but the default is case-agnostic.

### Tests

Tests live in `guessit/test/`. The YAML files (`episodes.yml`, `movies.yml`, `various.yml`, etc.) are the primary regression corpus: `test_yml.py` discovers every `.yml`/`.yaml` file and parametrizes one pytest case per entry, mapping a filename to its expected parsed properties. **To cover a new filename pattern or fix, add an entry to the relevant YAML file** rather than writing a new Python test. Entry strings support token prefixes parsed by `parse_token_options` (e.g. negation and "global match" checks). Python test files (`test_api.py`, `test_main.py`, `test_options.py`, `test_benchmark.py`) handle API, CLI, options, and benchmarks.

**Cross-parser tests** (`test_cross_parser.py`, marker `cross_parser`, opt-in via `pytest -m cross_parser`, excluded from the default run): thousands of `(release_name → expected fields)` assertions imported from the test fixtures of other permissively-licensed parsers (PTT, anitomy, scene-release-parser, PTN, go-ptn) and mapped into the guessit vocabulary by `scripts/import_cross_parser_tests.py`. The vendored data lives in `guessit/test/cross_parser/*.json` (generated — do not hand-edit; see `cross_parser/NOTICE.md` for MIT/MPL-2.0 attribution). There is **one test per external parser**. Independent parsers legitimately disagree, so these tests are not meant to make guessit match every label: every field guessit does not currently satisfy is recorded in `cross_parser/baseline.json`, and a parser's test fails only on a **new** divergence (a regression). Regenerate the datasets + baseline with `python scripts/import_cross_parser_tests.py` after an intentional behaviour change.

## Branch Strategy

- **develop**: main development branch (PR target)
- **main**: release branch (triggers semantic-release automation)
- Conventional commits required — enforced locally by the commitizen commit-msg
  hook (`.pre-commit-config.yaml`) and in CI by the `commitizen` job (`cz check`).
  Config: `[tool.commitizen]` in `pyproject.toml`. Versioning/releases stay owned
  by python-semantic-release, not commitizen.
- To auto-close the related issue when a PR merges, use a GitHub closing keyword
  (`closes #NNN` / `fixes #NNN`) in the commit message or PR body. A bare `(#NNN)`
  only references the issue — it does **not** close it.
