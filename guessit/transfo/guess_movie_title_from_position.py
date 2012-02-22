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

from guessit import Guess
import logging

log = logging.getLogger("guessit.transfo.guess_movie_title_from_position")



DEPENDS = []
PROVIDES = []

def process(mtree):
    def found_title(node, confidence):
        node.guess = Guess({ 'title': node.clean_value },
                           confidence = confidence)
        log.debug('Found with confidence %.2f: %s' % (confidence, node.guess))

    # specific cases:
    #  - movies/tttttt (yyyy)/tttttt.ccc
    try:
        if mtree.node_at((-4, 0)).value.lower() == 'movies':
            containing_folder = mtree.node_at((-3,))

            # Note:too generic, might solve all the unittests as they all contain 'movies'
            # in their path
            #
            #if containing_folder.is_leaf() and not containing_folder.guess:
            #    containing_folder.guess = Guess({ 'title': clean_string(containing_folder.value) },
            #                                    confidence = 0.7)

            year_group = containing_folder.first_leaf_containing('year')
            groups_before = containing_folder.previous_unidentified_leaves(year_group)

            found_title(groups_before[0], confidence = 0.8)
            return


    except:
        pass


    # if we have either format or videoCodec in the folder containing the file
    # or one of its parents, then we should probably look for the title in
    # there rather than in the basename
    try:
        props = mtree.previous_leaves_containing(mtree.children[-2],
                                                 [ 'videoCodec', 'format', 'language' ])
    except:
        props = []

    if props:
        group_idx = props[0].node_idx[0]
        if all(g.node_idx[0] == group_idx for g in props):
            # if they're all in the same group, take leftover info from there
            leftover = mtree.node_at((group_idx,)).unidentified_leaves()

            if leftover:
                found_title(leftover[0], confidence = 0.7)
                return

    # first leftover group in the last path part sounds like a good candidate for title,
    # except
    basename_leftover = mtree.node_at((-2,)).unidentified_leaves()
    try:
        folder_leftover = mtree.node_at((-3,)).unidentified_leaves()
    except:
        folder_leftover = []

    # look for title in basename if there are some remaining undidentified groups there
    if basename_leftover:
        title_candidate = basename_leftover[0]

        # if basename is only one word and the containing folder has at least 3 words in it,
        # we should take the title from the folder name
        # ex: Movies/Alice in Wonderland DVDRip.XviD-DiAMOND/dmd-aw.avi
        # ex: Movies/Somewhere.2010.DVDRip.XviD-iLG/i-smwhr.avi  <-- TODO: gets caught here?
        if (title_candidate.clean_value.count(' ') == 0 and
            folder_leftover and
            folder_leftover[0].clean_value.count(' ') >= 2):

            found_title(folder_leftover[0], confidence = 0.7)
            return

        # if there are only 2 unidentified groups, the first of which is inside
        # brackets or parentheses, we take the second one for the title:
        # ex: Movies/[阿维达].Avida.2006.FRENCH.DVDRiP.XViD-PROD.avi
        if len(basename_leftover) == 2 and basename_leftover[0].is_explicit():
            found_title(basename_leftover[1], confidence = 0.8)
            return

        # if all else fails, take the first remaining unidentified group in the
        # basename as title
        found_title(title_candidate, confidence = 0.6)
        return


    # if there are no leftover groups in the basename, look in the folder name
    if folder_leftover:
        found_title(folder_leftover[0], confidence = 0.5)
        return

    # if nothing worked, look if we have a very small group at the beginning of the basename
    basename_leftover = mtree.node_at((-2,)).unidentified_leaves(valid = lambda leaf: True)
    if basename_leftover:
        found_title(basename_leftover[0], confidence = 0.4)
        return
