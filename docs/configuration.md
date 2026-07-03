# Configuration files

Guessit supports configuration through configuration files.

Default configuration file is bundled inside guessit package from
[config/options.json][] file.

It is possible to disable the default configuration with
`--no-default-config` option, but you have then to provide a full
configuration file based on the default one.

Configuration files are loaded from the following paths:

> -   `~/.guessit/options.(json|yml|yaml)`
> -   `~/.config/guessit/options.(json|yml|yaml)`

It is also possible to disable those user configuration files with
`no-user-config` option.

Additional configuration files can be included using the `-c`/`--config`
option.

As many configuration files can be involved, they are deeply merged to
keep all values inside the effective configuration. The options passed
programmatically to `guessit()` are merged last, on top of the files.

# Merging and overriding values

Merging keeps values from every source rather than replacing them:

> -   scalar values (string, number, boolean) are replaced by the later source;
> -   list values are concatenated (the later values are appended to the
>     existing ones, skipping duplicates);
> -   dict values are deeply merged, key by key.

Because lists are concatenated, you cannot override a list option (such as
`allowed_countries` or `allowed_languages`) simply by providing a new list:
your values are added to the defaults instead of replacing them.

```python
>>> from guessit import guessit
>>> guessit('SS-GB.S01E01.1080p.x265-MeGusta.mkv', {'allowed_countries': []})['country']
<Country [GB]>
```

To drop the inherited value before merging, use the `pristine` option. Set it
to `True` to reset the whole configuration, or to a list of option names to
reset only those:

```python
>>> guessit('SS-GB.S01E01.1080p.x265-MeGusta.mkv',
...         {'pristine': ['allowed_countries'], 'allowed_countries': []})['title']
'SS-GB'
```

`pristine` is applied per source, resetting the matching options accumulated
from the previous sources before the current one is merged in. It is available
in configuration files and in the programmatic options, but not as a
command-line flag.

# Advanced configuration

Configuration files contains all options available through the command
line, but also an additional one named `advanced_config`.

This advanced configuration contains all internal parameters and they
are exposed to help you tweaking guessit to better fit your needs.

If no `advanced_config` is declared through all effective configuration
files, the default one will be used even when `--no-default-config` is
used.

We're willing to keep it backwards compatible, but in order to enhance
Guessit, these parameters might change without prior notice.

  [config/options.json]: https://github.com/guessit-io/guessit/blob/main/guessit/config/options.json/