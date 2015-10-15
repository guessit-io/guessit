GuessIt
=======

.. image:: http://img.shields.io/pypi/v/guessit.svg
    :target: https://pypi.python.org/pypi/guessit
    :alt: Latest Version

.. image:: http://img.shields.io/badge/license-LGPLv3-blue.svg
    :target: https://pypi.python.org/pypi/guessit
    :alt: LGPLv3 License

.. image:: http://img.shields.io/travis/wackou/guessit/2.x.svg
    :target: https://travis-ci.org/wackou/guessit
    :alt: Build Status

.. image:: http://img.shields.io/coveralls/wackou/guessit/2.x.svg
    :target: https://coveralls.io/github/wackou/guessit?branch=2.x
    :alt: Coveralls

`HuBoard <https://huboard.com/wackou/guessit>`_


GuessIt is a python library that extracts as much information as possible from a video file.

It has a very powerful filename matcher that allows to guess a lot of metadata from a video using its filename only.
This matcher works with both movies and tv shows episodes.

Important note
==============
GuessIt 2.x is a rewrite from scratch and is currently in Alpha. Support for additional features like hashes
computations has been dropped. GuessIt is now a release name parser only.

Previous stable version of GuessIt is still available in ``1.x`` branch and using `pip install guessit<2`.

Install
-------

Installing GuessIt is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install guessit

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install guessit

But, you really `shouldn't do that <http://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install>`_.

Filename matcher
----------------

The filename matcher is based on `Rebulk <https://www.github.com/Toilal/rebulk>`_ and is able to recognize many
properties from the filename. Guessed values are cleaned up and given in a readable format which may not match
exactly the raw filename.

Usage
-----
Work in progress ...

Support
-------

The project website for GuessIt is hosted at `ReadTheDocs <http://guessit.readthedocs.org/>`_.
There you will also find the User guide and Developer documentation.

This project is hosted on GitHub: `<https://github.com/wackou/guessit>`_

Contribute
----------

GuessIt is under active development, and contributions are more than welcome!

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
   There is a Contributor Friendly tag for issues that should be ideal for people who are not very
   familiar with the codebase yet.
#. Fork `the repository`_ on Github to start making your changes to the **2.x**
   branch (or branch off of it).
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :)

.. _the repository: https://github.com/wackou/guessit/tree/2.x

License
-------

GuessIt is licensed under the `LGPLv3 license <http://www.gnu.org/licenses/lgpl.html>`_.
