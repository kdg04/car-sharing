import csv
import sqlite3


conn = sqlite3.connect('CarSharingDB.db')

cursor = conn.cursor()
cursor.execute("SELECT * FROM time")
rows = cursor.fetchmany(30)
header = [description[0] for description in cursor.description]

print()
print(header)
for row in rows:
    print(row)

conn.commit()
conn.close()
