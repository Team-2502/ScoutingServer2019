import openpyxl
import os
import json
import tbapy
import pyrebase

import sensitiveInfo


def get_sykes_data():
    homeDir = os.path.expanduser('~')

    tba = tbapy.TBA(sensitiveInfo.tba_api_key())
    event = "2019dar"
    teams = [int(team['key'][3:]) for team in tba.event_teams(event)]

    pyrebase_config = {
        "apiKey": sensitiveInfo.firebase_api_key(),
        "authDomain": "offseasondds.firebaseapp.com",
        "databaseURL": "https://offseasondds.firebaseio.com",
        "storageBucket": "offseasondds.appspot.com",
        "serviceAccount": os.path.join(homeDir, "ScoutingServer/config/offseasondds-3695dd827748.json")
    }

    firebase = pyrebase.initialize_app(pyrebase_config)
    database = firebase.database()

    sykes_file = os.path.join(homeDir, 'ScoutingServer/config/sykes.xlsm')
    wb = openpyxl.load_workbook(sykes_file)
    pred_contrib = wb['predicted contributions']

    rows = [row for row in  pred_contrib.iter_rows(min_row=3, max_col=5, max_row= 3+len(teams), values_only=True)]

    for row in rows:
        team = {
            'teamNumber': row[0],
            'sykesData': {
                'teamName': row[1],
                'elo': row[2],
                'opr': row[4]
            }
        }
        team_number = team['teamNumber']
        with open(os.path.join(homeDir, f'ScoutingServer/cache/teams/{team_number}.json'), 'w') as file:
            json.dump(team, file)
        print(f'{team_number} cached')

        database.child("teams").child(team_number).set(team)
        print(f'{team_number} uploaded to Firebase')
    print('All team data pulled')


if __name__ == '__main__':
    get_sykes_data()
