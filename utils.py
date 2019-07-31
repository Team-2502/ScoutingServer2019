import math

import numpy

def avg(lis, exception=0.0):
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
        return sum(upper_half) / len(upper_half)


def SD(lis, exception=0.0):
    """Calculates the standard deviation of a list.

        lis is the list that the standard deviation is taken of.
        exception is returned if there is a divide by zero error. The
        default is 0.0 because if there is no data, there is no deviation.
        """
    lis = [item for item in lis if item is not None]
    if len(lis) == 0:
        return exception
    else:
        return numpy.std(lis)


def filter_timeline_actions(timds, **filters):
    """
    Shamelessly stolen almost verbatim from 1678
    Copyright (c) 2019 FRC Team 1678: Citrus Circuits

    Puts a timeline through a filter to use for calculations.

    timd is the TIMD that needs calculated data.
    filters are the specifications that certain data points inside the
    timeline must fit in order to be included in the returned timeline.
    example for filter - 'level=1' as an argument, '{'level': 1}' inside
    the function."""
    filtered_timeline = []
    # For each action, if any of the specifications are not met, the
    # loop breaks and moves on to the next action, but if all the
    # specifications are met, the action is added to the filtered
    # timeline.
    for timd in timds:
        for action in timd.get('timeline', []):
            for data_field, requirement in filters.items():
                # If the filter specifies time, it can either specify
                # sandstorm by making the requirement 'sandstorm' or specify
                # teleop by making the requirement 'teleop'.
                if data_field == 'actionTime':
                    if requirement == 'sandstorm' and action['actionTime'] < 135:
                        break
                    elif requirement == 'teleop' and action['actionTime'] >= 135:
                        break
                # Otherwise, it checks the requirement normally
                else:
                    if action.get(data_field) != requirement:
                        break
            # If all the requirements are met, the action is added to the
            # (returned) filtered timeline.
            else:
                filtered_timeline.append(action)
    return filtered_timeline


def percent_success_place(timds, **filters):
    successes = len(filter_timeline_actions([timd for timd in timds], **filters, actionType='place'))
    fails = len(filter_timeline_actions([timd for timd in timds], **filters, actionType='drop'))

    if successes == 0:
        return None

    return round(100 * (1 - (fails/successes)))
