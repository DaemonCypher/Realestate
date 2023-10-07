import pandas as pd
import numpy as np
import tensorflow as tf

# Load the saved model
loaded_model = tf.keras.models.load_model("saved_model/my_model")

# Load new data from `new_data.csv`
new_data = pd.read_csv('output.csv')

# Drop non-numeric columns (assuming same structure as `output.csv` with Address, Status, Data Date columns)
new_data = new_data.drop(columns=['Address', 'Status', 'Data Date'])

# After loading and preprocessing the new data
# Exclude the first month from the data to match the input shape the model expects
X_new = new_data.values[:, 1:]  # Exclude the first month
X_new = X_new.reshape((X_new.shape[0], X_new.shape[1], 1))


# Predict next month prices using the loaded model
predicted_prices = loaded_model.predict(X_new)

# Store predictions in a DataFrame
predicted_prices_df = pd.DataFrame(predicted_prices, columns=['Predicted Price for Next Month'])
print(predicted_prices_df)
