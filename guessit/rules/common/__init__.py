#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Common module
"""
import six

seps = six.u(' [](){}!?+*|&=%§-_~#/\.')  # list of tags/words separators

dash = (six.u('-'), six.u('[\W_]?'))  # abbreviation used by many rebulk objects.
