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
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    PublishToIoTCoreRequest
)

app = Flask(__name__)

publishtopic = "falldetection/test"

message =  {
  "timemillis": 000000000000
}

TIMEOUT = 10
qos = QOS.AT_LEAST_ONCE
subqos = QOS.AT_MOST_ONCE

ipc_client = awsiot.greengrasscoreipc.connect()

def notify():
    message["timemillis"] = round(time.time() * 1000)

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