import sqlite3
import csv
import pandas as pd
from datetime import datetime


##################################     Q1     #####################################

conn = sqlite3.connect('CarSharingDB.db')
cursor = conn.cursor()

sql = """
CREATE TABLE IF NOT EXISTS Car_Sharing (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    season TEXT,
    holiday INTEGER,
    workingday INTEGER,
    weather TEXT,
    temp REAL,
    temp_feel REAL,
    humidity REAL,
    windspeed REAL,
    demand REAL
);
"""
conn.execute(sql)
rows = []
with open('CarSharing.csv', 'r', newline='') as csvFile:
    reader = csv.reader(csvFile, delimiter=',')
    header = next(reader)   # skip the header
    for row in reader:
        rows.append(tuple(row))
        #print(row)                      # uncomment to check the row values

sql = """
INSERT INTO Car_Sharing(id, timestamp, season, holiday, 
                       workingday, weather, temp, temp_feel,
                       humidity, windspeed, demand)
                       VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""
conn.executemany(sql, rows)

sql = """
CREATE TABLE Car_Sharing_Backup AS
SELECT * FROM Car_Sharing;
"""
conn.execute(sql)

# Commit the changes and close the connection
conn.commit()

##################################     Q1     #####################################

##################################     Q2     #####################################

df = pd.read_csv('CarSharing.csv')
df['temp_feel'] = df['temp_feel'].ffill()   # as temp is recorded on daily basis, missing values are forward filled with adjacent values

df['temp_category'] = df['temp_feel'].apply(lambda temp: "Cold" if temp < 10 else ("Mild" if temp <= 25 else "Hot"))
cursor.execute("ALTER TABLE Car_Sharing ADD COLUMN 'temp_category' TEXT")

cursor.executemany("UPDATE Car_Sharing SET temp_category = ? WHERE rowid = ?", 
                   zip(df['temp_category'].to_list(), range(1, len(df['temp_category'].to_list()) + 1)))
conn.commit()

##################################     Q2     #####################################

##################################     Q3     #####################################


temperature_df = df[['temp', 'temp_feel', 'temp_category']]

sql_temp_col_drop = """
    ALTER TABLE Car_Sharing
    DROP COLUMN temp
"""

sql_temp_feel_col_drop = """
    ALTER TABLE Car_Sharing
    DROP COLUMN temp_feel
"""

# table definition of temperature
sql_create_table = """                       
    CREATE TABLE IF NOT EXISTS temperature (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temp REAL,
        temp_feel REAL,
        temp_category TEXT
    );
"""

cursor.execute(sql_create_table)
conn.commit()                        # Commit the changes to the database

temperature_df.to_sql('temperature', conn, if_exists='replace', index=False)         # Write the dataframe to an SQLite table named "temperature"

# drop the columns temp and temp_feel from CarSharing table
cursor.execute(sql_temp_col_drop)    
cursor.execute(sql_temp_feel_col_drop)
conn.commit()                        # Commit the changes to the database

##################################     Q3     #####################################

##################################     Q4     #####################################

sql_distinct_weather = """
    SELECT DISTINCT weather
        FROM Car_Sharing;
"""

cursor.execute(sql_distinct_weather)
rows = cursor.fetchall()

weather_codes = []
weather_code = 1
new_col = 'weather_code'
for row in rows:
    row_list = list(row)                          # Convert the row tuple to a list for modification
    row_list.append(weather_code)   
    modified_row = tuple(row_list)                # Convert the modified list back to a tuple
    weather_code += 1
    weather_codes.append(modified_row)
print(weather_codes)

weather_dict = dict(weather_codes)                # Convert weather_codes to a dictionary for efficient lookup
df['weather_code'] = pd.NA                        # Create a new column 'weather_code' in df and initialize it with NaN values

df['weather_code'] = df['weather'].map(weather_dict)   # Update the 'weather_code' column based on the weather_dict
print(df)

cursor.execute("ALTER TABLE Car_Sharing ADD COLUMN 'weather_code' TEXT")

cursor.executemany("UPDATE Car_Sharing SET weather_code = ? WHERE rowid = ?", 
                   zip(df['weather_code'].to_list(), range(1, len(df['weather_code'].to_list()) + 1)))
conn.commit()

##################################     Q4     #####################################

##################################     Q5     #####################################

sql_create_weather_table = """                       
    CREATE TABLE IF NOT EXISTS weather (
        weather TEXT,
        weather_code TEXT
    );
"""
cursor.execute(sql_create_weather_table)
conn.commit()

# Copy data from weather and weather_code columns in CarSharing to weather table
sql_insert_into_weather = """
    INSERT INTO weather(weather, weather_code)
    SELECT weather, weather_code
    FROM Car_Sharing;
"""
cursor.execute(sql_insert_into_weather)

cursor.execute("ALTER TABLE Car_Sharing DROP COLUMN weather;")
conn.commit()

##################################     Q5     #####################################

##################################     Q6     #####################################

sql_time_table = """
    CREATE TABLE IF NOT EXISTS time (
        timestamp DATETIME,
        hour INTEGER,
        weekday_name TEXT,
        month_name TEXT
    );
"""

cursor.execute(sql_time_table)
conn.commit()

# Convert the 'timestamp' column to datetime objects
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extract hour, weekday name, and month name from the timestamp
df['hour'] = df['timestamp'].dt.strftime('%H')
df['weekday_name'] = df['timestamp'].dt.strftime('%A')
df['month_name'] = df['timestamp'].dt.strftime('%B')

# Convert timestamp to string format for SQLite insertion
df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Insert data from the DataFrame into the "time" table
for index, row in df.iterrows():
    cursor.execute("INSERT INTO time(timestamp, hour, weekday_name, month_name) VALUES (?, ?, ?, ?)", 
                   (row['timestamp'], row['hour'], row['weekday_name'], row['month_name']))
conn.commit()

##################################     Q6     #####################################

##################################     Q7     #####################################

cursor.execute("SELECT * FROM Car_Sharing")  
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])    #form a dataframe from database table

#####  7a  ######

df['timestamp'] = pd.to_datetime(df['timestamp'])
df_2017 = df[df['timestamp'].dt.year == 2017]                   # Filter rows for the year 2017

highest_demand_row = df_2017.loc[df_2017['demand'].idxmax()]    # Find the row with the highest demand rate in 2017
print("Date and time with the highest demand rate in 2017:", highest_demand_row['timestamp'])


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

print(results)


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

# Calculate the average demand rate for different weather categories for the highest demand month
average_demand_weather_highest_month = df_highest_demand_month.groupby('temp_category')['demand'].mean().sort_values(ascending=False).reset_index()

# Print the table
print(average_demand_weather_highest_month)


##################################     Q7     #####################################