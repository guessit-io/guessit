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

    def _load_plugins(self, invoke_on_load, invoke_args, invoke_kwds):
        return self.order_extensions(EnabledExtensionManager._load_plugins(self, invoke_on_load, invoke_args, invoke_kwds))

    def _get_obj(self, ext):
        return ext.obj

extensions = None
def load():
    global extensions
    extensions = TransformerExtensionManager()
