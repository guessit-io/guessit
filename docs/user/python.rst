.. _python:


Python module usage
===================

The main entry points to the python module are the ``guess_video_info``,
``guess_movie_info`` and ``guess_episode_info``.

The ``guess_video_info`` function will try to autodetect the type of the
file, either movie, moviesubtitle, episode or episodesubtitle.

Pass them the filename and the desired information type:

    >>> import guessit
    >>> path = 'Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv'
    >>> guess = guessit.guess_movie_info(path, info = ['filename'])

    >>> print type(guess)
    <class 'guessit.guess.Guess'>

    >>> print guess
    {'videoCodec': 'h264', 'container': 'mkv', 'format': 'BluRay',
    'title': 'Dark City', 'releaseGroup': 'CHD', 'screenSize': '720p',
    'year': 1998, 'type': 'movie', 'audioCodec': 'DTS'}

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

A ``Guess`` instance is a dictionary which has an associated confidence
for each of the properties it has.

A ``Guess`` instance is also a python dict instance, so you can use it
wherever you would use a normal python dict.


