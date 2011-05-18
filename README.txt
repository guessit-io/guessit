GuessIt
=======

GuessIt is a python library that tries to extract as much information as
possible from a file.

It has a very powerful filename matcher that allows to guess a lot of
metadata from a video using only its filename. This matcher works with
both movies and tv shows episodes.

Guessit also allows you to compute a whole lof of hashes from a file,
namely all the ones you can find in the hashlib python module (md5,
sha1, ...), but also the Media Player Classic hash that is used (amongst
others) by OpenSubtitles and SMPlayer, as well as the ed2k hash.


Properties recognized by the filename matcher
---------------------------------------------

At the moment, the filename matcher is able to recognize the following
property types::

    [ title,                             # for movies and episodes
      series, season, episodeNumber,     # for episodes only
      date, year,                        # 'date' instance of datetime.date
      language, subtitleLanguage,        # instances of guessit.Language
      container, format,
      videoCodec, audioCodec,
      audioChannels, screenSize,
      releaseGroup, website,
      cdNumber, cdNumberTotal,
      edition, other
      ]


Command-line usage
==================

To have GuessIt try to guess some information from a filename, just run it as a command::

    user@home:~$ python guessit.py "Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv"
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
the videoCodec is h264, but only 60% confident that the title is 'Dark
City'.


You can use the '-v' or '--verbose' flag to have it display debug information.

You can also run a '--demo' mode which will run a few tests and
display the results.

Guessit also allows you to specify the type of information you want
using the -i or --info flag::

    user@home:~$  python guessit.py -i hash_md5,hash_sha1,hash_ed2k test/dummy.srt
    For: test/dummy.srt
    GuessIt found: {
        [1.00] "hash_ed2k": "ed2k://|file|dummy.srt|44|1CA0B9DED3473B926AA93A0A546138BB|/",
        [1.00] "hash_md5": "e781de9b94ba2753a8e2945b2c0a123d",
        [1.00] "hash_sha1": "bfd18e2f4e5d59775c2bc14d80f56971891ed620"
    }


Python module usage
===================

The main entry points to the python module are the guess_video_info,
guess_movie_info and guess_episode_info.

The guess_video_info function will try to autodetect the type of the
file, either movie, moviesubtitle, episode or episodesubtitle.

Pass them the filename and
the desired information type:

    >>> import guessit
    >>> guess = guessit.guess_movie_info('Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv', info = ['filename'])

    >>> print type(guess)
    <class 'guessit.guess.Guess'>

    >>> print guess
    {'videoCodec': 'h264', 'container': 'mkv', 'format': 'BluRay', 'title': 'Dark City', 'releaseGroup': 'CHD', 'screenSize': '720p', 'year': 1998, 'type': 'movie', 'audioCodec': 'DTS'}

    >>> print guess.nice_string()
    {
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

A Guess instance is a dictionary which has an associated confidence
for each of the properties it has.

A Guess instance is also a python dict instance, so you can use it
wherever you would use a normal python dict




How does the filename matcher work?
===================================

TODO
