import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
import datetime


def create_dataset(gps_data_list):
    data = []

    for gps_date in gps_data_list:
        for time_str, coords in gps_date.gps_times.items():
            time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
            time_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
            data.append([time_seconds, coords['long'], coords['lat']])

    return np.array(data)

def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=input_shape))
    model.add(Dense(2))
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return model

def train_lstm_model(model, X, y, epochs=100, batch_size=32):
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)

def predict_coordinates_lstm(gps_data_list, input_time):
    data = create_dataset(gps_data_list)
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    X, y = data_scaled[:, 0].reshape(-1, 1, 1), data_scaled[:, 1:]

    model = create_lstm_model((1, 1))
    train_lstm_model(model, X, y)

    input_time_obj = datetime.datetime.strptime(input_time, "%H:%M:%S").time()
    input_time_seconds = input_time_obj.hour * 3600 + input_time_obj.minute * 60 + input_time_obj.second
    input_time_scaled = scaler.transform([[input_time_seconds, 0, 0]])[:, 0].reshape(-1, 1, 1)

    predicted_coords_scaled = model.predict(input_time_scaled)
    predicted_coords = scaler.inverse_transform(np.concatenate((input_time_scaled.reshape(-1, 1), predicted_coords_scaled), axis=1))[:, 1:]

    return predicted_coords[0]