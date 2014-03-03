.. This is your project NEWS file which will contain the release notes.
.. Example: http://www.python.org/download/releases/2.6/NEWS.txt
.. The content of this file, along with README.rst, will appear in your
.. project's PyPI page.

History
=======



0.7.1 (2014-03-03)
------------------

* New property "special": values can be trailer, pilot, unaired
* New options for the guessit cmdline util: ``-y``, ``--yaml`` outputs the
  result in yaml format and ``-n``, ``--name-only`` analyzes the input as simple
  text (instead of filename)
* Added properties formatters and validators
* Removed support for python 3.2
* A healthy amount of code cleanup/refactoring and fixes :)


0.7 (2014-01-29)
----------------

* New plugin API that allows to register custom patterns / transformers
* Uses Babelfish for language and country detection
* Added Quality API to rate file quality from guessed property values
* Better and more accurate overall detection
* Added roman and word numeral detection
* Added 'videoProfile' and 'audioProfile' property
* Moved boolean properties to 'other' property value ('is3D' became 'other' = '3D')
* Added more possible values for various properties.
* Added command line option to list available properties and values
* Fixes for Python3 support


0.6.2 (2013-11-08)
------------------

* Added support for nfo files
* GuessIt can now output advanced information as json ('-a' on the command line)
* Better language detection
* Added new property: 'is3D'


0.6.1 (2013-09-18)
------------------

* New property "idNumber" that tries to identify a hash value or a
  serial number
* The usual bugfixes


0.6 (2013-07-16)
----------------

* Better packaging: unittests and doc included in source tarball
* Fixes everywhere: unicode, release group detection, language detection, ...
* A few speed optimizations


0.5.4 (2013-02-11)
------------------

* guessit can be installed as a system wide script (thanks @dplarson)
* Enhanced logging facilities
* Fixes for episode number and country detection


0.5.3 (2012-11-01)
------------------

* GuessIt can now optionally act as a wrapper around the 'guess-language' python
  module, and thus provide detection of the natural language in which a body of
  text is written

* Lots of fixes everywhere, mostly for properties and release group detection


0.5.2 (2012-10-02)
------------------

* Much improved auto-detection of filetype
* Fixed some issues with the detection of release groups


0.5.1 (2012-09-23)
------------------

* now detects 'country' property; also detect 'year' property for series
* more patterns and bugfixes


0.5 (2012-07-29)
----------------

* Python3 compatibility
* the usual assortment of bugfixes


0.4.2 (2012-05-19)
------------------

* added Language.tmdb language code property for TheMovieDB
* added ability to recognize list of episodes
* bugfixes for Language.__nonzero__ and episode regexps


0.4.1 (2012-05-12)
------------------

* bugfixes for unicode, paths on Windows, autodetection, and language issues


0.4 (2012-04-28)
----------------

* much improved language detection, now also detect language variants
* supports more video filetypes (thanks to Rob McMullen)


0.3.1 (2012-03-15)
------------------

* fixed package installation from PyPI
* better imports for the transformations (thanks Diaoul!)
* some small language fixes

0.3 (2012-03-12)
----------------

* fix to recognize 1080p format (thanks to Jonathan Lauwers)

0.3b2 (2012-03-02)
------------------

* fixed the package installation

0.3b1 (2012-03-01)
------------------

* refactored quite a bit, code is much cleaner now
* fixed quite a few tests
* re-vamped the documentation, wrote some more

0.2 (2011-05-27)
----------------

* new parser/matcher completely replaced the old one
* quite a few more unittests and fixes


0.2b1 (2011-05-20)
------------------

* brand new parser/matcher that is much more flexible and powerful
* lots of cleaning and a bunch of unittests


0.1 (2011-05-10)
----------------

* fixed a few minor issues & heuristics


0.1b2 (2011-03-12)
------------------

* Added PyPI trove classifiers
* fixed version number in setup.py


0.1b1 (2011-03-12)
------------------

* first pre-release version; imported from Smewt with a few enhancements already
  in there.
