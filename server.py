import sensitiveInfo
import createTIMD

import os
import pyrebase

homeDir = os.path.expanduser('~')

# Firebase setup
pyrebase_config = {
    "apiKey": sensitiveInfo.firebase_api_key(),
    "authDomain": "offseasondds.firebaseapp.com",
    "databaseURL": "https://offseasondds.firebaseio.com",
    "storageBucket": "offseasondds.appspot.com",
    "serviceAccount": os.path.join(homeDir, "ScoutingServer/config/offseasondds-3695dd827748.json")
}

firebase = pyrebase.initialize_app(pyrebase_config)
database = firebase.database()

while True:
    rawTIMDs = database.child('rawTIMDs').get()
    if rawTIMDs.val() is not None:
        for temp_timd in rawTIMDs.each():
            createTIMD.calculate_TIMD(temp_timd.val(), temp_timd.key())
            database.child("rawTIMDs").child(temp_timd.key()).remove()
