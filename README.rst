GuessIt
=======

.. image:: https://pypip.in/v/guessit/badge.png
    :target: https://pypi.python.org/pypi/guessit
    :alt: Latest Version

.. image:: https://pypip.in/license/guessit/badge.png
    :target: https://pypi.python.org/pypi/guessit
    :alt: License

.. image:: https://secure.travis-ci.org/wackou/guessit.png?branch=master
    :target: http://travis-ci.org/wackou/guessit
    :alt: Build Status

.. image:: https://coveralls.io/repos/wackou/guessit/badge.png?branch=master
    :target: https://coveralls.io/r/wackou/guessit?branch=master
    :alt: Coveralls


GuessIt is a python library that tries to extract as much information as
possible from a video file.

It has a very powerful filename matcher that allows to guess a lot of
metadata from a video using only its filename. This matcher works with
both movies and tv shows episodes.

For example, GuessIt can do the following::

    $ python -m guessit "Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi"
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



Features
--------

At the moment, the filename matcher is able to recognize the following
property types::

    [ title,                             # for movies and episodes
      series, season,                    # for episodes only
      episodeNumber, special,            # for episodes only
      date, year,                        # 'date' instance of datetime.date
      language, subtitleLanguage,        # instances of guessit.Language
      country,                           # instances of guessit.Country
      container, format,
      videoCodec, audioCodec,
      videoProfile, audioProfile,
      audioChannels, screenSize,
      releaseGroup, website,
      cdNumber, cdNumberTotal,
      filmNumber, filmSeries,
      bonusNumber, edition,
      idNumber,                          # tries to identify a hash or a serial number
      other
      ]


GuessIt also allows you to compute a whole lof of hashes from a file,
namely all the ones you can find in the hashlib python module (md5,
sha1, ...), but also the Media Player Classic hash that is used (amongst
others) by OpenSubtitles and SMPlayer, as well as the ed2k hash.

If you have the 'guess-language' python module installed, GuessIt can also
analyze a subtitle file's contents and detect which language it is written in.


Install
-------

Installing GuessIt is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install guessit

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install guessit

But, you really `shouldn't do that <http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install>`_.



Support
-------

The project website for GuessIt is hosted at `ReadTheDocs <http://guessit.readthedocs.org/>`_.
There you will also find the User guide and Developer documentation.

This project is hosted on GitHub: `<https://github.com/wackou/guessit>`_

Please report issues via the `bug tracker <https://github.com/wackou/guessit/issues>`_.


Contribute
----------

GuessIt is under active development, and contributions are more than welcome!

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
   There is a Contributor Friendly tag for issues that should be ideal for people who are not very
   familiar with the codebase yet.
#. Fork `the repository`_ on Github to start making your changes to the **master**
   branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :)

.. _the repository: https://github.com/wackou/guessit

License
-------

GuessIt is licensed under the `LGPLv3 license <http://www.gnu.org/licenses/lgpl.html>`_.
