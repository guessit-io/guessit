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

    def check_languages(self, languages):
        for lang1, lang2 in languages.items():
            self.assertEqual(Language(lang1), Language(lang2))

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

    def test_opensubtitles(self):
        languages = {'aa': 'aar', 'ab': 'abk', 'af': 'afr', 'ak': 'aka', 'sq': 'alb', 'am': 'amh', 'ar': 'ara',
                     'an': 'arg', 'hy': 'arm', 'as': 'asm', 'av': 'ava', 'ae': 'ave', 'ay': 'aym', 'az': 'aze',
                     'ba': 'bak', 'bm': 'bam', 'eu': 'baq', 'be': 'bel', 'bn': 'ben', 'bh': 'bih', 'bi': 'bis',
                     'bs': 'bos',              'bg': 'bul', 'my': 'bur', 'ca': 'cat', 'ch': 'cha', 'ce': 'che',
                     'zh': 'chi', 'cu': 'chu', 'cv': 'chv', 'kw': 'cor', 'co': 'cos', 'cr': 'cre', 'cs': 'cze',
                     'da': 'dan', 'dv': 'div', 'nl': 'dut', 'dz': 'dzo', 'en': 'eng', 'eo': 'epo', 'et': 'est',
                     'ee': 'ewe', 'fo': 'fao', 'fj': 'fij', 'fi': 'fin', 'fr': 'fre', 'fy': 'fry', 'ff': 'ful',
                     'ka': 'geo', 'de': 'ger', 'gd': 'gla', 'ga': 'gle', 'gl': 'glg', 'gv': 'glv', 'el': 'ell',
                     'gn': 'grn', 'gu': 'guj', 'ht': 'hat', 'ha': 'hau', 'he': 'heb', 'hz': 'her', 'hi': 'hin',
                     'ho': 'hmo', 'hr': 'hrv', 'hu': 'hun', 'ig': 'ibo', 'is': 'ice', 'io': 'ido', 'ii': 'iii',
                     'iu': 'iku', 'ie': 'ile', 'ia': 'ina', 'id': 'ind', 'ik': 'ipk', 'it': 'ita', 'jv': 'jav',
                     'ja': 'jpn', 'kl': 'kal', 'kn': 'kan', 'ks': 'kas', 'kr': 'kau', 'kk': 'kaz', 'km': 'khm',
                     'ki': 'kik', 'rw': 'kin', 'ky': 'kir', 'kv': 'kom', 'kg': 'kon', 'ko': 'kor', 'kj': 'kua',
                     'ku': 'kur', 'lo': 'lao', 'la': 'lat', 'lv': 'lav', 'li': 'lim', 'ln': 'lin', 'lt': 'lit',
                     'lb': 'ltz', 'lu': 'lub', 'lg': 'lug', 'mk': 'mac', 'mh': 'mah', 'ml': 'mal', 'mi': 'mao',
                     'mr': 'mar', 'ms': 'may', 'mg': 'mlg', 'mt': 'mlt',              'mn': 'mon', 'na': 'nau',
                     'nv': 'nav', 'nr': 'nbl', 'nd': 'nde', 'ng': 'ndo', 'ne': 'nep', 'nn': 'nno', 'nb': 'nob',
                     'no': 'nor', 'ny': 'nya', 'oc': 'oci', 'oj': 'oji', 'or': 'ori', 'om': 'orm', 'os': 'oss',
                     'pa': 'pan', 'fa': 'per', 'pi': 'pli', 'pl': 'pol', 'pt': 'por', 'ps': 'pus', 'qu': 'que',
                     'rm': 'roh', 'rn': 'run', 'ru': 'rus', 'sg': 'sag', 'sa': 'san',              'si': 'sin',
                     'sk': 'slo', 'sl': 'slv',              'sm': 'smo', 'sn': 'sna', 'sd': 'snd', 'so': 'som',
                     'st': 'sot', 'es': 'spa', 'sc': 'srd', 'ss': 'ssw', 'su': 'sun', 'sw': 'swa', 'sv': 'swe',
                     'ty': 'tah', 'ta': 'tam', 'tt': 'tat', 'te': 'tel', 'tg': 'tgk', 'tl': 'tgl', 'th': 'tha',
                     'bo': 'tib', 'ti': 'tir', 'to': 'ton', 'tn': 'tsn', 'ts': 'tso', 'tk': 'tuk', 'tr': 'tur',
                     'tw': 'twi', 'ug': 'uig', 'uk': 'ukr', 'ur': 'urd', 'uz': 'uzb', 've': 'ven', 'vi': 'vie',
                     'vo': 'vol', 'cy': 'wel', 'wa': 'wln', 'wo': 'wol', 'xh': 'xho', 'yi': 'yid', 'yo': 'yor',
                     'za': 'zha', 'zu': 'zul', 'ro': 'rum', 'po': 'pob', 'un': 'unk'}

        # could not identify these languages in the ISO-639-2 doc
        languages_taken_out =  { 'mo': 'mol', 'sr': 'scc', 'se': 'sme', 'br': 'bre', 'ay': 'ass' }

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


suite = allTests(TestLanguage)

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite)
