GuessIt
=======

.. image:: http://img.shields.io/pypi/v/guessit.svg
    :target: https://pypi.python.org/pypi/guessit
    :alt: Latest Version

.. image:: http://img.shields.io/badge/license-LGPLv3-blue.svg
    :target: https://pypi.python.org/pypi/guessit
    :alt: License

.. image:: http://img.shields.io/travis/guessit-io/guessit/1.x.svg
    :target: https://travis-ci.org/guessit-io/guessit
    :alt: Build Status

.. image:: http://img.shields.io/coveralls/guessit-io/guessit/1.x.svg
    :target: https://coveralls.io/github/guessit-io/guessit?branch=1.x
    :alt: Coveralls

.. image:: https://img.shields.io/badge/Hu-Board-7965cc.svg
    :target: https://huboard.com/guessit-io/guessit
    :alt: HuBoard

`HuBoard <https://huboard.com/guessit-io/guessit>`_


GuessIt is a python library that extracts as much information as
possible from a video filenames.

It has a very powerful matcher that allows to guess a lot of
metadata from a video using its filename only. This matcher works with
both movies and tv shows episodes.

For example, GuessIt can do the following::

    $ guessit "Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi"
    For: Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi
    GuessIt found: {
        [1.00] "mimetype": "video/x-msvideo",
        [0.80] "episodeNumber": 3,
        [0.80] "videoCodec": "XviD",
        [1.00] "container": "avi",
        [1.00] "format": "HDTV",
        [0.70] "series": "Treme",
        [0.50] "title": "Right Place, Wrong Time",
        [0.80] "releaseGroup": "NoTV",
        [0.80] "season": 1,
        [1.00] "type": "episode"
    }

Important note
--------------
GuessIt 2 has been rewriten from scratch and is currently in Alpha. GuessIt is now a release name parser only, and
support for additional features like hashes computations has been dropped.

To migrate from guessit ``0.x`` or ``1.x``, please read
`MIGRATION.rst <https://github.com/guessit-io/guessit/blob/master/MIGRATION.rst>`_.

Previous version of GuessIt is still available in ``1.x`` branch and using ``pip install guessit<2``, but won't be
maintained anymore.


Install
-------

Installing GuessIt is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install "guessit<2"

You can now launch a demo::

    $ guessit -d

and guess your own filename::

    $ guessit "Breaking.Bad.S05E08.720p.MP4.BDRip.[KoTuWa].mkv"
    For: Breaking.Bad.S05E08.720p.MP4.BDRip.[KoTuWa].mkv
    GuessIt found: {
        [1.00] "mimetype": "video/x-matroska",
        [1.00] "episodeNumber": 8,
        [0.30] "container": "mkv",
        [1.00] "format": "BluRay",
        [0.70] "series": "Breaking Bad",
        [1.00] "releaseGroup": "KoTuWa",
        [1.00] "screenSize": "720p",
        [1.00] "season": 5,
        [1.00] "type": "episode"
    }



Filename matcher
----------------

The filename matcher is based on pattern matching and is able to recognize many properties from the filename,
like ``title``, ``year``, ``series``, ``episodeNumber``, ``seasonNumber``,
``videoCodec``, ``screenSize``, ``language``. Guessed values are cleaned up and given in a readable format
which may not match exactly the raw filename.

The full list of available properties can be seen in the
`main documentation <http://guessit.readthedocs.org/en/latest/user/properties.html>`_.


Other features
--------------

GuessIt also allows you to compute a whole lot of hashes from a file,
namely all the ones you can find in the hashlib python module (md5,
sha1, ...), but also the Media Player Classic hash that is used (amongst
others) by OpenSubtitles and SMPlayer, as well as the ed2k hash.

If you have the 'guess-language' python package installed, GuessIt can also
analyze a subtitle file's contents and detect which language it is written in.

If you have the 'enzyme' python package installed, GuessIt can also detect the
properties from the actual video file metadata.


Usage
-----

guessit can be use from command line::

    $ guessit
    usage: guessit [-h] [-t TYPE] [-n] [-c] [-X DISABLED_TRANSFORMERS] [-v]
                   [-P SHOW_PROPERTY] [-u] [-a] [-y] [-f INPUT_FILE] [-d] [-p]
                   [-V] [-s] [--version] [-b] [-i INFO] [-S EXPECTED_SERIES]
                   [-T EXPECTED_TITLE] [-Y] [-D] [-L ALLOWED_LANGUAGES] [-E]
                   [-C ALLOWED_COUNTRIES] [-G EXPECTED_GROUP]
                   [filename [filename ...]]

    positional arguments:
      filename              Filename or release name to guess

    optional arguments:
      -h, --help            show this help message and exit

    Naming:
      -t TYPE, --type TYPE  The suggested file type: movie, episode. If undefined,
                            type will be guessed.
      -n, --name-only       Parse files as name only. Disable folder parsing,
                            extension parsing, and file content analysis.
      -c, --split-camel     Split camel case part of filename.
      -X DISABLED_TRANSFORMERS, --disabled-transformer DISABLED_TRANSFORMERS
                            Transformer to disable (can be used multiple time)
      -S EXPECTED_SERIES, --expected-series EXPECTED_SERIES
                            Expected series to parse (can be used multiple times)
      -T EXPECTED_TITLE, --expected-title EXPECTED_TITLE
                            Expected title (can be used multiple times)
      -Y, --date-year-first
                            If short date is found, consider the first digits as
                            the year.
      -D, --date-day-first  If short date is found, consider the second digits as
                            the day.
      -L ALLOWED_LANGUAGES, --allowed-languages ALLOWED_LANGUAGES
                            Allowed language (can be used multiple times)
      -E, --episode-prefer-number
                            Guess "serie.213.avi" as the episodeNumber 213.
                            Without this option, it will be guessed as season 2,
                            episodeNumber 13
      -C ALLOWED_COUNTRIES, --allowed-country ALLOWED_COUNTRIES
                            Allowed country (can be used multiple times)
      -G EXPECTED_GROUP, --expected-group EXPECTED_GROUP
                            Expected release group (can be used multiple times)

    Output:
      -v, --verbose         Display debug output
      -P SHOW_PROPERTY, --show-property SHOW_PROPERTY
                            Display the value of a single property (title, series,
                            videoCodec, year, type ...)
      -u, --unidentified    Display the unidentified parts.
      -a, --advanced        Display advanced information for filename guesses, as
                            json output
      -y, --yaml            Display information for filename guesses as yaml
                            output (like unit-test)
      -f INPUT_FILE, --input-file INPUT_FILE
                            Read filenames from an input file.
      -d, --demo            Run a few builtin tests instead of analyzing a file

    Information:
      -p, --properties      Display properties that can be guessed.
      -V, --values          Display property values that can be guessed.
      -s, --transformers    Display transformers that can be used.
      --version             Display the guessit version.

    guessit.io:
      -b, --bug             Submit a wrong detection to the guessit.io service

    Other features:
      -i INFO, --info INFO  The desired information type: filename, video,
                            hash_mpc or a hash from python's hashlib module, such
                            as hash_md5, hash_sha1, ...; or a list of any of them,
                            comma-separated


It can also be used as a python module::

    >>> from guessit import guess_file_info
    >>> guess_file_info('Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi')
    {u'mimetype': 'video/x-msvideo', u'episodeNumber': 3, u'videoCodec': u'XviD', u'container': u'avi', u'format':     u'HDTV', u'series': u'Treme', u'title': u'Right Place, Wrong Time', u'releaseGroup': u'NoTV', u'season': 1, u'type': u'episode'}


Support
-------

The project website for GuessIt is hosted at `ReadTheDocs <http://guessit.readthedocs.org/>`_.
There you will also find the User guide and Developer documentation.

This project is hosted on GitHub: `<https://github.com/guessit-io/guessit>`_

Please report issues and/or feature requests via the `bug tracker <https://github.com/guessit-io/guessit/issues>`_.

You can also report issues using the command-line tool::

    $ guessit --bug "filename.that.fails.avi"


Contribute
----------

GuessIt is under active development, and contributions are more than welcome!

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
   There is a Contributor Friendly tag for issues that should be ideal for people who are not very
   familiar with the codebase yet.
#. Fork `the repository`_ on Github to start making your changes to the **1.x**
   branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :)

.. _the repository: https://github.com/guessit-io/guessit

License
-------

GuessIt is licensed under the `LGPLv3 license <http://www.gnu.org/licenses/lgpl.html>`_.
