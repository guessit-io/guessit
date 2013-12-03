#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
# Copyright (c) 2013 Rémi Alvergnat <toilal.dev@gmail.com>
# Copyright (c) 2011 Ricard Marxer <ricardmp@gmail.com>
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

from __future__ import unicode_literals
from .containers import PropertiesContainer

from . import _psep

container = PropertiesContainer(canonical_from_pattern=False)

container.register_property('cdNumber', None, 'cd' + _psep + '(?P<cdNumber>[0-9])(?:' + _psep + 'of' + _psep + '(?P<cdNumberTotal>[0-9]))?', confidence=1.0, enhance=False, global_span=True)
container.register_property('cdNumberTotal', None, '([1-9])' + _psep + 'cds?', confidence=0.9, enhance=False)

container.register_property('edition', 'collector edition', 'collector', 'collector-edition', 'edition-collector')

container.register_property('edition', 'special edition', 'special-edition', 'edition-special')

container.register_property('edition', 'criterion edition', 'criterion-edition', 'edition-criterion')

container.register_property('edition', 'director\'s cut', 'director\'?s?-cut', 'director\'?s?-cut-edition', 'edition-director\'?s?-cut')

container.register_property('bonusNumber', None, 'x([0-9]{1,2})', enhance=False, global_span=True)

container.register_property('filmNumber', None, 'f([0-9]{1,2})', enhance=False, global_span=True)
