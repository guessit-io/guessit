#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API functions that can be used by external software
"""
from .rules import REBULK

from .options import parse_options


def matches(string, options=None):
    """
    Retrieves all matches from string as a list of Rebulk Match objects
    :param string: the filename or release name
    :type string: str
    :param options: the filename or release name
    :type options: str|dict
    :return:
    :rtype:
    """
    options = parse_options(options)
    return REBULK.matches(string, options)


def guessit(string, options=None):
    """
    Retrieves all matches from string as a dict
    :param string: the filename or release name
    :type string: str
    :param options: the filename or release name
    :type options: str|dict
    :return:
    :rtype:
    """
    options = parse_options(options)
    return REBULK.matches(string, options).to_dict(options.get('advanced', False))
