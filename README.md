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

Python usage
------------

As a library, `guessit()` returns an ordered `MatchesDict` of the detected properties:

    >>> from guessit import guessit

    >>> guessit('The.Matrix.1999.1080p.BluRay.x264-GROUP.mkv')
    MatchesDict({'title': 'The Matrix', 'year': 1999, 'screen_size': '1080p', 'source': 'Blu-ray', 'video_codec': 'H.264', 'release_group': 'GROUP', 'container': 'mkv', 'mimetype': 'video/matroska', 'type': 'movie'})

    >>> guessit('[Anime-Group] Attack on Titan - 25 [1080p][HEVC].mkv')
    MatchesDict({'release_group': 'Anime-Group', 'title': 'Attack on Titan', 'episode': 25, 'screen_size': '1080p', 'video_codec': 'H.265', 'video_profile': 'High Efficiency Video Coding', 'container': 'mkv', 'mimetype': 'video/matroska', 'type': 'episode'})

    >>> guessit('Shameless.US.S05E10.720p.HDTV.x264-KILLERS.mkv')
    MatchesDict({'title': 'Shameless', 'country': <Country [US]>, 'season': 5, 'episode': 10, 'screen_size': '720p', 'source': 'HDTV', 'video_codec': 'H.264', 'release_group': 'KILLERS', 'container': 'mkv', 'mimetype': 'video/matroska', 'type': 'episode'})

See the [API & options reference](https://guessit-io.github.io/guessit/api/) for the full API.

Documentation
-------------

Full documentation is available at [guessit-io.github.io/guessit](https://guessit-io.github.io/guessit).

JavaScript / TypeScript port
----------------------------

Looking for a JavaScript implementation? [guessit-js](https://github.com/opensubtitles/guessit-js) is a third-party TypeScript/WASM port (maintained by [OpenSubtitles](https://www.opensubtitles.org)) that runs in Node, browsers and WASM with no Python required. It is not affiliated with this project.

Support
-------

This project is hosted on [GitHub](https://github.com/guessit-io/guessit). Feel free to open an issue if you think you have found a bug or something is missing in guessit.

GuessIt relies on [Rebulk](https://github.com/Toilal/rebulk) project for pattern and rules registration.

License
-------

GuessIt is licensed under the [LGPLv3 license](http://www.gnu.org/licenses/lgpl.html).
