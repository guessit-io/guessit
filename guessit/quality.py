#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Rémi Alvergnat <toilal.dev@gmail.com>
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

from guessit.plugins.transformers import all_transformers


class QualitiesContainer():
    def __init__(self):
        self._qualities = {}

    def register_quality(self, name, canonical_form, rating):
        """Register a quality rating.

        :param name: Name of the property
        :type name: string
        :param canonical_form: Value of the property
        :type canonical_form: string
        :param rating: Estimated quality rating for the property
        :type rating: int
        """
        property_qualities = self._qualities.get(name)

        if property_qualities is None:
            property_qualities = {}
            self._qualities[name] = property_qualities

        property_qualities[canonical_form] = rating

    def unregister_quality(self, name, *canonical_forms):
        """Unregister quality ratings for given property name.

        If canonical_forms are specified, only those values will be unregistered

        :param name: Name of the property
        :type name: string
        :param canonical_forms: Value of the property
        :type canonical_forms: string
        """
        if not canonical_forms:
            if name in self._qualities:
                del self._qualities[name]
        else:
            property_qualities = self._qualities.get(name)
            if not property_qualities is None:
                for property_canonical_form in canonical_forms:
                    if property_canonical_form in property_qualities:
                        del property_qualities[property_canonical_form]
            if not property_qualities:
                del self._qualities[name]

    def clear_qualities(self,):
        """Unregister all defined quality ratings.
        """
        self._qualities.clear()

    def rate_quality(self, guess, *props):
        """Rate the quality of guess.

        :param guess: Guess to rate
        :type guess: :class:`guessit.guess.Guess`
        :param props: Properties to include in the rating. if empty, rating will be performed for all guess properties.
        :type props: varargs of string

        :return: Quality of the guess. The higher, the better.
        :rtype: int
        """
        rate = 0
        if not props:
            props = guess.keys()
        for prop in props:
            prop_value = guess.get(prop)
            prop_qualities = self._qualities.get(prop)
            if not prop_value is None and not prop_qualities is None:
                rate += prop_qualities.get(prop_value, 0)
        return rate

    def best_quality_properties(self, props, *guesses):
        """Retrieve the best quality guess, based on given properties

        :param props: Properties to include in the rating
        :type props: list of strings
        :param guesses: Guesses to rate
        :type guesses: :class:`guessit.guess.Guess`

        :return: Best quality guess from all passed guesses
        :rtype: :class:`guessit.guess.Guess`
        """
        best_guess = None
        best_rate = None
        for guess in guesses:
            rate = self.rate_quality(guess, *props)
            if best_rate is None or best_rate < rate:
                best_rate = rate
                best_guess = guess
        return best_guess

    def best_quality(self, *guesses):
        """Retrieve the best quality guess.

        :param guesses: Guesses to rate
        :type guesses: :class:`guessit.guess.Guess`

        :return: Best quality guess from all passed guesses
        :rtype: :class:`guessit.guess.Guess`
        """
        best_guess = None
        best_rate = None
        for guess in guesses:
            rate = self.rate_quality(guess)
            if best_rate is None or best_rate < rate:
                best_rate = rate
                best_guess = guess
        return best_guess


def best_quality_properties(props, *guesses):
    """Retrieve the best quality guess, based on given properties

    :param props: Properties to include in the rating
    :type props: list of strings
    :param guesses: Guesses to rate
    :type guesses: :class:`guessit.guess.Guess`

    :return: Best quality guess from all passed guesses
    :rtype: :class:`guessit.guess.Guess`
    """
    best_guess = None
    best_rate = None
    for guess in guesses:
        for transformer in all_transformers():
            rate = transformer.rate_quality(guess, *props)
            if best_rate is None or best_rate < rate:
                best_rate = rate
                best_guess = guess
    return best_guess


def best_quality(*guesses):
    """Retrieve the best quality guess.

    :param guesses: Guesses to rate
    :type guesses: :class:`guessit.guess.Guess`

    :return: Best quality guess from all passed guesses
    :rtype: :class:`guessit.guess.Guess`
    """
    best_guess = None
    best_rate = None
    for guess in guesses:
        for transformer in all_transformers():
            rate = transformer.rate_quality(guess)
            if best_rate is None or best_rate < rate:
                best_rate = rate
                best_guess = guess
    return best_guess
