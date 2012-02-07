#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2012 Nicolas Wack <wackou@gmail.com>
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

import logging

log = logging.getLogger("guessit.transfo.split_on_dash")


DEPENDS = []
PROVIDES = []

def process(mtree):
    for node in mtree.unidentified_leaves():
        indices = []
        didx = node.value.find('-')
        while didx > 0:
            indices.extend([ didx, didx+1 ])
            didx = node.value.find('-', didx+1)
        if indices:
            node.partition(indices)
