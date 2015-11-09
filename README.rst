GuessIt
=======

.. image:: http://img.shields.io/pypi/v/guessit.svg
    :target: https://pypi.python.org/pypi/guessit
    :alt: Latest Version

.. image:: http://img.shields.io/badge/license-LGPLv3-blue.svg
    :target: https://pypi.python.org/pypi/guessit
    :alt: LGPLv3 License

.. image:: http://img.shields.io/travis/wackou/guessit/2.x.svg
    :target: https://travis-ci.org/wackou/guessit
    :alt: Build Status

.. image:: http://img.shields.io/coveralls/wackou/guessit/2.x.svg
    :target: https://coveralls.io/github/wackou/guessit?branch=2.x
    :alt: Coveralls

`HuBoard <https://huboard.com/wackou/guessit>`_


GuessIt is a python library that extracts as much information as possible from a video filename.

It has a very powerful matcher that allows to guess a lot of metadata from a video using its filename only.
This matcher works with both movies and tv shows episodes.

For example, GuessIt can do the following::

    $ guessit "Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi"
    For: Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi
    GuessIt found: {
        "title": "Treme",
        "season": 1,
        "episode": 3,
        "episode_title": "Right Place, Wrong Time",
        "format": "HDTV",
        "video_codec": "XviD",
        "release_group": "NoTV",
        "container": "avi",
        "mimetype": "video/x-msvideo",
        "type": "episode"
    }

Important note
--------------
GuessIt 2 has been rewriten from scratch and is currently in Beta. GuessIt is now a release name parser only, and
support for additional features like hashes computations has been dropped.

To migrate from guessit ``0.x`` or ``1.x``, please read
`MIGRATION.rst <https://github.com/wackou/guessit/blob/2.x/MIGRATION.rst>`_.

Previous version of GuessIt is still available in ``1.x`` branch and using ``pip install guessit<2``, but won't be
maintained anymore.

Install
-------

Installing GuessIt is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install guessit

Filename matcher
----------------

The filename matcher is based on `Rebulk <https://www.github.com/Toilal/rebulk>`_ and is able to recognize many
properties from the filename. Guessed values are cleaned up and given in a readable format which may not match
exactly the raw filename.

Usage
-----

guessit can be use from command line::

    $ guessit
    usage: -c [-h] [-n] [-Y] [-D] [-L ALLOWED_LANGUAGES] [-C ALLOWED_COUNTRIES]
          [-E] [-T EXPECTED_TITLE] [-f INPUT_FILE] [-v] [-P SHOW_PROPERTY]
          [-a] [-j] [-y] [--version]
          [filename [filename ...]]

    positional arguments:
      filename              Filename or release name to guess

    optional arguments:
      -h, --help            show this help message and exit

    Naming:
      -n, --name-only       Parse files as name only, considering "/" and "\" like
                            other separators.
      -Y, --date-year-first
                            If short date is found, consider the first digits as
                            the year.
      -D, --date-day-first  If short date is found, consider the second digits as
                            the day.
      -L ALLOWED_LANGUAGES, --allowed-languages ALLOWED_LANGUAGES
                            Allowed language (can be used multiple times)
      -C ALLOWED_COUNTRIES, --allowed-countries ALLOWED_COUNTRIES
                            Allowed country (can be used multiple times)
      -E, --episode-prefer-number
                            Guess "serie.213.avi" as the episodeNumber 213.
                            Without this option, it will be guessed as season 2,
                            episodeNumber 13
      -T EXPECTED_TITLE, --expected-title EXPECTED_TITLE
                            Expected title to parse (can be used multiple times)

    Input:
      -f INPUT_FILE, --input-file INPUT_FILE
                            Read filenames from an input text file. File should
                            use UTF-8 charset.

    Output:
      -v, --verbose         Display debug output
      -P SHOW_PROPERTY, --show-property SHOW_PROPERTY
                            Display the value of a single property (title, series,
                            videoCodec, year, ...)
      -a, --advanced        Display advanced information for filename guesses, as
                            json output
      -j, --json            Display information for filename guesses as json
                            output
      -y, --yaml            Display information for filename guesses as yaml
                            output

    Information:
      --version             Display the guessit version.

It can also be used as a python module::

    >>> from guessit import guessit
    >>> guessit(u'Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi')  # doctest: +ALLOW_UNICODE
    MatchesDict([('title', 'Treme'), ('season', 1), ('episode', 3), ('episode_title', 'Right Place, Wrong Time'), ('format', 'HDTV'), ('video_codec', 'XviD'), ('release_group', 'NoTV'), ('container', 'avi'), ('mimetype', 'video/x-msvideo'), ('type', 'episode')])

``MatchesDict`` is a dict that keeps matches ordering.

Command line options can be given as dict or string to the second argument.

GuessIt only accept unicode string, so you need to use ``u`` prefix for input string on python 2.


Support
-------

This project is hosted on GitHub: `<https://github.com/wackou/guessit>`_

Docs will be available soon availabe ReadTheDocs.

Contribute
----------

GuessIt is under active development, and contributions are more than welcome!

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
   There is a Contributor Friendly tag for issues that should be ideal for people who are not very
   familiar with the codebase yet.
#. Fork `the repository`_ on Github to start making your changes to the **2.x**
   branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :)

.. _the repository: https://github.com/wackou/guessit/tree/2.x

License
-------

GuessIt is licensed under the `LGPLv3 license <http://www.gnu.org/licenses/lgpl.html>`_.
