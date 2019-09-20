import openpyxl
import os
import pyrebase

import sensitiveInfo


def get_sykes_data():
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

    sykes_file = os.path.join(homeDir, 'EMCC-2019Server/config/sykes.xlsx')
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
