#!/usr/bin/env python
"""
size property
"""

from __future__ import annotations

from typing import Any

from rebulk import Key, Rebulk
from rebulk.remodule import re

from ..common import dash
from ..common.pattern import is_disabled
from ..common.quantity import Size
from ..common.validators import seps_surround

#: Typed key (rebulk 5) binding the ``size`` match name to its :class:`Size` value.
SIZE = Key("size", Size, formatter=Size.fromstring)


def size(config: dict[str, Any]) -> Rebulk:
    """
    Builder for rebulk object.

    :param config: rule configuration
    :type config: dict
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk(disabled=lambda context: is_disabled(context, "size"))
    rebulk.regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])
    rebulk.defaults(validator=seps_surround)
    rebulk.regex(r"\d+-?[mgt]b", r"\d+\.\d+-?[mgt]b", key=SIZE, tags=["release-group-prefix"])

    return rebulk
