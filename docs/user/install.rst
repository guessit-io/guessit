.. _install:

Installation
============

This part of the documentation covers the installation of GuessIt.
The first step to using any software package is getting it properly installed.


Distribute & Pip
----------------

Installing GuessIt is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install guessit

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install guessit

But, you really `shouldn't do that <http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install>`_.



Get the Code
------------

GuessIt is actively developed on GitHub, where the code is
`always available <https://github.com/wackou/guessit>`_.

You can either clone the public repository::

    git clone git://github.com/wackou/guessit.git

Download the `tarball <https://github.com/wackou/guessit/tarball/master>`_::

    $ curl -L https://github.com/wackou/guessit/tarball/master -o guessit.tar.gz

Or, download the `zipball <https://github.com/wackou/guessit/zipball/master>`_::

    $ curl -L https://github.com/wackou/guessit/zipball/master -o guessit.zip


Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install
