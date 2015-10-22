#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-self-use, pointless-statement, missing-docstring, invalid-name

from ..__main__ import main

import pytest

import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def test_main_no_args():
    main([])


def test_main_verbose():
    main(['Fear.and.Loathing.in.Las.Vegas.FRENCH.ENGLISH.720p.HDDVD.DTS.x264-ESiR.mkv', '--verbose'])


def test_main_yaml():
    main(['Fear.and.Loathing.in.Las.Vegas.FRENCH.ENGLISH.720p.HDDVD.DTS.x264-ESiR.mkv', '--yaml'])


def test_main_json():
    main(['Fear.and.Loathing.in.Las.Vegas.FRENCH.ENGLISH.720p.HDDVD.DTS.x264-ESiR.mkv', '--json'])


def test_main_show_property():
    main(['Fear.and.Loathing.in.Las.Vegas.FRENCH.ENGLISH.720p.HDDVD.DTS.x264-ESiR.mkv', '-P', 'title'])


def test_main_advanced():
    main(['Fear.and.Loathing.in.Las.Vegas.FRENCH.ENGLISH.720p.HDDVD.DTS.x264-ESiR.mkv', '-a'])


def test_main_input():
    main(['--input', os.path.join(__location__, 'test-input-file.txt')])


def test_main_help():
    with pytest.raises(SystemExit):
        main(['--help'])


def test_main_version():
    main(['--version'])


def test_main_properties():
    main(['--properties'])


def test_main_value():
    main(['--values'])
