
GuessIt is a python library that extracts as much information as
possible from a video file.

It has a very powerful filename matcher that allows to guess a lot of
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



Filename matcher
----------------

The filename matcher is based on pattern matching and is able to recognize many properties from the filename,
like ``title``, ``year``, ``series``, ``episodeNumber``, ``seasonNumber``,
``videoCodec``, ``screenSize``, ``language``. Guessed values are cleaned up and given in a readable format
which may not match exactly the raw filename.

The full list of available properties can be seen here:

.. toctree::
   :maxdepth: 2

   user/properties


Other features
--------------

GuessIt also allows you to compute a whole lof of hashes from a file,
namely all the ones you can find in the hashlib python module (md5,
sha1, ...), but also the Media Player Classic hash that is used (amongst
others) by OpenSubtitles and SMPlayer, as well as the ed2k hash.

If you have the 'guess-language' python package installed, GuessIt can also
analyze a subtitle file's contents and detect which language it is written in.

If you have the 'enzyme' python package installed, GuessIt can also detect the
properties from the actual video file metadata.

Usage
-----

GuessIt can be used from the command line::

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


