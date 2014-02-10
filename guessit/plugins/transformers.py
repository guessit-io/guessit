#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2013 Nicolas Wack <wackou@gmail.com>
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

from __future__ import absolute_import, division, print_function, unicode_literals

from stevedore import ExtensionManager
from pkg_resources import EntryPoint

from stevedore.extension import Extension
from guessit.guess import Guess
from logging import getLogger

log = getLogger(__name__)


class Transformer(object):
    def __init__(self, priority=0):
        self.priority = priority
        self.log = getLogger(self.name)

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def fullname(self):
        return self.__module__ + "." + self.__class__.__name__

    def supported_properties(self):
        return {}

    def enabled(self):
        return True

    def second_pass_options(self, mtree, options={}):
        return (None, None)

    def should_process(self, mtree, options={}):
        return True

    def process(self, mtree, options={}, *args, **kwargs):
        pass

    def post_process(self, mtree, options={}, *args, **kwargs):
        pass

    def rate_quality(self, guess, *props):
        return 0


class TransfoException(Exception):
    def __init__(self, transformer, message):

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)

        self.transformer = transformer


def found_property(node, name, confidence):
    node.guess = Guess({name: node.clean_value}, confidence=confidence)
    log.debug('Found with confidence %.2f: %s' % (confidence, node.guess))


def find_and_split_node(node, strategy, skip_nodes, logger, partial_span=None):
    value = None
    if partial_span:
        value = node.value[partial_span[0]:partial_span[1]]
    else:
        value = node.value
    string = ' %s ' % value  # add sentinels
    for matcher, confidence, args, kwargs in strategy:
        all_args = [string, node]
        if args:
            all_args.append(args)

        if kwargs:
            matcher_result = matcher(*all_args, **kwargs)
        else:
            matcher_result = matcher(*all_args)

        if matcher_result:
            if not isinstance(matcher_result, Guess):
                result, span = matcher_result
            else:
                result, span = matcher_result, matcher_result.metadata().span

            if result:
                # readjust span to compensate for sentinels
                span = (span[0] - 1, span[1] - 1)

                # readjust span to compensate for partial_span
                if partial_span:
                    span = (span[0] + partial_span[0], span[1] + partial_span[0])

                partition_spans = None
                for skip_node in skip_nodes:
                    if skip_node.parent.node_idx == node.node_idx[:len(skip_node.parent.node_idx)] and\
                        skip_node.span == span:
                        partition_spans = node.get_partition_spans(skip_node.span)
                        partition_spans.remove(skip_node.span)
                        break

                if not partition_spans:
                    # restore sentinels compensation

                    guess = None
                    if isinstance(result, Guess):
                        if confidence is None:
                            confidence = result.confidence()
                        guess = result
                    else:
                        if confidence is None:
                            confidence = 1.0
                        guess = Guess(result, confidence=confidence, input=string, span=span)

                    msg = 'Found with confidence %.2f: %s' % (confidence, guess)
                    (logger or log).debug(msg)

                    node.partition(span)
                    absolute_span = (span[0] + node.offset, span[1] + node.offset)
                    for child in node.children:
                        if child.span == absolute_span:
                            child.guess = guess
                        else:
                            find_and_split_node(child, strategy, skip_nodes, logger)
                else:
                    for partition_span in partition_spans:
                        find_and_split_node(node, strategy, skip_nodes, logger, partition_span)


class SingleNodeGuesser(object):
    def __init__(self, guess_func, confidence, logger, *args, **kwargs):
        self.guess_func = guess_func
        self.confidence = confidence
        self.logger = logger
        self.skip_nodes = kwargs.pop('skip_nodes', [])
        self.args = args
        self.kwargs = kwargs

    def process(self, mtree):
        # strategy is a list of pairs (guesser, confidence)
        # - if the guesser returns a guessit.Guess and confidence is specified,
        #   it will override it, otherwise it will leave the guess confidence
        # - if the guesser returns a simple dict as a guess and confidence is
        #   specified, it will use it, or 1.0 otherwise
        strategy = [(self.guess_func, self.confidence, self.args, self.kwargs)]

        for node in mtree.unidentified_leaves():
            find_and_split_node(node, strategy, self.skip_nodes, self.logger)


class CustomTransformerExtensionManager(ExtensionManager):
    def __init__(self, namespace='guessit.transformer', invoke_on_load=True,
        invoke_args=(), invoke_kwds={}, propagate_map_exceptions=True, on_load_failure_callback=None,
                 verify_requirements=False):
        super(CustomTransformerExtensionManager, self).__init__(namespace=namespace,
                 invoke_on_load=invoke_on_load,
                 invoke_args=invoke_args,
                 invoke_kwds=invoke_kwds,
                 propagate_map_exceptions=propagate_map_exceptions,
                 on_load_failure_callback=on_load_failure_callback,
                 verify_requirements=verify_requirements)

    def order_extensions(self, extensions):
        """Order the loaded transformers

        It should follow those rules
           - website before language (eg: tvu.org.ru vs russian)
           - language before episodes_rexps
           - properties before language (eg: he-aac vs hebrew)
           - release_group before properties (eg: XviD-?? vs xvid)
        """
        if extensions is None:
            extensions = self.extensions
        extensions.sort(key=lambda ext: -ext.obj.priority)
        return extensions

    def _load_one_plugin(self, ep, invoke_on_load, invoke_args, invoke_kwds, verify_requirements):
        if not ep.dist:
            plugin = ep.load(require=False)
        else:
            plugin = ep.load(require=verify_requirements)
        if invoke_on_load:
            obj = plugin(*invoke_args, **invoke_kwds)
        else:
            obj = None
        return Extension(ep.name, ep, plugin, obj)

    def _load_plugins(self, invoke_on_load, invoke_args, invoke_kwds, verify_requirements):
        return self.order_extensions(super(CustomTransformerExtensionManager, self)._load_plugins(invoke_on_load, invoke_args, invoke_kwds, verify_requirements))

    def objects(self):
        return self.map(self._get_obj)

    def _get_obj(self, ext):
        return ext.obj

    def object(self, name):
        try:
            return self[name].obj
        except KeyError:
            return None

    def register_module(self, name, module_name):
        ep = EntryPoint(name, module_name)
        loaded = self._load_one_plugin(ep, invoke_on_load=True, invoke_args=(), invoke_kwds={})
        if loaded:
            self.extensions.append(loaded)
            self.extensions = self.order_extensions(self.extensions)
            self._extensions_by_name = None


class DefaultTransformerExtensionManager(CustomTransformerExtensionManager):
    @property
    def _internal_entry_points(self):
        return ['split_path_components = guessit.transfo.split_path_components:SplitPathComponents',
                                    'guess_filetype = guessit.transfo.guess_filetype:GuessFiletype',
                                    'split_explicit_groups = guessit.transfo.split_explicit_groups:SplitExplicitGroups',
                                    'guess_date = guessit.transfo.guess_date:GuessDate',
                                    'guess_website = guessit.transfo.guess_website:GuessWebsite',
                                    'guess_release_group = guessit.transfo.guess_release_group:GuessReleaseGroup',
                                    'guess_properties = guessit.transfo.guess_properties:GuessProperties',
                                    'guess_language = guessit.transfo.guess_language:GuessLanguage',
                                    'guess_video_rexps = guessit.transfo.guess_video_rexps:GuessVideoRexps',
                                    'guess_episodes_rexps = guessit.transfo.guess_episodes_rexps:GuessEpisodesRexps',
                                    'guess_weak_episodes_rexps = guessit.transfo.guess_weak_episodes_rexps:GuessWeakEpisodesRexps',
                                    'guess_bonus_features = guessit.transfo.guess_bonus_features:GuessBonusFeatures',
                                    'guess_year = guessit.transfo.guess_year:GuessYear',
                                    'guess_country = guessit.transfo.guess_country:GuessCountry',
                                    'guess_idnumber = guessit.transfo.guess_idnumber:GuessIdnumber',
                                    'split_on_dash = guessit.transfo.split_on_dash:SplitOnDash',
                                    'guess_episode_info_from_position = guessit.transfo.guess_episode_info_from_position:GuessEpisodeInfoFromPosition',
                                    'guess_movie_title_from_position = guessit.transfo.guess_movie_title_from_position:GuessMovieTitleFromPosition']

    def _find_entry_points(self, namespace):
        entry_points = {}
        # Internal entry points
        if namespace == self.namespace:
            for internal_entry_point_str in self._internal_entry_points:
                internal_entry_point = EntryPoint.parse(internal_entry_point_str)
                entry_points[internal_entry_point.name] = internal_entry_point

        # Package entry points
        setuptools_entrypoints = super(DefaultTransformerExtensionManager, self)._find_entry_points(namespace)
        for setuptools_entrypoint in setuptools_entrypoints:
            entry_points[setuptools_entrypoint.name] = setuptools_entrypoint

        return list(entry_points.values())

_extensions = None


def all_transformers():
    return _extensions.objects()


def get_transformer(name):
    return _extensions.object(name)


def add_transformer(name, module_name):
    _extensions.register_module(name, module_name)


def reload(custom=False):
    """
    Reload extension manager with default or custom one.
    :param custom: if True, custom manager will be used, else default one.
    Default manager will load default extensions from guessit and setuptools packaging extensions
    Custom manager will not load default extensions from guessit, using only setuptools packaging extensions.
    :type custom: boolean
    """
    global _extensions
    if custom:
        _extensions = CustomTransformerExtensionManager()
    else:
        _extensions = DefaultTransformerExtensionManager()

reload()
