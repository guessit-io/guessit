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
language_matrix = [ l.strip().split('|') for l in open(fileutils.file_in_same_dir(__file__, 'ISO-639-2_utf-8.txt')) ]

_lng3        = frozenset(filter(bool, (l[0] for l in language_matrix)))
_lng3term    = frozenset(filter(bool, (l[1] for l in language_matrix)))
_lng2        = frozenset(filter(bool, (l[2] for l in language_matrix)))
_lng_en_name = frozenset(filter(bool, (lng for l in language_matrix for lng in l[3].lower().split('; '))))
_lng_fr_name = frozenset(filter(bool, (lng for l in language_matrix for lng in l[4].lower().split('; '))))

_lng3_to_lng3term = dict((l[0], l[1]) for l in language_matrix if l[1])
_lng3term_to_lng3 = dict((l[1], l[0]) for l in language_matrix if l[1])

_lng3_to_lng2 = dict((l[0], l[2]) for l in language_matrix if l[2])
_lng2_to_lng3 = dict((l[2], l[0]) for l in language_matrix if l[2])

# we only return the first given english name, hoping it is the most used one
_lng3_to_lng_en_name = dict((l[0], l[3].split('; ')[0]) for l in language_matrix if l[3])
_lng_en_name_to_lng3 = dict((en_name, l[0]) for l in language_matrix if l[3] for en_name in l[3].split('; '))

# we only return the first given french name, hoping it is the most used one
_lng3_to_lng_fr_name = dict((l[0], l[4].split('; ')[0]) for l in language_matrix if l[4])
_lng_fr_name_to_lng3 = dict((fr_name, l[0]) for l in language_matrix if l[4] for fr_name in l[4].split('; '))


def is_language(language):
    language = language.lower()
    return any(language in lang_set for lang_set in (_lng3, _lng3term, _lng2, _lng_en_name, _lng_fr_name))

class Language(object):
    def __init__(self, language):
        lang = None
        if len(language) == 2:
            lang = _lng2_to_lng3.get(language)
        elif len(language) == 3:
            lang = language if language in _lng3 else _lng3term_to_lng3.get(language)
        else:
            lang = _lng_en_name_to_lng3.get(language) or _lng_fr_name_to_lng3.get(language)

        if lang is None:
            raise ValueError, 'The given string "%s" could not be identified as a language' % language

        self.lang = lang

    def __str__(self):
        return _lng3_to_lng_en_name[self.lang]

    def __repr__(self):
        return 'Language(%s)' % self
