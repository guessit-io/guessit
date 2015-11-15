History
=======

2.0b3 (2015-11-15)
------------------

- Add support for ``part`` with no space before number.
- Avoid ``uuid`` and ``crc32`` collision with ``season``/``episode`` properties.
- Add better space support for ``season``/``episode`` properties.
- Ensure ``date`` property is found when conflicting with ``season``/``episode`` properties.
- Fix ``IndexError`` when input has a closing group character with no opening one before.
- Add ``--type`` option.
- Add rebulk implicit option support.

2.0b2 (2015-11-14)
------------------

- Add python 2.6 support.


2.0b1 (2015-11-11)
------------------

- Enhance title guessing.
- Upgrade rebulk to ``0.6.1``.
- Rename ``properCount`` to ``proper_count``
- Avoid crash when using ``-p``/``-V`` option with ``--yaml`` and ``yaml`` module is not available.

2.0a4 (2015-11-09)
------------------

- Add ``-p``/``-V`` options to display properties and values that can be guessed.


2.0a3 (2015-11-08)
------------------

- Allow rebulk customization in API module.

2.0a2 (2015-11-07)
------------------

- Raise TypeError instead of AssertionError when non text is given to guessit API.
- Fix packaging issues with previous release blocking installation.

2.0a1 (2015-11-07)
------------------

- Rewrite from scratch using `Rebulk <https://www.github.com/Toilal/rebulk>`_
- Read `MIGRATION.rst <https://github.com/wackou/guessit/blob/2.x/MIGRATION.rst>`_ for migration guidelines.
