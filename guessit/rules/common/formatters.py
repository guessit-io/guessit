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


def reorder_title(title, articles=('the',), separators=(',', ', ')):
    """
    Reorder the title
    :param title:
    :type title:
    :param articles:
    :type articles:
    :param separators:
    :type separators:
    :return:
    :rtype:
    """
    ltitle = title.lower()
    for article in articles:
        for separator in separators:
            suffix = separator + article
            if ltitle[-len(suffix):] == suffix:
                return title[-len(suffix) + len(separator):] + ' ' + title[:-len(suffix)]
    return title


def chain(*formatters):
    """
    Chain formatter functions
    :param functions:
    :type functions:
    :return:
    :rtype:
    """
    def formatters_chain(input_string):  # pylint:disable=missing-docstring
        for formatter in formatters:
            input_string = formatter(input_string)
        return input_string

    return formatters_chain
