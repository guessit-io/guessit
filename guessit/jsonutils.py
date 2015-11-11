#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JSON Utils
"""
from collections import OrderedDict
import json

from rebulk.match import Match


class GuessitEncoder(json.JSONEncoder):
    """
    JSON Encoder for guessit response
    """

    def default(self, o):  # pylint:disable=method-hidden
        if isinstance(o, Match):
            ret = OrderedDict()
            ret['value'] = o.value
            if o.raw:
                ret['raw'] = o.raw
            ret['start'] = o.start
            ret['end'] = o.end
            return ret
        elif hasattr(o, 'name'):  # Babelfish languages/countries long name
            return o.name
        else:  # pragma: no cover
            return str(o)
