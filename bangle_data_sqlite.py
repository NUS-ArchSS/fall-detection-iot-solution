import sqlite3
import json


def insert_data(data):

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                (timestamp INTEGER, accel_x REAL, accel_y REAL, accel_z REAL, mag_x INTEGER, mag_y INTEGER, mag_z INTEGER)''')
    
    for row in data.values():
        c.execute("INSERT INTO sensor_data VALUES (?, ?, ?, ?, ?, ?, ?)", row)
        
    conn.commit()
    conn.close()