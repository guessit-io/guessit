Migration
=========
For version 2, has been rewritten from scratch. You can find in this file all information required to perform a
migration from previous version.

API
---
*Work in progress ...*

Options
-------
*Work in progress ...*

Properties
----------
For episode type, some properties have been renamed

- ``series`` is now ``title``.
- ``title`` is now ``episodeTitle``.

For movie type, some properties have been renamed

- ``filmtitle`` is now ``filmSeries``

All info type (``seriesinfo``, ``movieinfo``) have been removed in favor of checking the ``extension`` property for
``nfo`` value.

All other properties have been ported with the same name (*Work in progress ...*)