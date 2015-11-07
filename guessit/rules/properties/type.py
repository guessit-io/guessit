#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
type property
"""
from __future__ import unicode_literals

from rebulk.match import Match


def _type(matches, value):
    """
    Define type match with given value.
    :param matches:
    :param value:
    :return:
    """
    matches.append(Match(len(matches.input_string), len(matches.input_string), name='type', value=value))


def type_processor(matches):
    """
    Post processor to find file type based on all others found matches.
    :param matches:
    :return:
    """
    episode = matches.named('episode')
    season = matches.named('season')
    episode_details = matches.named('episode_details')

    if episode or season or episode_details:
        _type(matches, 'episode')
        return

    film = matches.named('film')
    if film:
        _type(matches, 'movie')
        return

    year = matches.named('year')
    date = matches.named('date')

    if date and not year:
        _type(matches, 'episode')
        return

    bonus = matches.named('bonus')
    if bonus and not year:
        _type(matches, 'episode')
        return

    crc32 = matches.named('crc32')
    anime_release_group = matches.named('release_group', lambda match: 'anime' in match.tags)
    if crc32 and anime_release_group:
        _type(matches, 'episode')
        return

    _type(matches, 'movie')
