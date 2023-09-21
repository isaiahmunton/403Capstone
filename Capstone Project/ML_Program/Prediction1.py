import datetime
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from gpsdate import GPSDate
import time  # Import the time module

# Fetch the service account key JSON file contents
cred = credentials.Certificate(r"C:\Users\isaia\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\Database Connection\serviceAccountKey.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-pet-based-tracker-database-default-rtdb.firebaseio.com/'
})

# Define a function to fetch GPS data for a specified date range
def fetch_gps_data(start_date_str):
    # Parse the input date string to a date object
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    # Subtract one day from the start date
    start_date = start_date - datetime.timedelta(days=1)
    
    # Create a reference to the Coords node in the database
    coords_ref = db.reference('Coords')
    # Print a message to indicate data fetching has started
    print("Fetching data from the database...")
    # Record the start time of data fetching
    start_time = time.time()
    # Fetch the ordered data from the database
    coords_data = coords_ref.order_by_key().get()
    # Record the end time of data fetching
    end_time = time.time()
    # Print a message to indicate data fetching has completed
    print("Data fetched.")
    # Print the time taken to fetch data
    print(f"Time taken to fetch data: {end_time - start_time} seconds")

    # Initialize an empty list to store GPS dates
    gps_dates = []

    # Initialize the current_date variable with the start date
    current_date = start_date
    # Loop until 14 GPS dates are fetched
    while len(gps_dates) < 14:
        # Convert the current date to a string
        date_str = current_date.strftime("%Y-%m-%d")

        # Check if the date string exists in the fetched data
        if date_str in coords_data:
            # Get the coordinates data for the current date
            coord_data = coords_data[date_str]
            # Create a GPSDate object with the date string
            gps_date = GPSDate(date_str)

            # Loop through the time strings and coordinates in the coordinate data
            for time_str, coords in coord_data.items():
                # Add the GPS time and coordinates to the GPSDate object
                gps_date.add_gps_time(time_str, coords['long'], coords['lat'])
            
            # Append the GPSDate object to the gps_dates list
            gps_dates.append(gps_date)

        # Subtract one day from the current date
        current_date = current_date - datetime.timedelta(days=1)

    # Return the list of GPS dates
    return gps_dates

# Define a function to calculate the average location for a specified time
# Define a function to calculate the average location for a specified time
def average_location(gps_dates, input_time):
    # Initialize an empty list to store data
    data = []
    # Loop through the GPS dates
    for gps_date in gps_dates:
        # Loop through the time strings and coordinates in the GPS times dictionary
        for time_str, coords in gps_date.gps_times.items():
            # Create a dictionary to store the timestamp and coordinates
            row = {
                'timestamp': f"{gps_date.date} {time_str}",
                'latitude': coords['lat'],
                'longitude': coords['long']
            }
            # Append the row to the data list
            data.append(row)

    # Convert the data list to a pandas DataFrame
    data_df = pd.DataFrame(data)
    # Convert the timestamp column to datetime objects
    data_df['timestamp'] = pd.to_datetime(data_df['timestamp'])
    # Extract the time of day from the timestamp column
    data_df['time_of_day'] = data_df['timestamp'].dt.time
    # Convert the input time string to a time object
    input_time = datetime.datetime.strptime(input_time, "%H:%M:%S").time()
    
    # Define a time delta of 15 minutes
    time_delta = datetime.timedelta(minutes=15)
    # Calculate the time difference between each row and the input time
    data_df['time_difference'] = data_df['time_of_day'].apply(lambda x: abs(datetime.datetime.combine(datetime.date.min, x) - datetime.datetime.combine(datetime.date.min, input_time)))
    # Filter the data to keep only rows with time difference less than or equal to the time delta
    similar_time_data = data_df[data_df['time_difference'] <= time_delta]

    # Calculate the average latitude and longitude of the similar time data
    average_latitude = similar_time_data['latitude'].mean()
    average_longitude = similar_time_data['longitude'].mean()

    # Return the average latitude and longitude
    return average_latitude, average_longitude

# Main script execution starts here
if __name__ == "__main__":
    # Prompt the user for the start date input
    start_date_input = input("Enter the starting date (YYYY-MM-DD): ")
    # Fetch the GPS data for the given start date
    gps_data_list = fetch_gps_data(start_date_input)

    # Print the fetched GPS data
    for gps_date in gps_data_list:
        print(gps_date, '\n')

    # Prompt the user for the time input
    input_time = input("Enter the time (HH:MM:SS): ")

    # Record the start time for prediction
    start_time = time.time()
    # Calculate the predicted latitude and longitude
    predicted_lat, predicted_long = average_location(gps_data_list, input_time)
    # Record the end time for prediction
    end_time = time.time()

    # Print the time taken for prediction
    print(f"Time taken to make the prediction: {end_time - start_time} seconds")
    # Print the predicted coordinates at the given input time
    print(f"Predicted coordinates at {input_time}: Long: {predicted_long}, Lat: {predicted_lat}")