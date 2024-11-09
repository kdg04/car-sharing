import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('CarSharingDB.db') 
cursor = conn.cursor()

cursor.execute("SELECT * FROM Car_Sharing")  
rows = cursor.fetchall()

#####  7a  ######

df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])    #form a dataframe from database table

df['timestamp'] = pd.to_datetime(df['timestamp'])
df_2017 = df[df['timestamp'].dt.year == 2017]                   # Filter rows for the year 2017

highest_demand_row = df_2017.loc[df_2017['demand'].idxmax()]    # Find the row with the highest demand rate in 2017
print("\nDate and time with the highest demand rate in 2017:\n", highest_demand_row['timestamp'])


#####  7b  #####


avg_demand_on_weekday = df_2017.groupby(df_2017['timestamp'].dt.strftime('%A'))['demand'].mean()
avg_demand_in_month = df_2017.groupby(df_2017['timestamp'].dt.strftime('%B'))['demand'].mean()
avg_demand_in_season = df_2017.groupby(df_2017['season'])['demand'].mean()

# weekdays, months, and seasons with highest and lowest average demand rates
highest_demand_weekday = avg_demand_on_weekday.idxmax(), avg_demand_on_weekday.max()
lowest_demand_weekday = avg_demand_on_weekday.idxmin(), avg_demand_on_weekday.min()

highest_demand_month = avg_demand_in_month.idxmax(), avg_demand_in_month.max()
lowest_demand_month = avg_demand_in_month.idxmin(), avg_demand_in_month.min()

highest_demand_season = avg_demand_in_season.idxmax(), avg_demand_in_season.max()
lowest_demand_season = avg_demand_in_season.idxmin(), avg_demand_in_season.min()

# Create a DataFrame to display the results
results = pd.DataFrame({
    ' Category': ['Weekday', 'Month', 'Season'],
    '   Highest Point': [highest_demand_weekday[0], highest_demand_month[0], highest_demand_season[0]],
    '   Highest Average Demand': [highest_demand_weekday[1], highest_demand_month[1], highest_demand_season[1]],
    '   Lowest Point': [lowest_demand_weekday[0], lowest_demand_month[0], lowest_demand_season[0]],
    '   Lowest Average Demand': [lowest_demand_weekday[1], lowest_demand_month[1], lowest_demand_season[1]]
})

print()
print(results)
print()


#####  7c  #####


selected_weekday = highest_demand_weekday[0]
df_selected_weekday = df[(df['timestamp'].dt.year == 2017) & (df['timestamp'].dt.strftime('%A') == selected_weekday)]

# Group by hour and calculate the average demand rate for each hour
average_demand_hour = df_selected_weekday.groupby(df_selected_weekday['timestamp'].dt.hour)['demand'].mean().reset_index()

# Sort the results in descending order based on the average demand rates
average_demand_hour_descending = average_demand_hour.sort_values(by='demand', ascending=False)


#print(average_demand_hour)
# Create a DataFrame to display the results
results_hour = pd.DataFrame({
    'Hour': average_demand_hour_descending['timestamp'],
    'Average Demand Rate': average_demand_hour_descending['demand']
})

print()
print(results_hour)


#####  7d  #####


# Calculate the prevalence of each weather category
weather_category_counts = df_2017['temp_category'].value_counts()

# The most prevalent weather condition based on weather_code
most_prevalent_weather = df_2017['weather_code'].mode().iloc[0]

# clean data for 'windspeed' and 'humidity'
string_indices = df_2017[df_2017['windspeed'].apply(lambda x: isinstance(x, str))].index
df_2017.loc[string_indices, 'windspeed'] = pd.to_numeric(df_2017.loc[string_indices, 'windspeed'], errors='coerce')

string_indices = df_2017[df_2017['humidity'].apply(lambda x: isinstance(x, str))].index
df_2017.loc[string_indices, 'humidity'] = pd.to_numeric(df_2017.loc[string_indices, 'humidity'], errors='coerce')

# Average, highest, and lowest wind speed and humidity for each month
monthly_stats = df_2017.groupby(df_2017['timestamp'].dt.month)[['windspeed', 'humidity']].agg(['mean', 'max', 'min'])

# Average demand rate for each weather category
average_demand_weather = df_2017.groupby('temp_category')['demand'].mean().sort_values(ascending=False).reset_index()

print()
print("Prevalence of Weather Categories in 2017:")
print(weather_category_counts)
print("\nMost Prevalent Weather Condition (Weather Code):", most_prevalent_weather)
print("\nMonthly Statistics for Wind Speed and Humidity:")
print(monthly_stats)
print("\nAverage Demand Rate for Each Weather Category in Descending Order:")
print(average_demand_weather)
print()


#####  7e  #####


# Identify the month with the highest average demand rate
highest_demand_month = df_2017.groupby(df_2017['timestamp'].dt.month)['demand'].mean().idxmax()
#print("highest demand month ", highest_demand_month)
print()

# Filter the DataFrame for the highest demand month
df_highest_demand_month = df_2017[df_2017['timestamp'].dt.month == highest_demand_month]
#print(df_highest_demand_month)
print()

weather_counts = df_highest_demand_month['temp_category'].value_counts()

# The most prevalent weather condition in the month with highest avg demand rate
most_prevalent_weather_in_highest_demand_mnth = weather_counts.idxmax()

print(f"\nMost prevalent weather condition in highest demand month in 2017: {most_prevalent_weather_in_highest_demand_mnth}\n")

# Average, highest, and lowest wind speed and humidity for the month with highest demand rate
month_stats = df_highest_demand_month.groupby(df_highest_demand_month['timestamp'].dt.month)[['windspeed', 'humidity']].agg(['mean', 'max', 'min'])
print(month_stats)

# Calculate the average demand rate for different weather categories for the highest demand month
average_demand_weather_highest_month = df_highest_demand_month.groupby('temp_category')['demand'].mean().sort_values(ascending=False).reset_index()

# Print the table
print(average_demand_weather_highest_month)
