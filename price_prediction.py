import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# Load the data
data = pd.read_csv('output.csv')

# Drop non-numeric columns
data = data.drop(columns=['Address','Status', 'Data Date'])

# Determine the maximum number of months
max_months = data.shape[1] - 1  # Subtract 1 to exclude the target column


# Pad the data to have a fixed number of months (if necessary)
# This step may not be necessary if all your data already has the same number of months
# X = ...  # Pad your data to have a fixed number of months

# Split the data into features (X) and target variable (y)
X = data.drop(columns=['2023-09'])
y = data['2023-09']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
scaler.fit(X_train)  # Fit the scaler on the training data
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_scaled = scaler.transform(X)  # Scale the entire dataset

# Build the neural network
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(max_months, activation='relu', input_shape=(max_months,)),  # Update input shape
    tf.keras.layers.Dense(max_months//2, activation='relu'),
    tf.keras.layers.Dense(max_months//4, activation='relu'),
    tf.keras.layers.Dense(1)  # Linear activation for regression
])

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Train the model
model.fit(X_train_scaled, y_train, epochs=50, batch_size=64, validation_data=(X_test_scaled, y_test))



# Evaluate the model
loss, mae = model.evaluate(X_test_scaled, y_test)
print(f'Mean Absolute Error: {mae}')

# Make predictions on the validation data
y_pred = model.predict(X_test_scaled)

# Compute R-squared (R²)
r2 = r2_score(y_test, y_pred)

# Print R-squared (R²)
print(f'R-squared (R²) on validation data: {r2}')


# Make predictions on the entire dataset
predictions = model.predict(X_scaled)

# Convert predictions to a pandas DataFrame
predictions_df = pd.DataFrame(predictions, columns=['Predicted Price'])
print(predictions_df)


# Assuming 'model' is the trained model
model.save("saved_model/my_model")

# The model will be saved in a directory 'saved_model/my_model'


