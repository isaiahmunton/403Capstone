import csv
import os
import time

import firebase_admin
from firebase_admin import credentials, firestore, db
import pandas as pd


# Fetch the service account key JSON file contents
cred = credentials.Certificate(r"C:\Users\isaia\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\Database Connection\serviceAccountKey.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-pet-based-tracker-database-default-rtdb.firebaseio.com/'
})

buzzer_ref = db.reference('Buzzer')

flag_state = input('Enter true or false (q to quit): ')
while (flag_state != 'q'):
    if flag_state == 'true':
        print('Buzzer flag set to true')
        buzzer_ref.set({
            'Buzzer' : True
        })
    elif flag_state == 'false':
        print('Buzzer flag set to false')
        buzzer_ref.set({
            'Buzzer' : False
        })
    elif flag_state == 'q':
        print('quitting')
        break
    else:
        print('invalid input')
    flag_state = input('Enter true or false (q to quit): ')