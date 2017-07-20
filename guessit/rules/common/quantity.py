#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quantity
"""
import re

import six


class Quantity(object):
    """
    Represent a quantity object with magnitude and units.
    """

    parser_re = re.compile(r'(?P<magnitude>\d+(?:[.]\d+)?)(?P<units>[^\d]+)')

    def __init__(self, magnitude, units):
        self.magnitude = magnitude
        self.units = units

    @classmethod
    def fromstring(cls, string):
        """
        Parse the string into a quantity object.
        :param string:
        :return:
        """
        values = cls.parser_re.match(string).groupdict()
        try:
            magnitude = int(values['magnitude'])
        except ValueError:
            magnitude = float(values['magnitude'])
        units = values['units'].upper()

        return Quantity(magnitude, units)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, six.string_types):
            return str(self) == other
        if not isinstance(other, Quantity):
            return NotImplemented
        return self.magnitude == other.magnitude and self.units == other.units

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '<Quantity [{0}]>'.format(self)

    def __str__(self):
        return '{0}{1}'.format(self.magnitude, self.units)
