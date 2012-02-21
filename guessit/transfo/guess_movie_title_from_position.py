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

            title_candidate = groups_before[0]
            title_candidate.guess = Guess({ 'title': title_candidate.clean_value },
                                          confidence = 0.8)
            log.debug('Found with confidence %.2f: %s' % (0.8, title_candidate.guess))


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

    leftover = None

    if props:
        group_idx = props[0].node_idx[0]
        if all(g.node_idx[0] == group_idx for g in props):
            # if they're all in the same group, take leftover info from there
            leftover = mtree.node_at((group_idx,)).unidentified_leaves()

    if props and leftover:
        title_candidate = leftover[0]
        title_candidate.guess = Guess({ 'title': title_candidate.clean_value }, confidence = 0.7)
        log.debug('Found with confidence %.2f: %s' % (0.7, title_candidate.guess))
    else:
        # first leftover group in the last path part sounds like a good candidate for title,
        # except if it's only one word and that the first group before has at least 3 words in it
        # (case where the filename contains an 8 chars short name and the movie title is
        #  actually in the parent directory name)
        leftover = mtree.node_at((-2,)).unidentified_leaves()
        try:
            previous_pgroup_leftover = mtree.node_at((-3,)).unidentified_leaves()
        except:
            previous_pgroup_leftover = []

        if leftover:
            title_candidate = leftover[0]

            if (title_candidate.clean_value.count(' ') == 0 and
                previous_pgroup_leftover and
                previous_pgroup_leftover[0].clean_value.count(' ') >= 2):

                previous_pgroup_leftover[0].guess = Guess({ 'title': previous_pgroup_leftover[0].clean_value },
                                                          confidence = 0.6)
                log.debug('Found with confidence %.2f: %s' % (0.6, previous_pgroup_leftover[0].guess))

            else:
                title_candidate.guess = Guess({ 'title': title_candidate.clean_value },
                                              confidence = 0.6)
                log.debug('Found with confidence %.2f: %s' % (0.6, title_candidate.guess))

        else:
            # if there were no leftover groups in the last path part, look in the one before that
            if previous_pgroup_leftover:
                title_candidate = previous_pgroup_leftover[0]
                title_candidate.guess = Guess({ 'title': title_candidate.clean_value },
                                              confidence = 0.6)
                log.debug('Found with confidence %.2f: %s' % (0.6, title_candidate.guess))

