Migration
=========
Guessit 2 has been rewritten from scratch. You can find in this file all information required to perform a
migration from previous version ``0.x`` or ``1.x``.

API
----
``guess_video_info``, ``guess_movie_info`` and ``guess_episode_info`` have been removed in favor of a unique function
``guessit``.

Example::

    >>> from guessit import guessit
    >>> guessit(u'Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi')  # doctest: +ALLOW_UNICODE
    MatchesDict([('title', 'Treme'), ('season', 1), ('episodeNumber', 3), ('episodeTitle', 'Right Place, Wrong Time'), ('format', 'HDTV'), ('videoCodec', 'XviD'), ('releaseGroup', 'NoTV'), ('container', 'avi'), ('mimetype', 'video/x-msvideo'), ('type', 'episode')])

``MatchesDict`` is a dict that keeps matches ordering.

Command line options can be given as dict or string to the second argument.

GuessIt only accept unicode string, so you need to use ``u`` prefix for input string on python 2.

Properties
----------
For ``episode`` type, some properties have been renamed

- ``series`` is now ``title``.
- ``title`` is now ``episodeTitle``.

``episodeList`` and ``partList`` were removed. ``episodeNumber`` and ``part`` properties that can now be a ``list``
when multiple values are found.

For ``movie`` type, some properties have been renamed

- ``filmtitle`` is now ``filmSeries``

All info ``type``, like ``seriesinfo`` and ``movieinfo``, have been removed in favor of checking the ``container``
property for ``nfo`` value.

All other properties have been ported with the same name.

Options
-------
Some options have been removed.

- ``-t TYPE, --type TYPE``

  GuessIt now guess filetype after all other matches and doesn't require user to specify the filetype in advance.

- ``-X DISABLED_TRANSFORMERS``, ``-s, --transformers``

  There's no transformer anymore.

- ``-S EXPECTED_SERIES``

  As ``series`` was renamed to ``title``, use ``-T EXPECTED_TITLE`` instead.

- ``-G EXPECTED_GROUP``

  GuessIt is now better to guess release group, so this option has been removed.

- ``-d, --demo``

  Probably not that useful.

- ``-i INFO, --info INFO``

  Features related to this option have been removed.

- ``-c, --split-camel``, ``-u, --unidentified``, ``-b, --bug``, ``-p, --properties``, ``-V, --values``

  Will be back soon... (work in progress)

Others GuessIt ``1.x`` options have been kept.

Output
------
Output produced by ``guessit`` api function is now an instance or
[OrderedDict](https://docs.python.org/2/library/collections.html#collections.OrderedDict). Property values are
automatically ordered based on filename, and you can still use this output as a default python ``dict``.

If multiple values are available for a property, value in the dict will be a ``list`` instance.

Advanced display option (``-a, --advanced``) output is also changed. It now list ``Match`` objects from
`Rebulk <https://github.com/Toilal/rebulk>`_, and may display duplicates that would have been merged in standard
output.::

    $ guessit "Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi" -a
    For: Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi
    GuessIt found: {
        "title": {
            "value": "Treme",
            "raw": "Treme.",
            "start": 0,
            "end": 6
        },
        "season": {
            "value": 1,
            "raw": "1",
            "start": 6,
            "end": 7
        },
        "episodeNumber": {
            "value": 3,
            "raw": "03",
            "start": 8,
            "end": 10
        },
        "episodeTitle": {
            "value": "Right Place, Wrong Time",
            "raw": ".Right.Place,.Wrong.Time.",
            "start": 10,
            "end": 35
        },
        "format": {
            "value": "HDTV",
            "raw": "HDTV",
            "start": 35,
            "end": 39
        },
        "videoCodec": {
            "value": "XviD",
            "raw": "XviD",
            "start": 40,
            "end": 44
        },
        "releaseGroup": {
            "value": "NoTV",
            "raw": "-NoTV",
            "start": 44,
            "end": 49
        },
        "container": {
            "value": "avi",
            "raw": ".avi",
            "start": 49,
            "end": 53
        },
        "mimetype": {
            "value": "video/x-msvideo",
            "start": 53,
            "end": 53
        },
        "type": {
            "value": "episode",
            "start": 53,
            "end": 53
        }
    }
