GuessIt
=======

Release v\ |version| (:ref:`Installation <install>`)

.. include:: presentation.rst


User Guide
----------

This part of the documentation, which is mostly prose, shows how to use
Guessit both from the command-line and as a python module which you can
use in your own projects.

.. toctree::
   :maxdepth: 2

   user/install
   user/commandline
   user/python


Web Service API
---------------

The guessit.io server also provides a free webservice that allows you to perform
filename detection, even you don't have python installed (eg: you need to use it
from an Android app, or NodeJS, etc.).

You can look at the documentation for the web API here: `<http://api.guessit.io>`_


Developer Guide
---------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 2

   dev/internals

You may also want to familiarize yourself with the following classes:

.. toctree::
   :maxdepth: 2

   api/guess
   api/matchtree
   api/matcher


.. include:: projectinfo.rst
