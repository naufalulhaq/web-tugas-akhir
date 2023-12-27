import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model

# Load encoder, scaler, and model once
encoder = joblib.load('items/encoder.joblib')
scaler = joblib.load('items/scaler.joblib')
model = load_model('items/model.h5')

def preprocess_data(input_df):
    # Columns to convert to float
    columns_to_convert = [
        'air_pollution_index', 'humidity', 'wind_speed', 'wind_direction',
        'visibility_in_miles', 'dew_point', 'temperature', 'rain_p_h',
        'snow_p_h', 'clouds_all', 'traffic_volume'
    ]

    # Convert specified columns to float
    input_df[columns_to_convert] = input_df[columns_to_convert].astype(float)

    # Categorical Features
    ohe_column = ['is_holiday', 'weather_type', 'weather_description']
    encoded_data = encoder.transform(input_df[ohe_column])

    # Concatenate Encoded Columns to Main DataFrame
    df_concated = pd.concat([input_df, pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out())], axis=1)
    df_concated.drop(columns=ohe_column, inplace=True)

    # Feature Engineering
    df_concated['date_time'] = pd.to_datetime(df_concated['date_time'])
    df_concated['day'] = df_concated['date_time'].dt.day
    df_concated['month'] = df_concated['date_time'].dt.month
    df_concated['hour'] = df_concated['date_time'].dt.hour

    # Set the 'date_time' as the index of the DataFrame
    df_concated.set_index('date_time', inplace=True)

    # Move Target column to the last
    df_concated['traffic_volume'] = df_concated.pop('traffic_volume')

    # Scale the data
    df_concated = pd.DataFrame(scaler.transform(df_concated), columns=scaler.get_feature_names_out(), index=df_concated.index)

    # Reshape into Input Data Requirement
    X = df_concated.values.reshape(1, 24, -1)  # Adjust the shape as per your model's requirement

    return X

def predict(input_df):
    X = preprocess_data(input_df)
    X_copy = np.repeat(model.predict(X), 62, axis=-1)
    X_unscale = scaler.inverse_transform(X_copy)[:,-1]
    return X_unscale