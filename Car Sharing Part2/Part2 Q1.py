import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('CarSharingDB.db') 
cursor = conn.cursor()

cursor.execute("SELECT * FROM Car_Sharing")  
rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])    # form a dataframe from database table

df.drop_duplicates(inplace=True)          # Drop duplicate rows
df.dropna(subset=['id', 'timestamp', 'season', 'holiday', 'workingday'], inplace=True)  # drop rows for column nulll values

numeric_cols = ['humidity', 'windspeed']

# for numeric columns, if non-numeric values present, force conversion to numeric values or NaN
for col in numeric_cols:
    string_indices = df[df[col].apply(lambda x: isinstance(x, str))].index
    df.loc[string_indices, col] = pd.to_numeric(df.loc[string_indices, col], errors='coerce')
    df[col] = df[col].fillna(df[col].mean())

df.to_csv('Updated_CarSharing.csv', index=False)   # Save the preprocessed data to a new CSV file

print("New File Updated_CarSharing saved")

