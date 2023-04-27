import csv
import os

import firebase_admin
from firebase_admin import credentials, firestore, db

# Fetch the service account key JSON file contents
cred = credentials.Certificate(r"C:\Users\isaia\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\Database Connection\serviceAccountKey.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-pet-based-tracker-database-default-rtdb.firebaseio.com/'
})

# Save data
ref = db.reference('py/')
users_ref = ref.child('users')
users_ref.set({
    'alanisawesome': {
        'data_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'data_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
})

# Update data
for  i in range(3):
    hopper_ref = users_ref.child('gracehop')
    hopper_ref.update({
        'nickname': 'Amazing Grace'
    })

# Read data
handle = db.reference('py/users/alanisawesome')

# Read the data at the posts reference (this is a blocking operation)
print(ref.get())

# db = firestore.client()
# collection_ref = db.collection("Coords")

# with open(r'C:\Users\isaia\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\ML Program\Clean_Data\CleanData.csv', 'r') as file:
#     reader = csv.reader(file)
#     next(reader)
#     for row in reader:
#         data = {
#             'X coord': row[0],
#             'Y coord': row[1]
#         }
#     collection_ref.add(data)
# db.close()