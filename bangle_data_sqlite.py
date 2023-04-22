import sqlite3
import json


def insert_data(data):
    conn = sqlite3.connect('bangle_data.db')
    c = conn.cursor()

    # Create table
    c.execute("CREATE TABLE IF NOT EXISTS sensor_data (data JSON)")

    c.execute("INSERT INTO sensor_data (data) VALUES (?)",
              (json.dumps(data),))

    conn.commit()

    conn.close()
