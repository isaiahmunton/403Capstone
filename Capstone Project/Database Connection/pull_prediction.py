import firebase_admin
from firebase_admin import credentials, db

# Fetch the service account key JSON file contents
cred = credentials.Certificate(r"C:\Users\isaia\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\Database Connection\serviceAccountKey.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-pet-based-tracker-database-default-rtdb.firebaseio.com/'
})

def save_prediction_and_flag(event):
    # Get the event data (newest coordinate)
    data = event.data
    print(data)
    f = open("flags/prediction.txt", "w")

    if data is None:
        print("No data available.")
        f.write("No data available.")
    else:
        print(f"Prediction flag = {data['New Request']}")
        f.write(str(data['New Request']))
        f.write('\n')
        print(f"Time = {data['Time']}")
        f.write(str(data['Time']))
    
    f.close()

# Reference the Coords node
coords_ref = db.reference('Prediction')

# Set up a listener for the Coords node
listener = coords_ref.listen(save_prediction_and_flag)

# Keep the program running
try:
    while True:
        pass
except KeyboardInterrupt:
    # Stop the listener when KeyboardInterrupt is received
    print("Stopping listener...")
    listener.close()