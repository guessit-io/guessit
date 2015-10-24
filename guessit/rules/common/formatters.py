#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Formatters
"""

from . import seps
import regex as re

_excluded_clean_chars = ',:;-/\\'
clean_chars = ""
for sep in seps:
    if sep not in _excluded_clean_chars:
        clean_chars += sep

def cleanup(input_string):
    """
    Removes and strip separators from input_string (but keep ',;' characters)
    :param input_string:
    :type input_string:
    :return:
    :rtype:
    """
    for char in clean_chars:
        input_string = input_string.replace(char, ' ')
    return re.sub(' +', ' ', strip(input_string))


def strip(input_string):
    """
    Strip separators from input_string
    :param input_string:
    :type input_string:
    :return:
    :rtype:
    """
    return input_string.strip(seps)
