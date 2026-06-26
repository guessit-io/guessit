#!/usr/bin/env python
"""
JSON Utils
"""
import json

from rebulk.match import Match
from six import text_type


class GuessitEncoder(json.JSONEncoder):
    """
    JSON Encoder for guessit response
    """

    def default(self, o):
        if isinstance(o, Match):
            return o.advanced
        if hasattr(o, 'name'):  # Babelfish languages/countries long name
            return text_type(o.name)
        # pragma: no cover
        return text_type(o)
