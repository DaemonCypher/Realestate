import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from database_helper import *
from collections import Counter
from dateutil.relativedelta import relativedelta
from datetime import datetime

def prepare_data(city):
    """Fetch and prepare data for a given city from the SQLite database."""
    
    # Connect to the SQLite database
    conn = sqlite3.connect("validAddress.db")
    
    # Fetch data from the database
    results = fetch_city_from_db(conn, 'validAddress', city)
    
    # Determine the most common history length
    most_common_length = Counter(len(row[3]) for row in results).most_common(1)[0][0]
    
    # Create headers for the DataFrame
    data_date_dt = datetime.strptime(results[0][6], '%Y-%m-%d %H:%M:%S.%f')
    header = ['Address'] + [(data_date_dt - relativedelta(months=i)).strftime('%Y-%m') for i in range(most_common_length - 1, -1, -1)]
    
    # Transform results
    modified_results = [(address, *history) for id, address, city, history, status, status_date, data_date, beds, baths, year_built, sqft in results if len(history) == most_common_length]
    
    # Convert to DataFrame
    data = pd.DataFrame(modified_results, columns=header)
    
    conn.close()
    
    return data

def train_model_CNN(data,city):
    """Train a 1D CNN model on the provided data and return evaluation metrics and predictions."""
    
    # Extract addresses and prepare data
    addresses = data['Address']
    data = data.drop(columns=['Address'])
    X = data.values[:, :-1].reshape((-1, data.shape[1]-1, 1))
    y = data.values[:, -1]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define and compile the model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])),
        tf.keras.layers.MaxPooling1D(pool_size=2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    # Train the model
    model.fit(X_train, y_train, epochs=20, batch_size=64, validation_data=(X_test, y_test))
    
    # Evaluate and predict
    loss, mae = model.evaluate(X_test, y_test, verbose=0)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    predicted_next_month_prices = model.predict(X)
    
    # Prepare results
    predicted_prices_df = pd.DataFrame({
        'Address': addresses,
        'Predicted_Next_Month_Price': predicted_next_month_prices.flatten()
    })
    #model.save(f"saved_model/{city}-model")
    return mae, r2, predicted_prices_df


def train_model_LSTM(data,city):
    
    # cnn for city and lstm for state wide 
    """Train a LSTM model on the provided data and return evaluation metrics and predictions."""
    
        # Extract addresses and prepare data
    addresses = data['Address']
    data = data.drop(columns=['Address'])
    X = data.values[:, :-1]  # All but the last month
    y = data.values[:, -1]  # Last month

    X = X.reshape((X.shape[0], X.shape[1], 1))
    max_months = data.shape[1] - 1  # Subtract 1 to exclude the target column

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build the LSTM model
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(max_months//2, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])),
        tf.keras.layers.Dense(max_months//4, activation='relu'),
        tf.keras.layers.Dense(1)  # Linear activation for regression
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # Train the model
    model.fit(X_train, y_train, epochs=20, batch_size=64, validation_data=(X_test, y_test))
    
    # Evaluate and predict
    loss, mae = model.evaluate(X_test, y_test, verbose=0)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    predicted_next_month_prices = model.predict(X)
    
    # Prepare results
    predicted_prices_df = pd.DataFrame({
        'Address': addresses,
        'Predicted_Next_Month_Price': predicted_next_month_prices.flatten()
    })
    #model.save(f"saved_model/{city}-model")
    return mae, r2, predicted_prices_df


def train_model(data,city):
    if city == None or city =="":
        train_model_LSTM(data,city)
    elif city != None or city !="":
        train_model_CNN(data,city)
    else:
        return None