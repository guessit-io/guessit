GuessIt

[![Latest Version](https://img.shields.io/pypi/v/guessit.svg)](https://pypi.python.org/pypi/guessit)
[![LGPLv3 License](https://img.shields.io/badge/license-LGPLv3-blue.svg)]()
[![Build Status](https://img.shields.io/github/workflow/status/guessit-io/guessit/ci)](https://github.com/guessit-io/guessit/actions?query=workflow%3Aci)
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

More information are available at [guessit.io](http://guessit.io/).

Support
-------

This project is hosted on [GitHub](https://github.com/guessit-io/guessit). Feel free to open an issue if you think you have found a bug or something is missing in guessit.

GuessIt relies on [Rebulk](https://github.com/Toilal/rebulk) project for pattern and rules registration.

License
-------

GuessIt is licensed under the [LGPLv3 license](http://www.gnu.org/licenses/lgpl.html).
