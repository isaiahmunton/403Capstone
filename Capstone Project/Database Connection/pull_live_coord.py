import firebase_admin
from firebase_admin import credentials, db

# Fetch the service account key JSON file contents
cred = credentials.Certificate(r"C:\Users\isaia\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\Database Connection\serviceAccountKey.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-pet-based-tracker-database-default-rtdb.firebaseio.com/'
})

def print_newest_coordinate(event):
    # Get the event data (newest coordinate)
    data = event.data

    if data is None:
        print("No data available.")
    else:
        latest_key = list(data.keys())[-1]
        if 'long' in data[latest_key] and 'lat' in data[latest_key]:
            print(f"New GPS Coordinate Uploaded:\nDate: {event.path}\nTime: {latest_key}\nLongitude: {data[latest_key]['long']}\nLatitude: {data[latest_key]['lat']}")
        else:
            print("Incomplete coordinate data.")

# Reference the Coords node
coords_ref = db.reference('Live Coord')

# Set up a listener for the Coords node
listener = coords_ref.listen(print_newest_coordinate)

# Keep the program running
try:
    while True:
        pass
except KeyboardInterrupt:
    # Stop the listener when KeyboardInterrupt is received
    print("Stopping listener...")
    listener.close()