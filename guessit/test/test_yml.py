#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-self-use, pointless-statement, missing-docstring, invalid-name
import pytest

import logging

import yaml
import yaml.constructor
from collections import OrderedDict
# io.open supports encoding= in python 2.7
from io import open  # pylint: disable=redefined-builtin

from .. import guessit

import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    From https://gist.github.com/enaeseth/844388
    """

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                                                    'expected a mapping node, but found %s' % node.id, node.start_mark)

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                                                        node.start_mark, 'found unacceptable key (%s)'
                                                        % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


class EntryResult(object):
    def __init__(self, string):
        if string[0] == '$':
            self.negates = True
            self.string = string[1:]
        else:
            self.negates = False
            self.string = string
        self.valid = []
        self.missing = []
        self.different = []
        self.extra = []

    @property
    def ok(self):
        if self.negates:
            return self.missing or self.different
        return not self.missing and not self.different and not self.extra

    @property
    def warning(self):
        if self.negates:
            return False
        return not self.missing and not self.different and self.extra

    @property
    def error(self):
        if self.negates:
            return not self.missing and not self.different
        return self.missing or self.different

    def __repr__(self):
        if self.ok:
            return self.string + ': OK!'
        elif self.warning:
            return '%s%s: WARNING! (valid=%i, extra=%i)' % ('$' if self.negates else '', self.string, len(self.valid))
        elif self.error:
            return '%s%s: ERROR! (valid=%i, missing=%i, different=%i, extra=%i)' % \
                   ('$' if self.negates else '', self.string, len(self.valid), len(self.missing), len(self.different),
                    len(self.extra))
        else:
            return '%s%s: UNKOWN! (valid=%i, missing=%i, different=%i, extra=%i)' % \
                   ('$' if self.negates else '', self.string, len(self.valid), len(self.missing), len(self.different),
                    len(self.extra))

    @property
    def details(self):
        ret = []
        if self.valid:
            ret.append('valid=' + str(len(self.valid)))
        for valid in self.valid:
            ret.append(' ' * 4 + str(valid))
        if self.missing:
            ret.append('missing=' + str(len(self.missing)))
        for missing in self.missing:
            ret.append(' ' * 4 + str(missing))
        if self.different:
            ret.append('different=' + str(len(self.different)))
        for different in self.different:
            ret.append(' ' * 4 + str(different))
        if self.extra:
            ret.append('extra=' + str(len(self.extra)))
        for extra in self.extra:
            ret.append(' ' * 4 + str(extra))
        return ret


class Results(list):
    def assert_ok(self):
        errors = [entry for entry in self if entry.error]
        assert not errors


class TestYml(object):
    """
    Run tests from yaml files.
    Multiple input strings having same expected results can be chained.
    Use $ marker to check inputs that should not match results.
    """
    @pytest.mark.parametrize('filename', [
        'rules/episodes.yml',
        'series.yml'
    ], ids=[
        'rules/episodes',
        'series'
    ])
    def test(self, filename):
        with open(os.path.join(__location__, filename), 'r', encoding='utf-8') as infile:
            data = yaml.load(infile, OrderedDictYAMLLoader)
        entries = Results()

        last_expected = None
        for string, expected in reversed(list(data.items())):
            if not expected:
                data[string] = last_expected
            else:
                last_expected = expected

        for string, expected in data.items():
            entry = self._test_entry(string, expected)
            if entry.ok:
                logging.debug('[' + filename + '] ' + str(entry))
            elif entry.warning:
                logging.warning('[' + filename + '] ' + str(entry))
            elif entry.error:
                logging.error('[' + filename + '] ' + str(entry))
                for line in entry.details:
                    logging.error('[' + filename + '] ' + ' ' * 4 + line)
            entries.append(entry)
        entries.assert_ok()

    def _test_entry(self, string, expected):
        result = guessit(string)

        entry = EntryResult(string)

        for expected_key, expected_value in expected.items():
            if expected_key in result.keys():
                if result[expected_key] != expected_value:
                    entry.different.append((expected_key, expected_value, result[expected_key]))
                else:
                    entry.valid.append((expected_key, expected_value))
            else:
                entry.missing.append((expected_key, expected_value))

        for result_key, result_value in result.items():
            if result_key not in expected.keys():
                entry.extra.append((result_key, result_value))

        return entry


