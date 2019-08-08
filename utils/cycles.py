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
    return calc_to_run(cycle_times, 0, cycles=True)


def total_cycle_time(cycle_list, **filters):
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
    return sum(cycle_times)


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