import math

import numpy


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

    if successes + fails == 0:
        return None

    return round(100 * (successes/(successes+fails)))


def create_cycle_list(decompressed_timds, action1, action2):
    # Creates the cycle_list, a list of tuples where the intake is the
    # first item and the placement or drop is the second. This is used
    # when calculating cycle times.
    cycle_list = []
    for timd in decompressed_timds:
        for action in timd.get('timeline', []):
            if action.get('actionType') in [action1, action2]:
                cycle_list.append(action)

        # There must be at least 2 actions to have a cycle.
        if len(cycle_list) > 1:
            if action1 == 'place' and action2 == 'intake':
                # If the first action in the list is a placement, it is a
                # preload, which doesn't count when calculating cycle times.
                if cycle_list[0].get('actionType') == action1:
                    cycle_list.pop(0)
                # If the last action in the list is an intake, it means the
                # robot finished with a game object, in which the cycle was
                # never completed.
                if cycle_list[-1].get('actionType') == action2:
                    cycle_list.pop(-1)
            # [::2] are the even-indexed items of the list, [1::2] are the
            # odd-indexed items of the list. The python zip function puts
            # matching-index items from two lists into tuples.
            paired_cycle_list = list(zip(cycle_list[::2], cycle_list[1::2]))
            return paired_cycle_list
    return []


def cycle_time_calculations(cycle_list, calc_to_run, **filters):
    filtered_cycles = []
    # For each cycle, if any of the specifications are not met, the
    # loop breaks and moves on to the next cycle, but if all the
    # specifications are met, the cycle is added to the filtered cycles.
    for cycle in cycle_list:
        for data_field, requirement in filters.items():
            if cycle[1].get(data_field) != requirement:
                break
        # If all the requirements are met, the cycle is added to the
        # (returned) filtered cycles.
        else:
            filtered_cycles.append(cycle)

    cycle_times = []
    for cycle in filtered_cycles:
        # Subtracts the second time from the first because the time
        # counts down in the timeline.
        cycle_times.append(cycle[0].get('actionTime') -
                           cycle[1].get('actionTime'))
    return calc_to_run(cycle_times, None, cycles=True)
