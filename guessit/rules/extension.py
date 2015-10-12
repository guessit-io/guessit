#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Season/Episode numbering support
"""
from rebulk import Rebulk

import regex as re

EXTENSION = Rebulk().regex_defaults(flags=re.IGNORECASE)
EXTENSION.defaults(name="extension")

EXTENSION.regex(r'\.(\L<exts>)$', exts=['srt', 'idx', 'sub', 'ssa', 'ass'], tags=["subtitle"], children=True)
EXTENSION.regex(r'\.(\L<exts>)$', exts=['nfo'], tags=["info"], children=True)
EXTENSION.regex(r'\.(\L<exts>)$', exts=['3g2', '3gp', '3gp2', 'asf', 'avi', 'divx', 'flv', 'm4v', 'mk2',
                                        'mka', 'mkv', 'mov', 'mp4', 'mp4a', 'mpeg', 'mpg', 'ogg', 'ogm',
                                        'ogv', 'qt', 'ra', 'ram', 'rm', 'ts', 'wav', 'webm', 'wma', 'wmv',
                                        'iso', 'vob'], tags=["video"], children=True)
