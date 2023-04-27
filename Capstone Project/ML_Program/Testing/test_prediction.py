import pandas as pd
import datetime
from gpsdate import GPSDate
from lstm_model import predict_coordinates_lstm

def read_csv_data(file_name):
    df = pd.read_csv(file_name)
    unique_dates = df['date'].unique()
    gps_dates = []

    for date_str in unique_dates:
        gps_date = GPSDate(date_str)
        date_df = df[df['date'] == date_str]

        for index, row in date_df.iterrows():
            time_str, long, lat = row['time'], row['long'], row['lat']
            gps_date.add_gps_time(time_str, long, lat)

        gps_dates.append(gps_date)

    return gps_dates

def predict_coordinates(gps_data_list, input_time):
    predicted_coords = predict_coordinates_lstm(gps_data_list, input_time)
    return predicted_coords[0], predicted_coords[1]

if __name__ == "__main__":
    file_name = "sample_gps_data.csv"
    gps_data_list = read_csv_data(file_name)

    input_time = input("Enter the time (HH:MM:SS): ")

    predicted_long, predicted_lat = predict_coordinates(gps_data_list, input_time)

    print(f"Predicted coordinates at {input_time}: Long: {predicted_long}, Lat: {predicted_lat}")