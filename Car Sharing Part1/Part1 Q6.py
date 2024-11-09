import sqlite3
import pandas as pd
from datetime import datetime

df = pd.read_csv('CarSharing.csv')
conn = sqlite3.connect('CarSharingDB.db') 
cursor = conn.cursor()

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