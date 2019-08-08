import sensitiveInfo

import json
import os
import pyrebase

from utils import *

def calculate_statistics(decompressed_timd):
    calculated_data = {}

    calculated_data['cargoScored'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo'))
    calculated_data['hatchesScored'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch'))
    calculated_data['totalCycles'] = calculated_data['cargoScored'] + calculated_data['hatchesScored']
    calculated_data['hatchesDropped'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='drop', actionPiece='hatch'))
    calculated_data['cargoDropped'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='drop', actionPiece='cargo'))
    calculated_data['cargoScoredSS'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', actionTime='sandstorm'))
    calculated_data['hatchScoredSS'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', actionTime='sandstorm'))
    calculated_data['cargoScoredTeleop'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', actionTime='teleop'))
    calculated_data['hatchScoredTeleop'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', actionTime='teleop'))
    calculated_data['hatchScoredRocket'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', actionPlace='rocket'))
    calculated_data['hatchScoredCargoShip'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', actionPlace='cargoShip'))
    calculated_data['hatchScoredLevel1'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', placeLevel='level1'))
    calculated_data['hatchScoredLevel2'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', placeLevel='level2'))
    calculated_data['hatchScoredLevel3'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', placeLevel='level3'))
    calculated_data['cargoScoredRocket'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', actionPlace='rocket'))
    calculated_data['cargoScoredCargoShip'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', actionPlace='cargoShip'))
    calculated_data['cargoScoredLevel1'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', placeLevel='level1'))
    calculated_data['cargoScoredLevel2'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', placeLevel='level2'))
    calculated_data['cargoScoredLevel3'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', placeLevel='level3'))
    calculated_data['piecesScoredCargoShip'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPlace='cargoShip'))
    calculated_data['piecesScoredRocket'] = len(cycles.filter_timeline_actions([decompressed_timd], actionType='place', actionPlace='rocket'))

    calculated_data['cargoPlaceSuccessRate'] = stats.percent_success_place([decompressed_timd], actionPiece='cargo')
    calculated_data['hatchPlaceSuccessRate'] = stats.percent_success_place([decompressed_timd], actionPiece='hatch')
    calculated_data['cargoShipPlaceSuccessRate'] = stats.percent_success_place([decompressed_timd], actionPlace='cargoShip')
    calculated_data['rocketPlaceSuccessRate'] = stats.percent_success_place([decompressed_timd], actionPlace='rocket')

    calculated_data['cargoIntakeSuccessRate'] = stats.percent_success_intake(decompressed_timd, actionPiece='cargo')
    calculated_data['hatchIntakeSuccessRate'] = stats.percent_success_intake(decompressed_timd, actionPiece='hatch')

    intake_to_place_cycle_list = cycles.create_cycle_list([decompressed_timd], 'place', 'intake')

    calculated_data['undefendedHatchAverageCycleTime'] = cycles.cycle_time_calculations(intake_to_place_cycle_list, stats.avg, actionPiece='hatch', wasDefended=False)
    calculated_data['undefendedCargoAverageCycleTime'] = cycles.cycle_time_calculations(intake_to_place_cycle_list, stats.avg, actionPiece='cargo', wasDefended=False)
    calculated_data['undefendedRocketAverageCycleTime'] = cycles.cycle_time_calculations(intake_to_place_cycle_list, stats.avg, actionPlace='rocket', wasDefended=False)
    calculated_data['undefendedCargoShipAverageCycleTime'] = cycles.cycle_time_calculations(intake_to_place_cycle_list, stats.avg, actionPlace='cargoShip', wasDefended=False)
    calculated_data['undefendedLevel3AverageCycleTime'] = cycles.cycle_time_calculations(intake_to_place_cycle_list, stats.avg, placeLevel='level3', wasDefended=False)

    calculated_data['defendedHatchAverageCycleTime'] = cycles.cycle_time_calculations(intake_to_place_cycle_list, stats.avg, actionPiece='hatch', wasDefended=True)
    calculated_data['defendedCargoAverageCycleTime'] = cycles.cycle_time_calculations(intake_to_place_cycle_list, stats.avg, actionPiece='cargo', wasDefended=True)
    calculated_data['defendedRocketAverageCycleTime'] = cycles.cycle_time_calculations(intake_to_place_cycle_list, stats.avg, actionPlace='rocket', wasDefended=True)
    calculated_data['defendedCargoShipAverageCycleTime'] = cycles.cycle_time_calculations(intake_to_place_cycle_list, stats.avg, actionPlace='cargoShip', wasDefended=True)
    calculated_data['defendedLevel3AverageCycleTime'] = cycles.cycle_time_calculations(intake_to_place_cycle_list, stats.avg, placeLevel='level3', wasDefended=True)

    calculated_data['trueOffensiveContribution'] = stats.true_offensive_contribution(decompressed_timd)

    incap_to_recap_cycle_list = cycles.create_cycle_list([decompressed_timd], 'incap', 'recap')
    calculated_data['timeIncap'] = cycles.total_cycle_time(incap_to_recap_cycle_list)

    defense_cycle_list = cycles.create_cycle_list([decompressed_timd], 'defense', 'offense')
    calculated_data['timeDefending'] = cycles.total_cycle_time(defense_cycle_list)

    calculated_data['timeClimbing'] = cycles.filter_timeline_actions([decompressed_timd], actionType='climb')[0].get('actionTime')

    return calculated_data


def calculate_climb(decompressed_timd):
    climb_action = cycles.filter_timeline_actions([decompressed_timd], actionType='climb')[0]
    climb_action['climbSuccessful'] = (climb_action['attemptedClimb'] == climb_action['actualClimb'])
    return climb_action


def calculate_timd(compressed_timd, timd_name, test=False):
    decompressed_timd = decompression.decompress_timd(compressed_timd)
    decompressed_timd['calculated'] = calculate_statistics(decompressed_timd)
    decompressed_timd['climb'] = calculate_climb(decompressed_timd)

    if not test:
        print(f'{timd_name} decompressed')

        homeDir = os.path.expanduser('~')

        pyrebase_config = {
            "apiKey": sensitiveInfo.firebase_api_key(),
            "authDomain": "offseasondds.firebaseapp.com",
            "databaseURL": "https://offseasondds.firebaseio.com",
            "storageBucket": "offseasondds.appspot.com",
            "serviceAccount": os.path.join(homeDir, "ScoutingServer/config/offseasondds-3695dd827748.json")
        }

        firebase = pyrebase.initialize_app(pyrebase_config)
        database = firebase.database()

        # Save data in local cache
        if not os.path.exists(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs')):
            os.makedirs(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs'))

        with open(os.path.join(homeDir, f'ScoutingServer/cache/TIMDs/{timd_name}.json'), 'w') as file:
            pass
            #json.dump(decompressed_timd, file)
        print(f'{timd_name} cached')

        database.child("TIMDs").child(timd_name).set(decompressed_timd)
        database.child("decompedTIMDs").child(timd_name).set(compressed_timd)
        print(f'{timd_name} uploaded to Firebase')

    return decompressed_timd