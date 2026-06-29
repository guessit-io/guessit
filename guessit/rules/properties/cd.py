#!/usr/bin/env python
"""
cd and cd_count properties
"""

from __future__ import annotations

from typing import Any

from rebulk import Rebulk
from rebulk.remodule import re

from ...config import load_config_patterns
from ..common import dash
from ..common.keys import CD, CD_COUNT
from ..common.pattern import is_disabled


def cd(config: dict[str, Any]) -> Rebulk:
    """
    Builder for rebulk object.

    :param config: rule configuration
    :type config: dict
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk(disabled=lambda context: is_disabled(context, "cd"))
    rebulk = rebulk.regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])

    load_config_patterns(
        rebulk, config, options={None: {"formatter": {"cd": CD.converter, "cd_count": CD_COUNT.converter}}}
    )

    return rebulk
