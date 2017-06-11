.. _migration2to3:

Migration
=========
Guessit 3 has introduced breaking changes from previous versions. You can find in this file all information required to
perform a migration from previous version ``2.x``.

API
---
No changes.

Properties
----------
Some properties have been renamed.

- ``format`` is now ``source``.


Values
------
The major changes in GuessIt 3 are around the values. Values were renamed in order to keep consistency and to be more
intuitive. Acronyms are uppercase (e.g.: ``HDTV``). Names follow the official name (e.g.: ``Blu-ray``). Words have only
the first letter capitalized (e.g.: ``Camera``) except prepositions (e.g.: ``on``) which are all lowercase.

The following values were changed:

``source`` (former ``format`` property)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- ``Cam`` is now ``Camera`` or ``HD Camera``
- ``Telesync`` is now ``Telesync`` or ``HD Telesync``
- ``PPV`` is now ``Pay-per-view``
- ``DVB`` is now ``Digital TV``
- ``VOD`` is now ``Video on Demand``
- ``WEBRip`` is now ``Web`` with additional property ``other: Rip``
- ``WEB-DL`` is now ``Web``
- ``AHDTV`` is now ``Analogue HDTV``
- ``UHDTV`` is now ``Ultra HDTV``
- ``HDTC`` is now ``HD Telecine``

``edition``
^^^^^^^^^^^
- ``Collector Edition`` is now ``Collector``
- ``Special Edition`` is now ``Special``
- ``Criterion Edition`` is now ``Criterion``
- ``Deluxe Edition`` is now ``Deluxe``
- ``Limited Edition`` is now ``Limited``
- ``Theatrical Edition`` is now ``Theatrical``
- ``Director's Definitive Cut`` was added.

``other``
^^^^^^^^^
- ``Rip`` was added. E.g.: ``DVDRip`` will output ``other: Rip``
- ``DDC`` was removed. ``DDC`` is now ``edition: Director's Definitive Cut``
- ``CC`` was removed. ``CC`` is now ``edition: Criterion``
