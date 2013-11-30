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

from __future__ import unicode_literals

from containers import PropertiesContainer

container = PropertiesContainer()

container.register_property('format', 'DVD', 'DVD', 'DVD-Rip', 'VIDEO-TS', 'DVDivX')
container.register_property('format', 'HD-DVD', 'HD-(?:DVD)?-Rip', 'HD-DVD')
container.register_property('format', 'BluRay', 'Blu-ray', 'B[DR]Rip')
container.register_property('format', 'HDTV', 'HD-TV')
container.register_property('format', 'DVB', 'DVB-Rip', 'DVB', 'PD-TV')
container.register_property('format', 'WEBRip', 'WEB-Rip')
container.register_property('format', 'VHS', 'VHS')
container.register_property('format', 'WEB-DL', 'WEB-DL')

container.register_property('screenSize', '360p', '(?:\d{3,}(?:\\|\/|x|\*))?360(?:i|p?x?)')
container.register_property('screenSize', '368p', '(?:\d{3,}(?:\\|\/|x|\*))?368(?:i|p?x?)')
container.register_property('screenSize', '480p', '(?:\d{3,}(?:\\|\/|x|\*))?480(?:i|p?x?)')
container.register_property('screenSize', '576p', '(?:\d{3,}(?:\\|\/|x|\*))?576(?:i|p?x?)')
container.register_property('screenSize', '720p', '(?:\d{3,}(?:\\|\/|x|\*))?720(?:i|p?x?)')
container.register_property('screenSize', '1080i', '(?:\d{3,}(?:\\|\/|x|\*))?1080i(?:i|p?x?)')
container.register_property('screenSize', '1080p', '(?:\d{3,}(?:\\|\/|x|\*))?1080(?:i|p?x?)')
container.register_property('screenSize', '4K', '(?:\d{3,}(?:\\|\/|x|\*))?2160(?:i|p?x?)')

container.register_property('videoCodec', 'XviD', 'Xvid')
container.register_property('videoCodec', 'DivX', 'DVDivX', 'DivX')
container.register_property('videoCodec', 'h264', '[hx]-264')
container.register_property('videoCodec', 'Rv10', 'Rv10')
container.register_property('videoCodec', 'Mpeg2', 'Mpeg2')

# has nothing to do here (or on filenames for that matter), but some
# releases use it and it helps to identify release groups, so we adapt
container.register_property('videoApi', 'DXVA', 'DXVA')

container.register_property('audioCodec', 'AC3', 'AC3')
container.register_property('audioCodec', 'DTS', 'DTS')
container.register_property('audioCodec', 'AAC', 'He-AAC', 'AAC-He', 'AAC')

container.register_property('audioChannels', '5.1', r'5\.1', 'DD5[._ ]1', '5ch')

container.register_property('episodeFormat', 'Minisode', r'Minisodes?')

container.register_properties('releaseGroup', 'ESiR', 'WAF', 'SEPTiC', 'iNT', 'PUKKA',
                                  'CHD', 'ViTE', 'TLF', 'FLAiTE',
                                  'MDX', 'GM4F', 'DVL', 'SVD', 'iLUMiNADOS',
                                  'aXXo', 'KLAXXON', 'NoTV', 'ZeaL', 'LOL',
                                  'CtrlHD', 'POD', 'WiKi', 'IMMERSE', 'FQM',
                                  '2HD', 'CTU', 'HALCYON', 'EbP', 'SiTV',
                                  'HDBRiSe', 'AlFleNi-TeaM', 'EVOLVE', '0TV',
                                  'TLA', 'NTB', 'ASAP', 'MOMENTUM', 'FoV', 'D-Z0N3',
                                  'TrollHD', 'ECI', 'MARINE-FORD'
                                  )
container.register_property('releaseGroup', r'[XCT]', r'\[XCT\]')

container.register_properties('weakReleaseGroup', 'DEiTY', 'FiNaLe', 'UnSeeN', 'KiNGS', 'CLUE', 'DIMENSION',
                                      'SAiNTS', 'ARROW', 'EuReKA', 'SiNNERS', 'DiRTY', 'REWARD',
                                      'REPTiLE',
                                      )

container.register_property('other', 'AudioFix', 'Audio-Fix', 'Audio-Fixed')
container.register_property('other', 'SyncFix', 'Sync-Fix', 'Sync-Fixed')
container.register_property('other', 'DualAudio', 'Dual-Audio')

container.register_properties('other', 'Proper', 'Repack', 'Dual-Audio', 'R5', 'Screener', '3D', 'Fix',
                           'Limited', 'Complete', 'Classic', 'Final',  # not so sure about these ones, could appear in a title
                           )

container.register_property('other', 'WideScreen', 'ws', 'wide-screen')

for prop in container.get_properties('format'):
    container.register_property('other', 'Screener', prop.pattern + '(-?Scr(?:eener)?)')
