#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API functions that can be used by external software
"""
from __future__ import unicode_literals

import six

from .rules import rebulk_builder

from .options import parse_options

builder = rebulk_builder
api = None


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
    global api  #pylint:disable=global-statement
    if not api:
        api = GuessItApi(builder())
    return api.guessit(string, options)


class GuessItApi(object):
    """
    An api class that can be configured with custom Rebulk configuration.
    """
    def __init__(self, rebulk):
        """
        :param rebulk: Rebulk instance to use.
        :type rebulk: Rebulk
        :return:
        :rtype:
        """
        self.rebulk = rebulk

    def guessit(self, string, options=None):
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
        return self.rebulk.matches(string, options).to_dict(options.get('advanced', False))
