import os
import json

import utils

TOTAL_AVERAGE_DATA_FIELDS = {
    'avgCargoScored': 'cargoScored',
    'avgHatchesScored': 'hatchesScored',
    'avgCargoScoredSandstorm': 'cargoScoredSS',
    'avgHatchesScoredSandstorm': 'hatchScoredSS',
    'avgCargoTeleop': 'cargoScoredTeleop',
    'avgHatchTeleop': 'hatchScoredTeleop',
    'avgCargoScoredL1': 'cargoScoredLevel1',
    'avgCargoScoredL2': 'cargoScoredLevel2',
    'avgCargoScoredL3': 'cargoScoredLevel3',
    'avgHatchesScoredL1': 'hatchScoredLevel1',
    'avgHatchesScoredL2': 'hatchScoredLevel2',
    'avgHatchesScoredL3': 'hatchScoredLevel3',
    'avgPiecesScoredRocket': 'piecesScoredRocket',
    'avgPiecesScoredCargoShip': 'piecesScoredCargoShip',
    'avgCargoDrops': 'cargoDropped',
    'avgHatchDrops': 'hatchesDropped',
    'avgTimeIncap': 'timeIncap',
    'avgTimeClimbing': 'timeClimbing',
    'avgTimeDefending': 'timeDefending'
}

L3M_AVERAGE_DATA_FIELDS = {
    'l3mCargoScored': 'cargoScored',
    'l3mHatchesScored': 'hatchesScored',
    'l3mCargoDrops': 'cargoDropped',
    'l3mHatchDrops': 'hatchesDropped',
    'l3mTimeIncap': 'timeIncap',
    'l3mTimeClimbing': 'timeClimbing',
    'l3mTimeDefending': 'timeDefending',
}

P75_DATA_FIELDS = {
    'p75CargoScored': 'cargoScored',
    'p75HatchesScored': 'hatchesScored',
    'p75CargoDrops': 'cargoDropped',
    'p75HatchDrops': 'hatchesDropped',
    'p75TimeIncap': 'timeIncap',
    'p75TimeClimbing': 'timeClimbing',
}

SD_DATA_FIELDS = {
    'SDCargoScored': 'cargoScored',
    'SDHatchesScored': 'hatchesScored',
    'SDCargoDrops': 'cargoDropped',
    'SDHatchDrops': 'hatchesDropped',
    'SDTimeIncap': 'timeIncap',
    'SDTimeClimbing': 'timeClimbing',
}

PERCENT_SUCCESS_DATA_FIELDS = {
    'cargoSuccessPlace': {'actionPiece': 'cargo'},
    'cargoSuccessPlaceDefended': {
        'actionPiece': 'cargo',
        'wasDefended': True,
    },
    'cargoSuccessPlaceUndefended': {
        'actionPiece': 'cargo',
        'wasDefended': False,
    },
    'cargoSuccessPlaceL1': {
        'actionPiece': 'cargo',
        'placeLevel': 1,
    },
    'cargoSuccessPlaceL2': {
        'actionPiece': 'cargo',
        'placeLevel': 2,
    },
    'cargoSuccessPlaceL3': {
        'actionPiece': 'cargo',
        'placeLevel': 3,
    },
    'cargoSuccessRocket': {
        'actionPiece': 'cargo',
        'actionPlace': 'rocket',
    },
    'cargoSuccessCargoShip': {
        'actionPiece': 'cargo',
        'actionPlace': 'cargoShip',
    },
    'hatchSuccessPlace': {
        'actionPiece': 'hatch',
    },
    'hatchSuccessPlaceDefended': {
        'actionPiece': 'hatch',
        'wasDefended': True,
    },
    'hatchSuccessPlaceUndefended': {
        'actionPiece': 'hatch',
        'wasDefended': False,
    },
    'hatchSuccessL1': {
        'actionPiece': 'hatch',
        'placeLevel': 1,
    },
    'hatchSuccessL2': {
        'actionPiece': 'hatch',
        'placeLevel': 2,
    },
    'hatchSuccessL3': {
        'actionPiece': 'hatch',
        'placeLevel': 3,
    },
    'hatchSuccessRocket': {
        'actionPiece': 'hatch',
        'actionPlace': 'rocket',
    },
    'hatchSuccessCargoShip': {
        'actionPiece': 'hatch',
        'actionPlace': 'cargoShip',
    },
}


def calculate_team(team_number):
    team = {'teamNumber': team_number}

    timds = get_TIMDS(team_number)
    l3m_timds = sorted(timds, key=lambda timd: timd.get('matchNumber'))[-3:]
    team['timds']: get_TIMDS(team_number)

    team_abilities = {}
    team_abilities['groundCargoPickup'] = True if len(utils.filter_timeline_actions(timds, actionType='intake', actionPiece='cargo')) > 0 else False
    team_abilities['groundHatchPickup'] = True if len(utils.filter_timeline_actions(timds, actionType='intake', actionPiece='cargo')) > 0 else False
    team_abilities['climbHab2'] = True if len(utils.filter_timeline_actions(timds, actionType='climb', actualClimb='level2')) > 0 else False
    team_abilities['climbHab3'] = True if len(utils.filter_timeline_actions(timds, actionType='climb', actualClimb='level3')) > 0 else False
    team_abilities['placeLevel2'] = True if len(utils.filter_timeline_actions(timds, actionType='place', placeLevel='level2')) > 0 else False
    team_abilities['placeLevel3'] = True if len(utils.filter_timeline_actions(timds, actionType='place', placeLevel='level3')) > 0 else False
    team['team_abilities'] = team_abilities

    defense = {}

    totals = {'cargoPlaced': len(utils.filter_timeline_actions(timds, actionType='place', actionPiece='cargo')),
              'hatchesPlaced': len(utils.filter_timeline_actions(timds, actionType='place', actionPiece='cargo')),
              'cyclesLevel1': len(utils.filter_timeline_actions(timds, actionType='place', placeLevel='level1')),
              'cyclesLevel2': len(utils.filter_timeline_actions(timds, actionType='place', placeLevel='level2')),
              'cyclesLevel3': len(utils.filter_timeline_actions(timds, actionType='place', placeLevel='level3')),
              'cyclesRocket': len(utils.filter_timeline_actions(timds, actionType='place', actionPlace='rocket')),
              'cyclesCargoShip': len(utils.filter_timeline_actions(timds, actionType='place', actionPlace='cargoShip'))}

    for average_data_field, timd_data_field in TOTAL_AVERAGE_DATA_FIELDS.items():
        totals[average_data_field] = utils.avg([timd['calculated'].get(timd_data_field) for timd in timds])
    team['totals'] = totals

    l3ms = {}
    for l3m_average_data_field, timd_data_field in L3M_AVERAGE_DATA_FIELDS.items():
        l3ms[l3m_average_data_field] = utils.avg([timd['calculated'].get(timd_data_field) for timd in l3m_timds])
    team['l3ms'] = l3ms

    p75s = {}
    for p75_data_field, timd_data_field in P75_DATA_FIELDS.items():
        p75s[p75_data_field] = utils.p75([timd['calculated'].get(timd_data_field) for timd in timds])
    team['p75s'] = p75s

    SDs = {}
    for SD_data_field, timd_data_field in SD_DATA_FIELDS.items():
        SDs[SD_data_field] = utils.SD([timd['calculated'].get(timd_data_field) for timd in timds])
    team['SDs'] = SDs

    percentages = {}
    for success_data_field, filters in PERCENT_SUCCESS_DATA_FIELDS.items():
        percentages[success_data_field] = utils.percent_success_place(utils.filter_timeline_actions(timds, **filters))

    percentages['hatchPercentageOfCycles'] = sum([timd['calculated']['hatchesScored'] for timd in timds]) / sum([timd['calculated']['totalCycles'] for timd in timds]) if sum([timd['calculated']['totalCycles'] for timd in timds]) != 0 else 0
    percentages['cargoPercentageOfCycles'] = sum([timd['calculated']['cargoScored'] for timd in timds]) / sum([timd['calculated']['totalCycles'] for timd in timds]) if sum([timd['calculated']['totalCycles'] for timd in timds]) != 0 else 0

    # percent defense
    # percent incap
    # percent no show
    # percent left hab
    # percent climbed
    # percent climb succeeded

    print(team)


def get_TIMDS(team_number):
    homeDir = os.path.expanduser('~')
    TIMDs = os.listdir(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs'))
    return [json.loads(open(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs/', TIMD)).read()) for TIMD in TIMDs if int(TIMD.split('-')[1]) == team_number]


if __name__ == '__main__':
    calculate_team(2337)
