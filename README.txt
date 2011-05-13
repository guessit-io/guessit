GuessIt
=======

GuessIt is a python library that tries to extract as much information as
possible from a filename.

GuessIt works with video files, both movies and tv shows episodes.

Currently, GuessIt only extract information from the filename, but it could very
well be in the future that it uses some other libraries to extract information
from the video metadata itself (ie: codec, bitrate, etc...)

Command-line usage
==================

To have GuessIt try to guess some information from a filename, just run it as a command:

user@home:~$ /home/download/tmp/testsmewt_bugs/series/Ren\ and\ Stimpy\ -\ Black_hole_\[DivX\].avi

For: /home/download/tmp/testsmewt_bugs/series/Ren and Stimpy - Black_hole_[DivX].avi
Found: {
    [0.10] "series": "Ren and Stimpy",
    [1.00] "videoCodec": "DivX",
    [1.00] "container": "avi",
    [0.80] "type": "episode"
}

user@home:~$

You can use the '-v' or '--verbose' flag to have it display debug information.

You can also run a '--demo' mode which will run a few tests and display the results


Python module usage
===================

TODO
