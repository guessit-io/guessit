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

from guessit.test.guessittest import *
from guessit import quality


class TestQuality(TestGuessit):
    def test_screenSize(self):
        guess_720p = guessit.guess_file_info("2012.2009.720p.BluRay.x264.DTS WiKi.mkv", 'autodetect')
        guess_1080p = guessit.guess_file_info("2012.2009.1080p.BluRay.x264.DTS WiKi.mkv", 'autodetect')

        best_quality_guess = quality.best_quality(guess_720p, guess_1080p)

        self.assertTrue(guess_1080p == best_quality_guess, "1080p release is not the best quality")

suite = allTests(TestQuality)

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite)
