import openpyxl
import os
import pyrebase

import sensitiveInfo


def pullPitScoutingData():
    homeDir = os.path.expanduser('~')

    pyrebase_config = {
        "apiKey": sensitiveInfo.firebase_api_key(),
        "authDomain": "emcc2019-fb7dd.firebaseapp.com",
        "databaseURL": "https://emcc2019-fb7dd.firebaseio.com",
        "storageBucket": "emcc2019-fb7dd.appspot.com",
        "serviceAccount": os.path.join(homeDir, "EMCC-2019Server/config/emcc2019-fb7dd-8de616e8bc8c.json")
    }

    firebase = pyrebase.initialize_app(pyrebase_config)
    database = firebase.database()

    pit_file = os.path.join(homeDir, 'EMCC-2019Server/config/pitscouting.xlsx')
    wb = openpyxl.load_workbook(pit_file)
    data = wb['Form Responses 1']

    rows = [row for row in data.iter_rows(min_row=2, min_col=1, max_col=8, values_only=True)]
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
    print("All pitscouting data pulled")


if __name__ == '__main__':
    pullPitScoutingData()
