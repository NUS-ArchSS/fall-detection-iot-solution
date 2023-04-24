import time
import paho.mqtt.client as mqtt
import ssl
import json
import os
from dotenv import load_dotenv

load_dotenv()

# MQTT configuration
MQTT_BROKER = os.environ["MQTT_BROKER"]
CA_CERTS_DIR=os.environ["CA_CERTS_DIR"]
CERTFILE_DIR=os.environ["CERTFILE_DIR"]
KEYFILE_DIR=os.environ["KEYFILE_DIR"]
MQTT_PORT = 8883
MQTT_TOPIC = "rpi/fall-detection"

# Callback when the MQTT client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed, return code: ", rc)

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect

# Set up the secure connection
client.tls_set(ca_certs=CA_CERTS_DIR, certfile=CERTFILE_DIR, keyfile=KEYFILE_DIR, tls_version=ssl.PROTOCOL_SSLv23)
# client.tls_insecure_set(True)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# client.loop_start()

def publishData(data_time):
    message =  {
        "bangle": "fall detected",
        "timemillis": data_time
    }
    print(message)
    client.publish(MQTT_TOPIC, payload=json.dumps(message), qos=0, retain=False)

# _thread.start_new_thread(publishData,("Spin-up new Thread...",))

# client.loop_forever()