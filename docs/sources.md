Getting the source code
=======================

GuessIt is actively developed on [GitHub](https://github.com/guessit-io/guessit).

You can either clone the public repository:

    $ git clone https://github.com/guessit-io/guessit.git

Download the [tarball](https://github.com/guessit-io/guessit/tarball/main):

    $ curl -L https://github.com/guessit-io/guessit/tarball/main -o guessit.tar.gz

Or download the [zipball](https://github.com/guessit-io/guessit/zipball/main):

    $ curl -L https://github.com/guessit-io/guessit/zipball/main -o guessit.zip

Once you have a copy of the source, you can install it into your site-packages folder like that:

    $ uv pip install .

or set up a development environment (creates a virtualenv and installs the dev/test dependencies) like that:

    $ uv sync
