import sensitiveInfo
import os
import pyrebase

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
database = firebase.database()

def createTIMD(temp_timd):
    header, body = temp_timd.split("|")
    print(header)
    print(body)

    timd_name, scouts_initials = header.split(",")
    database.child("TIMDs").child(timd_name).child("Scouts Initials").set(scouts_initials)
    hatches, cargo = 0, 0
    for cycle in body.split(","):
        print(cycle)
        if cycle == 'h':
            hatches += 1
        elif cycle == 'c':
            cargo += 1
    print(timd_name)
    print(hatches)
    print(cargo)
    database.child("TIMDs").child(timd_name).child("Hatches").set(hatches)
    database.child("TIMDs").child(timd_name).child("Cargo").set(cargo)


while True:
    TEMP_TIMDS = database.child('rawTIMDs').get()
    if TEMP_TIMDS is not None:
        for temp_timd in TEMP_TIMDS.each():
            createTIMD(temp_timd.val())
            database.child("rawTIMDs").child(temp_timd.key()).remove()
