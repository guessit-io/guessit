#!/usr/bin/env python
"""
size property
"""
from rebulk import Rebulk
from rebulk.remodule import re

from ..common import dash
from ..common.pattern import is_disabled
from ..common.quantity import Size
from ..common.validators import seps_surround


def size(config):
    """
    Builder for rebulk object.

    :param config: rule configuration
    :type config: dict
    :return: Created Rebulk object
    :rtype: Rebulk
    """
    rebulk = Rebulk(disabled=lambda context: is_disabled(context, 'size'))
    rebulk.regex_defaults(flags=re.IGNORECASE, abbreviations=[dash])
    rebulk.defaults(name='size', validator=seps_surround)
    rebulk.regex(r'\d+-?[mgt]b', r'\d+\.\d+-?[mgt]b', formatter=Size.fromstring, tags=['release-group-prefix'])

    return rebulk
