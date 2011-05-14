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

MAIN_LOGGING_LEVEL = logging.DEBUG


def currentPath():
    '''Returns the path in which the calling file is located.'''
    return dirname(join(os.getcwd(), sys._getframe(1).f_globals['__file__']))

def addImportPath(path):
    '''Function that adds the specified path to the import path. The path can be
    absolute or relative to the calling file.'''
    importPath = abspath(join(currentPath(), path))
    sys.path = [ importPath ] + sys.path

addImportPath('.')  # for the tests
addImportPath('..') # for import guessit


from guessit.slogging import setupLogging

setupLogging()
logging.getLogger().setLevel(MAIN_LOGGING_LEVEL)

log = logging.getLogger('GuessItTest')


import guessit
from guessit import *
from guessit.video import *
from guessit.movie import *
from guessit.episode import *
from guessit.matcher import *


def allTests(testClass):
    return TestLoader().loadTestsFromTestCase(testClass)


class TestGuessit(TestCase):

    def checkMinimumFieldsCorrect(self, guesser, filename):
        groundTruth = yaml.load(open(join(currentPath(), filename)).read())

        for filename, required in groundTruth.items():
            if isinstance(filename, str):
                filename = filename.decode('utf-8')

            log.debug('Checking guessed information for file: %s' % filename)

            found = guesser(filename)

            # props which are list of just 1 elem should be opened for easier writing of the tests
            for prop in ('language', 'subtitleLanguage'):
                value = found.get(prop, None)
                if isinstance(value, list) and len(value) == 1:
                    found[prop] = value[0]

            # compare all properties
            for prop, value in required.items():
                if prop not in found:
                    log.warning('Prop \'%s\' not found in: %s' % (prop, filename.encode('utf-8')))
                    continue

                if type(value) != type(found[prop]) and not (isinstance(value, basestring) and isinstance(found[prop], basestring)):
                    log.warning("Wrong prop value for '%s': expected = '%s' - received = '%s'" % (prop, value, found[prop]))

                elif isinstance(value, basestring):
                    if value.lower() != found[prop].lower():
                        log.warning("Wrong prop value for '%s': expected = '%s' - received = '%s'" % (prop, value, found[prop]))
                elif isinstance(value, list):
                    s1 = set(s.lower() for s in value)
                    s2 = set(s.lower() for s in found[prop])
                else:
                    if value != found[prop]:
                        log.warning("Wrong prop value for '%s': expected = '%s' - received = '%s'" % (prop, value, found[prop]))

            for prop, value in found.items():
                if prop not in required:
                    log.info("Found additional info for prop = '%s': '%s'" % (prop, value))
