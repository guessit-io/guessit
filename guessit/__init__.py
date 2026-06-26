#!/usr/bin/env python
"""
Extracts as much information as possible from a video file.
"""
from . import monkeypatch as _monkeypatch
from .__version__ import __version__
from .api import GuessItApi, guessit
from .options import ConfigurationException
from .rules.common.quantity import Size

__all__ = ['__version__', 'GuessItApi', 'guessit', 'ConfigurationException', 'Size']

_monkeypatch.monkeypatch_rebulk()
