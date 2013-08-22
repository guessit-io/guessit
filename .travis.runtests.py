#!/usr/bin/env python

import subprocess
import os

def local(cmd, envvars=None):
    if not envvars:
        subprocess.Popen(cmd.split()).communicate()
        return

    env = os.environ
    for var, value in envvars.items():
        env[var] = value
    subprocess.Popen(cmd.split(), env=env).communicate()



def doctests():
    local('nosetests --with-doctest -vv guessit')


TESTS = ['episode', 'movie', 'autodetect', 'autodetect_all', 'language',
         'utils', 'matchtree']

def unittests():
    for t in TESTS:
        local('python tests/test_%s.py' % t, envvars={'PYTHONPATH': '.'})

if __name__ == '__main__':
    doctests()
    unittests()