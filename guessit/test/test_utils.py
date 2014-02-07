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
from guessit.fileutils import split_path
from guessit.textutils import strip_brackets, str_replace, str_fill
from guessit import PY2


class TestUtils(TestGuessit):
    def test_splitpath(self):
        alltests = {('linux2', 'darwin'): {'/usr/bin/smewt': ['/', 'usr', 'bin', 'smewt'],
                                           'relative_path/to/my_folder/': ['relative_path', 'to', 'my_folder'],
                                           '//some/path': ['//', 'some', 'path'],
                                           '//some//path': ['//', 'some', 'path'],
                                           '///some////path': ['///', 'some', 'path']

                                             },
                     ('win32',): {'C:\\Program Files\\Smewt\\smewt.exe': ['C:\\', 'Program Files', 'Smewt', 'smewt.exe'],
                                  'Documents and Settings\\User\\config': ['Documents and Settings', 'User', 'config'],
                                  'C:\\Documents and Settings\\User\\config': ['C:\\', 'Documents and Settings', 'User', 'config'],
                                  # http://bugs.python.org/issue19945
                                  '\\\\netdrive\\share': ['\\\\', 'netdrive', 'share'] if PY2 else ['\\\\netdrive\\share'],
                                  '\\\\netdrive\\share\\folder': ['\\\\', 'netdrive', 'share', 'folder'] if PY2 else ['\\\\netdrive\\share\\', 'folder'],
                                  }
                     }
        for platforms, tests in alltests.items():
            if sys.platform in platforms:
                for path, split in tests.items():
                    self.assertEqual(split, split_path(path))

    def test_strip_brackets(self):
        allTests = (
                    ('[test]', 'test'),
                    ('{test2}', 'test2'),
                    ('(test3)', 'test3'),
                    ('(test4]', '(test4]'),
                    )

        for i, e in allTests:
            self.assertEqual(e, strip_brackets(i))

    def test_str_utils(self):
        self.assertEqual("Hello world", str_replace("Hello World", 6, 'w'))
        self.assertEqual("Hello *****", str_fill("Hello World", (6, 11), '*'))


suite = allTests(TestUtils)

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite)
