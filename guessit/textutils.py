#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Smewt - A smart collection manager
# Copyright (c) 2008 Nicolas Wack <wackou@gmail.com>
#
# Smewt is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Smewt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# string cleaning related functions

def stripBrackets(s):
    if not s:
        return s
    if s[0] == '[' and s[-1] == ']': return s[1:-1]
    if s[0] == '(' and s[-1] == ')': return s[1:-1]
    if s[0] == '{' and s[-1] == '}': return s[1:-1]
    return s


def cleanString(s):
    for c in ('.', '-', '_'):
        s = s.replace(c, ' ')
    parts = s.split()
    return ' '.join(p for p in parts if p != '')

# regexps-related functions
import re

def simpleMatch(string, regexp):
    try:
        return re.compile(regexp).search(string).groups()[0]
    except IndexError:
        raise ValueError("'%s' Does not match regexp '%s'" % (string, regexp))

def matchRegexp(string, regexp):
    """Tries to match the given string against the regexp (using named match groups)
    and raises a SmewtException if it didn't match."""
    match = re.compile(regexp, re.IGNORECASE | re.DOTALL).search(string)
    if match:
        return match.groupdict()
    raise ValueError("'%s' Does not match regexp '%s'" % (string, regexp))

def matchAllRegexp(string, regexps):
    """Matches the string against a list of regexps (using named match groups) and
    returns a list of all found matches."""
    result = []
    for regexp in regexps:
        s = string
        rexp = re.compile(regexp, re.IGNORECASE)
        match = rexp.search(s)
        while match:
            result.append(match.groupdict())
            s = s[match.span()[1]:]
            match = rexp.search(s)
    return result

def matchAnyRegexp(string, regexps):
    """Matches the string against a list of regexps (using named match groups) and
    returns the first match it could find, None if not found."""
    for regexp in regexps:
        result = re.compile(regexp, re.IGNORECASE).search(string)
        if result:
            return result.groupdict()
    return None

def multipleMatchRegexp(string, regexp):
    """Matches the given string against the regexp (using named match groups) and returns
    a list of all found matches in the string"""
    rexp = re.compile(regexp, re.IGNORECASE | re.DOTALL)
    result = []
    while True:
        match = rexp.search(string)
        if match:
            result += [ match.groupdict() ]
            # keep everything after what's been matched, and try to match again
            string = string[match.end(match.lastindex):]
        else:
            return result


#string-related functions

def between(s, left, right):
    return s.split(left)[1].split(right)[0]

def toUtf8(o):
    '''converts all unicode strings found in the given object to utf-8 strings'''

    if isinstance(o, unicode):
        return o.encode('utf-8')
    elif isinstance(o, list):
        return [ toUtf8(i) for i in o ]
    elif isinstance(o, dict):
        result = {}
        for key, value in o.items():
            result[toUtf8(key)] = toUtf8(value)
        return result

    else:
        return o


def levenshtein(a, b):
    if not a: return len(b)
    if not b: return len(a)

    m = len(a)
    n = len(b)
    d = []
    for i in range(m+1):
        d.append([0] * (n+1))

    for i in range(m+1):
        d[i][0] = i

    for j in range(n+1):
        d[0][j] = j

    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]:
                cost = 0
            else:
                cost = 1

            d[i][j] = min(d[i-1][j] + 1,     # deletion
                          d[i][j-1] + 1,     # insertion
                          d[i-1][j-1] + cost # substitution
                          )

    return d[m][n]
