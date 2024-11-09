import sqlite3
import pandas as pd

df = pd.read_csv('CarSharing_updated.csv')       # contains additional column 'temp_category'
conn = sqlite3.connect('CarSharingDB.db')        # Create a connection to the SQLite database
cursor = conn.cursor()

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
#print(weather_codes)

weather_dict = dict(weather_codes)                # Convert weather_codes to a dictionary for efficient lookup
df['weather_code'] = pd.NA                        # Create a new column 'weather_code' in df and initialize it with NaN values

df['weather_code'] = df['weather'].map(weather_dict)   # Update the 'weather_code' column based on the weather_dict
#print(df)

cursor.execute("ALTER TABLE Car_Sharing ADD COLUMN 'weather_code' TEXT")

cursor.executemany("UPDATE Car_Sharing SET weather_code = ? WHERE rowid = ?", 
                   zip(df['weather_code'].to_list(), range(1, len(df['weather_code'].to_list()) + 1)))
conn.commit()