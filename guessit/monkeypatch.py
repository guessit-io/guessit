#!/usr/bin/env python
"""
Monkeypatch initialisation functions
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any

from rebulk.match import Match


def monkeypatch_rebulk() -> None:
    """Monkeypatch rebulk classes"""

    @property  # type: ignore[misc]
    def match_advanced(self: Match) -> OrderedDict[str, Any]:
        """
        Build advanced dict from match
        :param self:
        :return:
        """

        ret: OrderedDict[str, Any] = OrderedDict()
        ret["value"] = self.value
        if self.raw:
            ret["raw"] = self.raw
        ret["start"] = self.start
        ret["end"] = self.end
        return ret

    Match.advanced = match_advanced  # type: ignore[attr-defined]
