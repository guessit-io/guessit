#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Formatters
"""

from . import seps


def cleanup(input_string):
    """
    Removes and strip separators from input_string
    :param input_string:
    :type input_string:
    :return:
    :rtype:
    """
    for sep in seps:
        input_string = input_string.replace(sep, ' ')
    return input_string.strip(seps)
