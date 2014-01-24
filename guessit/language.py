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

from guessit.patterns import sep
from guessit import UnicodeMixin, base_text_type, u, s
from guessit.textutils import find_words
from babelfish import Language, LANGUAGES, COUNTRIES
import babelfish
import re
import logging
from guessit.guess import Guess

__all__ = ['Language', 'UNDETERMINED',
           'search_language', 'guess_language']

log = logging.getLogger(__name__)

UNDETERMINED = babelfish.Language('und')

SYN = {('und', None): ['unknown', 'inconnu', 'unk', 'un'],
       ('ell', None): ['gr', 'greek'],
       ('spa', None): ['esp', 'español'],
       ('fra', None): ['français', 'vf', 'vff', 'vfi'],
       ('swe', None): ['se'],
       ('por', 'BR'): ['po', 'pb', 'pob', 'br', 'brazilian'],
       ('cat', None): ['català'],
       ('ces', None): ['cz'],
       ('ukr', None): ['ua'],
       ('zho', None): ['cn'],
       ('jpn', None): ['jp'],
       ('hrv', None): ['scr'],
       ('mul', None): ['multi', 'dl'],  # http://scenelingo.wordpress.com/2009/03/24/what-does-dl-mean/
       }


class GuessitConverter(babelfish.LanguageReverseConverter):

    _with_country_regexp = re.compile('(.*)\((.*)\)')
    _with_country_regexp2 = re.compile('(.*)-(.*)')

    def __init__(self):
        self.codes = set()
        self.guessit_exceptions = {}

        self.alpha3b = babelfish.language_converters['alpha3b']
        self.alpha2 = babelfish.language_converters['alpha2']
        self.name = babelfish.language_converters['name']

        self.codes |= LANGUAGES | self.alpha3b.codes | self.alpha2.codes | self.name.codes

        for (alpha3, country), synlist in SYN.items():
            for syn in synlist:
                self.guessit_exceptions[syn.lower()] = (alpha3, country, None)
                self.codes.add(syn)

    def convert(self, alpha3, country=None):
        return str(babelfish.Language(alpha3, country))

    def reverse(self, name):
        with_country = (GuessitConverter._with_country_regexp.match(name) or
                        GuessitConverter._with_country_regexp2.match(name))

        if with_country:
            lang = babelfish.Language.fromguessit(with_country.group(1).strip())
            lang.country = babelfish.Country.fromguessit(with_country.group(2).strip())
            return (lang.alpha3, lang.country.alpha2 if lang.country else None, lang.script or None)

        # exceptions come first, as they need to override a potential match
        # with any of the other guessers
        try:
            return self.guessit_exceptions[name.lower()]
        except KeyError:
            pass

        for conv in [babelfish.Language,
                     babelfish.Language.fromalpha3b,
                     babelfish.Language.fromalpha2,
                     babelfish.Language.fromname,
                     babelfish.Language.fromopensubtitles]:
            try:
                c = conv(name)
                return c.alpha3, c.country, c.script
            except (ValueError, babelfish.LanguageReverseError):
                pass

        raise babelfish.LanguageReverseError(name)


ALL_NAMES = frozenset(c.lower() for c in GuessitConverter().codes)

babelfish.language_converters['guessit'] = GuessitConverter()

COUNTRIES_SYN = {'ES': ['españa'],
                 'GB': ['UK'],
                 'BR': ['brazilian', 'bra'],
                 # FIXME: this one is a bit of a stretch, not sure how to do
                 #        it properly, though...
                 'MX': ['Latinoamérica', 'latin america']
                 }


class GuessitCountryConverter(babelfish.CountryReverseConverter):
    def __init__(self):
        self.codes = set()
        self.guessit_exceptions = {}

        self.name = babelfish.country_converters['name']

        self.codes |= set(COUNTRIES.keys()) | self.name.codes

        for alpha2, synlist in COUNTRIES_SYN.items():
            for syn in synlist:
                self.guessit_exceptions[syn.lower()] = alpha2
                self.codes.add(syn)

    def convert(self, alpha2):
        return str(babelfish.Country(alpha2))

    def reverse(self, name):
        # exceptions come first, as they need to override a potential match
        # with any of the other guessers
        try:
            return self.guessit_exceptions[name.lower()]
        except KeyError:
            pass

        try:
            return babelfish.Country(name.upper()).alpha2
        except ValueError:
            pass

        for conv in [babelfish.Country.fromname]:
            try:
                return conv(name).alpha2
            except babelfish.CountryReverseError:
                pass

        raise babelfish.CountryReverseError(name)


babelfish.country_converters['guessit'] = GuessitCountryConverter()


class Language(UnicodeMixin):
    """This class represents a human language.

    You can initialize it with pretty much anything, as it knows conversion
    from ISO-639 2-letter and 3-letter codes, English and French names.

    You can also distinguish languages for specific countries, such as
    Portuguese and Brazilian Portuguese.

    There are various properties on the language object that give you the
    representation of the language for a specific usage, such as .alpha3
    to get the ISO 3-letter code, or .opensubtitles to get the OpenSubtitles
    language code.

    >>> Language('fr')
    Language(French)

    >>> s(Language('eng').english_name)
    'english'

    >>> s(Language('pt(br)').country.english_name)
    'Brazil'

    >>> s(Language('Español (Latinoamérica)').country.english_name)
    'Latin America'

    >>> Language('Spanish (Latin America)') == Language('Español (Latinoamérica)')
    True

    >>> s(Language('zz', strict=False).english_name)
    'Undetermined'

    >>> s(Language('pt(br)').opensubtitles)
    'pob'
    """

    def __init__(self, language, country=None, strict=False):
        language = u(language.strip().lower())
        country = babelfish.Country(country.upper()) if country else None

        try:
            self.lang = babelfish.Language.fromguessit(language)
            # user given country overrides guessed one
            if country:
                self.lang.country = country

        except babelfish.LanguageReverseError:
            msg = 'The given string "%s" could not be identified as a language' % language
            if strict:
                raise ValueError(msg)

            log.debug(msg)
            self.lang = UNDETERMINED

    @property
    def country(self):
        return self.lang.country

    @property
    def alpha2(self):
        return self.lang.alpha2

    @property
    def alpha3(self):
        return self.lang.alpha3

    @property
    def alpha3term(self):
        return self.lang.alpha3b

    @property
    def english_name(self):
        return self.lang.name

    @property
    def opensubtitles(self):
        return self.lang.opensubtitles

    @property
    def tmdb(self):
        if self.country:
            return '%s-%s' % (self.alpha2, self.country.alpha2)
        return self.alpha2

    def __hash__(self):
        return hash(self.lang)

    def __eq__(self, other):
        if isinstance(other, Language):
            # in Guessit, languages are considered equal if their main languages are equal
            return self.alpha3 == other.alpha3

        if isinstance(other, base_text_type):
            try:
                return self == Language(other)
            except ValueError:
                return False

        return False

    def __ne__(self, other):
        return not self == other

    def __bool__(self):
        return self.lang != UNDETERMINED
    __nonzero__ = __bool__

    def __unicode__(self):
        if self.lang.country:
            return '%s(%s)' % (self.english_name, self.country.alpha2)
        else:
            return self.english_name

    def __repr__(self):
        if self.lang.country:
            return 'Language(%s, country=%s)' % (self.english_name, self.lang.country)
        else:
            return 'Language(%s)' % self.english_name


# list of common words which could be interpreted as languages, but which
# are far too common to be able to say they represent a language in the
# middle of a string (where they most likely carry their commmon meaning)
LNG_COMMON_WORDS = frozenset([
    # english words
    'is', 'it', 'am', 'mad', 'men', 'man', 'run', 'sin', 'st', 'to',
    'no', 'non', 'war', 'min', 'new', 'car', 'day', 'bad', 'bat', 'fan',
    'fry', 'cop', 'zen', 'gay', 'fat', 'one', 'cherokee', 'got', 'an', 'as',
    'cat', 'her', 'be', 'hat', 'sun', 'may', 'my', 'mr', 'rum', 'pi',
    # french words
    'bas', 'de', 'le', 'son', 'ne', 'ca', 'ce', 'et', 'que',
    'mal', 'est', 'vol', 'or', 'mon', 'se',
    # spanish words
    'la', 'el', 'del', 'por', 'mar',
    # other
    'ind', 'arw', 'ts', 'ii', 'bin', 'chan', 'ss', 'san', 'oss', 'iii',
    'vi', 'ben', 'da', 'lt', 'ch',
    # new from babelfish
    'mkv', 'avi', 'dmd', 'the', 'dis', 'cut', 'stv', 'des', 'dia', 'and',
    'cab', 'sub', 'mia', 'rim', 'las', 'une', 'par', 'srt', 'ano', 'toy',
    'job', 'gag', 'reel', 'www', 'for', 'ayu', 'csi', 'ren', 'moi', 'sur',
    'fer', 'fun', 'two', 'big', 'psy', 'air'
    ])


subtitle_prefixes = ['sub', 'subs', 'st', 'vost', 'subforced', 'fansub', 'hardsub']
subtitle_suffixes = ['subforced', 'fansub', 'hardsub']

_possible_languages_hashed = {}
for valid_name in set(ALL_NAMES) - LNG_COMMON_WORDS:
    _possible_languages_hashed[valid_name] = ('language', valid_name)
    for subtitle_prefix in subtitle_prefixes:
        _possible_languages_hashed[subtitle_prefix + valid_name] = ('subtitleLanguage', valid_name)
    for subtitle_suffix in subtitle_suffixes:
        _possible_languages_hashed[valid_name + subtitle_suffix] = ('subtitleLanguage', valid_name)


def find_possible_languages(string):
    """Find possible languages in the string

    :return: list of tuple (property, language, word)
    """
    found_words = set(find_words(string))

    valid_words = []
    for word in found_words:
        lword = word.lower()
        result = _possible_languages_hashed.get(lword)
        if result:
            valid_words.append((result[0], result[1], word))

    return valid_words


def search_language(string, lang_filter=None):
    """Looks for language patterns, and if found return the language object,
    its group span and an associated confidence.

    you can specify a list of allowed languages using the lang_filter argument,
    as in lang_filter = [ 'fr', 'eng', 'spanish' ]

    >>> search_language('movie [en].avi')
    (Language(English), (7, 9), 0.8)

    >>> search_language('the zen fat cat and the gay mad men got a new fan', lang_filter = ['en', 'fr', 'es'])
    (None, None, None)
    """

    if lang_filter:
        lang_filter = set(babelfish.Language.fromguessit(lang) for lang in lang_filter)

    confidence = 1.0  # for all of them

    for prop, lang, word in find_possible_languages(string):
        pos = string.find(word)
        end = pos + len(word)

        language = Language(lang)
        if lang_filter and language not in lang_filter:
            continue

        if language != 'mul' and not hasattr(language, 'alpha2'):
            # Found language has no alpha2 equilavent. It's probably an uncommon language.
            continue

        # only allow those languages that have a 2-letter code, those that
        # don't are too esoteric and probably false matches
        #if language.lang not in lng3_to_lng2:
        #    continue

        # confidence depends on alpha2, alpha3, english name, ...
        if len(lang) == 2:
            confidence = 0.8
        elif len(lang) == 3:
            confidence = 0.9
        elif prop == 'subtitleLanguage':
            confidence = 0.6  # Subtitle prefix found with language
        else:
            # Note: we could either be really confident that we found a
            #       language or assume that full language names are too
            #       common words and lower their confidence accordingly
            confidence = 0.3  # going with the low-confidence route here

        return Guess({prop: language}, confidence=confidence, input=string, span=(pos, end))

    return None


def guess_language(text):
    """Guess the language in which a body of text is written.

    This uses the external guess-language python module, and will fail and return
    Language(Undetermined) if it is not installed.
    """
    try:
        from guess_language import guessLanguage
        return babelfish.Language.fromguessit(guessLanguage(text))

    except ImportError:
        log.error('Cannot detect the language of the given text body, missing dependency: guess-language')
        log.error('Please install it from PyPI, by doing eg: pip install guess-language')
        return UNDETERMINED
