#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessIt - A library for guessing information from filenames
# Copyright (c) 2011 Nicolas Wack <wackou@gmail.com>
#
# GuessIt is free software; you can redistribute it and/or modify it under
# the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessIt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import datetime
import re

def search_date(string):
    """Looks for date patterns, and if found return the date and group span.
    Assumes there are sentinels at the beginning and end of the string that
    always allow matching a non-digit delimiting the date."""
    dsep = r'[-/]'

    date_rexps = [ r'[^0-9]' +
                   r'(?P<year>[0-9]{4})' +
                   r'(?P<month>[0-9]{2})' +
                   r'(?P<day>[0-9]{2})' +
                   r'[^0-9]',

                   r'[^0-9]' +
                   r'(?P<year>[0-9]{4})' + dsep +
                   r'(?P<month>[0-9]{2})' + dsep +
                   r'(?P<day>[0-9]{2})' +
                   r'[^0-9]',

                   r'[^0-9]' +
                   r'(?P<day>[0-9]{2})' + dsep +
                   r'(?P<month>[0-9]{2})' + dsep +
                   r'(?P<year>[0-9]{4})' +
                   r'[^0-9]'
                   ]

    for drexp in date_rexps:
        match = re.search(drexp, string)

        if match:
            d = match.groupdict()
            year, month, day = int(d['year']), int(d['month']), int(d['day'])
            date = None
            try:
                date = datetime.date(year, month, day)
            except ValueError:
                try:
                    date = datetime.date(year, day, month)
                except ValueError:
                    pass

            if date is None:
                continue

            # check date plausibility
            if not 1900 < date.year < datetime.date.today().year + 5:
                continue

            # looks like we have a valid date
            # note: span is  [+1,-1] because we don't want to include the non-digit char
            start, end = match.span()
            return (date, (start+1, end-1))

    return None, None
