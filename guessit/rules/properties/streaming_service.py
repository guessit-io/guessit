#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
streaming_service property
"""
from rebulk import Rebulk
from rebulk.rules import Rule, RemoveMatch

from ...rules.common import seps
from ...rules.common.validators import seps_surround


def streaming_service():
    """Streaming service property.

    :return:
    :rtype: Rebulk
    """
    rebulk = Rebulk().string_defaults(ignore_case=True)
    rebulk.defaults(name='streaming_service', validator=seps_surround)

    rebulk.string('AE', value='A&E')
    rebulk.string('AMBC', value='ABC')
    rebulk.string('AMZN', value='Amazon Prime')
    rebulk.string('AS', value='Adult Swim')
    rebulk.string('iP', value='BBC iPlayer')
    rebulk.string('CBS', value='CBS')
    rebulk.string('CC', value='Comedy Central')
    rebulk.string('CR', value='Crunchy Roll')
    rebulk.string('CW', value='The CW')
    rebulk.string('DISC', value='Discovery')
    rebulk.string('DSNY', value='Disney')
    rebulk.string('EPIX', value='ePix')
    rebulk.string('HBO', value='HBO Go')
    rebulk.string('HIST', value='History')
    rebulk.string('IFC', value='IFC')
    rebulk.string('PBS', value='PBS')
    rebulk.string('NATG', value='National Geographic')
    rebulk.string('NBA', value='NBA TV')
    rebulk.string('NBC', value='NBC')
    rebulk.string('NFL', value='NFL')
    rebulk.string('NICK', value='Nickelodeon')
    rebulk.string('NF', value='Netflix')
    rebulk.string('SESO', value='SeeSo')
    rebulk.string('SPKE', value='Spike TV')
    rebulk.string('SYFY', value='Syfy')
    rebulk.string('TFOU', value='TFou')
    rebulk.string('TVL', value='TV Land')
    rebulk.string('UFC', value='UFC')

    rebulk.rules(ValidateStreamingService)

    return rebulk


class ValidateStreamingService(Rule):
    """Validate streaming service matches."""

    priority = 32
    consequence = RemoveMatch

    def when(self, matches, context):
        """Streaming service is always before format.

        :param matches:
        :type matches: rebulk.match.Matches
        :param context:
        :type context: dict
        :return:
        """
        to_remove = []
        for service in matches.named('streaming_service'):
            next_match = matches.next(service, predicate=lambda match: match.name == 'format', index=0)
            if next_match and not matches.holes(service.end, next_match.start,
                                                predicate=lambda match: match.value.strip(seps)):
                if service.value == 'Comedy Central':
                    # Current match is a valid streaming service, removing invalid closed caption (CC) matches
                    to_remove.extend(matches.named('other', predicate=lambda match: match.value == 'CC'))
                continue

            to_remove.append(service)

        return to_remove
