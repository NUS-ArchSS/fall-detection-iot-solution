"""
sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.datacollector=1.0.1"
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove com.example.datacollector
"""
from flask import Flask, request, jsonify
import requests

import sqlite3
from datetime import datetime

app = Flask(__name__)

"""
curl --location --request POST 'http://localhost:8000/data' --header 'Content-Type: application/json' --data-raw '{"acc_x": 9.681701660156250000, "acc_y": 1.020812988281250000, "acc_z": 1.863098144531250000, "mag_x": -0.815185546875000000, "mag_y": 0.412353515625000000, "mag_z": 0.079833984375000000, "ctime":1234567}'
{
  "message": "Data saved successfully"
}
"""
def init_db():
    conn = sqlite3.connect('/tmp/sensor_data.db')
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
            create_timestamp INTEGER,
            result INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/data', methods=['POST'])
def save_data():
    data = request.get_json()

    if not data or not all(key in data for key in ["mag_x", "mag_y", "mag_z", "acc_x", "acc_y", "acc_z", "ctime"]):
        return jsonify({"error": "Invalid data format"}), 400

    if_fall = detect(mag_x=data['mag_x'], mag_y=data['mag_y'], mag_z=data['mag_z'], acc_x=data['acc_x'], acc_y=data['acc_y'],
           acc_z=data['acc_z'])
    result = ''
    if if_fall:
        result = 1
    else:
        result = 0

    conn = sqlite3.connect('/tmp/sensor_data.db')
    c = conn.cursor()
    current_timestamp = int(datetime.utcnow().timestamp() * 1000)
    c.execute('''
        INSERT INTO sensor_data (mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, create_timestamp, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data["mag_x"], data["mag_y"], data["mag_z"], data["acc_x"], data["acc_y"], data["acc_z"],
        data['ctime'], result))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data saved successfully"}), 201


def detect(mag_x, mag_y, mag_z, acc_x, acc_y, acc_z):
    url = "http://localhost:5000/fall_detection"
    headers = {"Content-Type": "application/json"}
    data = {
        "mag_x": mag_x,
        "mag_y": mag_y,
        "mag_z": mag_z,
        "acc_x": acc_x,
        "acc_y": acc_y,
        "acc_z": acc_z
    }

    response = requests.post(url, json=data, headers=headers)

    if response.content.decode('utf-8') == 'yes':
        return True
    else:
        return False


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8000)
