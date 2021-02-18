"""
Config module.
"""
from importlib import import_module

from rebulk import Rebulk

_regex_prefix = 're:'
_function_prefix = 'fn:'

_function_cache = {}


def _process_option(name, value):
    if name == 'validator':
        return _process_option_validator(value)
    return value


def _process_option_validator(value):
    if value.startswith(_function_prefix):
        function_id = value[len(_function_prefix):]
        if function_id in _function_cache:
            return _function_cache[function_id]
        if '.' in function_id:
            module_name, func_name = function_id.rsplit('.', 1)
        else:
            module_name = "guessit.rules.common.validators"
            func_name = function_id
        mod = import_module(module_name)
        func = getattr(mod, func_name)
        _function_cache[function_id] = func
        return func
    return value


def load_config_patterns(rebulk: Rebulk,
                         config: dict,
                         pattern_options: dict = None,
                         regex_options: dict = None,
                         string_options: dict = None):
    """
    Load patterns defined in given config.
    :param rebulk: Rebulk builder to use.
    :param config: dict containing pattern definition.
    :return:
    """
    for value, items in config.items():
        patterns = items if isinstance(items, list) else [items]
        for pattern in patterns:
            options = dict(pattern_options) if pattern_options else {}
            if isinstance(pattern, dict):
                options.update(pattern)
                pattern = options.get('pattern')
            else:
                options = {}
            regex = options.get('regex', False)

            if not regex and pattern.startswith(_regex_prefix):
                regex = True
                pattern = pattern[len(_regex_prefix):]

            if regex and regex_options:
                options.update(regex_options)
            elif not regex and string_options:
                options.update(string_options)
            if isinstance(pattern, dict):
                options.update(pattern)

            options.pop('pattern', None)
            options.pop('regex', None)

            options = {name: _process_option(name, value) for name, value in options.items()}

            if regex:
                rebulk.regex(pattern, value=value, **options)
            else:
                rebulk.string(pattern, value=value, **options)
