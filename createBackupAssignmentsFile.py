import tbapy
import random
import os
import json
import pyrebase

# File with functions which return info such as API keys and passwords
import sensitiveInfo

homeDir = os.path.expanduser('~')

# Firebase setup
pyrebase_config = {
    "apiKey": sensitiveInfo.firebase_api_key(),
    "authDomain": "offseasondds.firebaseapp.com",
    "databaseURL": "https://offseasondds.firebaseio.com",
    "storageBucket": "offseasondds.appspot.com",
    "serviceAccount": os.path.join(homeDir, "ScoutingData/config/offseasondds-3695dd827748.json")
}
firebase = pyrebase.initialize_app(pyrebase_config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(sensitiveInfo.firebase_email(), sensitiveInfo.firebase_password())
database = firebase.database()

# Setup for tbapy
tba = tbapy.TBA(sensitiveInfo.tba_api_key())
event = "2019dar"

# Get a list of all qualifying matches at an event
try:
    matches = [match for match in tba.event_matches(event, simple=True) if match['comp_level'] == 'qm']

# TODO Make this except clause more specfic
except:
    print("Error getting matches from TBA, check event and API keys.")
    exit(1)

full_assignments = {}

for match in matches:
    # Query TBA for info about each match
    match_num = match['match_number']
    redTeams = match['alliances']['red']['team_keys']
    redTeams = [int(team[3:]) for team in redTeams]
    blueTeams = match['alliances']['blue']['team_keys']
    blueTeams = [int(team[3:]) for team in blueTeams]
    teams = redTeams + blueTeams

    assignments = {}
    numScouts = 6
    scouts = ['scout' + str(x) for x in range(1, numScouts + 1)]
    available_scouts = list(scouts)

    # Assign each scout to a team
    for team in teams:
        # Distribute scouts evenly among teams as possible
        for x in range(int(numScouts / 6)):
            chosen_scout = random.choice(available_scouts)
            assignments[chosen_scout] = {'team': team, 'alliance': ('red' if team in redTeams else 'blue')}
            available_scouts.remove(chosen_scout)

    # For scouts that cannot be assigned evenly pick a random team to scout
    extra_teams = random.sample(set(teams), numScouts % len(teams))
    for team in extra_teams:
        chosen_scout = random.choice(available_scouts)
        assignments[chosen_scout] = {'team': team, 'alliance': ('red' if team in redTeams else 'blue')}
        available_scouts.remove(chosen_scout)

    full_assignments["match"+str(match_num)] = assignments

# Save file as json and txt
with open(os.path.join(homeDir, 'ScoutingData/assignments/BackupAssignments.json'), 'w') as f:
    json.dump(full_assignments, f)

with open(os.path.join(homeDir, 'ScoutingData/assignments/BackupAssignments.txt'), 'w') as f:
    f.write(json.dumps(full_assignments))

# Upload assignments to Firebase
database.child("assignments").child("BackupAssignments").set(json.dumps(full_assignments))
