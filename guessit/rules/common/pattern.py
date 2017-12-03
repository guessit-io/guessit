#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pattern utility functions
"""


def is_enabled(context, name):
    """Whether a specific pattern is enabled.

    The context object might define an inclusion list (includes) or an exclusion list (excludes)
    A pattern is considered enabled if it's not found in the exclusion list and
    it's found in the inclusion list or the inclusion list is empty or not defined.

    :param context:
    :param name:
    :return:
    """
    excludes = context.get('excludes')
    if excludes and name in excludes:
        return False

    includes = context.get('includes')
    if includes and name not in includes:
        return False

    return True
