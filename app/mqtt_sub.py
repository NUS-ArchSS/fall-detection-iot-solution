import paho.mqtt.client as mqtt

# MQTT broker configuration
# broker_address = "192.168.1.112"
broker_address = "127.0.0.1"
broker_port = 1883  # Default MQTT port

# Callback functions


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    # Subscribe to the topic from which the Raspberry Pi publishes
    client.subscribe("falldetection")


def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")


# Create an MQTT client
client = mqtt.Client()

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port, 60)

# Start the MQTT network loop to process incoming messages
client.loop_start()

# Keep the script running to receive messages
while True:
    pass

# Disconnect from the MQTT broker
client.disconnect()
