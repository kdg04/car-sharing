import sqlite3
import pandas as pd

conn = sqlite3.connect('CarSharingDB.db') 
cursor = conn.cursor()

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