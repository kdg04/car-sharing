import sqlite3
import pandas as pd

#df = pd.read_csv('CarSharing_updated.csv')       # updated CarSharing csv file  with additional column 'temp_category'
conn = sqlite3.connect('CarSharingDB.db')        # Create a connection to the SQLite database
cursor = conn.cursor()

cursor.execute("SELECT * FROM Car_Sharing")  
rows = cursor.fetchall()

df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

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

