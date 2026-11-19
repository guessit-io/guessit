#!/usr/bin/env python
"""
JSON Utils
"""

import json
from typing import Any

from rebulk.match import Match


class GuessitEncoder(json.JSONEncoder):
    """
    JSON Encoder for guessit response
    """

    def default(self, o: Any) -> Any:
        if isinstance(o, Match):
            return o.advanced  # type: ignore[attr-defined]
        if hasattr(o, "name"):  # Babelfish languages/countries long name
            return str(o.name)
        # pragma: no cover
        return str(o)
