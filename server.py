import sensitiveInfo
from calculations import calculateTIMD, calculateTeam, pullPitscoutingData

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
    while True:
        rawTIMDs = database.child('rawTIMDs').get()
        if rawTIMDs.val() is None:
            time.sleep(5000)
        else:
            for temp_timd in rawTIMDs.each():
                calculateTIMD.calculate_timd(temp_timd.val(), temp_timd.key())
                database.child("rawTIMDs").child(temp_timd.key()).remove()
                team_num = temp_timd.key().split("-")[1]
                calculateTeam.calculate_team(team_num)


if __name__ == "__main__":
    run_server_comp()
