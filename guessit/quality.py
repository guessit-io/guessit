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

_qualities = {}


def rate_quality(guess, *props):
    """
    Rate the quality of a guess.

    @param guess: Guess object to rate
    @param props: properties to include in the rating.
                 if empty, rating will be performed for all guess properties.

    @return: int value representing the quality of the guess. The higher, the better.
    """
    rate = 0
    if not props:
        props = guess.keys()
    for prop in props:
        prop_value = guess.get(prop)
        prop_qualities = _qualities.get(prop)
        if not prop_value is None and not prop_qualities is None:
            rate += prop_qualities.get(prop_value, 0)
    return rate


def best_quality_properties(props, *guesses):
    """
    Retrieves the best quality guess from all passed guesses, based on given properties

    @param props: list of properties to include in the rating
    @param guesses: guesses to rate

    @return: best quality guess from all passed guesses
    """
    best_guess = None
    best_rate = None
    for guess in guesses:
        rate = rate_quality(guess, *props)
        if best_rate is None or best_rate < rate:
            best_rate = rate
            best_guess = guess
    return best_guess


def best_quality(*guesses):
    """
    Retrieves the best quality guess from all passed guesses

    @param guesses: guesses to rate

    @return: best quality guess from all passed guesses
    """
    best_guess = None
    best_rate = None
    for guess in guesses:
        rate = rate_quality(guess)
        if best_rate is None or best_rate < rate:
            best_rate = rate
            best_guess = guess
    return best_guess


def register_quality(property_name, property_canonical_form, rating):
    """
    Register a quality rating for given property name and canonical_form

    @param property_name: name of the property
    @param property_canonical_form: canonical form of the property
    @param rating: estimated quality rating for the property
    """
    property_qualities = _qualities.get(property_name)

    if property_qualities is None:
        property_qualities = {}
        _qualities[property_name] = property_qualities

    property_qualities[property_canonical_form] = rating


def unregister_quality(property_name, *property_canonical_forms):
    """
    Unregister quality ratings for given property name.

    If property_canonical_forms are specified, only those values will be unregistered

    @param property_name: name of the property
    @param property_canonical_form: canonical form of the property
    """
    if not property_canonical_forms:
        if property_name in _qualities:
            del _qualities[property_name]
    else:
        property_qualities = _qualities.get(property_name)
        if not property_qualities is None:
            for property_canonical_form in property_canonical_forms:
                if property_canonical_form in property_qualities:
                    del property_qualities[property_canonical_form]
        if not property_qualities:
            del _qualities[property_name]


def clear_qualities():
    """
    Unregister all defined quality ratings
    """
    _qualities.clear()


register_quality('screenSize', '360p', -300)
register_quality('screenSize', '368p', -200)
register_quality('screenSize', '480p', -100)
register_quality('screenSize', '576p', 0)
register_quality('screenSize', '720p', 100)
register_quality('screenSize', '1080i', 180)
register_quality('screenSize', '1080p', 200)
register_quality('screenSize', '4K', 400)
