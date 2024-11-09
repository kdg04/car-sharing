import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from math import sqrt
from prettytable import PrettyTable

import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Load CSV file into a DataFrame
df = pd.read_csv('CarSharing.csv')

# Convert 'timestamps' column to datetime format and set it as the index
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M')
df.set_index('timestamp', inplace=True)

# Resample data to calculate weekly average demand rate
weekly_avg_demand = df['demand'].resample('W-MON').mean()

# print(weekly_avg_demand.head())

# Split data into training and testing sets (70% training, 30% testing)
train_size = int(len(weekly_avg_demand) * 0.7)
train_data, test_data = weekly_avg_demand[:train_size], weekly_avg_demand[train_size:]

table = PrettyTable()
table.field_names = ["ADF Statistic", "P-value", "d"]

# Perform differencing if the ADF test hints at non-stationarity
def check_stationarity(data):
    # Handle missing values
    data = data.dropna()
    
    result = adfuller(data)
    adf_stats, p_value = result[0], result[1]
    # Add data to the table
    table.add_row([adf_stats, p_value, d])
    print(table)

    if p_value <= 0.05:
        print("Series is stationary at significance level 0.05 at d = ", d)
        return True
    else:
        print("Series is not stationary at significance level 0.05. Performing differencing ...\n")
        return False

max_differencing = 2  # Set a maximum level of differencing
d = 0       
is_stationary = check_stationarity(train_data)

while not is_stationary:
    if d >= max_differencing:
        print("Stationarity not achieved after maximum differencing.")
        break
    train_data = train_data.diff().dropna()
    d += 1
    is_stationary = check_stationarity(train_data)

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

plot_acf(train_data)
plot_pacf(train_data)
plt.show()

p = int(input("Enter the value of p : "))
q = int(input("Enter the value of q : "))

# Fit ARIMA model to the training data
model = ARIMA(train_data, order=(p, d, q))  # Example order, you can adjust based on model performance
model_fit = model.fit()

# Fill missing values in test_data with the mean value
test_data_filled = test_data.fillna(test_data.mean())


# Make predictions on the testing data
predictions = model_fit.forecast(steps=len(test_data))

# Make predictions for future weeks
future_steps = 4  # adjust for convenience

frequency = 'W-MON'

# Convert predictions to a DataFrame with dates
future_dates = pd.date_range(start=weekly_avg_demand.index[-1], periods=future_steps + 1, freq=frequency)[1:]

future_predictions = model_fit.forecast(steps=future_steps, index=future_dates)


future_df = pd.DataFrame({'Date': future_dates, 'Predicted Demand Rate': future_predictions})


# Fill missing values in test_data with the mean value
test_data_filled = test_data.fillna(test_data.mean())

# Calculate RMSE
# Ensure the lengths of test_data_filled and future_predictions match for RMSE calculation
if len(test_data_filled) == len(future_predictions):
    rmse = sqrt(mean_squared_error(test_data_filled, future_predictions))
else:
    # Adjust the lengths of test_data_filled and future_predictions to match for RMSE calculation
    min_len = min(len(test_data_filled), len(future_predictions))
    test_data_filled = test_data_filled[:min_len]
    future_predictions = future_predictions[:min_len]
    rmse = sqrt(mean_squared_error(test_data_filled, future_predictions))

print(f'Root Mean Squared Error (RMSE): {rmse}')

print('Future predictions:')
print(future_predictions)
