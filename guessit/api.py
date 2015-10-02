#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API functions that can be used by external software
"""

from .rules import REBULK


def guessit(string):
    """
    Retrieves all matches from string
    :param string: the filename or release name
    :type string: str
    :return:
    :rtype:
    """
    return REBULK.matches(string).to_dict()
