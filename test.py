import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the saved model
loaded_model = tf.keras.models.load_model('saved_model/my_model')

# Assuming you have the data for the next month in a CSV file called 'next_month.csv'
# Load the next month data
next_month_data = pd.read_csv('output.csv')

# Drop non-numeric columns (assuming the same columns are to be dropped as before)
next_month_data = next_month_data.drop(columns=['Address', 'Status', 'Data Date','2023-09'])

# Standardize the data using the same scaler used before
# It's important to use the same scaler to ensure the data is scaled in the same way as the training data
scaler = StandardScaler()  # Assuming the scaler was initialized like this before
scaler.fit(next_month_data)  # If the scaler was saved before, load it instead of fitting a new one
next_month_data_scaled = scaler.transform(next_month_data)

# Make predictions on the next month data
next_month_predictions = loaded_model.predict(next_month_data_scaled)

# Convert predictions to a pandas DataFrame
next_month_predictions_df = pd.DataFrame(next_month_predictions, columns=['Predicted Price'])
print(next_month_predictions_df)
