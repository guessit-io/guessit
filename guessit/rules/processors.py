#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Processors
"""
from rebulk import Rebulk


def prefer_last_path(matches):
    """
    If multiple match are found, keep the one in filename part.

    :param matches:
    :param context:
    :return:
    """
    for name in matches.names:
        named_list = matches.named(name)
        if len(named_list) > 1:
            keep_list = []
            for named in named_list:
                marker = matches.markers.at_match(named,
                                                  lambda marker: marker.name == 'path' and 'last' in marker.tags, 0)
                if marker:
                    keep_list.append(named)
            if keep_list:
                for named in named_list:
                    if named not in keep_list:
                        matches.remove(named)


PROCESSORS = Rebulk().processor(prefer_last_path)
