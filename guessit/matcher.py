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


from date import search_date, search_year
from guessit.guess import Guess
from patterns import websites, properties, sep

def format_guess(guess):
    """Format all the found values to their natural type.
    For instance, a year would be stored as an int value, etc...

    Note that this modifies the dictionary given as input.
    """
    for prop, value in guess.items():
        if prop in ('season', 'episodeNumber', 'year', 'cdNumber', 'cdNumberTotal'):
            guess[prop] = int(guess[prop])
        elif isinstance(value, basestring):
            if prop in ('edition',):
                value = clean_string(value)
            guess[prop] = canonical_form(value)

    return guess


def guess_date(string):
    date, span = search_date(string)
    if date:
        return { 'date': date }, span
    else:
        return None, None

def guess_year(string):
    year, span = search_year(string)
    if year:
        return { 'year': year }, span
    else:
        return None, None

def guess_website(string):
    low = string.lower()
    for site in websites:
        pos = low.find(site.lower())
        if pos != -1:
            return { 'website': site }, (pos, pos+len(site))
    return None, None

def guess_video_rexps(string):
    for rexp, confidence, span_adjust in video_rexps:
        match = re.search(rexp, string, re.IGNORECASE)
        if match:
            metadata = match.groupdict()
            # is this the better place to put it? (maybe, as it is at least the soonest that we can catch it)
            if 'cdNumberTotal' in metadata and metadata['cdNumberTotal'] is None:
                del metadata['cdNumberTotal']
            return (Guess(metadata, confidence = confidence),
                    (match.start() + span_adjust[0],
                     match.end() + span_adjust[1]))

    return None, None

def guess_episodes_rexps(string):
    for rexp, confidence, span_adjust in episode_rexps:
        match = re.search(rexp, string, re.IGNORECASE)
        if match:
            return (Guess(match.groupdict(), confidence = confidence),
                    (match.start() + span_adjust[0],
                     match.end() + span_adjust[1]))

    return None, None

@use_node
def guess_weak_episodes_rexps(string, node):
    if 'episodeNumber' in node.root.info:
        return None, None

    for rexp, span_adjust in weak_episode_rexps:
        match = re.search(rexp, string, re.IGNORECASE)
        if match:
            metadata = match.groupdict()
            span = (match.start() + span_adjust[0], match.end() + span_adjust[1])

            epnum = int(metadata['episodeNumber'])
            if epnum > 100:
                return Guess({ 'season': epnum // 100,
                               'episodeNumber': epnum % 100 }, confidence = 0.6), span
            else:
                return Guess(metadata, confidence = 0.3), span

    return None, None


def guess_release_group(string):
    group_names = [ r'\.(Xvid)-(?P<releaseGroup>.*?)[ \.]',
                    r'\.(DivX)-(?P<releaseGroup>.*?)[\. ]',
                    r'\.(DVDivX)-(?P<releaseGroup>.*?)[\. ]',
                    ]
    for rexp in group_names:
        match = re.search(rexp, string, re.IGNORECASE)
        if match:
            metadata = match.groupdict()
            metadata.update({ 'videoCodec': match.group(1) })
            return metadata, (match.start() + 1, match.end() - 1)

    return None, None

def guess_properties(string):
    low = string.lower()
    for prop, values in properties.items():
        for value in values:
            pos = low.find(value.lower())
            if pos != -1:
                end = pos + len(value)
                # make sure our word is always surrounded by separators
                if ((pos > 0 and low[pos-1] not in sep) or
                    (end < len(low) and low[end] not in sep)):
                    # note: sep is a regexp, but in this case using it as
                    #       a sequence achieves the same goal
                    continue
                return { prop: value }, (pos, end)

    return None, None


def guess_language(string):
    language, span, confidence = search_language(string)
    if language:
        # is it a subtitle language?
        if 'sub' in clean_string(string[:span[0]]).lower().split(' '):
            return Guess({ 'subtitleLanguage': language }, confidence = confidence), span
        else:
            return Guess({ 'language': language }, confidence = confidence), span

    return None, None


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




def post_process(mtree):
    # 1- try to promote language to subtitle language where it makes sense
    for node in mtree.nodes():
        if 'language' not in node.guess:
            continue

        def promote_subtitle():
            node.guess.set('subtitleLanguage', node.guess['language'], confidence = node.guess.confidence('language'))
            del node.guess['language']

        # - if we matched a language in a file with a sub extension and that the group
        #   is the last group of the filename, it is probably the language of the subtitle
        #   (eg: 'xxx.english.srt')
        if (mtree.node_at((-1,)).value.lower() in subtitle_exts and
            node == mtree.leaves()[-2]):
            promote_subtitle()

        # - if a language is in an explicit group just preceded by "st", it is a subtitle
        #   language (eg: '...st[fr-eng]...')
        try:
            idx = node.node_idx
            previous = mtree.node_at((idx[0], idx[1]-1)).leaves()[-1]
            if previous.value.lower()[-2:] == 'st':
                promote_subtitle()
        except:
            pass

    # 2- ", the" at the end of a series title should be prepended to it
    for node in mtree.nodes():
        if 'series' not in node.guess:
            continue

        series = node.guess['series']
        lseries = series.lower()

        if lseries[-4:] == ',the':
            node.guess['series'] = 'The ' + series[:-4]

        if lseries[-5:] == ', the':
            node.guess['series'] = 'The ' + series[:-5]


def find_and_split_node(node, strategy):
    string = ' %s ' % node.value # add sentinels
    for matcher, confidence in strategy:
        if getattr(matcher, 'use_node', False):
            result, span = matcher(string, node)
        else:
            result, span = matcher(string)

        if result:
            span = (span[0]-1, span[1]-1) # readjust span to compensate for sentinels
            if isinstance(result, Guess):
                if confidence is None:
                    confidence = result.confidence(result.keys()[0])
            else:
                if confidence is None:
                    confidence = 1.0

            guess = format_guess(Guess(result, confidence = confidence))
            log.debug('Found with confidence %.2f: %s' % (confidence, guess))

            node.partition(span)
            absolute_span = (span[0] + node.offset, span[1] + node.offset)
            for child in node.children:
                if child.span == absolute_span:
                    child.guess = guess
                else:
                    find_and_split_node(child, strategy)
            return



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

        # 1- first split our path into dirs + basename + ext
        split_path_components(mtree)

        # try to detect the file type
        filetype, other = guess_filetype(filename, filetype)
        mtree.guess = Guess({ 'type': filetype }, confidence = 1.0)
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

        # strategy is a list of pairs (guesser, confidence)
        # - if the guesser returns a guessit.Guess and confidence is specified,
        #   it will override it, otherwise it will leave the guess confidence
        # - if the guesser returns a simple dict as a guess and confidence is
        #   specified, it will use it, or 1.0 otherwise
        movie_strategy = [ (guess_date, 1.0),
                           (guess_year, 1.0),
                           (guess_video_rexps, None),
                           (guess_website, 1.0),
                           (guess_release_group, 0.8),
                           (guess_properties, 1.0),
                           (guess_language, None)
                           ]

        episode_strategy = [ (guess_date, 1.0),
                             (guess_video_rexps, None),
                             (guess_episodes_rexps, None),
                             (guess_website, 1.0),
                             (guess_release_group, 0.8),
                             (guess_properties, 1.0),
                             (guess_weak_episodes_rexps, 0.6),
                             (guess_language, None)
                           ]

        if mtree.guess['type'] in ('episode', 'episodesubtitle'):
            strategy = episode_strategy
        else:
            strategy = movie_strategy

        # 3- try to match information for specific patterns
        for node in mtree.nodes_at_depth(2):
            find_and_split_node(node, strategy)

        # split into '-' separated subgroups (with required separator chars
        # around the dash)
        for node in mtree.unidentified_leaves():
            indices = []
            didx = node.value.find('-')
            while didx > 0:
                indices.extend([ didx, didx+1 ])
                didx = node.value.find('-', didx+1)
            if indices:
                node.partition(indices)


        # 4- try to identify the remaining unknown groups by looking at their position
        #    relative to other known elements
        if mtree.guess['type'] in ('episode', 'episodesubtitle'):
            guess_episode_info_from_position(mtree)
        else:
            guess_movie_title_from_position(mtree)

        # 5- perform some post-processing steps
        post_process(mtree)

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

