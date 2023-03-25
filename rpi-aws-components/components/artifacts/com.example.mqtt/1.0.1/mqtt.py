import time
import traceback
import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.client as client
import json
from awsiot.greengrasscoreipc.model import (
    IoTCoreMessage,
    QOS,
    PublishToIoTCoreRequest
)

publishtopic = "mypi/button"

message =  {
  "button": "b4pressed",
  "timemillis": 000000000000
}

TIMEOUT = 10
qos = QOS.AT_LEAST_ONCE
subqos = QOS.AT_MOST_ONCE

ipc_client = awsiot.greengrasscoreipc.connect()

#button 4 callback
def button4pressed():
    message["timemillis"] = round(time.time() * 1000)

    msgstring = json.dumps(message)
    print("going to publish...456")
    pubrequest = PublishToIoTCoreRequest()
    pubrequest.topic_name = publishtopic
    pubrequest.payload = bytes(msgstring, "utf-8")
    pubrequest.qos = qos
    operation = ipc_client.new_publish_to_iot_core()
    operation.activate(pubrequest)
    future = operation.get_response()
    future.result(TIMEOUT)
    print("done publish...456")

button4pressed()

print("button event detect finished")

while True:
  pass

print("you should never see this line")