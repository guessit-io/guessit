
GuessIt is a python library that tries to extract as much information as
possible from a video file.

It has a very powerful filename matcher that allows to guess a lot of
metadata from a video using only its filename. This matcher works with
both movies and tv shows episodes.

For example, GuessIt can do the following::

    $ python guessit.py "Treme.1x03.Right.Place,.Wrong.Time.HDTV.XviD-NoTV.avi"
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
      series, season, episodeNumber,     # for episodes only
      date, year,                        # 'date' instance of datetime.date
      language, subtitleLanguage,        # instances of guessit.Language
      country,                           # instances of guessit.Country
      container, format,
      videoCodec, audioCodec,
      audioChannels, screenSize,
      releaseGroup, website,
      cdNumber, cdNumberTotal,
      filmNumber, filmSeries,
      bonusNumber, edition,
      idNumber,                          # tries to identify a hash or a serial number
      other
      ]


Guessit also allows you to compute a whole lof of hashes from a file,
namely all the ones you can find in the hashlib python module (md5,
sha1, ...), but also the Media Player Classic hash that is used (amongst
others) by OpenSubtitles and SMPlayer, as well as the ed2k hash.
