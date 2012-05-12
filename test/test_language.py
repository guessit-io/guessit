#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2012 Nicolas Wack <wackou@gmail.com>
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


from guessittest import *

class TestLanguage(TestGuessit):

    def check_languages(self, languages, scheme=None):
        for lang1, lang2 in languages.items():
            self.assertEqual(Language(lang1, scheme=scheme),
                             Language(lang2, scheme=scheme))

    def test_addic7ed(self):
        languages = {u'English': 'en',
                     u'English (US)': 'en',
                     u'English (UK)': 'en',
                     u'Italian': 'it',
                     u'Portuguese': 'pt',
                     u'Portuguese (Brazilian)': 'pt',
                     u'Romanian': 'ro',
                     u'Español (Latinoamérica)': 'es',
                     u'Español (España)': 'es',
                     u'Spanish (Latin America)': 'es',
                     u'Español': 'es',
                     u'Spanish': 'es',
                     u'Spanish (Spain)': 'es',
                     u'French': 'fr',
                     u'Greek': 'el',
                     u'Arabic': 'ar',
                     u'German': 'de',
                     u'Croatian': 'hr',
                     u'Indonesian': 'id',
                     u'Hebrew': 'he',
                     u'Russian': 'ru',
                     u'Turkish': 'tr',
                     u'Swedish': 'se',
                     u'Czech': 'cs',
                     u'Dutch': 'nl',
                     u'Hungarian': 'hu',
                     u'Norwegian': 'no',
                     u'Polish': 'pl',
                     u'Persian': 'fa'}

        self.check_languages(languages)

    def test_subswiki(self):
        languages = {u'English (US)': 'en', u'English (UK)': 'en', u'English': 'en',
                     u'French': 'fr', u'Brazilian': 'po', u'Portuguese': 'pt',
                     u'Español (Latinoamérica)': 'es', u'Español (España)': 'es',
                     u'Español': 'es', u'Italian': 'it', u'Català': 'ca'}

        self.check_languages(languages)

    def test_tvsubtitles(self):
        languages = {u'English': 'en', u'Español': 'es', u'French': 'fr', u'German': 'de',
                     u'Brazilian': 'br', u'Russian': 'ru', u'Ukrainian': 'ua', u'Italian': 'it',
                     u'Greek': 'gr', u'Arabic': 'ar', u'Hungarian': 'hu', u'Polish': 'pl',
                     u'Turkish': 'tr', u'Dutch': 'nl', u'Portuguese': 'pt', u'Swedish': 'sv',
                     u'Danish': 'da', u'Finnish': 'fi', u'Korean': 'ko', u'Chinese': 'cn',
                     u'Japanese': 'jp', u'Bulgarian': 'bg', u'Czech': 'cz', u'Romanian': 'ro'}

        self.check_languages(languages)

    def test_opensubtitles(self):
        opensubtitles_langfile = file_in_same_dir(__file__, 'opensubtitles_languages_2012_05_09.txt')
        langs = [ l.strip().split('\t') for l in open(opensubtitles_langfile) ][1:]
        for lang in langs:
            # incompatible duplicate in opensubtitles' API itself
            # in case of duplicates, the one removed is the one which has
            # the most functionality disabled, ie lang[3] == '0' or
            # lang[4] == '0'
            if lang[0] in ['eus', 'fra', 'deu', 'hye', 'ice', 'kat', 'mkd',
                           'mri', 'msa', 'mya', 'nld', 'fas', 'scr', 'slk',
                           'sqi', 'srp', 'bod', 'cym', 'zho', 'ron', 'unk',
                           'ass']:
                continue

            # check that we recognize the opensubtitles language code correctly
            # and that we are able to output this code from a language
            self.assertEqual(lang[0], Language(lang[0], scheme='opensubtitles').opensubtitles)
            if lang[1]:
                # check we recognize the opensubtitles 2-letter code correctly
                self.check_languages({lang[0]: lang[1]}, scheme='opensubtitles')

    def test_subtitulos(self):
        languages = {u'English (US)': 'en', u'English (UK)': 'en', u'English': 'en',
                     u'French': 'fr', u'Brazilian': 'po', u'Portuguese': 'pt',
                     u'Español (Latinoamérica)': 'es', u'Español (España)': 'es',
                     u'Español': 'es', u'Italian': 'it', u'Català': 'ca'}

        self.check_languages(languages)

    def test_thesubdb(self):
        languages = {'af': 'af', 'cs': 'cs', 'da': 'da', 'de': 'de', 'en': 'en', 'es': 'es', 'fi': 'fi',
                     'fr': 'fr', 'hu': 'hu', 'id': 'id', 'it': 'it', 'la': 'la', 'nl': 'nl', 'no': 'no',
                     'oc': 'oc', 'pl': 'pl', 'pt': 'pt', 'ro': 'ro', 'ru': 'ru', 'sl': 'sl', 'sr': 'sr',
                     'sv': 'sv', 'tr': 'tr'}

        self.check_languages(languages)

    def test_language_object(self):
        self.assertEqual(len(list(set([Language('qwerty'), Language('asdf')]))), 1)
        d = { Language('qwerty'): 7 }
        d[Language('asdf')] = 23
        self.assertEqual(d[Language('qwerty')], 23)

    def test_exceptions(self):
        self.assertEqual(Language('br'), Language('pt(br)'))

        # languages should be equal regardless of country
        self.assertEqual(Language('br'), Language('pt'))

        self.assertEqual(Language('unknown'), Language('und'))


suite = allTests(TestLanguage)

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite)
