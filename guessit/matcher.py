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

from guessit import fileutils, textutils
from guessit.matchtree import MatchTree
from guessit.guess import Guess, merge_similar_guesses, merge_all, choose_int, choose_string
from guessit.date import search_date, search_year
from guessit.language import search_language
from guessit.filetype import guess_filetype
from guessit.transfo import format_guess
from guessit.patterns import video_exts, subtitle_exts, sep, deleted, video_rexps, websites, episode_rexps, weak_episode_rexps, non_episode_title, find_properties, canonical_form, unlikely_series, group_delimiters
from guessit.matchtree import get_group, find_group, leftover_valid_groups, tree_to_string
from guessit.textutils import find_first_level_groups, split_on_groups, blank_region, clean_string, to_utf8
import datetime
import os.path
import re
import copy
import logging
import mimetypes

log = logging.getLogger("guessit.newmatcher")


def use_node(f):
    f.use_node = True
    return f




from date import search_date, search_year
from guessit.guess import Guess
from patterns import websites, properties, sep



def guess_movie_title_from_position(mtree):
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

            year_group = [ leaf for leaf in containing_folder.leaves() if 'year' in leaf.guess ][0]
            groups_before = [ leaf for leaf in containing_folder.unidentified_leaves()
                              if leaf.node_idx < year_group.node_idx ]

            title_candidate = groups_before[0]
            title_candidate.guess = Guess({ 'title': title_candidate.clean_value },
                                          confidence = 0.8)
            log.debug('Found with confidence %.2f: %s' % (0.8, title_candidate.guess))


    except:
        pass


    # if we have either format or videoCodec in the folder containing the file
    # or one of its parents, then we should probably look for the title in
    # there rather than in the basename
    props = [ leaf for leaf in mtree.leaves()
              if (leaf.node_idx <= (len(mtree.children)-2,) and
                  ('videoCodec' in leaf.guess or
                   'format' in leaf.guess or
                   'language' in leaf.guess)) ]

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


def match_from_epnum_position(mtree, node):
    epnum_idx = node.node_idx

    # a few helper functions to be able to filter using high-level semantics
    def before_epnum_in_same_pathgroup():
        return [ leaf for leaf in mtree.unidentified_leaves()
                 if leaf.node_idx[0] == epnum_idx[0] and leaf.node_idx[1:] < epnum_idx[1:] ]

    def after_epnum_in_same_pathgroup():
        return [ leaf for leaf in mtree.unidentified_leaves()
                 if leaf.node_idx[0] == epnum_idx[0] and leaf.node_idx[1:] > epnum_idx[1:] ]

    def before_epnum_in_same_explicitgroup():
        return [ leaf for leaf in mtree.unidentified_leaves()
                 if leaf.node_idx[:2] == epnum_idx[:2] and leaf.node_idx[2:] < epnum_idx[2:] ]

    def after_epnum_in_same_explicitgroup():
        return [ leaf for leaf in mtree.unidentified_leaves()
                 if leaf.node_idx[:2] == epnum_idx[:2] and leaf.node_idx[2:] > epnum_idx[2:] ]

    # if we have at least 1 valid group before the episodeNumber, then it's probably
    # the series name
    series_candidates = before_epnum_in_same_pathgroup()
    if len(series_candidates) >= 1:
        series_candidates[0].guess = Guess({ 'series': series_candidates[0].clean_value }, confidence = 0.7)

    # only 1 group after (in the same path group) and it's probably the episode title
    title_candidates = filter(lambda n: n.clean_value.lower() not in non_episode_title,
                              after_epnum_in_same_pathgroup())

    if len(title_candidates) == 1:
        title_candidates[0].guess = Guess({ 'title': title_candidates[0].clean_value }, confidence = 0.5)
    else:
        # try in the same explicit group, with lower confidence
        title_candidates = filter(lambda n: n.clean_value.lower() not in non_episode_title,
                                  after_epnum_in_same_explicitgroup())
        if len(title_candidates) == 1:
            title_candidates[0].guess = Guess({ 'title': title_candidates[0].clean_value }, confidence = 0.4)

    # epnumber is the first group and there are only 2 after it in same path group
    #  -> season title - episode title
    title_candidates = filter(lambda n: n.clean_value.lower() not in non_episode_title,
                              after_epnum_in_same_pathgroup())
    if ('title' not in mtree.info and                # no title
        before_epnum_in_same_pathgroup() == [] and   # no groups before
        len(title_candidates) == 2):                 # only 2 groups after

        title_candidates[0].guess = Guess({ 'series': title_candidates[0].clean_value }, confidence = 0.4)
        title_candidates[1].guess = Guess({ 'title':  title_candidates[1].clean_value }, confidence = 0.4)


    # if we only have 1 remaining valid group in the pathpart before the filename,
    # then it's likely that it is the series name
    try:
        series_candidates = mtree.node_at((-3,)).unidentified_leaves()
    except:
        series_candidates = []

    if len(series_candidates) == 1:
        series_candidates[0].guess = Guess({ 'series': series_candidates[0].clean_value }, confidence = 0.5)



def guess_episode_info_from_position(mtree):
    eps = [ node for node in mtree.leaves() if 'episodeNumber' in node.guess ]
    if eps:
        match_from_epnum_position(mtree, eps[0])

    else:
        # if we don't have the episode number, but at least 2 groups in the
        # last path group, then it's probably series - eptitle
        title_candidates = filter(lambda n: n.clean_value.lower() not in non_episode_title,
                                  mtree.node_at((-2,)).unidentified_leaves())

        if len(title_candidates) >= 2:
            title_candidates[0].guess = Guess({ 'series': title_candidates[0].clean_value }, confidence = 0.4)
            title_candidates[1].guess = Guess({ 'title':  title_candidates[1].clean_value }, confidence = 0.4)

    # if there's a path group that only contains the season info, then the previous one
    # is most likely the series title (ie: .../series/season X/...)
    eps = [ node for node in mtree.nodes()
            if 'season' in node.guess and 'episodeNumber' not in node.guess ]

    if eps:
        previous = [ node for node in mtree.unidentified_leaves()
                     if node.node_idx[0] == eps[0].node_idx[0] - 1 ]
        if len(previous) == 1:
            previous[0].guess = Guess({ 'series': previous[0].clean_value }, confidence = 0.5)

    # reduce the confidence of unlikely series
    for node in mtree.nodes():
        if 'series' in node.guess:
          if node.guess['series'].lower() in unlikely_series:
              node.guess.set_confidence('series', node.guess.confidence('series') * 0.5)





class IterativeMatcher(object):
    def __init__(self, filename, filetype = 'autodetect'):
        """An iterative matcher tries to match different patterns that appear
        in the filename.

        The 'filetype' argument indicates which type of file you want to match.
        If it is 'autodetect', the matcher will try to see whether it can guess
        that the file corresponds to an episode, or otherwise will assume it is
        a movie.

        The recognized 'filetype' values are:
        [ autodetect, subtitle, movie, moviesubtitle, episode, episodesubtitle ]


        The IterativeMatcher works mainly in 2 steps:

        First, it splits the filename into a match_tree, which is a tree of groups
        which have a semantic meaning, such as episode number, movie title,
        etc...

        The match_tree created looks like the following:

        0000000000000000000000000000000000000000000000000000000000000000000000000000000000 111
        0000011111111111112222222222222233333333444444444444444455555555666777777778888888 000
        0000000000000000000000000000000001111112011112222333333401123334000011233340000000 000
        __________________(The.Prestige).______.[____.HP.______.{__-___}.St{__-___}.Chaps].___
        xxxxxttttttttttttt               ffffff  vvvv    xxxxxx  ll lll     xx xxx         ccc
        [XCT].Le.Prestige.(The.Prestige).DVDRip.[x264.HP.He-Aac.{Fr-Eng}.St{Fr-Eng}.Chaps].mkv

        The first 3 lines indicates the group index in which a char in the
        filename is located. So for instance, x264 is the group (0, 4, 1), and
        it corresponds to a video codec, denoted by the letter'v' in the 4th line.
        (for more info, see guess.matchtree.tree_to_string)


         Second, it tries to merge all this information into a single object
         containing all the found properties, and does some (basic) conflict
         resolution when they arise.
        """

        if filetype not in ('autodetect', 'subtitle', 'video',
                            'movie', 'moviesubtitle',
                            'episode', 'episodesubtitle'):
            raise ValueError, "filetype needs to be one of ('autodetect', 'subtitle', 'video', 'movie', 'moviesubtitle', 'episode', 'episodesubtitle')"
        if not isinstance(filename, unicode):
            log.debug('WARNING: given filename to matcher is not unicode...')

        mtree = MatchTree(filename)
        mtree.guess.set('type', filetype, confidence = 1.0)

        def apply_transfo(transfo_name):
            # FIXME: there should be a more idiomatic way of doing this...
            exec 'from transfo.%s import process' % transfo_name in globals(), locals()
            process(mtree)

        # 1- first split our path into dirs + basename + ext
        # 2- split each of those into explicit groups, if any
        # note: be careful, as this might split some regexps with more confidence such as
        #       Alfleni-Team, or [XCT] or split a date such as (14-01-2008)
        apply_transfo('split_groups')


        # 3- try to match information for specific patterns
        if mtree.guess['type'] in ('episode', 'episodesubtitle'):
            strategy = [ 'guess_date', 'guess_video_rexps', 'guess_episodes_rexps',
                         'guess_website', 'guess_release_group', 'guess_properties',
                         'guess_weak_episodes_rexps', 'guess_language' ]
        else:
            strategy = [ 'guess_date', 'guess_year', 'guess_video_rexps',
                         'guess_website', 'guess_release_group', 'guess_properties',
                         'guess_language' ]

        for name in strategy:
            apply_transfo(name)

        # split into '-' separated subgroups (with required separator chars
        # around the dash)
        apply_transfo('split_on_dash')

        # 4- try to identify the remaining unknown groups by looking at their position
        #    relative to other known elements
        if mtree.guess['type'] in ('episode', 'episodesubtitle'):
            guess_episode_info_from_position(mtree)
        else:
            guess_movie_title_from_position(mtree)

        # 5- perform some post-processing steps
        apply_transfo('post_process')

        log.debug('Found match tree:\n%s' % (to_utf8(tree_to_string(mtree))))

        self.match_tree = mtree


    def matched(self):
        # we need to make a copy here, as the merge functions work in place and
        # calling them on the match tree would modify it

        parts = [ node.guess for node in self.match_tree.nodes() if node.guess ]
        parts = copy.deepcopy(parts)

        # 1- try to merge similar information together and give it a higher confidence
        for int_part in ('year', 'season', 'episodeNumber'):
            merge_similar_guesses(parts, int_part, choose_int)

        for string_part in ('title', 'series', 'container', 'format', 'releaseGroup', 'website',
                            'audioCodec', 'videoCodec', 'screenSize', 'episodeFormat'):
            merge_similar_guesses(parts, string_part, choose_string)

        result = merge_all(parts, append = ['language', 'subtitleLanguage', 'other'])

        # 2- some last minute post-processing
        if (result['type'] == 'episode' and
            'season' not in result and
            result.get('episodeFormat', '') == 'Minisode'):
            result['season'] = 0

        log.debug('Final result: ' + result.nice_string())
        return result

