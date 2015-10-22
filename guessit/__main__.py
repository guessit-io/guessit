#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Entry point module
"""
# pragma: no cover
from __future__ import print_function
from collections import OrderedDict
from rebulk.match import Match

import six

import os
import logging

from guessit.__version__ import __version__

from guessit.options import argument_parser
from guessit.api import guessit

import json


class GuessitEncoder(json.JSONEncoder):
    """
    JSON Encoder for guessit response
    """
    def default(self, o):  # pylint:disable=method-hidden
        if isinstance(o, Match):
            ret = OrderedDict()
            ret['value'] = o.value
            ret['raw'] = o.raw
            ret['start'] = o.start
            ret['end'] = o.end
            return ret
        else:
            return str(o)


def guess_filename(filename, options):
    """
    Guess a single filename using given options
    """
    if not options.yaml and not options.json and not options.show_property:
        print('For:', filename)

    guess = guessit(filename, vars(options))

    if options.show_property:
        print(guess.get(options.show_property, ''))
        return

    if options.json:
        print(json.dumps(guess, cls=GuessitEncoder, ensure_ascii=False))
    elif options.yaml:
        import yaml
        ystr = yaml.safe_dump({filename: dict(guess)}, default_flow_style=False, allow_unicode=True)
        i = 0
        for yline in ystr.splitlines():
            if i == 0:
                print("? " + yline[:-1])
            elif i == 1:
                print(":" + yline[1:])
            else:
                print(yline)
            i += 1
    else:
        print('GuessIt found:', json.dumps(guess, cls=GuessitEncoder, indent=4, ensure_ascii=False))


def main(args=None):  # pylint:disable=too-many-branches
    """
    Main function for entry point
    """
    if six.PY2:  # pragma: no cover
        import codecs
        import locale
        import sys

        # see http://bugs.python.org/issue2128
        if os.name == 'nt':
            for i, j in enumerate(sys.argv):
                sys.argv[i] = j.decode(locale.getpreferredencoding())

        # see https://github.com/wackou/guessit/issues/43
        # and http://stackoverflow.com/questions/4545661/unicodedecodeerror-when-redirecting-to-file
        # Wrap sys.stdout into a StreamWriter to allow writing unicode.
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

    if args is None:  # pragma: no cover
        options = argument_parser.parse_args()
    else:
        options = argument_parser.parse_args(args)
    if options.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    help_required = True
    if options.properties or options.values:
        #display_properties(options)
        # TODO: Add display of available properties
        help_required = False

    if options.version:
        print('+-------------------------------------------------------+')
        print('+                   GuessIt ' + __version__ + (28-len(__version__)) * ' ' + '+')
        print('+-------------------------------------------------------+')
        print('|      Please report any bug or feature request at      |')
        print('|       https://github.com/wackou/guessit/issues.       |')
        print('+-------------------------------------------------------+')
        help_required = False

    if options.yaml:
        try:
            import yaml, babelfish
            def default_representer(dumper, data):
                """Default representer"""
                return dumper.represent_str(str(data))
            yaml.SafeDumper.add_representer(babelfish.Language, default_representer)
            yaml.SafeDumper.add_representer(babelfish.Country, default_representer)
        except ImportError:  # pragma: no cover
            options.yaml = False
            print('PyYAML not found. Using default output.')

    filenames = []
    if options.filename:
        filenames.extend(options.filename)
    if options.input_file:
        input_file = open(options.input_file, 'r')
        try:
            filenames.extend([line.strip() for line in input_file.readlines()])
        finally:
            input_file.close()

    filenames = list(filter(lambda f: f, filenames))

    if filenames:
        for filename in filenames:
            help_required = False
            guess_filename(filename, options)

    if help_required:  # pragma: no cover
        argument_parser.print_help()

if __name__ == '__main__':  # pragma: no cover
    main()
