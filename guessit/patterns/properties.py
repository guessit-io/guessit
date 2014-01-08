#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
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

from .containers import PropertiesContainer
from guessit.patterns import build_or_pattern
from guessit.quality import register_quality

container = PropertiesContainer()

# http://en.wikipedia.org/wiki/Pirated_movie_release_types
container.register_property('format', 'VHS', 'VHS')
container.register_property('format', 'Cam', 'CAM', 'CAMRip')
container.register_property('format', 'Telesync', 'TELESYNC', 'PDVD')
container.register_property('format', 'Telesync', 'TS', confidence=0.2)
container.register_property('format', 'Workprint', 'WORKPRINT', 'WP')
container.register_property('format', 'Telecine', 'TELECINE', 'TC')
container.register_property('format', 'Pay-Per-View', 'PPV', 'PPV-Rip')
container.register_property('format', 'DVD', 'DVD', 'DVD-Rip', 'VIDEO-TS')
container.register_property('format', 'DVB', 'DVB-Rip', 'DVB', 'PD-TV')
container.register_property('format', 'HDTV', 'HD-TV')
container.register_property('format', 'VOD', 'VOD', 'VOD-Rip')
container.register_property('format', 'WEBRip', 'WEB-Rip')
container.register_property('format', 'WEB-DL', 'WEB-DL')
container.register_property('format', 'HD-DVD', 'HD-(?:DVD)?-Rip', 'HD-DVD')
container.register_property('format', 'BluRay', 'Blu-ray', 'B[DR]', 'B[DR]-Rip', 'BD[59]', 'BD25', 'BD50')

register_quality('format', 'VHS', -100)
register_quality('format', 'Cam', -90)
register_quality('format', 'Telesync', -80)
register_quality('format', 'Workprint', -70)
register_quality('format', 'Telecine', -60)
register_quality('format', 'Pay-Per-View', -50)
register_quality('format', 'DVB', -20)
register_quality('format', 'DVD', 0)
register_quality('format', 'HDTV', 20)
register_quality('format', 'VOD', 40)
register_quality('format', 'WEBRip', 50)
register_quality('format', 'WEB-DL', 60)
register_quality('format', 'HD-DVD', 80)
register_quality('format', 'BluRay', 100)

container.register_property('screenSize', '360p', '(?:\d{3,}(?:\\|\/|x|\*))?360(?:i|p?x?)')
container.register_property('screenSize', '368p', '(?:\d{3,}(?:\\|\/|x|\*))?368(?:i|p?x?)')
container.register_property('screenSize', '480p', '(?:\d{3,}(?:\\|\/|x|\*))?480(?:i|p?x?)')
container.register_property('screenSize', '576p', '(?:\d{3,}(?:\\|\/|x|\*))?576(?:i|p?x?)')
container.register_property('screenSize', '720p', '(?:\d{3,}(?:\\|\/|x|\*))?720(?:i|p?x?)')
container.register_property('screenSize', '1080i', '(?:\d{3,}(?:\\|\/|x|\*))?1080i(?:i|p?x?)')
container.register_property('screenSize', '1080p', '(?:\d{3,}(?:\\|\/|x|\*))?1080(?:i|p?x?)')
container.register_property('screenSize', '4K', '(?:\d{3,}(?:\\|\/|x|\*))?2160(?:i|p?x?)')

register_quality('screenSize', '360p', -300)
register_quality('screenSize', '368p', -200)
register_quality('screenSize', '480p', -100)
register_quality('screenSize', '576p', 0)
register_quality('screenSize', '720p', 100)
register_quality('screenSize', '1080i', 180)
register_quality('screenSize', '1080p', 200)
register_quality('screenSize', '4K', 400)

profile_pattern = build_or_pattern(["BS", "EP", "MP", "HP", "AVC"])

container.register_property('videoCodec', 'XviD', 'XviD', 'XviD-' + profile_pattern)
container.register_property('videoCodec', 'DivX', 'DVDivX', 'DivX', 'DivX-' + profile_pattern)
container.register_property('videoCodec', 'h264', '[hx]-264', '[hx]-264-' + profile_pattern)
container.register_property('videoCodec', '10bit', '(?:[hx]-264)?-10.?bit', '(?:[hx]-264)?-hi10p')

container.register_property('videoCodec', 'Real', 'Rv\d{2}') # http://en.wikipedia.org/wiki/RealVideo
container.register_property('videoCodec', 'Mpeg2', 'Mpeg2')

# has nothing to do here (or on filenames for that matter), but some
# releases use it and it helps to identify release groups, so we adapt
container.register_property('videoApi', 'DXVA', 'DXVA')

container.register_property('audioCodec', 'MP3', 'MP3')
container.register_property('audioCodec', 'DolbyDigital', 'DD')
container.register_property('audioCodec', 'AAC', 'HE-AAC', 'AAC-HE', 'LC-AAC', 'AAC-LC', 'AAC')
container.register_property('audioCodec', 'AC3', 'AC3')
container.register_property('audioCodec', 'Flac', 'FLAC')
container.register_property('audioCodec', 'DTS', 'DTS')
container.register_property('audioCodec', 'DTS-HD', 'DTS-HD')
container.register_property('audioCodec', 'TrueHD', 'True-HD')
container.register_property('audioCodec', 'DTS-HDMA', 'DTS-HD-MA')

register_quality('audioCodec', 'MP3', 10)
register_quality('audioCodec', 'DolbyDigital', 30)
register_quality('audioCodec', 'AAC', 35)
register_quality('audioCodec', 'AC3', 40)
register_quality('audioCodec', 'Flac', 45)
register_quality('audioCodec', 'DTS', 100)
register_quality('audioCodec', 'DTS-HD', 150)
register_quality('audioCodec', 'TrueHD', 150)
register_quality('audioCodec', 'DTS-HDMA', 200)

container.register_property('audioChannels', '7.1', '7[\W_]1', '7ch')
container.register_property('audioChannels', '5.1', '5[\W_]1', '5ch')
container.register_property('audioChannels', '2.0', '2[\W_]0', '2ch', 'stereo')
container.register_property('audioChannels', '1.0', '1[\W_]0', '1ch', 'mono')

register_quality('audioChannels', '1.0', -100)
register_quality('audioChannels', '2.0', 0)
register_quality('audioChannels', '5.1', 100)
register_quality('audioChannels', '7.1', 200)

container.register_property('episodeFormat', 'Minisode', r'Minisodes?')

container.register_property('other', 'AudioFix', 'Audio-Fix', 'Audio-Fixed')
container.register_property('other', 'SyncFix', 'Sync-Fix', 'Sync-Fixed')
container.register_property('other', 'DualAudio', 'Dual-Audio')

container.register_properties('other', 'Proper', 'Repack', 'Dual-Audio', 'R5', 'Screener', '3D', 'Fix', 'HD', 'HQ', 'DDC')
container.register_property('other', 'WideScreen', 'ws', 'wide-screen')
container.register_properties('other', 'Limited', 'Complete', 'Classic', 'Final', 'Unrated', weak=True)

for prop in container.get_properties('format'):
    container.register_property('other', 'Screener', prop.pattern + '(-?Scr(?:eener)?)')
