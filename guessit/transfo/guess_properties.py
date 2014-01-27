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

from guessit.plugins import Transformer
from guessit.patterns.containers import PropertiesContainer
from guessit.quality import QualitiesContainer
from guessit.transfo import SingleNodeGuesser


class GuessProperties(Transformer):
    def __init__(self):
        Transformer.__init__(self, 35)

        self.container = PropertiesContainer()
        self.qualities = QualitiesContainer()

        # http://en.wikipedia.org/wiki/Pirated_movie_release_types
        self.container.register_property('format', 'VHS', 'VHS')
        self.container.register_property('format', 'Cam', 'CAM', 'CAMRip')
        self.container.register_property('format', 'Telesync', 'TELESYNC', 'PDVD')
        self.container.register_property('format', 'Telesync', 'TS', confidence=0.2)
        self.container.register_property('format', 'Workprint', 'WORKPRINT', 'WP')
        self.container.register_property('format', 'Telecine', 'TELECINE', 'TC')
        self.container.register_property('format', 'PPV', 'PPV', 'PPV-Rip')  # Pay Per View
        self.container.register_property('format', 'DVD', 'DVD', 'DVD-Rip', 'VIDEO-TS')
        self.container.register_property('format', 'DVB', 'DVB-Rip', 'DVB', 'PD-TV')
        self.container.register_property('format', 'HDTV', 'HD-TV')
        self.container.register_property('format', 'VOD', 'VOD', 'VOD-Rip')
        self.container.register_property('format', 'WEBRip', 'WEB-Rip')
        self.container.register_property('format', 'WEB-DL', 'WEB-DL')
        self.container.register_property('format', 'HD-DVD', 'HD-(?:DVD)?-Rip', 'HD-DVD')
        self.container.register_property('format', 'BluRay', 'Blu-ray', 'B[DR]', 'B[DR]-Rip', 'BD[59]', 'BD25', 'BD50')

        self.qualities.register_quality('format', 'VHS', -100)
        self.qualities.register_quality('format', 'Cam', -90)
        self.qualities.register_quality('format', 'Telesync', -80)
        self.qualities.register_quality('format', 'Workprint', -70)
        self.qualities.register_quality('format', 'Telecine', -60)
        self.qualities.register_quality('format', 'Pay-Per-View', -50)
        self.qualities.register_quality('format', 'DVB', -20)
        self.qualities.register_quality('format', 'DVD', 0)
        self.qualities.register_quality('format', 'HDTV', 20)
        self.qualities.register_quality('format', 'VOD', 40)
        self.qualities.register_quality('format', 'WEBRip', 50)
        self.qualities.register_quality('format', 'WEB-DL', 60)
        self.qualities.register_quality('format', 'HD-DVD', 80)
        self.qualities.register_quality('format', 'BluRay', 100)

        self.container.register_property('screenSize', '360p', '(?:\d{3,}(?:\\|\/|x|\*))?360(?:i|p?x?)')
        self.container.register_property('screenSize', '368p', '(?:\d{3,}(?:\\|\/|x|\*))?368(?:i|p?x?)')
        self.container.register_property('screenSize', '480p', '(?:\d{3,}(?:\\|\/|x|\*))?480(?:i|p?x?)')
        self.container.register_property('screenSize', '480p', 'hr', confidence=0.2)
        self.container.register_property('screenSize', '576p', '(?:\d{3,}(?:\\|\/|x|\*))?576(?:i|p?x?)')
        self.container.register_property('screenSize', '720p', '(?:\d{3,}(?:\\|\/|x|\*))?720(?:i|p?x?)')
        self.container.register_property('screenSize', '900p', '(?:\d{3,}(?:\\|\/|x|\*))?900(?:i|p?x?)')
        self.container.register_property('screenSize', '1080i', '(?:\d{3,}(?:\\|\/|x|\*))?1080i(?:i|p?x?)')
        self.container.register_property('screenSize', '1080p', '(?:\d{3,}(?:\\|\/|x|\*))?1080(?:i|p?x?)')
        self.container.register_property('screenSize', '4K', '(?:\d{3,}(?:\\|\/|x|\*))?2160(?:i|p?x?)')

        self.qualities.register_quality('screenSize', '360p', -300)
        self.qualities.register_quality('screenSize', '368p', -200)
        self.qualities.register_quality('screenSize', '480p', -100)
        self.qualities.register_quality('screenSize', '576p', 0)
        self.qualities.register_quality('screenSize', '720p', 100)
        self.qualities.register_quality('screenSize', '900p', 130)
        self.qualities.register_quality('screenSize', '1080i', 180)
        self.qualities.register_quality('screenSize', '1080p', 200)
        self.qualities.register_quality('screenSize', '4K', 400)

        # http://blog.mediacoderhq.com/h264-profiles-and-levels/
        _videoProfiles = {'BS':('BS',),
                     'EP':('EP', 'XP'),
                     'MP':('MP',),
                     'HP':('HP', 'HiP'),
                     '10bit':('10.?bit', 'Hi10P'),
                     'Hi422P':('Hi422P',),
                     'Hi444PP':('Hi444PP'),
                     }

        self.container.register_property('videoCodec', 'Real', 'Rv\d{2}')  # http://en.wikipedia.org/wiki/RealVideo
        self.container.register_property('videoCodec', 'Mpeg2', 'Mpeg2')
        self.container.register_property('videoCodec', 'DivX', 'DVDivX', 'DivX')
        self.container.register_property('videoCodec', 'XviD', 'XviD')
        self.container.register_property('videoCodec', 'h264', '[hx]-264(?:-AVC)?', 'MPEG-4(?:-AVC)')
        self.container.register_property('videoCodec', 'h265', '[hx]-265(?:-HEVC)?', 'HEVC')

        for profile, profile_regexps in _videoProfiles.items():
            for profile_regexp in profile_regexps:
                # container.register_property('videoProfile', profile, profile_regexp)
                for prop in self.container.get_properties('videoCodec'):
                    self.container.register_property('videoProfile', profile, prop.pattern + '(-' + profile_regexp + ')')
                    self.container.register_property('videoProfile', profile, '(' + profile_regexp + '-)' + prop.pattern)

        self.qualities.register_quality('videoCodec', 'Real', -50)
        self.qualities.register_quality('videoCodec', 'Mpeg2', -30)
        self.qualities.register_quality('videoCodec', 'DivX', -10)
        self.qualities.register_quality('videoCodec', 'XviD', 0)
        self.qualities.register_quality('videoCodec', 'h264', 100)
        self.qualities.register_quality('videoCodec', 'h265', 150)

        self.qualities.register_quality('videoProfile', 'BS', -20)
        self.qualities.register_quality('videoProfile', 'EP', -10)
        self.qualities.register_quality('videoProfile', 'MP', 0)
        self.qualities.register_quality('videoProfile', 'HP', 10)
        self.qualities.register_quality('videoProfile', '10bit', 15)
        self.qualities.register_quality('videoProfile', 'Hi422P', 25)
        self.qualities.register_quality('videoProfile', 'Hi444PP', 35)

        # has nothing to do here (or on filenames for that matter), but some
        # releases use it and it helps to identify release groups, so we adapt
        self.container.register_property('videoApi', 'DXVA', 'DXVA')

        self.container.register_property('audioCodec', 'MP3', 'MP3')
        self.container.register_property('audioCodec', 'DolbyDigital', 'DD')
        self.container.register_property('audioCodec', 'AAC', 'AAC')
        self.container.register_property('audioCodec', 'AC3', 'AC3')
        self.container.register_property('audioCodec', 'Flac', 'FLAC')
        self.container.register_property('audioCodec', 'DTS', 'DTS')
        self.container.register_property('audioCodec', 'TrueHD', 'True-HD')

        _audioProfiles = {'DTS': {'HD': ('HD',),
                                  'HDMA': ('HD-MA',),
                                  },
                            'AAC': {'HE': ('HE',),
                                    'LC': ('LC',),
                                    },
                             'AC3': {'HQ': ('HQ',),
                                    }
                           }

        for audioCodec, codecProfiles in _audioProfiles.items():
            for profile, profile_regexps in codecProfiles.items():
                for profile_regexp in profile_regexps:
                    for prop in self.container.get_properties('audioCodec', audioCodec):
                        self.container.register_property('audioProfile', profile, prop.pattern + '(-' + profile_regexp + ')')
                        self.container.register_property('audioProfile', profile, '(' + profile_regexp + '-)' + prop.pattern)

        self.qualities.register_quality('audioCodec', 'MP3', 10)
        self.qualities.register_quality('audioCodec', 'DolbyDigital', 30)
        self.qualities.register_quality('audioCodec', 'AAC', 35)
        self.qualities.register_quality('audioCodec', 'AC3', 40)
        self.qualities.register_quality('audioCodec', 'Flac', 45)
        self.qualities.register_quality('audioCodec', 'DTS', 100)
        self.qualities.register_quality('audioCodec', 'TrueHD', 120)

        self.qualities.register_quality('audioProfile', 'HD', 20)
        self.qualities.register_quality('audioProfile', 'HDMA', 50)
        self.qualities.register_quality('audioProfile', 'LC', 0)
        self.qualities.register_quality('audioProfile', 'HQ', 0)
        self.qualities.register_quality('audioProfile', 'HE', 20)

        self.container.register_property('audioChannels', '7.1', '7[\W_]1', '7ch')
        self.container.register_property('audioChannels', '5.1', '5[\W_]1', '5ch')
        self.container.register_property('audioChannels', '2.0', '2[\W_]0', '2ch', 'stereo')
        self.container.register_property('audioChannels', '1.0', '1[\W_]0', '1ch', 'mono')

        self.qualities.register_quality('audioChannels', '1.0', -100)
        self.qualities.register_quality('audioChannels', '2.0', 0)
        self.qualities.register_quality('audioChannels', '5.1', 100)
        self.qualities.register_quality('audioChannels', '7.1', 200)

        self.container.register_property('episodeFormat', 'Minisode', r'Minisodes?')

        self.container.register_property('other', 'AudioFix', 'Audio-Fix', 'Audio-Fixed')
        self.container.register_property('other', 'SyncFix', 'Sync-Fix', 'Sync-Fixed')
        self.container.register_property('other', 'DualAudio', 'Dual-Audio')

        self.container.register_properties('other', 'Proper', 'Repack', 'R5', 'Screener', '3D', 'Fix', 'HD', 'HQ', 'DDC')
        self.container.register_property('other', 'WideScreen', 'ws', 'wide-screen')
        self.container.register_properties('other', 'Limited', 'Complete', 'Classic', 'Final', 'Unrated', 'LiNE', weak=True)

        for prop in self.container.get_properties('format'):
            self.container.register_property('other', 'Screener', prop.pattern + '(-?Scr(?:eener)?)')

    def guess_properties(self, string):
        found = self.container.find_properties(string)
        return self.container.as_guess(found, string)

    def supported_properties(self):
        return self.container.get_supported_properties()

    def process(self, mtree):
        SingleNodeGuesser(self.guess_properties, 1.0, self.log).process(mtree)

    def rate_quality(self, guess, *props):
        return self.qualities.rate_quality(guess)
