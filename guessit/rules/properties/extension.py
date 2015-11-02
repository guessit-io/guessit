#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Season/Episode numbering support
'''
from rebulk import Rebulk

import regex as re

from ..common.validators import seps_surround

EXTENSION = Rebulk().regex_defaults(flags=re.IGNORECASE).string_defaults(ignore_case=True)
EXTENSION.defaults(name='extension',
                   formatter=lambda value: value[1:],
                   conflict_solver=lambda match, other: other
                   if other.name in ['container', 'format', 'videoCodec']
                   else '__default__')

subtitles = ['srt', 'idx', 'sub', 'ssa', 'ass']
info = ['nfo']
videos = ['3g2', '3gp', '3gp2', 'asf', 'avi', 'divx', 'flv', 'm4v', 'mk2',
          'mka', 'mkv', 'mov', 'mp4', 'mp4a', 'mpeg', 'mpg', 'ogg', 'ogm',
          'ogv', 'qt', 'ra', 'ram', 'rm', 'ts', 'wav', 'webm', 'wma', 'wmv',
          'iso', 'vob']
torrent = ['torrent']

EXTENSION.regex(r'\.\L<exts>$', exts=subtitles, tags=['subtitle'])
EXTENSION.regex(r'\.\L<exts>$', exts=info, tags=['info'])
EXTENSION.regex(r'\.\L<exts>$', exts=videos, tags=['video'])
EXTENSION.regex(r'\.\L<exts>$', exts=torrent, tags=['torrent'])


EXTENSION.defaults(name='container',
                   validator=seps_surround,
                   conflict_solver=lambda match, other: match
                   if other.name in ['extension', 'format', 'videoCodec']
                   else '__default__')

EXTENSION.string(*subtitles, tags=['subtitle'])
EXTENSION.string(*videos, tags=['video'])
EXTENSION.string(*torrent, tags=['torrent'])
