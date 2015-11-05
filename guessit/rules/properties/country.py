#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Country
"""
# pylint: disable=no-member
from __future__ import unicode_literals

from rebulk import Rebulk

import babelfish

from ..common.words import COMMON_WORDS, iter_words


COUNTRIES_SYN = {'ES': ['españa'],
                 'GB': ['UK'],
                 'BR': ['brazilian', 'bra'],
                 # FIXME: this one is a bit of a stretch, not sure how to do it properly, though...
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

COUNTRY = Rebulk().defaults(name='country')


def is_valid_country(country, context=None):
    """
    Check if country is valid.
    """
    if context and context.get('allowed_countries'):
        allowed_countries = context.get('allowed_countries')
        return country.name.lower() in allowed_countries or country.alpha2.lower() in allowed_countries
    else:
        return country.name.lower() not in COMMON_WORDS and country.alpha2.lower() not in COMMON_WORDS


def find_countries(string, context=None):
    """
    Find countries in given string.
    """
    ret = []
    for word_match in iter_words(string.strip().lower()):
        try:
            country = babelfish.Country.fromguessit(word_match.group())
            if is_valid_country(country, context):
                ret.append((word_match.start(), word_match.end(), {'value': country}))
        except babelfish.Error:
            continue
    return ret


COUNTRY.functional(find_countries,
                   #  Prefer language and any other property over country if not US or GB.
                   conflict_solver=lambda match, other: match
                   if other.name != 'language' or match.value not in [babelfish.Country('US'), babelfish.Country('GB')]
                   else other)

