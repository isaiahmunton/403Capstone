import csv
import os
import time

import firebase_admin
from firebase_admin import credentials, firestore, db
import pandas as pd

# Obtain the Firebase credentials from the JSON file
cred = credentials.Certificate(r"C:\Users\isaia\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\Database Connection\serviceAccountKey.json")

start_time = time.time()
# Initialize the Firebase app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-pet-based-tracker-database-default-rtdb.firebaseio.com/'
})

# Read the CleanData.csv file, skipping the first row
df = pd.read_csv(r'~\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\ML_Program\Clean_Data\CleanData.csv')

# Get a reference to the 'Coords' node in the Firebase Realtime Database
coords_ref = db.reference('Coords')
live_coords_ref = db.reference('Live Coord')
prediction_requset = db.reference('Prediction')

prediction_requset.update({
    'New Request': 'true'
})
prediction_requset.update({
    'Time': ''
})

# Dummy variable to break out of the for loop early
x = 0
# Save first date
old_date = ''
# Keep track of time it takes to upload each point
upload_times = []
# Iterate through rows
for i, row in df.iterrows():
    # Round longitude and latitude to 3 decimal places
    rounded_long = round(row[1], 3)
    rounded_lat = round(row[2], 3)
    # Record the start time for uploading a point
    upload_start_time = time.time()

    # Check if the current date is the same as the old date
    if old_date == row[0][:10]:
        # If the date is the same, update the date node with the new coordinates
        for i in range(3):
            date_ref = coords_ref.child(row[0][:10])
            #live_date_ref = live_coords_ref.child(row[0][:10])
            date_ref.update({
                row[0][11:19]: {
                    'long': rounded_long,
                    'lat': rounded_lat,
                }
            })
            live_coords_ref.set({
                row[0][11:19]: {
                    'long': rounded_long,
                    'lat': rounded_lat,
                }
            })
    else:
        # If the date is different, set a new date node with the coordinates
        date_ref = coords_ref.child(row[0][:10])
        date_ref.set({
            row[0][11:19]: {
                'long': rounded_long,
                'lat': rounded_lat,
            }
        })
        live_coords_ref.set({
            row[0][11:19]: {
                'long': rounded_long,
                'lat': rounded_lat,
            }
        })

    # Append the time it took to upload a point to the upload_times list
    upload_times.append(time.time() - upload_start_time)
    # Update the old_date variable with the current date
    old_date = row[0][:10]
    # Print the current value of x (for progress tracking)
    print(x)
    # Increment x by 1
    x += 1
    # Break the loop after processing 1000 points
    if x > 500:
        break

# Calculate and print the average time to upload a point
print("--- Average time to upload a point: %s seconds ---" % (sum(upload_times)/len(upload_times)))