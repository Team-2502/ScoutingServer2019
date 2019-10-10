import sensitiveInfo
from calculations import calculateTIMD, calculateTeam, pullPitscoutingData
import export

import os
import pyrebase
import time

homeDir = os.path.expanduser('~')

# Firebase setup
pyrebase_config = {
        "apiKey": sensitiveInfo.firebase_api_key(),
        "authDomain": "emcc2019-fb7dd.firebaseapp.com",
        "databaseURL": "https://emcc2019-fb7dd.firebaseio.com",
        "storageBucket": "emcc2019-fb7dd.appspot.com",
        "serviceAccount": os.path.join(homeDir, "EMCC-2019Server/config/emcc2019-fb7dd-8de616e8bc8c.json")
    }

firebase = pyrebase.initialize_app(pyrebase_config)
database = firebase.database()


def reset_timds():
    for timd in database.child('decompedTIMDs').get().each():
        database.child("rawTIMDs").child(timd.key()).set(timd.val())
        database.child("decompedTIMDs").child(timd.key()).remove()


def run_server_testing():
    pullPitscoutingData.pullPitScoutingData()

    rawTIMDs = database.child('rawTIMDs').get()
    if rawTIMDs.val() is None:
        reset_timds()

    rawTIMDs = database.child('rawTIMDs').get()
    for temp_timd in rawTIMDs.each():
        calculateTIMD.calculate_timd(temp_timd.val(), temp_timd.key())
        database.child("rawTIMDs").child(temp_timd.key()).remove()
        team_num = temp_timd.key().split("-")[1]
        calculateTeam.calculate_team(team_num)


def run_server_comp():
    current_unfinished_match = 1
    timds_in_last_match = 0

    while True:
        rawTIMDs = database.child('rawTIMDs').get()
        if rawTIMDs.val() is None:
            time.sleep(5)
        else:
            for temp_timd in rawTIMDs.each():
                timd = calculateTIMD.calculate_timd(temp_timd.val(), temp_timd.key())

                match_num = timd['match_number']
                if match_num == current_unfinished_match:
                    timds_in_last_match += 1
                    if timds_in_last_match == 6:
                        print("\nAll TIMDs for QM " + str(current_unfinished_match) + " synced\n")
                        timds_in_last_match = 0
                        export.export_spreadsheet()
                        print("Data exported")
                        export.upload_to_drive(" Post QM" + str(current_unfinished_match) + "Full Export")
                        print("Data uploaded to Drive\n")
                        current_unfinished_match += 1

                database.child("rawTIMDs").child(temp_timd.key()).remove()
                team_num = temp_timd.key().split("-")[1]
                calculateTeam.calculate_team(team_num, timd)


if __name__ == "__main__":
    run_server_comp()
