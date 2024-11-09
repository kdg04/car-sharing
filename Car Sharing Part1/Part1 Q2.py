import sqlite3
import csv
import pandas as pd

df = pd.read_csv('CarSharing.csv')
conn = sqlite3.connect('CarSharingDB.db')
cursor = conn.cursor()

df['temp_feel'] = df['temp_feel'].ffill()   # as temp is recorded on daily basis, missing values are forward filled with adjacent values

df['temp_category'] = df['temp_feel'].apply(lambda temp: "Cold" if temp < 10 else ("Mild" if temp <= 25 else "Hot"))

cursor.execute("ALTER TABLE Car_Sharing ADD COLUMN 'temp_category' TEXT")

cursor.executemany("UPDATE Car_Sharing SET temp_category = ? WHERE rowid = ?", 
                   zip(df['temp_category'].to_list(), range(1, len(df['temp_category'].to_list()) + 1)))
conn.commit()


df.to_csv('CarSharing_updated.csv', index=False)   # Save the updated DataFrame back to CSV
