.. _install:

Installation
============

This part of the documentation covers the installation of GuessIt.
The first step to using any software package is getting it properly installed.


Installing with Pip
-------------------

Installing GuessIt is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install guessit


Getting the source code
-----------------------

GuessIt is actively developed on GitHub, where the code is
`always available <https://github.com/wackou/guessit>`_.

You can either clone the public repository::

    $ git clone git://github.com/wackou/guessit.git

Download the `tarball <https://github.com/wackou/guessit/tarball/master>`_::

    $ curl -L https://github.com/wackou/guessit/tarball/master -o guessit.tar.gz

Or download the `zipball <https://github.com/wackou/guessit/zipball/master>`_::

    $ curl -L https://github.com/wackou/guessit/zipball/master -o guessit.zip


Once you have a copy of the source, you can embed it in your Python package,
install it into your site-packages folder like that::

    $ python setup.py install

or use it directly from the source folder for development::

    $ python setup.py develop
