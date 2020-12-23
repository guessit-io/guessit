Migration
=========

Guessit 2 has been rewritten from scratch. You can find in this file all information required to perform a migration from previous version `0.x` or `1.x`.

API
---

`guess_video_info`, `guess_movie_info` and `guess_episode_info` have been removed in favor of a unique function `guessit`.

Example:

    >>> from guessit import guessit
    >>> guessit('Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi')
    MatchesDict([('title', 'Treme'), ('season', 1), ('episode', 3), ('episode_title', 'Right Place, Wrong Time'), ('format', 'HDTV'), ('video_codec', 'XviD'), ('release_group', 'NoTV'), ('container', 'avi'), ('mimetype', 'video/x-msvideo'), ('type', 'episode')])

`MatchesDict` is a dict that keeps matches ordering.

Command line options can be given as dict or string to the second argument.

Properties
----------

Some properties have been renamed.

-   `series` is now `title`.
-   `title` is now `episode_title` (for `episode` `type` only).
-   `episodeNumber` is now `episode`.
-   `bonusNumber` is now `bonus`
-   `filmNumber` is now `film`
-   `cdNumber` is now `cd ` and `cdNumberTotal` is now `cd_count`
-   `idNumber` is now `uuid`

`episodeList` and `partList` have been removed. `episode_number` and `part` properties that can now contains an `int` or a `list[int]`.

All info `type`, like `seriesinfo` and `movieinfo`. You can check directly `nfo` value in `container` property.

All `camelCase` properties have been renamed to `underscore_case`.

-   `releaseGroup` is now `release_group`
-   `episodeCount` is now `episode_count`
-   `episodeDetails` is now `episode_details`
-   `episodeFormat` is now `episode_format`
-   `screenSize` is now `screen_size`
-   `videoCodec` is now `video_codec`
-   `videoProfile` is now `video_profile`
-   `videoApi` is now `video_api`
-   `audioChannels` is now `audio_channels`
-   `audioCodec` is now `audio_codec`
-   `audioProfile` is now `audio_profile`
-   `subtitleLanguage` is now `subtitle_language`
-   `bonusTitle` is now `bonus_title`
-   `properCount` is now `proper_count`

Options
-------

Some options have been removed.

-   `-X DISABLED_TRANSFORMERS`, `-s, --transformers`

    There's no transformer anymore.

-   `-S EXPECTED_SERIES`

    As `series` was renamed to `title`, use `-T EXPECTED_TITLE` instead.

-   `-G EXPECTED_GROUP`

    GuessIt is now better to guess release group, so this option has been removed.

-   `-d, --demo`

    Probably not that useful.

-   `-i INFO, --info INFO`

    Features related to this option have been removed.

-   `-c, --split-camel`, `-u, --unidentified`, `-b, --bug`

    Will be back soon... (work in progress)

Other GuessIt `1.x` options have been kept.

Output
------

Output produced by `guessit` api function is now an instance of [OrderedDict](https://docs.python.org/2/library/collections.html#collections.OrderedDict). Property values are automatically ordered based on filename, and you can still use this output as a default python `dict`.

If multiple values are available for a property, value in the dict will be a `list` instance.

`country` 2-letter code is not added to the title anymore. As `country` is added to the returned guess dict, it's up to the user to edit the guessed title.

Advanced display option (`-a, --advanced`) output is also changed. It now list `Match` objects from [Rebulk](https://github.com/Toilal/rebulk), and may display duplicates that would have been merged in standard output.:

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
        "episode": {
            "value": 3,
            "raw": "03",
            "start": 8,
            "end": 10
        },
        "episode_title": {
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
        "video_codec": {
            "value": "XviD",
            "raw": "XviD",
            "start": 40,
            "end": 44
        },
        "release_group": {
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
