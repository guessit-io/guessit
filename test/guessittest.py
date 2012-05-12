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

from unittest import *

import yaml, logging, sys, os
from os.path import *

MAIN_LOGGING_LEVEL = logging.INFO


def currentPath():
    '''Returns the path in which the calling file is located.'''
    return dirname(join(os.getcwd(), sys._getframe(1).f_globals['__file__']))

def addImportPath(path):
    '''Function that adds the specified path to the import path. The path can be
    absolute or relative to the calling file.'''
    importPath = abspath(join(currentPath(), path))
    sys.path = [ importPath ] + sys.path

# do not add those because it messes with the dirs when testing the pypi sdist
#addImportPath('.')  # for the tests
#addImportPath('..') # for import guessit


from guessit.slogging import setupLogging

setupLogging()
logging.getLogger().setLevel(MAIN_LOGGING_LEVEL)

log = logging.getLogger(__name__)


import guessit
from guessit import *
from guessit.matcher import *
from guessit.textutils import to_utf8
from guessit.fileutils import *

def allTests(testClass):
    return TestLoader().loadTestsFromTestCase(testClass)


class TestGuessit(TestCase):

    def checkMinimumFieldsCorrect(self, guesser, filename, removeType = True):
        groundTruth = yaml.load(open(join(currentPath(), filename)).read())

        for filename, required in groundTruth.items():
            if isinstance(filename, str):
                filename = filename.decode('utf-8')

            log.debug('\n' + '-' * 120)
            log.info('Guessing information for file: %s' % to_utf8(filename))

            found = guesser(filename)

            # no need for this in the unittests
            if removeType:
                del found['type']
            for prop in ('container', 'mimetype'):
                if prop in found:
                    del found[prop]

            # props which are list of just 1 elem should be opened for easier writing of the tests
            for prop in ('language', 'subtitleLanguage', 'other'):
                value = found.get(prop, None)
                if isinstance(value, list) and len(value) == 1:
                    found[prop] = value[0]

            # compare all properties
            for prop, value in required.items():
                if prop not in found:
                    log.warning('Prop \'%s\' not found in: %s' % (prop, to_utf8(filename)))
                    continue

                #if type(value) != type(found[prop]) and not (isinstance(value, basestring) and isinstance(found[prop], basestring)):
                #    log.warning("Wrong prop types for '%s': expected = '%s' - received = '%s'" % (prop, to_utf8(value), found[prop]))

                if isinstance(value, basestring) and isinstance(found[prop], basestring):
                    if value.lower() != found[prop].lower():
                        log.warning("Wrong prop value str for '%s': expected = '%s' - received = '%s'" % (prop, to_utf8(value), to_utf8(found[prop])))
                elif isinstance(value, list) and isinstance(found[prop], list):
                    s1 = set(str(s).lower() for s in value)
                    s2 = set(str(s).lower() for s in found[prop])
                    if s1 != s2:
                        log.warning("Wrong prop value list for '%s': expected = '%s' - received = '%s'" % (prop, to_utf8(value), to_utf8(found[prop])))
                else:
                    if found[prop] != value:
                        log.warning("Wrong prop value for '%s': expected = '%s' - received = '%s'" % (prop, to_utf8(value), to_utf8(found[prop])))

            for prop, value in found.items():
                if prop not in required:
                    log.warning("Found additional info for prop = '%s': '%s'" % (prop, to_utf8(value)))
