#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Formatters
"""
from rebulk.remodule import re

from rebulk.formatters import formatters

from . import seps


_excluded_clean_chars = ',:;-/\\'
clean_chars = ""
for sep in seps:
    if sep not in _excluded_clean_chars:
        clean_chars += sep


def cleanup(input_string):
    """
    Removes and strip separators from input_string (but keep ',;' characters)

    It also keep separators for single characters (Mavels Agents of S.H.I.E.L.D.)

    :param input_string:
    :type input_string:
    :return:
    :rtype:
    """
    clean_string = input_string
    for char in clean_chars:
        clean_string = clean_string.replace(char, ' ')

    # Restore input separator if they separate single characters.
    # Useful for Mavels Agents of S.H.I.E.L.D.
    # https://github.com/guessit-io/guessit/issues/278

    indices = [i for i, letter in enumerate(clean_string) if letter in seps]

    dots = set()
    if indices:
        clean_list = list(clean_string)

        potential_indices = []

        for i in indices:
            b = i-2
            n = i+2
            if b >= 0 and input_string[i] == input_string[b] and input_string[i-1] not in seps\
                    and (n >= len(input_string) or input_string[n] == input_string[i] and input_string[n-1] not in seps):
                potential_indices.append(i)

        replace_indices = []

        for potential_index in potential_indices:
            if potential_index - 2 in potential_indices or potential_index + 2 in potential_indices:
                replace_indices.append(potential_index)

        if replace_indices:
            for replace_index in replace_indices:
                dots.add(input_string[replace_index])
                clean_list[replace_index] = input_string[replace_index]
            clean_string = ''.join(clean_list)

    clean_string = strip(clean_string, ''.join([sep for sep in seps if sep not in dots]))

    clean_string = re.sub(' +', ' ', clean_string)
    return clean_string


def strip(input_string, chars=seps):
    """
    Strip separators from input_string
    :param input_string:
    :param chars:
    :type input_string:
    :return:
    :rtype:
    """
    return input_string.strip(chars)


def raw_cleanup(raw):
    """
    Cleanup a raw value to perform raw comparison
    :param raw:
    :type raw:
    :return:
    :rtype:
    """
    return formatters(cleanup, strip)(raw.lower())


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
