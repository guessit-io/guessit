#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-self-use, pointless-statement, missing-docstring, invalid-name
import pytest


from ..__main__ import main


def test_main_no_args():
    main()
