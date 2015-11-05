#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mimetype property
"""
import mimetypes

from rebulk.match import Match


def mimetype_processor(matches):
    """
    Mimetype post processor
    :param matches:
    :type matches:
    :return:
    :rtype:
    """
    mime, _ = mimetypes.guess_type(matches.input_string, strict=False)
    if mime is not None:
        matches.append(Match(0, len(matches.input_string), name='mimetype', value=mime))
