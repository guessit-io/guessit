#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Common module
"""
import six

seps = six.u(r' [](){}+*|&=§-_~#/\.,;:')  # list of tags/words separators

title_seps = six.u(r'-+/\|;')  # separators for title

dash = (six.u(r'-'), six.u(r'[\W_]'))  # abbreviation used by many rebulk objects.
alt_dash = (six.u(r'@'), six.u(r'[\W_]'))  # abbreviation used by many rebulk objects.
