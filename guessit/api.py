#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API functions that can be used by external software
"""
from __future__ import unicode_literals

import six

from .rules import REBULK

from .options import parse_options


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
    if not isinstance(string, six.text_type):
        raise TypeError("guessit input must be %s." % six.text_type.__name__)
    options = parse_options(options)
    return REBULK.matches(string, options).to_dict(options.get('advanced', False))
