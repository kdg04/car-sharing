import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

# Load the data and preprocess
df = pd.read_csv('Updated_CarSharing.csv')
df.drop(['id', 'timestamp'], axis=1, inplace=True)  # Drop unrelated columns
df.dropna(inplace=True)  # Drop rows with missing values
df = pd.get_dummies(df, columns=['season', 'holiday', 'workingday', 'temp_category', 'weather_code'])     # Encode categorical variables

# Split the data into features and target
X = df.drop('demand', axis=1)
y = df['demand']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Random Forest Regressor
rf_regressor = RandomForestRegressor()
rf_regressor.fit(X_train, y_train)
rf_predictions = rf_regressor.predict(X_test)
rf_mse = mean_squared_error(y_test, rf_predictions)

# Deep Neural Network
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the DNN model using the functional API
shape = X_train_scaled.shape[1]
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(shape=(shape,)),  # Specify the input shape using `shape`
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')
history = model.fit(X_train_scaled, y_train, epochs=50, validation_split=0.2, verbose=0)
dnn_predictions = model.predict(X_test_scaled)
dnn_mse = mean_squared_error(y_test, dnn_predictions)

print(f"Random Forest Regressor MSE: {rf_mse}")
print(f"Deep Neural Network MSE: {dnn_mse}")
