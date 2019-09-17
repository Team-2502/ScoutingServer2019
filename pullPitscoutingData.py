import openpyxl
import os
import json
import pyrebase

import sensitiveInfo


def pullPitScoutingData():
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

    wb = openpyxl.load_workbook('pitscouting.xlsx')
    data = wb['Form Responses 1']

    rows = [row for row in data.iter_rows(min_row=2, min_col=1, max_col=8, max_row=68, values_only=True)]
    for row in rows:
        if not row[1]:
            break
        teamNumber = row[1]
        pitscouting = {
            'drivetrain': row[2],
            'length': row[6],
            'width': row[7]
            }
        database.child("teams").child(teamNumber).child('pitscouting').set(pitscouting)
        print(f'{teamNumber} pitscouting uploaded to Firebase')


if __name__ == '__main__':
    pullPitScoutingData()
