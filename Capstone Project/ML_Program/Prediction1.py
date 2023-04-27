import datetime
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from gpsdate import GPSDate
from lstm_model import create_dataset, create_lstm_model, train_lstm_model, predict_coordinates_lstm
import time

# Obtain the Firebase credentials from the JSON file
cred = credentials.Certificate(r"C:\Users\isaia\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\Database Connection\serviceAccountKey.json")

# Initialize the Firebase app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-pet-based-tracker-database-default-rtdb.firebaseio.com/'
})

# Define a function to fetch GPS data from the Firebase Realtime Database
def fetch_gps_data(start_date_str):
    # Convert the start date string to a date object
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    # Subtract one day from the start date
    start_date = start_date - datetime.timedelta(days=1)
    
    # Get a reference to the 'Coords' node in the database
    coords_ref = db.reference('Coords')
    print("Fetching data from the database...")
    start_time = time.time()  # Record the start time
    # Retrieve the GPS coordinates data from the database, ordered by key
    coords_data = coords_ref.order_by_key().get()
    end_time = time.time()  # Record the end time
    print("Data fetched.")
    print(f"Time taken to fetch data: {end_time - start_time} seconds")

    # Initialize an empty list to store GPS dates
    gps_dates = []

    # Initialize the current date to the start date
    current_date = start_date
    # Loop until 14 GPS dates are collected
    while len(gps_dates) < 14:
        # Convert the current date to a string in the format "YYYY-MM-DD"
        date_str = current_date.strftime("%Y-%m-%d")

        # If the current date is in the fetched coordinates data
        if date_str in coords_data:
            # Get the coordinate data for the current date
            coord_data = coords_data[date_str]
            # Create a GPSDate object for the current date
            gps_date = GPSDate(date_str)

            # Iterate through the coordinate data items
            for time_str, coords in coord_data.items():
                # Add the GPS time and coordinates to the GPSDate object
                gps_date.add_gps_time(time_str, coords['long'], coords['lat'])
            
            # Add the GPSDate object to the list of GPS dates
            gps_dates.append(gps_date)

        # Subtract one day from the current date
        current_date = current_date - datetime.timedelta(days=1)

    # Return the list of GPS dates
    return gps_dates

# Define a function to predict the coordinates using the LSTM model
def predict_coordinates(gps_data_list, input_time):
    # Call the predict_coordinates_lstm function with the GPS data list and input time
    predicted_coords = predict_coordinates_lstm(gps_data_list, input_time)
    # Return the predicted longitude and latitude
    return predicted_coords[0], predicted_coords[1]

if __name__ == "__main__":
    # Prompt the user to enter the starting date
    start_date_input = input("Enter the starting date (YYYY-MM-DD): ")
    # Fetch the GPS data using the provided starting date
    gps_data_list = fetch_gps_data(start_date_input)

    # Print each GPS date in the GPS data list
    for gps_date in gps_data_list:
        print(gps_date, '\n')

    # Prompt the user to enter the time
    input_time = input("Enter the time (HH:MM:SS): ")

    start_time = time.time()  # Record the start time
    predicted_long, predicted_lat = predict_coordinates(gps_data_list, input_time)
    end_time = time.time()  # Record the end time

    print(f"Time taken to make the prediction: {end_time - start_time} seconds")
    print(f"Predicted coordinates at {input_time}: Long: {predicted_long}, Lat: {predicted_lat}")
