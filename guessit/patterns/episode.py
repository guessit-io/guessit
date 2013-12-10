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

from __future__ import absolute_import, division, print_function, unicode_literals

from . import sep
from .numeral import numeral, digital_numeral

# format: [ (regexp, confidence, span_adjust) ]
episode_rexps = [  # ... Season 2 ...
                  (r'(?:season|saison)\s+(?P<season>%s)' % (numeral,), 1.0, (0, 0)),

                  # ... s02e13 ...
                  (r's(?P<season>' + digital_numeral + ')[^0-9]?(?P<episodeNumber>(?:-?[e-]' + digital_numeral + ')+)[^0-9]', 1.0, (0, -1)),

                  # ... s03-x02 ... # FIXME: redundant? remove it?
                  #(r'[Ss](?P<season>[0-9]{1,3})[^0-9]?(?P<bonusNumber>(?:-?[xX-][0-9]{1,3})+)[^0-9]', 1.0, (0, -1)),

                  # ... 2x13 ...
                  (r'[^0-9](?P<season>' + digital_numeral + ')[^0-9 .-]?(?P<episodeNumber>(?:-?x' + digital_numeral + ')+)[^0-9]', 1.0, (1, -1)),

                  # ... s02 ...
                  #(sep + r's(?P<season>[0-9]{1,2})' + sep, 0.6, (1, -1)),
                  (r's(?P<season>' + digital_numeral + ')[^0-9]', 0.6, (0, -1)),

                  # v2 or v3 for some mangas which have multiples rips
                  (r'(?P<episodeNumber>' + digital_numeral + ')v[23]' + sep, 0.6, (0, 0)),

                  # ... ep 23 ...
                  ('(?:ep|episode)' + sep + r'(?P<episodeNumber>' + numeral + ')[^0-9]', 0.7, (0, -1)),

                  # ... e13 ... for a mini-series without a season number
                  (sep + r'e(?P<episodeNumber>' + digital_numeral + ')' + sep, 0.6, (1, -1))

                  ]

weak_episode_rexps = [  # ... 213 or 0106 ...
                       (sep + r'(?P<episodeNumber>[0-9]{2,4})' + sep, (1, -1))
                       ]

non_episode_title = ['extras', 'rip']

unlikely_series = ['series']
