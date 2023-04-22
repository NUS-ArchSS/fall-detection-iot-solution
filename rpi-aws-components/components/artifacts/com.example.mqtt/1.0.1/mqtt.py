"""
sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.mqtt=1.0.1"
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove com.example.mqtt
"""
import time
import traceback
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
from flask import Flask, request, jsonify
import json
from datetime import datetime

from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    PublishToIoTCoreRequest
)

app = Flask(__name__)

# Define a global variable to store the last request time
last_request_time = time.time()

publishtopic = "falldetection/test"

message =  {
  "device": "Bangle.js 60c6",
  "msg_id": 000000000000,
  "fall_detected": "true",
  "current_time": 1
}

TIMEOUT = 10
qos = QOS.AT_LEAST_ONCE
subqos = QOS.AT_MOST_ONCE

ipc_client = awsiot.greengrasscoreipc.connect()

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
        message["current_time"]  = now.strftime("%H:%M:%S")

        msgstring = json.dumps(message)
        print("going to publish...")
        pubrequest = PublishToIoTCoreRequest()
        pubrequest.topic_name = publishtopic
        pubrequest.payload = bytes(msgstring, "utf-8")
        pubrequest.qos = qos
        operation = ipc_client.new_publish_to_iot_core()
        operation.activate(pubrequest)
        future = operation.get_response()
        future.result(TIMEOUT)
        print("done publish...")
        return 'Sent notification.'

@app.route('/notify', methods=['POST'])
def post_request():
    # data = request.get_json()
    # Acc_X = data['acc_x']
    # Acc_Y = data['acc_y']
    # # need to support heart rate

    # input_json = '{{"Acc_X": {}, "Acc_Y": {}, "Acc_Z": {}, "Mag_X": {}, "Mag_Y": {}, "Mag_Z": {}}}'.format(Acc_X, Acc_Y,
    #                                                                                                        Acc_Z, Mag_X,
    #                                                                                                        Mag_Y, Mag_Z)
    # print(input_json)
    notify()
    return 'NUS ISS dummy response'
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5010)