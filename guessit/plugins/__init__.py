#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
#
# GuessIt is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessIt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function, unicode_literals

import abc
import logging
from abc import ABCMeta, abstractmethod


class Transformer(object):
    __metaclass__ = ABCMeta

    def __init__(self, priority=0):
        self.priority = priority
        self.log = logging.getLogger(self.name)

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def fullname(self):
        return self.__module__ + "." + self.__class__.__name__

    def supported_properties(self):
        return {}

    def enabled(self):
        return True

    def second_pass_options(self, mtree):
        return (None, None)

    def should_process(self, matcher):
        return True

    @abstractmethod
    def process(self, mtree, *args, **kwargs):
        pass

    def rate_quality(self, guess, *props):
        return 0
