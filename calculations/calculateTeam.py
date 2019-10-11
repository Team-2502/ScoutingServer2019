import os
import json
import pyrebase

import sensitiveInfo
from utils import *
import calculations.calculateRankings

TOTAL_AVERAGE_DATA_FIELDS = {
    'avgCargoScored': 'cargoScored',
    'avgHatchesScored': 'hatchesScored',
    'avgCargoScoredSandstorm': 'cargoScoredSS',
    'avgHatchesScoredSandstorm': 'hatchScoredSS',
    'avgCargoTeleop': 'cargoScoredTeleop',
    'avgHatchTeleop': 'hatchScoredTeleop',
    'avgTotalTeleopCycles': 'totalTeleopCycles',
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
    'avgTimeDefending': 'timeDefending',
    'avgTOC': 'trueOffensiveContribution'
}

L3M_AVERAGE_DATA_FIELDS = {
    'l3mCargoScored': 'cargoScored',
    'l3mHatchesScored': 'hatchesScored',
    'l3mPiecesScoredRocket': 'piecesScoredRocket',
    'l3mPiecesScoredCargoShip': 'piecesScoredCargoShip',
    'l3mCargoScoredL1': 'cargoScoredLevel1',
    'l3mCargoScoredL2': 'cargoScoredLevel2',
    'l3mCargoScoredL3': 'cargoScoredLevel3',
    'l3mHatchesScoredL1': 'hatchScoredLevel1',
    'l3mHatchesScoredL2': 'hatchScoredLevel2',
    'l3mHatchesScoredL3': 'hatchScoredLevel3',
    'l3mCargoDrops': 'cargoDropped',
    'l3mHatchDrops': 'hatchesDropped',
    'l3mTimeIncap': 'timeIncap',
    'l3mTimeClimbing': 'timeClimbing',
    'l3mTimeDefending': 'timeDefending'
}

P75_DATA_FIELDS = {
    'p75CargoScored': 'cargoScored',
    'p75HatchesScored': 'hatchesScored',
    'p75CargoTeleop': 'cargoScoredTeleop',
    'p75HatchTeleop': 'hatchScoredTeleop',
    'p75CargoDrops': 'cargoDropped',
    'p75HatchDrops': 'hatchesDropped',
    'p75TimeIncap': 'timeIncap',
    'p75TimeClimbing': 'timeClimbing',
    'p75TOC': 'trueOffensiveContribution',
    'p75PiecesScoredRocket': 'piecesScoredRocket',
    'p75PiecesScoredCargoShip': 'piecesScoredCargoShip',
    'p75CargoScoredL1': 'cargoScoredLevel1',
    'p75HatchesScoredL1': 'hatchScoredLevel1',
    'p75CargoScoredL3': 'cargoScoredLevel3',
    'p75HatchesScoredL3': 'hatchScoredLevel3'
}

SD_DATA_FIELDS = {
    'SDCargoScored': 'cargoScored',
    'SDHatchesScored': 'hatchesScored',
    'SDCargoDrops': 'cargoDropped',
    'SDHatchDrops': 'hatchesDropped',
    'SDTimeIncap': 'timeIncap',
    'SDTimeClimbing': 'timeClimbing',
}

MAX_DATA_FIELDS = {
    'maxCargoScored': 'cargoScored',
    'maxHatchesScored': 'hatchesScored',
    'maxPiecesScoredRocket': 'piecesScoredRocket',
    'maxPiecesScoredCargoShip': 'piecesScoredCargoShip',
    'maxCargoDrops': 'cargoDropped',
    'maxHatchDrops': 'hatchesDropped',
    'maxTOC': 'trueOffensiveContribution'
}

PERCENT_SUCCESS_DATA_FIELDS = {
    'cargoSuccessPlace': {
        'actionPiece': 'cargo'
    },
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
        'placeLevel': 'level1',
    },
    'cargoSuccessPlaceL2': {
        'actionPiece': 'cargo',
        'placeLevel': 'level2',
    },
    'cargoSuccessPlaceL3': {
        'actionPiece': 'cargo',
        'placeLevel': 'level3',
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
        'placeLevel': 'level1',
    },
    'hatchSuccessL2': {
        'actionPiece': 'hatch',
        'placeLevel': 'level2',
    },
    'hatchSuccessL3': {
        'actionPiece': 'hatch',
        'placeLevel': 'level3',
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

AVERAGE_CYCLE_TIME_DATA_FIELDS = {
    'cargoOverall': {
        'actionPiece': 'cargo',
    },
    'cargoDefended': {
        'actionPiece': 'cargo',
        'wasDefended': True,
    },
    'cargoUndefended': {
        'actionPiece': 'cargo',
        'wasDefended': False,
    },
    'cargoL1': {
        'actionPiece': 'cargo',
        'placeLevel': 'level1',
    },
    'cargoL2': {
        'actionPiece': 'cargo',
        'placeLevel': 'level2',
    },
    'cargoL3': {
        'actionPiece': 'cargo',
        'placeLevel': 'level3',
    },
    'cargoRocket': {
        'actionPiece': 'cargo',
        'actionPlace': 'rocket',
    },
    'cargoCargoShip': {
        'actionPiece': 'cargo',
        'actionPlace': 'cargoShip',
    },
    'hatchOverall': {
        'actionPiece': 'hatch',
    },
    'hatchDefended': {
        'actionPiece': 'hatch',
        'wasDefended': True,
    },
    'hatchUndefended': {
        'actionPiece': 'hatch',
        'wasDefended': False,
    },
    'hatchL1': {
        'actionPiece': 'hatch',
        'placeLevel': 'level1',
    },
    'hatchL2': {
        'actionPiece': 'hatch',
        'placeLevel': 'level2',
    },
    'hatchL3': {
        'actionPiece': 'hatch',
        'placeLevel': 'level3',
    },
    'hatchRocket': {
        'actionPiece': 'hatch',
        'actionPlace': 'rocket',
    },
    'hatchCargoShip': {
        'actionPiece': 'hatch',
        'actionPlace': 'cargoShip',
    },
}

L3M_AVERAGE_CYCLE_TIME_DATA_FIELDS = {
    'l3mCargoOverall': {
        'actionPiece': 'cargo',
        'wasDefended': True,
    },
    'l3mCargoDefended': {
        'actionPiece': 'cargo',
        'wasDefended': True,
    },
    'l3mCargoUndefended': {
        'actionPiece': 'cargo',
        'wasDefended': False,
    },
    'l3mCargoL1': {
        'actionPiece': 'cargo',
        'placeLevel': 'level1',
    },
    'l3mCargoL2': {
        'actionPiece': 'cargo',
        'placeLevel': 'level2',
    },
    'l3mCargoL3': {
        'actionPiece': 'cargo',
        'placeLevel': 'level3',
    },
    'l3mCargoRocket': {
        'actionPiece': 'cargo',
        'actionPlace': 'rocket',
    },
    'l3mCargoCargoShip': {
        'actionPiece': 'cargo',
        'actionPlace': 'cargoShip',
    },
    'l3mHatchOverall': {
        'actionPiece': 'hatch',
    },
    'l3mHatchDefended': {
        'actionPiece': 'hatch',
        'wasDefended': True,
    },
    'l3mHatchUndefended': {
        'actionPiece': 'hatch',
        'wasDefended': False,
    },
    'l3mHatchL1': {
        'actionPiece': 'hatch',
        'placeLevel': 'level1',
    },
    'l3mHatchL2': {
        'actionPiece': 'hatch',
        'placeLevel': 'level2',
    },
    'l3mHatchL3': {
        'actionPiece': 'hatch',
        'placeLevel': 'level3',
    },
    'l3mHatchRocket': {
        'actionPiece': 'hatch',
        'actionPlace': 'rocket',
    },
    'l3mHatchCargoShip': {
        'actionPiece': 'hatch',
        'actionPlace': 'cargoShip',
    },
}

P75_CYCLE_TIME_DATA_FIELDS = {
    'p75CargoOverall': {
        'actionPiece': 'cargo',
        'wasDefended': True,
    },
    'p75CargoDefended': {
        'actionPiece': 'cargo',
        'wasDefended': True,
    },
    'p75CargoUndefended': {
        'actionPiece': 'cargo',
        'wasDefended': False,
    },
    'p75CargoL1': {
        'actionPiece': 'cargo',
        'placeLevel': 'level1',
    },
    'p75CargoL2': {
        'actionPiece': 'cargo',
        'placeLevel': 'level2',
    },
    'p75CargoL3': {
        'actionPiece': 'cargo',
        'placeLevel': 'level3',
    },
    'p75CargoRocket': {
        'actionPiece': 'cargo',
        'actionPlace': 'rocket',
    },
    'p75CargoCargoShip': {
        'actionPiece': 'cargo',
        'actionPlace': 'cargoShip',
    },
    'p75HatchOverall': {
        'actionPiece': 'hatch',
    },
    'p75HatchDefended': {
        'actionPiece': 'hatch',
        'wasDefended': True,
    },
    'p75HatchUndefended': {
        'actionPiece': 'hatch',
        'wasDefended': False,
    },
    'p75HatchL1': {
        'actionPiece': 'hatch',
        'placeLevel': 'level1',
    },
    'p75HatchL2': {
        'actionPiece': 'hatch',
        'placeLevel': 'level2',
    },
    'p75HatchL3': {
        'actionPiece': 'hatch',
        'placeLevel': 'level3',
    },
    'p75HatchRocket': {
        'actionPiece': 'hatch',
        'actionPlace': 'rocket',
    },
    'p75HatchCargoShip': {
        'actionPiece': 'hatch',
        'actionPlace': 'cargoShip',
    },
}

SD_CYCLE_TIME_DATA_FIELDS = {
    'SDCargoOverall': {
        'actionPiece': 'cargo',
        'wasDefended': True,
    },
    'SDCargoDefended': {
        'actionPiece': 'cargo',
        'wasDefended': True,
    },
    'SDCargoUndefended': {
        'actionPiece': 'cargo',
        'wasDefended': False,
    },
    'SDCargoL1': {
        'actionPiece': 'cargo',
        'placeLevel': 'level1',
    },
    'SDCargoL2': {
        'actionPiece': 'cargo',
        'placeLevel': 'level2',
    },
    'SDCargoL3': {
        'actionPiece': 'cargo',
        'placeLevel': 'level3',
    },
    'SDCargoRocket': {
        'actionPiece': 'cargo',
        'actionPlace': 'rocket',
    },
    'SDCargoCargoShip': {
        'actionPiece': 'cargo',
        'actionPlace': 'cargoShip',
    },
    'SDHatchOverall': {
        'actionPiece': 'hatch',
    },
    'SDHatchDefended': {
        'actionPiece': 'hatch',
        'wasDefended': True,
    },
    'SDHatchUndefended': {
        'actionPiece': 'hatch',
        'wasDefended': False,
    },
    'SDHatchL1': {
        'actionPiece': 'hatch',
        'placeLevel': 'level1',
    },
    'SDHatchL2': {
        'actionPiece': 'hatch',
        'placeLevel': 'level2',
    },
    'SDHatchL3': {
        'actionPiece': 'hatch',
        'placeLevel': 'level3',
    },
    'SDHatchRocket': {
        'actionPiece': 'hatch',
        'actionPlace': 'rocket',
    },
    'SDHatchCargoShip': {
        'actionPiece': 'hatch',
        'actionPlace': 'cargoShip',
    },
}


def get_team(team_number):
    homeDir = os.path.expanduser('~')
    teams = os.listdir(os.path.join(homeDir, 'EMCC-2019Server/cache/teams'))
    return [json.loads(open(os.path.join(homeDir, 'EMCC-2019Server/cache/teams/', team)).read()) for team in teams if team != '.DS_Store' and int(team.split('.')[0]) == int(team_number)][0]


def calculate_team(team_number, last_timd, is_json=False):
    if is_json is not False:
        team = is_json
        timds = team['timds']

    else:
        try:
            team = get_team(team_number)
            timds = get_timds(team_number)
        except ValueError:
            team = {'teamNumber': last_timd['team_number']}
            timds = [last_timd]

        team['timds'] = sorted(timds, key=lambda timd: timd['header']['matchNumber'])

    num_matches = len(timds)
    num_no_shows = len([timd for timd in timds if timd['header']['isNoShow']])

    timds = [timd for timd in timds if not timd['header']['isNoShow']]

    l3m_timds = sorted(timds, key=lambda timd: timd['header']['matchNumber'])[-3:]

    team_abilities = {}
    team_abilities['groundCargoPickup'] = True if len(cycles.filter_timeline_actions(timds, actionType='intake', actionPiece='cargo', actionPlace='ground')) > 0 else False
    team_abilities['groundHatchPickup'] = True if len(cycles.filter_timeline_actions(timds, actionType='intake', actionPiece='hatch', actionPlace='ground')) > 0 else False
    team_abilities['climbHab2'] = True if len(cycles.filter_timeline_actions(timds, actionType='climb', actualClimb='level2')) > 0 else False
    team_abilities['climbHab3'] = True if len(cycles.filter_timeline_actions(timds, actionType='climb', actualClimb='level3')) > 0 else False
    team_abilities['placeLevel2'] = True if len(cycles.filter_timeline_actions(timds, actionType='place', placeLevel='level2')) > 0 else False
    team_abilities['placeLevel3'] = True if len(cycles.filter_timeline_actions(timds, actionType='place', placeLevel='level3')) > 0 else False
    team_abilities['startLevel2'] = True if len([timd for timd in timds if timd['header']['startLevel'] == 'hab2']) > 0 else False
    team_abilities['placeHatch'] = True if len(cycles.filter_timeline_actions(timds, actionType='place', actionPiece='hatch')) > 0 else False
    team_abilities['placeCargo'] = True if len(cycles.filter_timeline_actions(timds, actionType='place', actionPiece='cargo')) > 0 else False
    team['team_abilities'] = team_abilities

    totals = {'cargoPlaced': len(cycles.filter_timeline_actions(timds, actionType='place', actionPiece='cargo')),
              'hatchesPlaced': len(cycles.filter_timeline_actions(timds, actionType='place', actionPiece='hatch')),
              'cyclesLevel1': len(cycles.filter_timeline_actions(timds, actionType='place', placeLevel='level1')),
              'cyclesLevel2': len(cycles.filter_timeline_actions(timds, actionType='place', placeLevel='level2')),
              'cyclesLevel3': len(cycles.filter_timeline_actions(timds, actionType='place', placeLevel='level3')),
              'cyclesRocket': len(cycles.filter_timeline_actions(timds, actionType='place', actionPlace='rocket')),
              'cyclesCargoShip': len(cycles.filter_timeline_actions(timds, actionType='place', actionPlace='cargoShip')),
              'timeDefending': sum([timd['calculated']['timeDefending'] for timd in timds]),
              'timeIncap': sum([timd['calculated']['timeIncap'] for timd in timds])}

    for average_data_field, timd_data_field in TOTAL_AVERAGE_DATA_FIELDS.items():
        totals[average_data_field] = stats.avg([timd['calculated'].get(timd_data_field) for timd in timds])
    team['totals'] = totals

    l3ms = {}
    for l3m_average_data_field, timd_data_field in L3M_AVERAGE_DATA_FIELDS.items():
        l3ms[l3m_average_data_field] = stats.avg([timd['calculated'].get(timd_data_field) for timd in l3m_timds])
    for success_data_field, filters in PERCENT_SUCCESS_DATA_FIELDS.items():
        l3ms['l3ms' + success_data_field] = stats.percent_success_place(l3m_timds, **filters)
    team['l3ms'] = l3ms

    p75s = {}
    for p75_data_field, timd_data_field in P75_DATA_FIELDS.items():
        p75s[p75_data_field] = stats.p75([timd['calculated'].get(timd_data_field) for timd in timds])
    team['p75s'] = p75s

    SDs = {}
    for SD_data_field, timd_data_field in SD_DATA_FIELDS.items():
        SDs[SD_data_field] = stats.SD([timd['calculated'].get(timd_data_field) for timd in timds])
    team['SDs'] = SDs

    maxes = {}
    for max_data_field, timd_data_field in MAX_DATA_FIELDS.items():
        maxes[max_data_field] = stats.maximum([timd['calculated'].get(timd_data_field) for timd in timds])
    team['maxes'] = maxes

    percentages = {}
    for success_data_field, filters in PERCENT_SUCCESS_DATA_FIELDS.items():
        percentages[success_data_field] = stats.percent_success_place(timds, **filters)

    percentages['hatchPercentageOfCycles'] = sum([timd['calculated']['hatchesScored'] for timd in timds]) / sum([timd['calculated']['totalCycles'] for timd in timds]) if sum([timd['calculated']['totalCycles'] for timd in timds]) != 0 else 0
    percentages['hatchPercentageOfCycles'] = round(100 * (1 - percentages['hatchPercentageOfCycles']))
    percentages['cargoPercentageOfCycles'] = sum([timd['calculated']['cargoScored'] for timd in timds]) / sum([timd['calculated']['totalCycles'] for timd in timds]) if sum([timd['calculated']['totalCycles'] for timd in timds]) != 0 else 0
    percentages['cargoPercentageOfCycles'] = round(100 * (1 - percentages['cargoPercentageOfCycles']))

    percentages['percentMatchesStartHab1'] = len([timd for timd in timds if timd['header']['startLevel'] == 'hab1']) / len(timds) if len(timds) is not 0 else 0
    percentages['percentMatchesStartHab1'] = round(100 * (percentages['percentMatchesStartHab1']))
    percentages['percentMatchesStartHab2'] = len([timd for timd in timds if timd['header']['startLevel'] == 'hab2']) / len(timds) if len(timds) is not 0 else 0
    percentages['percentMatchesStartHab2'] = round(100 * (percentages['percentMatchesStartHab2']))
    percentages['leftHab'] = round(100 * (len([timd for timd in timds if timd['header']['leftHab']]) / len(timds))) if len(timds) is not 0 else 0

    percentages['hab3ClimbSuccessRate'] = round(100 * (len(cycles.filter_timeline_actions(timds, actionType='climb', actualClimb='level3')) / len(cycles.filter_timeline_actions(timds, actionType='climb', attemptedClimb='level3')))) if len(cycles.filter_timeline_actions(timds, actionType='climb', attemptedClimb='level3')) != 0 else None
    percentages['hab2ClimbSuccessRate'] = round(100 * (len(cycles.filter_timeline_actions(timds, actionType='climb', actualClimb='level2')) / len(cycles.filter_timeline_actions(timds, actionType='climb', attemptedClimb='level2')))) if len(cycles.filter_timeline_actions(timds, actionType='climb', attemptedClimb='level2')) != 0 else None
    percentages['percentMatchesClimbHab3'] = round(100 * (len(cycles.filter_timeline_actions(timds, actionType='climb', actualClimb='level3')) / len(timds))) if len(timds) is not 0 else 0
    percentages['percentMatchesClimbHab2'] = round(100 * (len(cycles.filter_timeline_actions(timds, actionType='climb', actualClimb='level2')) / len(timds))) if len(timds) is not 0 else 0
    percentages['percentMatchesClimbHab1'] = round(100 * (len(cycles.filter_timeline_actions(timds, actionType='climb', actualClimb='level1')) / len(timds))) if len(timds) is not 0 else 0

    percentages['percentOfTotalTeleopDefending'] = round(100 * (team['totals']['timeDefending'] / (len(timds) * 135))) if len(timds) is not 0 else 0

    percentages['percentOfTimeIncap'] = round(100 * (team['totals']['timeIncap'] / (len(timds) * 150))) if len(timds) is not 0 else 0

    percentages['percentOfMatchesNoShow'] = round(100 * (num_no_shows / num_matches + num_no_shows))

    team['percentages'] = percentages

    cycle_times = {}
    for average_cycle_data_field, filters in AVERAGE_CYCLE_TIME_DATA_FIELDS.items():
        cycle_times[average_cycle_data_field] = cycles.cycle_time_calculations(cycles.create_cycle_list(timds, 'place', 'intake'), stats.avg, **filters)
    for l3m_average_cycle_data_field, filters in L3M_AVERAGE_CYCLE_TIME_DATA_FIELDS.items():
        cycle_times[l3m_average_cycle_data_field] = cycles.cycle_time_calculations(cycles.create_cycle_list(l3m_timds, 'place', 'intake'), stats.avg, **filters)
    for p75_cycle_data_field, filters in P75_CYCLE_TIME_DATA_FIELDS.items():
        cycle_times[p75_cycle_data_field] = cycles.cycle_time_calculations(cycles.create_cycle_list(timds, 'place', 'intake'), stats.p75, **filters)
    for SD_cycle_data_field, filters in SD_CYCLE_TIME_DATA_FIELDS.items():
        cycle_times[SD_cycle_data_field] = cycles.cycle_time_calculations(cycles.create_cycle_list(timds, 'place', 'intake'), stats.SD, **filters)

    team['cycle_times'] = cycle_times

    team['rankings'] = calculations.calculateRankings.calculate_rankings(int(team_number), team)

    print(f'{team_number} calculated')

    homeDir = os.path.expanduser('~')

    pyrebase_config = {
        "apiKey": sensitiveInfo.firebase_api_key(),
        "authDomain": "emcc2019-fb7dd.firebaseapp.com",
        "databaseURL": "https://emcc2019-fb7dd.firebaseio.com",
        "storageBucket": "emcc2019-fb7dd.appspot.com",
        "serviceAccount": os.path.join(homeDir, "EMCC-2019Server/config/emcc2019-fb7dd-8de616e8bc8c.json")
    }

    if is_json is False:
        firebase = pyrebase.initialize_app(pyrebase_config)
        database = firebase.database()

        # team['pitscouting'] = dict(database.child("teams").child(team_number).child('pitscouting').get().val())
        # team['sykes'] = dict(database.child("teams").child(team_number).child('sykes').get().val())

        # Save data in local cache
        if not os.path.exists(os.path.join(homeDir, 'EMCC-2019Server/cache/teams')):
            os.makedirs(os.path.join(homeDir, 'EMCC-2019Server/cache/teams'))

        with open(os.path.join(homeDir, f'EMCC-2019Server/cache/teams/{team_number}.json'), 'w') as file:
            json.dump(team, file)
        print(f'{team_number} cached')

        database.child("teams").child(team_number).set(team)
        print(f'{team_number} uploaded to Firebase\n')

    return team


def get_timds(team_number):
    homeDir = os.path.expanduser('~')
    TIMDs = [timd for timd in os.listdir(os.path.join(homeDir, 'EMCC-2019Server/cache/TIMDs')) if timd != '.DS_Store']
    return [json.loads(open(os.path.join(homeDir, 'EMCC-2019Server/cache/TIMDs/', TIMD)).read()) for TIMD in TIMDs if int(TIMD.split('-')[1]) == int(team_number)]
