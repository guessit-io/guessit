#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2014 Nicolas Wack <wackou@gmail.com>
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
from guessit.fileutils import split_path, file_in_same_dir
from guessit.textutils import strip_brackets, str_replace, str_fill
from guessit import PY2
from guessit import __main__


class TestMain(TestGuessit):
    def test_list_properties(self):
        __main__.main(["-p"])
        __main__.main(["-l"])

    def test_list_transformers(self):
        __main__.main(["--transformers"])
        __main__.main(["-l", "--transformers"])

    def test_demo(self):
        __main__.main(["-d"])
        __main__.main(["-l"])

    def test_filename(self):
        __main__.main(["A.Movie.2014.avi"])
        __main__.main(["A.Movie.2014.avi", "A.2nd.Movie.2014.avi"])
        __main__.main(["-y", "A.Movie.2014.avi"])
        __main__.main(["-a", "A.Movie.2014.avi"])
        __main__.main(["-v", "A.Movie.2014.avi"])
        __main__.main(["-t", "movie", "A.Movie.2014.avi"])
        __main__.main(["-t", "episode", "A.Serie.S02E06.avi"])
        __main__.main(["-i", "hash_mpc", file_in_same_dir(__file__, "1MB")])
        __main__.main(["-i", "hash_md5", file_in_same_dir(__file__, "1MB")])

suite = allTests(TestMain)

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite)
