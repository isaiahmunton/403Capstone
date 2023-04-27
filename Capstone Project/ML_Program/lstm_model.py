import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
import datetime


# Define the create_dataset function, which takes a list of GPS data objects and returns a numpy array
def create_dataset(gps_data_list):
    data = []

    # Loop through each GPS date object in the input list
    for gps_date in gps_data_list:
        # Loop through each GPS time in the date object's gps_times dictionary
        for time_str, coords in gps_date.gps_times.items():
            # Convert the time string to a datetime.time object
            time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
            # Calculate the total number of seconds in the time object
            time_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
            # Append the time_seconds and coordinates to the data list
            data.append([time_seconds, coords['long'], coords['lat']])

    # Convert the data list to a numpy array and return it
    return np.array(data)

# Define the create_lstm_model function, which takes an input shape and returns a Keras LSTM model
def create_lstm_model(input_shape):
    model = Sequential()
    # Add an LSTM layer with 50 units and a ReLU activation function
    model.add(LSTM(50, activation='relu', input_shape=input_shape))
    # Add a Dense layer with 2 output units
    model.add(Dense(2))
    # Compile the model with an Adam optimizer and a mean squared error loss function
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model

# Define the train_lstm_model function, which trains a given model on given data
def train_lstm_model(model, X, y, epochs=100, batch_size=32):
    # Fit the model to the data with the specified epochs and batch size, without printing progress
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)

# Define the predict_coordinates_lstm function, which predicts coordinates for a given input time
def predict_coordinates_lstm(gps_data_list, input_time):
    # Create a dataset from the GPS data list
    data = create_dataset(gps_data_list)
    # Instantiate a MinMaxScaler object
    scaler = MinMaxScaler()
    # Scale the dataset using the scaler
    data_scaled = scaler.fit_transform(data)

    # Separate the input features (X) and target values (y)
    X, y = data_scaled[:, 0].reshape(-1, 1, 1), data_scaled[:, 1:]

    # Create an LSTM model with the appropriate input shape
    model = create_lstm_model((1, 1))
    # Train the LSTM model on the data
    train_lstm_model(model, X, y)

    # Convert the input_time string to a datetime.time object
    input_time_obj = datetime.datetime.strptime(input_time, "%H:%M:%S").time()
    # Calculate the total number of seconds in the input_time object
    input_time_seconds = input_time_obj.hour * 3600 + input_time_obj.minute * 60 + input_time_obj.second
    # Scale the input_time_seconds using the scaler
    input_time_scaled = scaler.transform([[input_time_seconds, 0, 0]])[:, 0].reshape(-1, 1, 1)
    # Make a prediction using the LSTM model for the input_time_scaled
    predicted_coords_scaled = model.predict(input_time_scaled)
    # Inverse transform the predicted coordinates using the scaler
    predicted_coords = scaler.inverse_transform(np.concatenate((input_time_scaled.reshape(-1, 1), predicted_coords_scaled), axis=1))[:, 1:]

    # Return the predicted coordinates (longitude, latitude) as a tuple
    return predicted_coords[0]
