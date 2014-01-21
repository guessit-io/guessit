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

from stevedore import EnabledExtensionManager
from pkg_resources import EntryPoint

from stevedore.extension import Extension


def _is_enabled(extension):
    return extension.obj.enabled()


class TransformerExtensionManager(EnabledExtensionManager):
    def __init__(self, namespace='guessit.transformer', check_func=_is_enabled, invoke_on_load=True,
        invoke_args=(), invoke_kwds={},
        propagate_map_exceptions=True):
        EnabledExtensionManager.__init__(self, namespace, check_func, invoke_on_load=invoke_on_load,
                                         invoke_args=invoke_args, invoke_kwds=invoke_kwds,
                                         propagate_map_exceptions=propagate_map_exceptions)

    def __iter__(self):
        return EnabledExtensionManager.__iter__(self)

    def objects(self):
        return self.map(self._get_obj)

    def _find_entry_points(self, namespace):
        entry_points = {}
        # Internal entry points
        if namespace == 'guessit.transformer':
            internal_entry_points_str = ['split_path_components = guessit.transfo.split_path_components:SplitPathComponents',
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
                                    'guess_movie_title_from_position = guessit.transfo.guess_movie_title_from_position:GuessMovieTitleFromPosition',
                                    'post_process = guessit.transfo.post_process:PostProcess']
            for internal_entry_point_str in internal_entry_points_str:
                internal_entry_point = EntryPoint.parse(internal_entry_point_str)
                entry_points[internal_entry_point.name] = internal_entry_point

        # Package entry points
        setuptools_entrypoints = super(EnabledExtensionManager, self)._find_entry_points(namespace)
        for setuptools_entrypoint in setuptools_entrypoints:
            entry_points[setuptools_entrypoint.name] = setuptools_entrypoint

        return list(entry_points.values())

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

    def _load_one_plugin(self, ep, invoke_on_load, invoke_args, invoke_kwds):
        if not ep.dist:
            plugin = ep.load(require=False)
        else:
            plugin = ep.load()
        if invoke_on_load:
            obj = plugin(*invoke_args, **invoke_kwds)
        else:
            obj = None
        return Extension(ep.name, ep, plugin, obj)

    def _load_plugins(self, invoke_on_load, invoke_args, invoke_kwds):
        return self.order_extensions(EnabledExtensionManager._load_plugins(self, invoke_on_load, invoke_args, invoke_kwds))

    def _get_obj(self, ext):
        return ext.obj

extensions = TransformerExtensionManager()
