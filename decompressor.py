import utils

TEMP_TIMD_COMP_KEYS = {
    'A': 'matchNumber',
    'B': 'teamNumber',
    'C': 'assignmentMode',
    'D': 'scoutKey',
    'E': 'driversStation',
    'F': 'isReplay',
    'G': 'isNoShow',
    'H': 'startLevel',
    'I': 'preloadPiece',
    'J': 'leftHab',
    'K': 'actionType',
    'L': 'actionPlace',
    'M': 'actionTime',
    'N': 'actionPiece',
    'O': 'placeLevel',
    'P': 'wasDefended',
    'Q': 'cargoShipSide',
    'R': 'actualClimb',
    'S': 'attemptedClimb',
    'T': 'isDoubleClimb',
    'U': 'isTripleClimb'
}

TEMP_TIMD_COMP_VALUES = {
    't': True,
    'f': False,
    'a': 'file',
    'b': 'override',
    'c': 'red1',
    'd': 'red2',
    'e': 'red3',
    'g': 'blue1',
    'h': 'blue2',
    'i': 'blue3',
    'j': 'hab1',
    'k': 'hab2',
    'l': 'cargo',
    'm': 'hatch',
    'n': 'none',
    'o': 'humanPlayerStation',
    'p': 'ground',
    'q': 'intake',
    'r': 'place',
    's': 'level1',
    'u': 'level2',
    'v': 'level3',
    'w': 'front',
    'x': 'side',
    'y': 'rocket',
    'z': 'cargoShip',
    'aa': 'drop',
    'ab': 'middleField',
    'ac': 'incap',
    'ad': 'recap',
    'ae': 'climb',
    'af': 'defenseStart',
    'ag': 'defenseEnd',
}

SCOUT_NAME_VALUES = {
    "a": "Ryan A",
    "b": "Evan L",
    "c": "Ritik M",
    "d": "Ravisha J",
    "e": "Ishan S"
}

very_cool_timd = 'A2B1114CbDaEdFtGfHkImJt|KrLzM143NmOsQxPf,KqLoM140Nm,KrLzM135NmOsQxPf,KqLoM129Nm,KrLyM122NmOvPf,KqLoM118Nm,KrLyM114NmOvPf,KqLpM111Nl,KrLyM107NlOvPf,KqLpM101Nl,KrLyM99NlOvPf,KqLoM97Nm,KrLyM92NmOuPf,KqLoM88Nm,KrLyM84NmOuPf,KqLoM80Nm,KrLyM75NmOsPf,KqLoM72Nm,KrLyM68NmOsPf,KqLpM66Nl,KrLyM62NlOuPf,KqLpM60Nl,KrLyM57NlOuPf,KqLpM53Nl,KrLyM51NlOsPf,KqLpM48Nl,KrLyM46NlOsPf,KqLpM42Nl,KrLzM39NlOsQxPf,KqLoM35Nm,KrLzM30NmOsQwPf,KqLpM28Nl,KrLzM24NlOsQwPf,KqLoM19Nm,KrLyM10NmOvPf,KaeM7RvSv'


def decompress_timd(temp_timd):
    header, timeline = temp_timd.split("|")
    decompressed_header = decompress_header(header)
    team_number = decompressed_header.get('teamNumber')
    match_number = decompressed_header.get('matchNumber')
    decompressed_timeline = decompress_timeline(timeline)
    decompressed_timd = {'header': decompressed_header, 'timeline': decompressed_timeline, 'team_number': team_number, 'match_number': match_number}
    print(decompressed_timd)
    return decompressed_timd


def decompress_header(header):
    return decompress_action(header)


def decompress_timeline(timeline):
    compressed_timeline = timeline.split(",")
    decompressed_timeline = []
    for action in compressed_timeline:
        decompressed_action = decompress_action(action)
        decompressed_timeline.append(decompressed_action)
    return decompressed_timeline


def decompress_value(compressed_value):
    # Value is a compressed string
    if compressed_value.isalpha():
        return TEMP_TIMD_COMP_VALUES[compressed_value]
    # Value is a number, usually a time
    else:
        try:
            return int(compressed_value)
        # TODO Value is '', don't know what this is
        except ValueError:
            return compressed_value


def decompress_action(action):
    decompressed_action = {}
    last_key_index = 0
    for index, character in enumerate(action):
        # First character
        if index == 0:
            last_key_index = 0
        # Last character
        if index == len(action) - 1:
            compressed_value = action[last_key_index + 1:]
            value = decompress_value(compressed_value)
            compressed_key = action[last_key_index]
            key = TEMP_TIMD_COMP_KEYS[compressed_key]
            decompressed_action[key] = value
            last_key_index = index
        # TODO Prepare for having keys that are longer than one character
        # Next capital letter key
        elif character.isupper():
            compressed_key = action[last_key_index]
            key = TEMP_TIMD_COMP_KEYS[compressed_key]

            # Value from end of last key to this key
            compressed_value = action[last_key_index + 1:index]
            # Scout names stored in separate dictionary
            if key == 'scoutKey':
                value = SCOUT_NAME_VALUES[compressed_value]
            else:
                value = decompress_value(compressed_value)

            decompressed_action[key] = value
            last_key_index = index
    return decompressed_action


def calculate_calculated_data(decompressed_timd):
    calculated_data = {}

    calculated_data['cargoScored'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='cargo'))
    calculated_data['hatchesScored'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='hatch'))
    calculated_data['hatchesDropped'] = len(filter_timeline_actions(decompressed_timd, actionType='drop', actionPiece='hatch'))
    calculated_data['cargoDropped'] = len(filter_timeline_actions(decompressed_timd, actionType='drop', actionPiece='cargo'))
    calculated_data['cargoScoredSS'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='cargo', actionTime='sandstorm'))
    calculated_data['hatchScoredSS'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='hatch', actionTime='sandstorm'))
    calculated_data['cargoScoredTeleop'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='cargo', actionTime='teleop'))
    calculated_data['hatchScoredTeleop'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='hatch', actionTime='teleop'))
    calculated_data['hatchScoredRocket'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='hatch', actionPlace='rocket'))
    calculated_data['hatchScoredCargoShip'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='hatch', actionPlace='cargoShip'))
    calculated_data['hatchScoredLevel1'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='hatch', placeLevel='level1'))
    calculated_data['hatchScoredLevel2'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='hatch', placeLevel='level2'))
    calculated_data['hatchScoredLevel3'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='hatch', placeLevel='level3'))
    calculated_data['cargoScoredRocket'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='cargo', actionPlace='rocket'))
    calculated_data['cargoScoredCargoShip'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='cargo', actionPlace='cargoShip'))
    calculated_data['cargoScoredLevel1'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='cargo', placeLevel='level1'))
    calculated_data['cargoScoredLevel2'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='cargo', placeLevel='level2'))
    calculated_data['cargoScoredLevel3'] = len(filter_timeline_actions(decompressed_timd, actionType='place', actionPiece='cargo', placeLevel='level3'))

    # calculated_data['timeIncap']

    calculated_data['cargoPlaceSuccessRate'] = percent_success_place(decompressed_timd, actionPiece='cargo')
    calculated_data['hatchPlaceSuccessRate'] = percent_success_place(decompressed_timd, actionPiece='hatch')
    calculated_data['cargoShipPlaceSuccessRate'] = percent_success_place(decompressed_timd, actionPlace='cargoShip')
    calculated_data['rocketPlaceSuccessRate'] = percent_success_place(decompressed_timd, actionPlace='rocket')

    calculated_data['cargoIntakeSuccessRate'] = percent_success_intake(decompressed_timd, actionPiece='cargo')
    calculated_data['hatchIntakeSuccessRate'] = percent_success_intake(decompressed_timd, actionPiece='hatch')

    # Creates the cycle_list, a list of tuples where the intake is the
    # first item and the placement or drop is the second. This is used
    # when calculating cycle times.
    cycle_list = []
    for action in decompressed_timd.get('timeline', []):
        if action.get('actionType') in ['intake', 'place']:
            cycle_list.append(action)

    # There must be at least 2 actions to have a cycle.
    if len(cycle_list) > 1:
        # If the first action in the list is a placement, it is a
        # preload, which doesn't count when calculating cycle times.
        if cycle_list[0].get('actionType') == 'place':
            cycle_list.pop(0)
        # If the last action in the list is an intake, it means the
        # robot finished with a game object, in which the cycle was
        # never completed.
        if cycle_list[-1].get('actionType') == 'intake':
            cycle_list.pop(-1)
        # [::2] are the even-indexed items of the list, [1::2] are the
        # odd-indexed items of the list. The python zip function puts
        # matching-index items from two lists into tuples.
        paired_cycle_list = list(zip(cycle_list[::2], cycle_list[1::2]))

        calculated_data['undefendedHatchAverageCycleTime'] = average_cycle_time(paired_cycle_list, actionPiece='hatch', wasDefended=False)
        calculated_data['undefendedCargoAverageCycleTime'] = average_cycle_time(paired_cycle_list, actionPiece='cargo', wasDefended=False)
        calculated_data['undefendedRocketAverageCycleTime'] = average_cycle_time(paired_cycle_list, actionPlace='rocket', wasDefended=False)
        calculated_data['undefendedCargoShipAverageCycleTime'] = average_cycle_time(paired_cycle_list, actionPlace='cargoShip', wasDefended=False)
        calculated_data['undefendedLevel3AverageCycleTime'] = average_cycle_time(paired_cycle_list, placeLevel='level3', wasDefended=False)

        calculated_data['defendedHatchAverageCycleTime'] = average_cycle_time(paired_cycle_list, actionPiece='hatch', wasDefended=True)
        calculated_data['defendedCargoAverageCycleTime'] = average_cycle_time(paired_cycle_list, actionPiece='cargo', wasDefended=True)
        calculated_data['defendedRocketAverageCycleTime'] = average_cycle_time(paired_cycle_list, actionPlace='rocket', wasDefended=True)
        calculated_data['defendedCargoShipAverageCycleTime'] = average_cycle_time(paired_cycle_list, actionPlace='cargoShip', wasDefended=True)
        calculated_data['defendedLevel3AverageCycleTime'] = average_cycle_time(paired_cycle_list, placeLevel='level3', wasDefended=True)

    calculated_data['trueOffensiveContribution'] = true_offensive_contribution(decompressed_timd)

    return calculated_data


def filter_timeline_actions(timd, **filters):
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


def percent_success_place(timd, **filters):
    successes = len(filter_timeline_actions(timd, **filters, actionType='place'))
    fails = len(filter_timeline_actions(timd, **filters, actionType='drop'))

    return round(100 * (1 - (fails/successes)))


def percent_success_intake(timd, **filters):
    successes = len(filter_timeline_actions(timd, **filters, actionType='intake'))
    fails = len(filter_timeline_actions(timd, **filters, actionType='drop'))

    return round(100 * (1 - (fails / successes)))


def average_cycle_time(cycle_list, **filters):
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
    return utils.avg(cycle_times, None)


def true_offensive_contribution(timd):
    total_contribution = 0
    if timd['header'].get('leftHab'):
        if timd['header'].get('startLevel') == 'hab1':
            total_contribution += 3
        elif timd['header'].get('startLevel') == 'hab2':
            total_contribution += 6
    for action in timd.get('timeline', []):
        if action.get('actionType') == 'climb':
            if action.get('actualClimb') == 'level1':
                total_contribution += 3
            elif action.get('actualClimb') == 'level2':
                total_contribution += 6
            elif action.get('actualClimb') == 'level3':
                total_contribution += 12
        elif action.get('actionType') == 'place':
            if action.get('actionPiece') == 'cargo':
                total_contribution += 3
            elif action.get('actionPiece') == 'hatch':
                if action.get('actionTime') >= 135:
                    # In sandstorm so a cargo is trapped
                    total_contribution += 5
                else:
                    total_contribution += 2

    return total_contribution


def calculate_TIMD(compressed_timd):
    decompressed_timd = decompress_timd(compressed_timd)
    decompressed_timd['calculated'] = calculate_calculated_data(decompressed_timd)
    print("{" + "\n".join("{}: {}".format(k, v) for k, v in decompressed_timd["calculated"].items()) + "}")


calculate_TIMD(very_cool_timd)