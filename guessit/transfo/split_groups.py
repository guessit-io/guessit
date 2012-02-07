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

from guessit import Guess, fileutils
from guessit.filetype import guess_filetype
from guessit.textutils import find_first_level_groups
from guessit.patterns import group_delimiters
import os.path
import mimetypes
import logging

log = logging.getLogger("guessit.transfo.split_groups")



def split_tree(mtree, components):
    offset = 0
    for c in components:
        start = mtree.value.find(c, offset)
        end = start + len(c)
        mtree.add_child(span = (mtree.offset + start,
                                mtree.offset + end))
        offset = end


def split_path_components(mtree):
    # FIXME: duplicate from fileutils
    """Returns the filename split into [ dir*, basename, ext ]."""
    components = fileutils.split_path(mtree.value)
    basename = components.pop(-1)
    components += list(os.path.splitext(basename))
    components[-1] = components[-1][1:] # remove the '.' from the extension

    split_tree(mtree, components)

def split_explicit_groups(mtree):
    """return the string split into explicit groups, that is, those either
    between parenthese, square brackets or curly braces, and those separated
    by a dash."""
    groups = find_first_level_groups(mtree.value, group_delimiters[0])
    for delimiters in group_delimiters:
        groups = reduce(lambda l, x: l + find_first_level_groups(x, delimiters), groups, [])

    # do not do this at this moment, it is not strong enough and can break other
    # patterns, such as dates, etc...
    #groups = reduce(lambda l, x: l + x.split('-'), groups, [])

    split_tree(mtree, groups)


DEPENDS = []
PROVIDES = [ 'type', 'mimetype' ]

def process(mtree):
    filename = mtree.string

    # 1- first split our path into dirs + basename + ext
    split_path_components(mtree)

    # try to detect the file type
    filetype, other = guess_filetype(filename, mtree.guess.get('type', 'autodetect'))
    mtree.guess.set('type', filetype, confidence = 1.0)
    log.debug('Found with confidence %.2f: %s' % (1.0, mtree.guess))

    filetype_info = Guess(other, confidence = 1.0)

    # guess the mimetype of the filename
    # TODO: handle other mimetypes not found on the default type_maps
    # mimetypes.types_map['.srt']='text/subtitle'
    mime, _ = mimetypes.guess_type(filename, strict=False)
    if mime is not None:
        filetype_info.update({ 'mimetype': mime }, confidence = 1.0)

    mtree.node_at((-1,)).guess = filetype_info
    log.debug('Found with confidence %.2f: %s' % (1.0, mtree.node_at((-1,)).guess))

    # 2- split each of those into explicit groups, if any
    # note: be careful, as this might split some regexps with more confidence such as
    #       Alfleni-Team, or [XCT] or split a date such as (14-01-2008)
    for c in mtree.children:
        split_explicit_groups(c)
