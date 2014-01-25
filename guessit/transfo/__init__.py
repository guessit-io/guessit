#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
#
# GuessIt is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessIt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function, unicode_literals

from guessit import base_text_type, Guess
from guessit.patterns.numeral import parse_numeral
from guessit.textutils import clean_string
import logging

log = logging.getLogger(__name__)


class TransfoException(Exception):
    def __init__(self, transformer, message):

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)

        self.transformer = transformer


def found_property(node, name, confidence):
    node.guess = Guess({name: node.clean_value}, confidence=confidence)
    log.debug('Found with confidence %.2f: %s' % (confidence, node.guess))


def format_guess(guess):
    """Format all the found values to their natural type.
    For instance, a year would be stored as an int value, etc...

    Note that this modifies the dictionary given as input.
    """
    for prop, value in guess.items():
        if prop in ('season', 'episodeNumber', 'year', 'cdNumber',
                    'cdNumberTotal', 'bonusNumber', 'filmNumber'):
            guess[prop] = parse_numeral(guess[prop])

    return guess


def find_and_split_node(node, strategy, skip_nodes, logger, partial_span=None):
    value = None
    if partial_span:
        value = node.value[partial_span[0]:partial_span[1]]
    else:
        value = node.value
    string = ' %s ' % value  # add sentinels
    for matcher, confidence, args, kwargs in strategy:
        all_args = [string]
        if getattr(matcher, 'use_node', False):
            all_args.append(node)
        if args:
            all_args.append(args)

        if kwargs:
            matcher_result = matcher(*all_args, **kwargs)
        else:
            matcher_result = matcher(*all_args)

        if matcher_result:
            if not isinstance(matcher_result, Guess):
                result, span = matcher_result
            else:
                result, span = matcher_result, matcher_result.metadata().span

            if result:
                # readjust span to compensate for sentinels
                span = (span[0] - 1, span[1] - 1)

                # readjust span to compensate for partial_span
                if partial_span:
                    span = (span[0] + partial_span[0], span[1] + partial_span[0])

                partition_spans = None
                for skip_node in skip_nodes:
                    if skip_node.parent.node_idx == node.node_idx[:len(skip_node.parent.node_idx)] and\
                        skip_node.span == span:
                        partition_spans = node.get_partition_spans(skip_node.span)
                        partition_spans.remove(skip_node.span)
                        break

                if not partition_spans:
                    # restore sentinels compensation

                    guess = None
                    if isinstance(result, Guess):
                        if confidence is None:
                            confidence = result.confidence()
                        guess = result
                    else:
                        if confidence is None:
                            confidence = 1.0
                        guess = Guess(result, confidence=confidence, input=string, span=span)

                    guess = format_guess(guess)
                    msg = 'Found with confidence %.2f: %s' % (confidence, guess)
                    (logger or log).debug(msg)

                    node.partition(span)
                    absolute_span = (span[0] + node.offset, span[1] + node.offset)
                    for child in node.children:
                        if child.span == absolute_span:
                            child.guess = guess
                        else:
                            find_and_split_node(child, strategy, skip_nodes, logger)
                else:
                    for partition_span in partition_spans:
                        find_and_split_node(node, strategy, skip_nodes, logger, partition_span)


class SingleNodeGuesser(object):
    def __init__(self, guess_func, confidence, logger, *args, **kwargs):
        self.guess_func = guess_func
        self.confidence = confidence
        self.logger = logger
        self.skip_nodes = kwargs.pop('skip_nodes', [])
        self.args = args
        self.kwargs = kwargs

    def process(self, mtree):
        # strategy is a list of pairs (guesser, confidence)
        # - if the guesser returns a guessit.Guess and confidence is specified,
        #   it will override it, otherwise it will leave the guess confidence
        # - if the guesser returns a simple dict as a guess and confidence is
        #   specified, it will use it, or 1.0 otherwise
        strategy = [(self.guess_func, self.confidence, self.args, self.kwargs)]

        for node in mtree.unidentified_leaves():
            find_and_split_node(node, strategy, self.skip_nodes, self.logger)
