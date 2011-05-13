#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2011 Nicolas Wack <wackou@gmail.com>
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

from guessit.guess import Guess, merge_append_guesses, merge_all
from guessit import fileutils, textutils
import os.path
import re
import logging

log = logging.getLogger('guessit.language')


_reverse_language_map = { 'English': [ 'english', 'eng', 'en' ],
                          'French': [ 'french', 'fr', 'francais', u'français' ],
                          'Spanish': [ 'spanish', 'es', 'esp', 'espanol', u'español' ], # should we remove 'es'? (very common in spanish)
                          'Italian': [ 'italian', 'italiano', 'ita' ]  # no 'it', too common a word
                          }

_language_map = {}
for lang, langs in _reverse_language_map.items():
    for l in langs:
        _language_map[l] = lang


# downloaded from http://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt
#
# Description of the fields:
# "An alpha-3 (bibliographic) code, an alpha-3 (terminologic) code (when given),
# an alpha-2 code (when given), an English name, and a French name of a language
# are all separated by pipe (|) characters."
language_matrix = [ l.strip().split('|') for l in open('ISO-639-2_utf-8.txt') ]

class Language(object):
    def __init__(self, language):
        if len(language) == 2:
            pass
        elif len(language) == 3:
            pass
        else:
            pass

