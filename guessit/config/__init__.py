"""
Config module.
"""
from rebulk import Rebulk

_regex_prefix = 're:'


def load_config_patterns(rebulk: Rebulk, config: dict):
    """
    Load patterns defined in given config.
    :param rebulk: Rebulk builder to use.
    :param config: dict containing pattern definition.
    :return:
    """
    for value, items in config.items():
        patterns = items if isinstance(items, list) else [items]
        for pattern in patterns:
            if isinstance(pattern, dict):
                kwargs = dict(pattern)
                pattern = kwargs.pop('pattern')
            else:
                kwargs = {}
            regex = kwargs.pop('regex', False)
            if not regex and pattern.startswith(_regex_prefix):
                regex = True
                pattern = pattern[len(_regex_prefix):]
            if regex:
                rebulk.regex(pattern, value=value, **kwargs)
            else:
                rebulk.string(pattern, value=value, **kwargs)
