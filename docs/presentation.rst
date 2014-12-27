
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

The filename matcher is based on regular expressions and tree splitting to guess values from input filename.

It is able to find many properties, like ``title``, ``year``, ``series``, ``episodeNumber``, ``seasonNumber``,
``videoCodec``, ``screenSize``, ``language``. Guessed values are cleaned up and given in a readable format
which may not match the raw filename.

``DVDSCR`` will be guessed as ``format`` = ``DVD`` + ``other`` = ``Screener``.

``1920x1080`` will be guessed as ``screenSize`` = ``1080p``.

``DD5.1`` will be guessed as ``audioCodec`` = ``DolbyDigital`` + ``audioChannel`` = ``5.1``.

Here's the exhaustive list of properties that guessit can find:


Main properties
~~~~~~~~~~~~~~~~~

- **type**

  Type of the file.

  - ``unknown``, ``movie``, ``episode``, ``moviesubtitle``, ``episodesubtitle``


- **title**

  Title of movie or episode.

- **container**

  Container of the file.

  - ``3g2``, ``wmv``, ``webm``, ``mp4``, ``avi``, ``mp4a``, ``mpeg``, ``sub``, ``mka``, ``m4v``, ``ts``, ``mkv``, ``ra``, ``rm``, ``wma``, ``ass``, ``mpg``, ``ram``, ``3gp``, ``ogv``, ``mov``, ``ogm``, ``asf``, ``divx``, ``ogg``, ``ssa``, ``qt``, ``idx``, ``nfo``, ``wav``, ``flv``, ``3gp2``, ``iso``, ``mk2``, ``srt``


- **date**

  Date found in filename.


- **year**

  Year of movie (or episode).


- **releaseGroup**

  Name of (non)scene group that released the file.


- **website**

  Name of website contained in the filename.


Episode properties
~~~~~~~~~~~~~~~~~~

- **series**

  Name of series.


- **season**

  Season number.


- **episodeNumber**

  Episode number.


- **episodeList**

  List of episode numbers if several were found.

  - note: If several are found, ``episodeNumber`` is the first item of this list.


- **seasonList**

  List of season numbers if several were found.

  - note: If several are found, ``seasonNumber`` is the first item of this list.


- **episodeCount**

  Total number of episodes.


- **seasonCount**

  Total number of seasons.


- **episodeDetails**

  Some details about the episode.

  - ``Bonus`` ``Oav`` ``Ova`` ``Omake`` ``Extras`` ``Unaired`` ``Special`` ``Pilot``


- **episodeFormat**

  Episode format of the series.

  - ``Minisode``

- **part**

  Part number of the episode.


- **version**

  Version of the episode.

  - In anime fansub scene, new versions are released with tag ``<episode>v[0-9]``.


Video properties
~~~~~~~~~~~~~~~~

- **format**

  Format of the initial source

  - ``HDTV`` ``WEB-DL`` ``TV`` ``VOD`` ``BluRay`` ``DVD`` ``WEBRip`` ``Workprint`` ``Telecine`` ``VHS`` ``DVB`` ``Telesync``  ``HD-DVD`` ``PPV`` ``Cam``


- **screenSize**

  Resolution of video.
  - ``720p`` ``1080p`` ``1080i`` ``<width>x<height>`` ``4K`` ``360p`` ``368p`` ``480p`` ``576p`` ``900p``


- **videoCodec**
  Codec used for video.

  - ``h264`` ``h265`` ``DivX`` ``XviD`` ``Real`` ``Mpeg2``


- **videoProfile**
  Codec profile used for video.

  - ``8bit`` ``10bit`` ``HP`` ``BP`` ``MP`` ``XP`` ``Hi422P`` ``Hi444PP``


- **videoApi**
  API used for the video.

  - ``DXVA``


Audio properties
~~~~~~~~~~~~~~~~

- **audioChannels**

  Number of channels for audio.

  - ``1.0`` ``2.0`` ``5.1`` ``7.1``


- **audioCodec**
  Codec used for audio.

  - ``DTS`` ``TrueHD`` ``DolbyDigital``  ``AAC`` ``AC3`` ``MP3`` ``Flac``


- **audioProfile**
  The codec profile used for audio.

  - ``LC`` ``HQ`` ``HD`` ``HE`` ``HDMA``


Localization properties
~~~~~~~~~~~~~~~~~~~~~~~

- **Country**

  Country(ies) of content. Often found in series, ``Shameless (US)`` for instance.

  - ``[<babelfish.Country>]`` (This class equals name and iso code)


- **Language**

  Language(s) of the audio soundtrack.

  - ``[<babelfish.Language>]`` (This class equals name and iso code)


- **subtitleLanguage**

  Language(s) of the subtitles.

  - ``[<babelfish.Language>]`` (This class equals name and iso code)


Other properties
~~~~~~~~~~~~~~~~

- **bonusNumber**

  Bonus number.


- **bonusTitle**

  Bonus title.


- **cdNumber**

  CD number.


- **cdNumberTotal**

  Total number of CD.


- **crc32**

  CRC32 of the file.


- **idNumber**

  Volume identifier (UUID).


- **edition**

  Edition of the movie.

  - ``Special Edition``, ``Collector Edition``, ``Director's cut``, ``Criterion Edition``, ``Deluxe Edition``


- **filmNumber**

  Film number of this movie.


- **filmSeries**

  Film series of this movie.

- **other**

  Other property will appear under this property.

  - ``Fansub``, ``HR``, ``HQ``, ``Netflix``, ``Screener``, ``Unrated``, ``HD``, ``3D``, ``SyncFix``, ``Bonus``, ``WideScreen``, ``Fastsub``, ``R5``, ``AudioFix``, ``DDC``, ``Trailer``, ``Complete``, ``Limited``, ``Classic``, ``Proper``, ``DualAudio``, ``LiNE``


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

guessit can be used from command line::

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


