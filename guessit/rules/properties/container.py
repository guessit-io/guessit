#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Container support
"""
from __future__ import unicode_literals

from rebulk import Rebulk

import regex as re

from ..common.validators import seps_surround

CONTAINER = Rebulk().regex_defaults(flags=re.IGNORECASE).string_defaults(ignore_case=True)
CONTAINER.defaults(name='container',
                   formatter=lambda value: value[1:],
                   tags=['extension'],
                   conflict_solver=lambda match, other: other
                   if other.name in ['format', 'video_codec'] or
                   other.name == 'container' and 'extension' not in other.tags
                   else '__default__')

subtitles = ['srt', 'idx', 'sub', 'ssa', 'ass']
info = ['nfo']
videos = ['3g2', '3gp', '3gp2', 'asf', 'avi', 'divx', 'flv', 'm4v', 'mk2',
          'mka', 'mkv', 'mov', 'mp4', 'mp4a', 'mpeg', 'mpg', 'ogg', 'ogm',
          'ogv', 'qt', 'ra', 'ram', 'rm', 'ts', 'wav', 'webm', 'wma', 'wmv',
          'iso', 'vob']
torrent = ['torrent']

CONTAINER.regex(r'\.\L<exts>$', exts=subtitles, tags=['extension', 'subtitle'])
CONTAINER.regex(r'\.\L<exts>$', exts=info, tags=['extension', 'info'])
CONTAINER.regex(r'\.\L<exts>$', exts=videos, tags=['extension', 'video'])
CONTAINER.regex(r'\.\L<exts>$', exts=torrent, tags=['extension', 'torrent'])


CONTAINER.defaults(name='container',
                   validator=seps_surround,
                   conflict_solver=lambda match, other: match
                   if other.name in ['format', 'video_codec'] or other.name == 'container' and 'extension' in other.tags
                   else '__default__')

CONTAINER.string(*[sub for sub in subtitles if sub not in ['sub']], tags=['subtitle'])
CONTAINER.string(*videos, tags=['video'])
CONTAINER.string(*torrent, tags=['torrent'])
