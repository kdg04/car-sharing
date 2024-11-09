import sqlite3
import csv
conn = sqlite3.connect('CarSharingDB.db')
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
conn.close()



