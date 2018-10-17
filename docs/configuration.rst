.. _configuration:

Configuration files
===================
Guessit supports configuration through configuration file.

This can be done using the ``-c``/``--config`` option, or by creating files at the following locations.

Default configuration file is bundled inside guessit package from `config/options.json <https://github.com/guessit-io/guessit/blob/develop/guessit/config/options.json/>`_ file.

It is possible to disable the default configuration with ``--no-default-config`` option, but you have then to provide a
full configuration file based on the default one.

Configuration files are also loaded from the following paths:

  * ``~/.guessit/options.(json|yml|yaml)``
  * ``~/.config/guessit/options.(json|yml|yaml)``

It is also possible to disable those user configuration files with ``no-user-config`` option.

As many configuration files can be involved, they are deeply merged to keep all values inside the effective
configuration.

Advanced configuration
======================
Configuration files contains all options available through the command line, but also an additional one named
``advanced_configuration``.

This advanced configuration contains all internal parameters and they are exposed to help you tweaking guessit to
better fit your needs.

If no ``advanced_configuration`` is declared through all effective configuration files, the default one will be used
even when ``--no-default-config`` is used.

We're willing to keep it backwards compatible, but in order to enhance Guessit, these parameters might change without
prior notice.
