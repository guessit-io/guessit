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

from guessit import Guess
from guessit.patterns import deleted
from guessit.textutils import clean_string, str_fill, find_first_level_groups
from guessit.fileutils import split_path
from guessit.patterns import group_delimiters
import os.path
import logging

log = logging.getLogger("guessit.matchtree")



def old_tree_to_string(tree):
    """Return a string representation for the given tree.

    The lines convey the following information:
     - line 1: path idx
     - line 2: explicit group idx
     - line 3: group index
     - line 4: remaining info
     - line 5: meaning conveyed

    Meaning is a letter indicating what type of info was matched by this group,
    for instance 't' = title, 'f' = format, 'l' = language, etc...

    An example is the following:

    0000000000000000000000000000000000000000000000000000000000000000000000000000000000 111
    0000011111111111112222222222222233333333444444444444444455555555666777777778888888 000
    0000000000000000000000000000000001111112011112222333333401123334000011233340000000 000
    __________________(The.Prestige).______.[____.HP.______.{__-___}.St{__-___}.Chaps].___
    xxxxxttttttttttttt               ffffff  vvvv    xxxxxx  ll lll     xx xxx         ccc
    [XCT].Le.Prestige.(The.Prestige).DVDRip.[x264.HP.He-Aac.{Fr-Eng}.St{Fr-Eng}.Chaps].mkv

    (note: the last line representing the filename is not pat of the tree representation)
    """
    m_tree = [ '', # path level index
               '', # explicit group index
               '', # matched regexp and dash-separated
               '', # groups leftover that couldn't be matched
               '', # meaning conveyed: E = episodenumber, S = season, ...
               ]

    def add_char(pidx, eidx, gidx, remaining, meaning = None):
        nr = len(remaining)
        def to_hex(x):
            if isinstance(x, int):
                return str(x) if x < 10 else chr(55+x)
            return x
        m_tree[0] = m_tree[0] + to_hex(pidx) * nr
        m_tree[1] = m_tree[1] + to_hex(eidx) * nr
        m_tree[2] = m_tree[2] + to_hex(gidx) * nr
        m_tree[3] = m_tree[3] + remaining
        m_tree[4] = m_tree[4] + str(meaning or ' ') * nr

    def meaning(result):
        mmap = { 'episodeNumber': 'E',
                 'season': 'S',
                 'extension': 'e',
                 'format': 'f',
                 'language': 'l',
                 'videoCodec': 'v',
                 'audioCodec': 'a',
                 'website': 'w',
                 'container': 'c',
                 'series': 'T',
                 'title': 't',
                 'date': 'd',
                 'year': 'y',
                 'releaseGroup': 'r',
                 'screenSize': 's'
                 }

        if result is None:
            return ' '

        for prop, l in mmap.items():
            if prop in result:
                return l

        return 'x'

    for pidx, pathpart in enumerate(tree):
        for eidx, explicit_group in enumerate(pathpart):
            for gidx, (group, remaining, result) in enumerate(explicit_group):
                add_char(pidx, eidx, gidx, remaining, meaning(result))

        # special conditions for the path separator
        if pidx < len(tree) - 2:
            add_char(' ', ' ', ' ', '/')
        elif pidx == len(tree) - 2:
            add_char(' ', ' ', ' ', '.')

    return '\n'.join(m_tree)



def iterate_groups(match_tree):
    """Iterate over all the groups in a match_tree and return them as pairs
    of (group_pos, group) where:
     - group_pos = (pidx, eidx, gidx)
     - group = (string, remaining, guess)
    """
    for pidx, pathpart in enumerate(match_tree):
        for eidx, explicit_group in enumerate(pathpart):
            for gidx, group in enumerate(explicit_group):
                yield (pidx, eidx, gidx), group


def find_group(match_tree, prop):
    """Find the list of groups that resulted in a guess that contains the
    asked property."""
    result = []
    for gpos, (string, remaining, guess) in iterate_groups(match_tree):
        if guess and prop in guess:
            result.append(gpos)
    return result

def get_group(match_tree, gpos):
    pidx, eidx, gidx = gpos
    return match_tree[pidx][eidx][gidx]


def leftover_valid_groups(match_tree, valid = lambda s: len(s[0]) > 3):
    """Return the list of valid string groups (eg: len(s) > 3) that could not be
    matched to anything as a list of pairs (cleaned_str, group_pos)."""
    leftover = []
    for gpos, (group, remaining, guess) in iterate_groups(match_tree):
        if not guess:
            clean_str = clean_string(remaining)
            if valid((clean_str, gpos)):
                leftover.append((clean_str, gpos))

    return leftover



class BaseMatchTree(object):
    """A MatchTree represents the hierarchical split of a string into its
    constituent semantic groups."""

    def __init__(self, string = '', span = None, parent = None):
        # TODO: make sure string is unicode (?)
        self.string = string
        self.span = span or (0,len(string))
        self.parent = parent
        self.children = []
        self.guess = Guess()

    @property
    def value(self):
        return self.string[self.span[0]:self.span[1]]

    @property
    def clean_value(self):
        return clean_string(self.value)

    @property
    def offset(self):
        return self.span[0]

    @property
    def info(self):
        result = dict(self.guess)

        for c in self.children:
            result.update(c.info)

        return result

    @property
    def root(self):
        if not self.parent:
            return self

        return self.parent.root

    @property
    def depth(self):
        if self.is_leaf():
            return 0

        return 1 + max(c.depth for c in self.children)


    def is_leaf(self):
        return self.children == []

    def add_child(self, span):
        child = MatchTree(self.string, span = span, parent = self)
        self.children.append(child)

    def partition(self, indices):
        indices = sorted(indices)
        if indices[0] != 0:
            indices.insert(0, 0)
        if indices[-1] != len(self.value):
            indices.append(len(self.value))

        for start, end in zip(indices[:-1], indices[1:]):
            self.add_child(span = (start + self.offset, end + self.offset))


    def nodes_at_depth(self, depth):
        if depth == 0:
            yield self

        for child in self.children:
            for node in child.nodes_at_depth(depth-1):
                yield node

    @property
    def node_idx(self):
        if self.parent is None:
            return ()
        return self.parent.node_idx + (self.parent.children.index(self),)

    def node_at(self, idx):
        if not idx:
            return self

        try:
            return self.children[idx[0]].node_at(idx[1:])
        except:
            raise ValueError('Non-existent node index: %s' % (idx,))

    def nodes(self):
        yield self
        for child in self.children:
            for node in child.nodes():
                yield node

    def _leaves(self):
        if self.is_leaf():
            yield self
        else:
            for child in self.children:
                for leaf in child._leaves():
                    yield leaf

    def leaves(self):
        return list(self._leaves())



class MatchTree(BaseMatchTree):
    """The MatchTree contains a few "utility" methods which are not necessary
    for the BaseMatchTree, but add a lot of convenience for writing
    higher-level rules."""

    def _unidentified_leaves(self):
        for leaf in self._leaves():
            if not leaf.guess and len(leaf.clean_value) >= 2:
                yield leaf

    def unidentified_leaves(self):
        return list(self._unidentified_leaves())

    def _leaves_containing(self, property_name):
        if isinstance(property_name, basestring):
            property_name = [ property_name ]

        for leaf in self._leaves():
            for prop in property_name:
                if prop in leaf.guess:
                    yield leaf
                    break

    def leaves_containing(self, property_name):
        return list(self._leaves_containing(property_name))

    def first_leaf_containing(self, property_name):
        try:
            return next(self._leaves_containing(property_name))
        except StopIteration:
            return None

    def _previous_unidentified_leaves(self, node):
        node_idx = node.node_idx
        for leaf in self._unidentified_leaves():
            if leaf.node_idx < node_idx:
                yield leaf

    def previous_unidentified_leaves(self, node):
        return list(self._previous_unidentified_leaves(node))

    def _previous_leaves_containing(self, node, property_name):
        node_idx = node.node_idx
        for leaf in self._leaves_containing(property_name):
            if leaf.node_idx < node_idx:
                yield leaf

    def previous_leaves_containing(self, node, property_name):
        return list(self._previous_leaves_containing(node, property_name))

    def is_explicit(self):
        """Return whether the group was explicitly enclosed by
        parentheses/square brackets/etc."""
        return (self.value[0] + self.value[-1]) in group_delimiters


def tree_to_string(mtree):
    empty_line = ' ' * len(mtree.string)

    def to_hex(x):
        if isinstance(x, int):
            return str(x) if x < 10 else chr(55+x)
        return x

    def meaning(result):
        mmap = { 'episodeNumber': 'E',
                 'season': 'S',
                 'extension': 'e',
                 'format': 'f',
                 'language': 'l',
                 'videoCodec': 'v',
                 'audioCodec': 'a',
                 'website': 'w',
                 'container': 'c',
                 'series': 'T',
                 'title': 't',
                 'date': 'd',
                 'year': 'y',
                 'releaseGroup': 'r',
                 'screenSize': 's'
                 }

        if result is None:
            return ' '

        for prop, l in mmap.items():
            if prop in result:
                return l

        return 'x'

    lines = [ empty_line ] * (mtree.depth + 2) # +2: remaining, meaning
    lines[-2] = mtree.string

    for node in mtree.nodes():
        if node == mtree:
            continue

        idx = node.node_idx
        depth = len(idx) - 1
        if idx:
            lines[depth] = str_fill(lines[depth], node.span, to_hex(idx[-1]))
        if node.guess:
            lines[-2] = str_fill(lines[-2], node.span, '_')
            lines[-1] = str_fill(lines[-1], node.span, meaning(node.guess))

    lines.append(mtree.string)

    return '\n'.join(lines)

