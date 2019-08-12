import math
import numpy

import utils
from utils.cycles import filter_timeline_actions


def avg(lis, exception=0.0, cycles=False):
    """
    Shamelessly stolen almost verbatim from 1678
    Copyright (c) 2019 FRC Team 1678: Citrus Circuits

    Calculates the average of a list.

    lis is the list that is averaged.
    exception is returned if there is a divide by zero error. The
    default is 0.0 because the main usage in in percentage calculations.
    """
    lis = [item for item in lis if item is not None]
    if len(lis) == 0:
        return exception
    else:
        return round(sum(lis) / len(lis), 1)


def maximum(lis, exception=0.0, cycles=False):
    """
    Shamelessly stolen almost verbatim from 1678
    Copyright (c) 2019 FRC Team 1678: Citrus Circuits

    Calculates the average of a list.

    lis is the list that is averaged.
    exception is returned if there is a divide by zero error. The
    default is 0.0 because the main usage in in percentage calculations.
    """
    lis = [item for item in lis if item is not None]
    if len(lis) == 0:
        return exception
    else:
        return round(max(lis))


def p75(lis, exception=0.0, cycles=False):
    lis = [item for item in lis if item is not None]
    if len(lis) == 0:
        return exception
    else:
        # If the cycles specifcation is true, it takes the lower half of
        # the list, which are the faster cycle times.
        if cycles is True:
            # 'math.ceil()' rounds the float up to be an int.
            upper_half = lis[:math.ceil(len(lis) / 2)]
        else:
            # 'math.floor()' rounds the float down to be an int.
            upper_half = lis[-math.floor(len(lis) / 2):]
        return round(sum(upper_half) / len(upper_half), 1)


def SD(lis, exception=0.0, cycles=False):
    """Calculates the standard deviation of a list.

        lis is the list that the standard deviation is taken of.
        exception is returned if there is a divide by zero error. The
        default is 0.0 because if there is no data, there is no deviation.
        """
    lis = [item for item in lis if item is not None]
    if len(lis) == 0:
        return exception
    else:
        return round(float(numpy.std(lis)), 1)


def percent_success_place(timds, **filters):
    successes = len(filter_timeline_actions([timd for timd in timds], **filters, actionType='place'))
    fails = len(filter_timeline_actions([timd for timd in timds], **filters, actionType='drop'))

    if successes + fails == 0:
        return None

    return round(100 * (successes/(successes+fails)))


def percent_success_intake(timd, **filters):
    successes = len(filter_timeline_actions([timd], **filters, actionType='intake'))
    fails = len(filter_timeline_actions([timd], **filters, actionType='drop'))

    if successes + fails == 0:
        return None

    return round(100 * (successes / (fails + successes)))


def true_offensive_contribution(timd):
    total_contribution = 0
    if timd['header'].get('leftHab'):
        if timd['header'].get('startLevel') == 'hab1':
            total_contribution += 3
        elif timd['header'].get('startLevel') == 'hab2':
            total_contribution += 6
    for action in timd.get('timeline', []):
        if action.get('actionType') == 'place':
            if action.get('actionPiece') == 'cargo':
                total_contribution += 3
            elif action.get('actionPiece') == 'hatch':
                if action.get('actionTime') >= 135:
                    # In sandstorm so a cargo is trapped
                    total_contribution += 5
                else:
                    total_contribution += 2

    return total_contribution


def sum_sd(SDs):
    return sum(map(lambda x: x ** 2 , filter(lambda s: s != None, SDs))) ** 0.5
