GuessIt
=======

[![Latest Version](https://img.shields.io/pypi/v/guessit.svg)](https://pypi.python.org/pypi/guessit)
[![LGPLv3 License](https://img.shields.io/badge/license-LGPLv3-blue.svg)]()
[![Build Status](https://img.shields.io/github/workflow/status/guessit-io/guessit/ci)](https://github.com/guessit-io/guessit/actions?query=workflow%3Aci)
[![Coveralls](https://img.shields.io/coveralls/guessit-io/guessit/main.svg)](https://coveralls.io/github/guessit-io/guessit?branch=main)
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

Install
-----

Install GuessIt with [pip](https://pip.pypa.io/):

```bash
pip install guessit
```

Or add it to your project with [uv](https://docs.astral.sh/uv/):

```bash
uv add guessit
```

You can also run the CLI without installing it, with uvx:

```bash
uvx guessit "Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi"
```

You can also [install GuessIt from sources](./sources.md).

Usage
-----

GuessIt can be used from the command line:

```bash
$ guessit "Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi"
```

Run `guessit --help` for the full list of options. Use `guessit -p` to list the
properties GuessIt can detect and `guessit -V` to list their possible values.

It can also be used as a python module:

```python
>>> from guessit import guessit
>>> guessit('Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi')
MatchesDict({'title': 'Treme', 'season': 1, 'episode': 3, 'episode_title': 'Right Place, Wrong Time', 'source': 'HDTV', 'video_codec': 'Xvid', 'release_group': 'NoTV', 'container': 'avi', 'mimetype': 'video/x-msvideo', 'type': 'episode'})

```

`MatchesDict` is a dict that keeps matches ordering.

Command line options can be given as dict or string to the second argument. See
the [API & options reference](./api.md) for the full API and every option.

Configuration
-------------

Find more about Guessit configuration at [configuration page](./configuration.md).

Support
-------

This project is hosted on [GitHub](https://github.com/guessit-io/guessit). Feel free to open an issue if you think you have found a bug or something is missing in guessit.

Some filename shapes are inherently ambiguous to a structural parser; the ones guessit deliberately does not resolve are documented on the [known limitations page](./known-limitations.md).

GuessIt relies on [Rebulk](https://github.com/Toilal/rebulk) project for pattern and rules registration.

License
-------

GuessIt is licensed under the [LGPLv3 license](http://www.gnu.org/licenses/lgpl.html).
