import openpyxl
import os
import pyrebase

import sensitiveInfo


def get_sykes_data():
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

    sykes_file = os.path.join(homeDir, 'ScoutingServer/config/sykes2.xlsx')
    wb = openpyxl.load_workbook(sykes_file)
    pred_contrib = wb['Sheet1']

    print("loaded")

    rows = [row for row in pred_contrib.iter_rows(min_row=2, max_col=5, values_only=True)]

    for row in rows:
        if not row[0]:
            break
        teamNumber = row[0]
        sykesData = {
            'teamName': row[1],
            'elo': row[2],
            'opr': row[4]
            }

        database.child("teams").child(teamNumber).child("sykes").set(sykesData)
        print(f'{teamNumber} Sykes uploaded to Firebase')
    print('All Sykes data pulled')


if __name__ == '__main__':
    get_sykes_data()
