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

from guessit.patterns import sep

# string cleaning related functions

def stripBrackets(s):
    if not s:
        return s
    if s[0] == '[' and s[-1] == ']': return s[1:-1]
    if s[0] == '(' and s[-1] == ')': return s[1:-1]
    if s[0] == '{' and s[-1] == '}': return s[1:-1]
    return s

def find_any(s, chars):
    """Return the index of the first appearence of any char from chars in s.
    If no such character appear, return the length of the string (and not -1!!)."""
    pos = len(s)
    for c in chars:
        try:
            pos = min(pos, s.index(c))
        except ValueError: pass

    return pos

def clean_string(s):
    for c in sep:
        s = s.replace(c, ' ')
    parts = s.split()
    return ' '.join(p for p in parts if p != '')

# needed for the new Matcher

from guessit.patterns import deleted

def str_replace(string, pos, c):
    return string[:pos] + c + string[pos+1:]

def blank_region(string, region, blank_sep = deleted):
    start, end = region
    return string[:start] + blank_sep * (end - start) + string[end:]


def find_first_level_groups_span(string, enclosing):
    """Return a list of pairs (start, end) for the groups delimited by the given
    enclosing characters.
    This does not return nested groups, ie: '(ab(c)(d))' will return a single group
    containing the whole string.

    >>> find_first_level_groups_span('abcd', '()')
    []

    >>> find_first_level_groups_span('abc(de)fgh', '()')
    [(3, 7)]

    >>> find_first_level_groups_span('(ab(c)(d))', '()')
    [(0, 10)]

    >>> find_first_level_groups_span('ab[c]de[f]gh(i)', '[]')
    [(2, 5), (7, 10)]
    """
    opening, closing = enclosing
    depth = [] # depth is a stack of indices where we opened a group
    result = []
    for i, c, in enumerate(string):
        if c == opening:
            depth.append(i)
        elif c == closing:
            try:
                start = depth.pop()
                end = i
                if not depth:
                    # we emptied our stack, so we have a 1st level group
                    result.append((start, end+1))
            except IndexError:
                # we closed a group which was not opened before
                pass

    return result


def split_on_groups(string, groups):
    """Split the given string using the different known groups for boundaries.

    >>> split_on_groups('0123456789', [ (2, 4) ])
    ['01', '23', '456789']

    >>> split_on_groups('0123456789', [ (2, 4), (4, 6) ])
    ['01', '23', '45', '6789']

    >>> split_on_groups('0123456789', [ (5, 7), (2, 4) ])
    ['01', '23', '4', '56', '789']

    """
    if not groups:
        return [ string ]

    boundaries = sorted(set(reduce(lambda l, x: l + list(x), groups, [])))
    if boundaries[0] != 0:
        boundaries.insert(0, 0)
    if boundaries[-1] != len(string):
        boundaries.append(len(string))

    groups = [ string[start:end] for start, end in zip(boundaries[:-1], boundaries[1:]) ]

    return filter(bool, groups) # return only non-empty groups




def find_first_level_groups(string, enclosing, blank_sep = None):
    """Return a list of groups that could be split because of explicit grouping.
    The groups are delimited by the given enclosing characters.

    You can also specify if you want to blank the separator chars in the returned
    list of groups by specifying a character for it. None means it won't be replaced.

    This does not return nested groups, ie: '(ab(c)(d))' will return a single group
    containing the whole string.

    >>> find_first_level_groups('', '()')
    ['']

    >>> find_first_level_groups('abcd', '()')
    ['abcd']

    >>> find_first_level_groups('abc(de)fgh', '()')
    ['abc', '(de)', 'fgh']

    >>> find_first_level_groups('(ab(c)(d))', '()', blank_sep = '_')
    ['_ab(c)(d)_']

    >>> find_first_level_groups('ab[c]de[f]gh(i)', '[]')
    ['ab', '[c]', 'de', '[f]', 'gh(i)']

    >>> find_first_level_groups('()[]()', '()', blank_sep = '-')
    ['--', '[]', '--']

    """
    groups = find_first_level_groups_span(string, enclosing)
    if blank_sep:
        for start, end in groups:
            string = str_replace(string, start, blank_sep)
            string = str_replace(string, end-1, blank_sep)

    return split_on_groups(string, groups)



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

def matchAllRegexpWithSpan(string, regexps):
    """Matches the string against a list of regexps (using named match groups) and
    returns a list of all found matches coupled with their full group span."""
    result = []
    for regexp in regexps:
        s = string
        rexp = re.compile(regexp, re.IGNORECASE)
        match = rexp.search(s)
        while match:
            result.append((match.groupdict(), match.span()))
            s = s[match.span()[1]:]
            match = rexp.search(s)
    return result

def matchAllRegexp(string, regexps):
    """Matches the string against a list of regexps (using named match groups) and
    returns a list of all found matches."""
    return [ match for match, span in matchAllRegexpWithSpan(string, regexps) ]

def matchAllRegexpMinIndex(string, regexps):
    """Matches the string against a list of regexps (using named match groups) and
    returns a list of all found matches, as well as the index of the beginning of the
    first match group."""
    result = []
    minidx = len(string)
    for regexp in regexps:
        s = string
        removed = 0
        rexp = re.compile(regexp, re.IGNORECASE)
        match = rexp.search(s)
        while match:
            result.append(match.groupdict())
            beg, end = match.span()
            minidx = min(minidx, beg+removed)
            s = s[end:]
            removed += end
            match = rexp.search(s)
    return result, minidx

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
