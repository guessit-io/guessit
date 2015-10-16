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

import regex as re
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
    def __init__(self, string, negates=False):
        self.string = string
        self.negates = negates
        self.valid = []
        self.missing = []
        self.different = []
        self.extra = []
        self.others = []

    @property
    def ok(self):
        if self.negates:
            return self.missing or self.different
        return not self.missing and not self.different and not self.extra and not self.others

    @property
    def warning(self):
        if self.negates:
            return False
        return not self.missing and not self.different and self.extra

    @property
    def error(self):
        if self.negates:
            return not self.missing and not self.different and not self.others
        return self.missing or self.different or self.others

    def __repr__(self):
        if self.ok:
            return self.string + ': OK!'
        elif self.warning:
            return '%s%s: WARNING! (valid=%i, extra=%i)' % ('-' if self.negates else '', self.string, len(self.valid),
                                                            len(self.extra))
        elif self.error:
            return '%s%s: ERROR! (valid=%i, missing=%i, different=%i, extra=%i, others=%i)' % \
                   ('-' if self.negates else '', self.string, len(self.valid), len(self.missing), len(self.different),
                    len(self.extra), len(self.others))
        else:
            return '%s%s: UNKOWN! (valid=%i, missing=%i, different=%i, extra=%i, others=%i)' % \
                   ('-' if self.negates else '', self.string, len(self.valid), len(self.missing), len(self.different),
                    len(self.extra), len(self.others))

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
        if self.others:
            ret.append('others=' + str(len(self.others)))
        for other in self.others:
            ret.append(' ' * 4 + str(other))
        return ret


class Results(list):
    def assert_ok(self):
        errors = [entry for entry in self if entry.error]
        assert not errors


def files_and_ids(predicate=None):
    files = []
    ids = []

    for (dirpath, _, filenames) in os.walk(__location__):
        if dirpath == __location__:
            dirpath_rel = ''
        else:
            dirpath_rel = os.path.relpath(dirpath, __location__)
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            filepath = os.path.join(dirpath_rel, filename)
            if ext == '.yml' and (not predicate or predicate(filepath)):
                files.append(filepath)
                ids.append(os.path.join(dirpath_rel, name))

    return files, ids


class TestYml(object):
    """
    Run tests from yaml files.
    Multiple input strings having same expected results can be chained.
    Use $ marker to check inputs that should not match results.
    """

    options_re = re.compile(r'^([ \+-]+)(.*)')

    files, ids = files_and_ids()

    @pytest.mark.parametrize('filename', files, ids=ids)
    def test(self, filename):
        with open(os.path.join(__location__, filename), 'r', encoding='utf-8') as infile:
            data = yaml.load(infile, OrderedDictYAMLLoader)
        entries = Results()

        last_expected = None
        for string, expected in reversed(list(data.items())):
            if expected is None:
                data[string] = last_expected
            else:
                last_expected = expected

        for string, expected in data.items():
            entry = self.check(str(string), expected)
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

    def check(self, string, expected):
        negates, global_, string = self.parse_token_options(string)

        result = guessit(string)

        entry = EntryResult(string, negates)

        if global_:
            self.check_global(string, result, entry)

        self.check_expected(result, expected, entry)

        return entry

    def parse_token_options(self, string):
        matches = self.options_re.search(string)
        negates = False
        global_ = False
        if matches:
            string = matches.group(2)
            for opt in matches.group(1):
                if '-' in opt:
                    negates = True
                if '+' in opt:
                    global_ = True
        return negates, global_, string

    def check_global(self, string, result, entry):
        global_span = None
        for result_matches in result.matches.values():
            for result_match in result_matches:
                if not global_span:
                    global_span = list(result_match.span)
                else:
                    if global_span[0] > result_match.span[0]:
                        global_span[0] = result_match.span[0]
                    if global_span[1] < result_match.span[1]:
                        global_span[1] = result_match.span[1]
        if global_span and global_span[1] - global_span[0] < len(string):
            entry.others.append("Match is not global")

    def check_expected(self, result, expected, entry):
        if expected:
            for expected_key, expected_value in expected.items():
                if expected_key:
                    negates_key, _, result_key = self.parse_token_options(expected_key)
                    if result_key in result.keys():
                        if result[result_key] != expected_value:
                            if negates_key:
                                entry.valid.append((expected_key, expected_value))
                            else:
                                entry.different.append((expected_key, expected_value, result[expected_key]))
                        else:
                            if negates_key:
                                entry.different.append((expected_key, expected_value, result[expected_key]))
                            else:
                                entry.valid.append((expected_key, expected_value))
                    elif not negates_key:
                        entry.missing.append((expected_key, expected_value))

        for result_key, result_value in result.items():
            if result_key not in expected.keys():
                entry.extra.append((result_key, result_value))


