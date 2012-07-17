.. _commandline:

Command-line usage
==================

To have GuessIt try to guess some information from a filename, just run it as a command::

    $ python guessit.py "Movies/Dark City (1998)/Dark.City.(1998).DC.BDRip.720p.DTS.X264-CHD.mkv"
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

You can also run a ``--demo`` mode which will run a few tests and
display the results.

By default, GuessIt will try to autodetect the type of file you are asking it to
guess, movie or episode. If you want to force one of those, use the ``-t movie`` or
``-t episode`` flags.

Guessit also allows you to specify the type of information you want
using the ``-i`` or ``--info`` flag::

    $ python guessit.py -i hash_md5,hash_sha1,hash_ed2k tests/dummy.srt
    For: tests/dummy.srt
    GuessIt found: {
        [1.00] "hash_ed2k": "ed2k://|file|dummy.srt|44|1CA0B9DED3473B926AA93A0A546138BB|/",
        [1.00] "hash_md5": "e781de9b94ba2753a8e2945b2c0a123d",
        [1.00] "hash_sha1": "bfd18e2f4e5d59775c2bc14d80f56971891ed620"
    }


You can see the list of options that guessit.py accepts like that::

    $ python guessit.py -h
    Usage: guessit.py [options] file1 [file2...]

    Options:
      -h, --help            show this help message and exit
      -v, --verbose         display debug output
      -i INFO, --info=INFO  the desired information type: filename, hash_mpc or a
                            hash from python's hashlib module, such as hash_md5,
                            hash_sha1, ...; or a list of any of them, comma-
                            separated
      -t FILETYPE, --type=FILETYPE
                            the suggested file type: movie, episode or autodetect
      -d, --demo            run a few builtin tests instead of analyzing a file
