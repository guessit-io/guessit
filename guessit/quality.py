#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2011 Nicolas Wack <wackou@gmail.com>
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

qualities = {
                       'screenSize': { '360p': -300,
                                   '368p': -200,
                                   '480p': -100,
                                   '576p': 0,
                                   '720p': 100,
                                   '1080i': 180,
                                   '1080p': 200,
                                   '4K': 400
                                   }
                      }


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
        prop_qualities = qualities.get(prop)
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
