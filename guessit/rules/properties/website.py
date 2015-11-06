#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Website property.
"""
from __future__ import unicode_literals

from pkg_resources import resource_stream  # @UnresolvedImport

from rebulk import Rebulk

import regex as re

WEBSITE = Rebulk().regex_defaults(flags=re.IGNORECASE)
WEBSITE.defaults(name="website")

TLDS = [l.strip().decode('utf-8')
        for l in resource_stream('guessit', 'tlds-alpha-by-domain.txt').readlines()
        if b'--' not in l][1:]  # All registered domain extension

SAFE_TLDS = ['com', 'org', 'net']  # For sure a website extension
SAFE_SUBDOMAINS = ['www']  # For sure a website subdomain
SAFE_PREFIX = ['co', 'com', 'org', 'net']  # Those words before a tlds are sure

WEBSITE.regex(r'(?:[^a-z0-9]|^)((?:\L<safe_subdomains>\.)+(?:[a-z-]+\.)+(?:\L<tlds>))(?:[^a-z0-9]|$)',
              safe_subdomains=SAFE_SUBDOMAINS, tlds=TLDS, children=True)
WEBSITE.regex(r'(?:[^a-z0-9]|^)((?:\L<safe_subdomains>\.)*[a-z-]+\.(?:\L<safe_tlds>))(?:[^a-z0-9]|$)',
              safe_subdomains=SAFE_SUBDOMAINS, safe_tlds=SAFE_TLDS, children=True)
WEBSITE.regex(r'(?:[^a-z0-9]|^)((?:\L<safe_subdomains>\.)*[a-z-]+\.(?:\L<safe_prefix>\.)+(?:\L<tlds>))(?:[^a-z0-9]|$)',
              safe_subdomains=SAFE_SUBDOMAINS, safe_prefix=SAFE_PREFIX, tlds=TLDS, children=True)
