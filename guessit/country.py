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

from . import fileutils
import logging

log = logging.getLogger('guessit.country')


# parsed from http://en.wikipedia.org/wiki/ISO_3166-1
#
# Description of the fields:
# "An English name, an alpha-2 code (when given),
# an alpha-3 code (when given), a numeric code, and an ISO 31666-2 code
# are all separated by pipe (|) characters."
_iso3166_contents = fileutils.load_file_in_same_dir(__file__,
                                                    'ISO-3166-1_utf8.txt')
country_matrix = [ l.strip().decode('utf-8').split('|')
                   for l in _iso3166_contents.strip().split('\n') ]

country_to_alpha3 = dict((c[0].lower(), c[2].lower()) for c in country_matrix)
country_to_alpha3.update(dict((c[1].lower(), c[2].lower()) for c in country_matrix))
country_to_alpha3.update(dict((c[2].lower(), c[2].lower()) for c in country_matrix))

country_alpha3_to_en_name = dict((c[2].lower(), c[0]) for c in country_matrix)
country_alpha3_to_alpha2 = dict((c[2].lower(), c[1].lower()) for c in country_matrix)



class Country(object):
    """This class represents a country.

    You can initialize it with pretty much anything, as it knows conversion
    from ISO-3166 2-letter and 3-letter codes, and an English name.
    """
    def __init__(self, country):
        self.alpha3 = country_to_alpha3.get(country.lower())

        if not self.alpha3:
            msg = 'The given string "%s" could not be identified as a country'
            raise ValueError(msg % country)

    @property
    def alpha2(self):
        return country_alpha3_to_alpha2[self.alpha3]

    @property
    def english_name(self):
        return country_alpha3_to_en_name[self.alpha3]

    def __hash__(self):
        return hash(self.alpha3)

    def __eq__(self, other):
        if isinstance(other, Country):
            return self.alpha3 == other.alpha3

        if isinstance(other, basestring):
            try:
                return self == Country(other)
            except ValueError:
                return False

        return False

    def __ne__(self, other):
        return not self == other

    def __unicode__(self):
        return self.english_name

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return 'Country(%s)' % self.english_name

