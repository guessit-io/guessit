.. _commandline:

Command-line usage
==================

To have GuessIt try to guess some information from a filename, just run it as a command::

    $ guessit "Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv"
    For: Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv
    GuessIt found: {
        [1.00] "videoCodec": "h264",
        [1.00] "container": "mkv",
        [1.00] "format": "BluRay",
        [0.60] "title": "Dark City",
        [1.00] "releaseGroup": "CHD",
        [1.00] "screenSize": "720p",
        [1.00] "year": 1998,
        [1.00] "type": "movie",
        [1.00] "audioCodec": "DTS"
    }

The numbers between square brackets indicate the confidence in the
value, so for instance in the previous example, GuessIt is sure that
the videoCodec is h264, but only 60% confident that the title is
'Dark City'.


You can use the ``-v`` or ``--verbose`` flag to have it display debug information.

You can use the ``-p`` or ``-V`` flags to display the properties names or the
multiple values they can take.

You can also run a ``--demo`` mode which will run a few tests and
display the results.

By default, GuessIt will try to autodetect the type of file you are asking it to
guess, movie or episode. If you want to force one of those, use the ``-t movie`` or
``-t episode`` flags.

If input file is remote file or a release name with no folder and extension,
you should use the ``-n`` or ``--name-only`` flag. It will disable folder and extension
parsing, and any concrete file related analysis.

Guessit also allows you to specify the type of information you want
using the ``-i`` or ``--info`` flag::

    $ guessit -i hash_md5,hash_sha1,hash_ed2k tests/dummy.srt
    For: tests/dummy.srt
    GuessIt found: {
        [1.00] "hash_ed2k": "ed2k://|file|dummy.srt|44|1CA0B9DED3473B926AA93A0A546138BB|/",
        [1.00] "hash_md5": "e781de9b94ba2753a8e2945b2c0a123d",
        [1.00] "hash_sha1": "bfd18e2f4e5d59775c2bc14d80f56971891ed620"
    }


You can see the list of options that guessit.py accepts like that::

    $ guessit --help
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

