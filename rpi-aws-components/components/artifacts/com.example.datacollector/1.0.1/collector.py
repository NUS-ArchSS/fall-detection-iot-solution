from flask import Flask, request, jsonify
import requests

import sqlite3
from datetime import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mag_x REAL,
            mag_y REAL,
            mag_z REAL,
            acc_x REAL,
            acc_y REAL,
            acc_z REAL,
            heart_rate REAL,
            create_timestamp INTEGER
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/data', methods=['POST'])
def save_data():
    data = request.get_json()

    if not data or not all(key in data for key in ["mag_x", "mag_y", "mag_z", "acc_x", "acc_y", "acc_z", "heart_rate"]):
        return jsonify({"error": "Invalid data format"}), 400

    if_fall = detect(mag_x=data['mag_x'], mag_y=data['mag_y'], mag_z=data['mag_z'], acc_x=data['acc_x'], acc_y=data['acc_y'],
           acc_z=data['acc_z'], heart_rate=data['heart_rate'])
    result = ''
    if if_fall:
        result = 'true'
    else:
        result = 'false'

    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    current_timestamp = int(datetime.utcnow().timestamp() * 1000)
    c.execute('''
        INSERT INTO sensor_data (mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, heart_rate, create_timestamp, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data["mag_x"], data["mag_y"], data["mag_z"], data["acc_x"], data["acc_y"], data["acc_z"], data["heart_rate"],
          current_timestamp, result))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data saved successfully"}), 201


def detect(mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, heart_rate):
    url = "http://127.0.0.1:5000/fall_detection"
    headers = {"Content-Type": "application/json"}
    data = {
        "mag_x": mag_x,
        "mag_y": mag_y,
        "mag_z": mag_z,
        "acc_x": acc_x,
        "acc_y": acc_y,
        "acc_z": acc_z,
        "heart_rate": heart_rate
    }

    response = requests.post(url, json=data, headers=headers)

    if response.content.decode('utf-8') == 'yes':
        return True
    else:
        return False


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8000)
