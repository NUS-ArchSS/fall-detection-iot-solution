"""
sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.mqtt=1.0.2"
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove com.example.mqtt
"""
import time
import traceback
from flask import Flask, request, jsonify
import json
from datetime import datetime
import paho.mqtt.client as mqtt


app = Flask(__name__)

# Define a global variable to store the last request time
last_request_time = time.time()

# MQTT broker configuration
# broker_address = "192.168.1.112"
broker_address = "127.0.0.1"
broker_port = 1883  # Default MQTT port

message = {
    "device": "Bangle.js 60c6",
    "msg_id": 000000000000,
    "fall_detected": "true",
    "current_time": 1
}


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")


def on_publish(client, userdata, mid):
    print("Message published")


# Create an MQTT client
client = mqtt.Client()

# Assign callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)


def notify():
    global last_request_time
    current_time = time.time()
    time_elapsed = current_time - last_request_time

    if time_elapsed < 5:
        return 'Too Many notification request. Calm down for 30 seconds'
    else:
        last_request_time = current_time

        message["msg_id"] = round(time.time() * 1000)
        now = datetime.now()
        message["current_time"] = now.strftime("%H:%M:%S")

        msgstring = json.dumps(message)

        # Publish a message to a topic
        topic = "falldetection"
        client.publish(topic, msgstring)

        print("done publish...")
        return 'Sent notification.'


@app.route('/notify', methods=['POST'])
def post_request():
    # data = request.get_json()
    # Acc_X = data['acc_x']
    # Acc_Y = data['acc_y']
    # # need to support heart rate

    # input_json = '{{"Acc_X": {}, "Acc_Y": {}, "Acc_Z": {}, "Mag_X": {}, "Mag_Y": {}, "Mag_Z": {}}}'.format(Acc_X,
    # Acc_Y, Acc_Z, Mag_X, Mag_Y, Mag_Z) print(input_json)
    notify()
    return jsonify({"message": "Sent notification."}), 200


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5010)
