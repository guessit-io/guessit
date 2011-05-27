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

By default, GuessIt will try to autodetect the type of file you are asking it to
guess, movie or episode. If you want to force one of those, use the '-t movie' or
'-t episode' flags.

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
    >>> filename = 'Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv'
    >>> guess = guessit.guess_movie_info(filename, info = ['filename'])

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

A Guess instance is a dictionary which has an associated confidence
for each of the properties it has.

A Guess instance is also a python dict instance, so you can use it
wherever you would use a normal python dict




How does the filename matcher work?
===================================

This is a very succinct description of how the matcher works, but will give
you the main ideas.

The main process is a 2-step one:
 - we first try to detect known patterns inside the filename, and mark
   them as recognized
 - we then look at the remaining blocks in the filename (those that
   have not been recognized) and try to assign them whichever meaning
   they likely have.

All the parts that have been identified are in fact leaves of a
3-level deep tree, which is called the MatchTree.

As all this might sound a bit abstract, let's look at an example more
in details:

For: Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv

We get the following MatchTree::

    0000000 1111111111111111 2222222222222222222222222222222222222222222 333
    0000000 0000000000111111 0000000000111111222222222222222222222222222 000
    0000000 0000000000011112 0000000000011112000011111233334555677778999 000
    'Movies/Dark City (____)/__________(____).DC._____.____.___.____-___.___
                       yyyy  tttttttttt yyyy     fffff ssss aaa vvvv rrr ccc
    'Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv

The first 3 lines represent the indices of the groups in the match tree, the
4th line contains the remaining groups that have not been identified, the 5th
shows the semantic meaning of the groups, and the 6th is just the original
filename to be able to see what happened.

What happened during the matching is the following:

 - first, we split the filename into its path components, ie: all the parent
   directories and the extension. This gives us 4 groups (labelled 0 to 3)
   which are indicated on the 1st line.
 - then we split each of those by looking as what is called "explicit groups",
   and which correspond to parts which are delimited by parentheses, square
   brackets, etc... Their indices are indicated on the 2nd line
 - then, inside each of these explicit groups we look for known patterns, which
   in this case gives us the year (1998), the format (BDRip), the screen
   size (720p), the video codec (x264) and the release group (CHD).
 - we then split each explicit group using those find patterns, and assign a
   final group index to each of those found and remaining. These are indicated
   on the 3rd line.

Once the known pattern are found, we can now try to estimate the remaining patterns
using some positional rules. In this case:

 - the first remaining (ie: unidentified) group of the last path group (ie: the
   file basename) is likely to be the movie title, in this case 'Dark City'.

And here is how we get the match tree!

Once the match tree is fully parsed, the only task remaining is to get all the
groups and decide on a value for each guessed property, for instance if there
were conflicts in the detected values. In our example, 'year' appears twice, but
as it has the same value, it will be merged into a single 'year' property with a
confidence that represents the combined confidence of both guesses.