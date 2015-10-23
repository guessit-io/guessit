#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Language and subtitleLanguage
"""
# pylint: disable=no-member
from __future__ import absolute_import, division, print_function, unicode_literals

import regex as re
from babelfish import Language, Country
import babelfish
from rebulk import Rebulk, Rule

from guessit.rules.common.validators import seps_surround

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
       ('mul', None): ['multi', 'dl']}  # http://scenelingo.wordpress.com/2009/03/24/what-does-dl-mean/


class GuessitConverter(babelfish.LanguageReverseConverter):  # pylint: disable=missing-docstring
    _with_country_regexp = re.compile(r'(.*)\((.*)\)')
    _with_country_regexp2 = re.compile(r'(.*)-(.*)')

    def __init__(self):
        self.guessit_exceptions = {}
        for (alpha3, country), synlist in SYN.items():
            for syn in synlist:
                self.guessit_exceptions[syn.lower()] = (alpha3, country, None)

    @property
    def codes(self):  # pylint: disable=missing-docstring
        return (babelfish.language_converters['alpha3b'].codes |
                babelfish.language_converters['alpha2'].codes |
                babelfish.language_converters['name'].codes |
                babelfish.language_converters['opensubtitles'].codes |
                babelfish.country_converters['name'].codes |
                frozenset(self.guessit_exceptions.keys()))

    def convert(self, alpha3, country=None, script=None):
        return str(babelfish.Language(alpha3, country, script))

    def reverse(self, name):
        with_country = (GuessitConverter._with_country_regexp.match(name) or
                        GuessitConverter._with_country_regexp2.match(name))

        name = name.lower()
        if with_country:
            lang = Language.fromguessit(with_country.group(1).strip())
            lang.country = babelfish.Country.fromguessit(with_country.group(2).strip())
            return lang.alpha3, lang.country.alpha2 if lang.country else None, lang.script or None

        # exceptions come first, as they need to override a potential match
        # with any of the other guessers
        try:
            return self.guessit_exceptions[name]
        except KeyError:
            pass

        for conv in [babelfish.Language,
                     babelfish.Language.fromalpha3b,
                     babelfish.Language.fromalpha2,
                     babelfish.Language.fromname,
                     babelfish.Language.fromopensubtitles]:
            try:
                reverse = conv(name)
                return reverse.alpha3, reverse.country, reverse.script
            except (ValueError, babelfish.LanguageReverseError):
                pass

        raise babelfish.LanguageReverseError(name)


babelfish.language_converters['guessit'] = GuessitConverter()

COUNTRIES_SYN = {'ES': ['españa'],
                 'GB': ['UK'],
                 'BR': ['brazilian', 'bra'],
                 # FIXME: this one is a bit of a stretch, not sure how to do
                 #        it properly, though...
                 'MX': ['Latinoamérica', 'latin america']}


class GuessitCountryConverter(babelfish.CountryReverseConverter):  # pylint: disable=missing-docstring
    def __init__(self):
        self.guessit_exceptions = {}

        for alpha2, synlist in COUNTRIES_SYN.items():
            for syn in synlist:
                self.guessit_exceptions[syn.lower()] = alpha2

    @property
    def codes(self):  # pylint: disable=missing-docstring
        return (babelfish.country_converters['name'].codes |
                frozenset(babelfish.COUNTRIES.values()) |
                frozenset(self.guessit_exceptions.keys()))

    def convert(self, alpha2):
        if alpha2 == 'GB':
            return 'UK'
        return str(Country(alpha2))

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


# list of common words which could be interpreted as languages, but which
# are far too common to be able to say they represent a language in the
# middle of a string (where they most likely carry their commmon meaning)
LNG_COMMON_WORDS = frozenset([
    # english words
    'is', 'it', 'am', 'mad', 'men', 'man', 'run', 'sin', 'st', 'to',
    'no', 'non', 'war', 'min', 'new', 'car', 'day', 'bad', 'bat', 'fan',
    'fry', 'cop', 'zen', 'gay', 'fat', 'one', 'cherokee', 'got', 'an', 'as',
    'cat', 'her', 'be', 'hat', 'sun', 'may', 'my', 'mr', 'rum', 'pi', 'bb',
    'bt', 'tv', 'aw', 'by', 'md', 'mp', 'cd', 'lt', 'gt', 'in', 'ad', 'ice',
    'ay', 'at', 'star', 'so', 'he',
    # french words
    'bas', 'de', 'le', 'son', 'ne', 'ca', 'ce', 'et', 'que',
    'mal', 'est', 'vol', 'or', 'mon', 'se', 'je', 'tu', 'me',
    'ne', 'ma', 'va', 'au',
    # japanese words,
    'wa', 'ga', 'ao',
    # spanish words
    'la', 'el', 'del', 'por', 'mar', 'al',
    # other
    'ind', 'arw', 'ts', 'ii', 'bin', 'chan', 'ss', 'san', 'oss', 'iii',
    'vi', 'ben', 'da', 'lt', 'ch', 'sr', 'ps', 'cx',
    # new from babelfish
    'mkv', 'avi', 'dmd', 'the', 'dis', 'cut', 'stv', 'des', 'dia', 'and',
    'cab', 'sub', 'mia', 'rim', 'las', 'une', 'par', 'srt', 'ano', 'toy',
    'job', 'gag', 'reel', 'www', 'for', 'ayu', 'csi', 'ren', 'moi', 'sur',
    'fer', 'fun', 'two', 'big', 'psy', 'air',
    # movie title
    'brazil',
    # release groups
    'bs',  # Bosnian
    'kz',
    # countries
    'gt', 'lt', 'im',
    # part/pt
    'pt'
])

LNG_COMMON_WORDS_STRICT = frozenset(['brazil'])

subtitle_prefixes = ['sub', 'subs', 'st', 'vost', 'subforced', 'fansub', 'hardsub']
subtitle_suffixes = ['subforced', 'fansub', 'hardsub', 'sub', 'subs']
lang_prefixes = ['true']

all_lang_prefixes_suffixes = subtitle_prefixes + subtitle_suffixes + lang_prefixes

_words_rexp = re.compile(r'\w+', re.UNICODE)


def find_languages(string, options=None):
    """Find languages in the string

    :return: list of tuple (property, Language, lang_word, word)
    """
    allowed_languages = options.get('allowed_languages')
    common_words = LNG_COMMON_WORDS_STRICT if allowed_languages else LNG_COMMON_WORDS

    matches = []
    for word_match in _words_rexp.finditer(string.replace('_', ' ')):
        word = word_match.group()
        start, end = word_match.span()

        lang_word = word.lower()
        key = 'language'
        for prefix in subtitle_prefixes:
            if lang_word.startswith(prefix):
                lang_word = lang_word[len(prefix):]
                key = 'subtitleLanguage'
        for suffix in subtitle_suffixes:
            if lang_word.endswith(suffix):
                lang_word = lang_word[:len(suffix)-1]
                key = 'subtitleLanguage'
        for prefix in lang_prefixes:
            if lang_word.startswith(prefix):
                lang_word = lang_word[len(prefix):]
        if lang_word not in common_words and word.lower() not in common_words:
            try:
                lang = Language.fromguessit(lang_word)
                if allowed_languages:
                    if lang.name.lower() in allowed_languages \
                            or lang.alpha2.lower() in allowed_languages \
                            or lang.alpha3.lower() in allowed_languages:
                        matches.append((start, end, {'name': key, 'value': lang}))
                # Keep language with alpha2 equivalent. Others are probably
                # uncommon languages.
                elif lang == 'mul' or hasattr(lang, 'alpha2'):
                    matches.append((start, end, {'name': key, 'value': lang}))
            except babelfish.Error:
                pass
    return matches


LANGUAGE = Rebulk()


class SubtitlePrefixLanguageRule(Rule):
    """
    Convert language guess as subtitleLanguage if previous match is a subtitle language prefix
    """
    def when(self, matches, context):
        ret = []
        for language in matches.named('language'):
            prefix = matches.previous(language, lambda match: match.name == 'subtitleLanguage.prefix', 0)
            if not prefix:
                group_marker = matches.markers.at_match(language, lambda marker: marker.name == 'group', 0)
                if group_marker:
                    prefix = matches.previous(group_marker, lambda match: match.name == 'subtitleLanguage.prefix', 0)
            if prefix:
                ret.append((prefix, language))
        return ret

    def then(self, matches, when_response, context):
        for prefix, language in when_response:
            while prefix in matches:
                # make sure we remove all prefix as it can be in suffix list too.
                matches.remove(prefix)
            matches.remove(language)
            language.name = 'subtitleLanguage'
            matches.append(language)


class SubtitleSuffixLanguageRule(Rule):
    """
    Convert language guess as subtitleLanguage if next match is a subtitle language suffix
    """
    priority = -1

    def when(self, matches, context):
        ret = []
        for language in matches.named('language'):
            suffix = matches.next(language, lambda match: match.name == 'subtitleLanguage.suffix', 0)
            if suffix:
                ret.append((suffix, language))
        return ret

    def then(self, matches, when_response, context):
        for suffix, language in when_response:
            while suffix in matches:
                # make sure we remove all suffix as it can be in prefix list too.
                matches.remove(suffix)
            matches.remove(language)
            language.name = 'subtitleLanguage'
            matches.append(language)


LANGUAGE.string(*subtitle_prefixes, name="subtitleLanguage.prefix", ignore_case=True, private=True,
                validator=seps_surround)
LANGUAGE.string(*subtitle_suffixes, name="subtitleLanguage.suffix", ignore_case=True, private=True,
                validator=seps_surround)
LANGUAGE.functional(find_languages)
LANGUAGE.rules(SubtitlePrefixLanguageRule)
LANGUAGE.rules(SubtitleSuffixLanguageRule)
