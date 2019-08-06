import utils
import sensitiveInfo

import json
import os
import pyrebase

from utils import percent_success_place, cycle_time_calculations
from utils.cycles import total_cycle_time, filter_timeline_actions
from utils.decompression import decompress_timd
from utils.statistics import percent_success_intake, true_offensive_contribution

very_cool_timd = 'A2B1114CbDaEdFtGfHkImJt|KrLzM143NmOsQxPf,KqLoM140Nm,KrLzM135NmOsQxPf,KqLoM129Nm,KrLyM122NmOvPf,KqLoM118Nm,KrLyM114NmOvPf,KqLpM111Nl,KrLyM107NlOvPf,KqLpM101Nl,KrLyM99NlOvPf,KqLoM97Nm,KrLyM92NmOuPf,KqLoM88Nm,KrLyM84NmOuPf,KqLoM80Nm,KrLyM75NmOsPf,KqLoM72Nm,KrLyM68NmOsPf,KqLpM66Nl,KrLyM62NlOuPf,KqLpM60Nl,KrLyM57NlOuPf,KqLpM53Nl,KrLyM51NlOsPf,KqLpM48Nl,KrLyM46NlOsPf,KqLpM42Nl,KrLzM39NlOsQxPf,KqLoM35Nm,KrLzM30NmOsQwPf,KqLpM28Nl,KrLzM24NlOsQwPf,KqLoM19Nm,KrLyM10NmOvPf,KaeM7RvSv'


def calculate_statistics(decompressed_timd):
    calculated_data = {}

    calculated_data['cargoScored'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo'))
    calculated_data['hatchesScored'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch'))
    calculated_data['totalCycles'] = calculated_data['cargoScored'] + calculated_data['hatchesScored']
    calculated_data['hatchesDropped'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='drop', actionPiece='hatch'))
    calculated_data['cargoDropped'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='drop', actionPiece='cargo'))
    calculated_data['cargoScoredSS'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', actionTime='sandstorm'))
    calculated_data['hatchScoredSS'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', actionTime='sandstorm'))
    calculated_data['cargoScoredTeleop'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', actionTime='teleop'))
    calculated_data['hatchScoredTeleop'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', actionTime='teleop'))
    calculated_data['hatchScoredRocket'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', actionPlace='rocket'))
    calculated_data['hatchScoredCargoShip'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', actionPlace='cargoShip'))
    calculated_data['hatchScoredLevel1'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', placeLevel='level1'))
    calculated_data['hatchScoredLevel2'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', placeLevel='level2'))
    calculated_data['hatchScoredLevel3'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='hatch', placeLevel='level3'))
    calculated_data['cargoScoredRocket'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', actionPlace='rocket'))
    calculated_data['cargoScoredCargoShip'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', actionPlace='cargoShip'))
    calculated_data['cargoScoredLevel1'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', placeLevel='level1'))
    calculated_data['cargoScoredLevel2'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', placeLevel='level2'))
    calculated_data['cargoScoredLevel3'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPiece='cargo', placeLevel='level3'))
    calculated_data['piecesScoredCargoShip'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPlace='cargoShip'))
    calculated_data['piecesScoredRocket'] = len(utils.filter_timeline_actions([decompressed_timd], actionType='place', actionPlace='rocket'))

    calculated_data['cargoPlaceSuccessRate'] = percent_success_place([decompressed_timd], actionPiece='cargo')
    calculated_data['hatchPlaceSuccessRate'] = percent_success_place([decompressed_timd], actionPiece='hatch')
    calculated_data['cargoShipPlaceSuccessRate'] = percent_success_place([decompressed_timd], actionPlace='cargoShip')
    calculated_data['rocketPlaceSuccessRate'] = percent_success_place([decompressed_timd], actionPlace='rocket')

    calculated_data['cargoIntakeSuccessRate'] = percent_success_intake(decompressed_timd, actionPiece='cargo')
    calculated_data['hatchIntakeSuccessRate'] = percent_success_intake(decompressed_timd, actionPiece='hatch')

    intake_to_place_cycle_list = utils.create_cycle_list([decompressed_timd], 'place', 'intake')

    calculated_data['undefendedHatchAverageCycleTime'] = cycle_time_calculations(intake_to_place_cycle_list, utils.avg, actionPiece='hatch', wasDefended=False)
    calculated_data['undefendedCargoAverageCycleTime'] = cycle_time_calculations(intake_to_place_cycle_list, utils.avg, actionPiece='cargo', wasDefended=False)
    calculated_data['undefendedRocketAverageCycleTime'] = cycle_time_calculations(intake_to_place_cycle_list, utils.avg, actionPlace='rocket', wasDefended=False)
    calculated_data['undefendedCargoShipAverageCycleTime'] = cycle_time_calculations(intake_to_place_cycle_list, utils.avg, actionPlace='cargoShip', wasDefended=False)
    calculated_data['undefendedLevel3AverageCycleTime'] = cycle_time_calculations(intake_to_place_cycle_list, utils.avg, placeLevel='level3', wasDefended=False)

    calculated_data['defendedHatchAverageCycleTime'] = cycle_time_calculations(intake_to_place_cycle_list, utils.avg, actionPiece='hatch', wasDefended=True)
    calculated_data['defendedCargoAverageCycleTime'] = cycle_time_calculations(intake_to_place_cycle_list, utils.avg, actionPiece='cargo', wasDefended=True)
    calculated_data['defendedRocketAverageCycleTime'] = cycle_time_calculations(intake_to_place_cycle_list, utils.avg, actionPlace='rocket', wasDefended=True)
    calculated_data['defendedCargoShipAverageCycleTime'] = cycle_time_calculations(intake_to_place_cycle_list, utils.avg, actionPlace='cargoShip', wasDefended=True)
    calculated_data['defendedLevel3AverageCycleTime'] = cycle_time_calculations(intake_to_place_cycle_list, utils.avg, placeLevel='level3', wasDefended=True)

    calculated_data['trueOffensiveContribution'] = true_offensive_contribution(decompressed_timd)

    incap_to_recap_cycle_list = utils.create_cycle_list([decompressed_timd], 'incap', 'recap')
    calculated_data['timeIncap'] = total_cycle_time(incap_to_recap_cycle_list)

    defense_cycle_list = utils.create_cycle_list([decompressed_timd], 'defense', 'offense')
    calculated_data['timeDefending'] = total_cycle_time(defense_cycle_list)

    calculated_data['timeClimbing'] = utils.filter_timeline_actions([decompressed_timd], actionType='climb')[0].get('actionTime')

    return calculated_data


def calculate_climb(decompressed_timd):
    climb_action = utils.filter_timeline_actions([decompressed_timd], actionType='climb')[0]
    climb_action['climbSuccessful'] = (climb_action['attemptedClimb'] == climb_action['actualClimb'])
    return climb_action


def calculate_timd(compressed_timd, timd_name):
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

    decompressed_timd = decompress_timd(compressed_timd)
    decompressed_timd['calculated'] = calculate_statistics(decompressed_timd)
    decompressed_timd['climb'] = calculate_climb(decompressed_timd)
    print(decompressed_timd)
    print(f'{timd_name} decompressed')

    # Save data in local cache
    if not os.path.exists(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs')):
        os.makedirs(os.path.join(homeDir, 'ScoutingServer/cache/TIMDs'))

    with open(os.path.join(homeDir, f'ScoutingServer/cache/TIMDs/{timd_name}.json'), 'w') as file:
        json.dump(decompressed_timd, file)
    print(f'{timd_name} cached')

    database.child("TIMDs").child(timd_name).set(decompressed_timd)
    print(f'{timd_name} uploaded to Firebase')


if __name__ == '__main__':
    calculate_timd(very_cool_timd, 'QM2-1114-a')