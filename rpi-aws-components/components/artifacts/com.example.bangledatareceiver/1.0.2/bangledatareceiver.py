"""
sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.bangledatareceiver=1.0.1"
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove com.example.bangledatareceiver
"""
import asyncio
import logging
import queue
import threading
import time
import requests

from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

logger = logging.getLogger(__name__)
SERVICE_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# Define the two FIFO queues
accl_queue = queue.Queue()
mag_queue = queue.Queue()


def process_data(data_bytearray, accl_queue: queue, mag_queue: queue):
    # Convert the bytearray to a string
    # bytearray(b'1681367616818.033203125,Accel,-0.20727539062,-0.73022460937,-0.71899414062,\n1681367616821.6953125,Mag,300,622,257,\n')
    line = data_bytearray.decode('utf-8')

    """ data:
    Accelerometer: x,y,z
    1681353316941.78198242187,Accel,0.02404785156,-0.06604003906,-1.12475585937,
    HRMraw: heart rate raw data, filt, vcPPG, vcPPGoffs 
    1681353316963.296875,HRMraw,5566,-32768,1751,1032,
    Magnetometer: x,y,z
    1681353317265.97021484375,Mag,296,661,257,
    HRM: bpm, confidence
    1681354187341.98950195312,HRM,58,0,
    """
    # Split the string into lines
    data_lines = line.strip().split('\n')

    # Process each line and store the resulting dictionaries in a list
    data_list = []
    for line in data_lines:
        # Remove the trailing comma
        line = line.rstrip(',')

        # Check if any data exist
        if any(keyword in line for keyword in ["Accel", "Mag"]):
            line_parts = line.split(",")
            # if data value not null
            if len(line_parts) > 1:
                data_time = line_parts[0]
                name = line_parts[1]
                data_values = line_parts[2:]
                # Store data in a dictionary
                data_dict = {
                    "data_time": data_time,
                    "name": name,
                    "data_values": data_values
                }
                if name == 'Accel':
                    if len(data_values) >= 3:
                        accl_queue.put(data_dict)
                else:
                    if len(data_values) >= 3:
                        mag_queue.put(data_dict)
                # data_list.append(data_dict)


def handle_data(characteristic: BleakGATTCharacteristic, data: bytearray):
    # logger.info(str(data))
    process_data(data, accl_queue, mag_queue)


# Define the consumer thread function


def consumer():
    while True:
        try:
            # print('Try to get a message from accl_queue')
            message1 = accl_queue.get_nowait()
        except queue.Empty:
            time.sleep(0.1)
            continue

        try:
            # print('Try to get a message from mag_queue')
            message2 = mag_queue.get_nowait()
        except queue.Empty:
            time.sleep(0.1)
            continue

        # Process the message
        # print("Received message:", message1, message2)

        url = "http://localhost:8000/data"
        headers = {"Content-Type": "application/json"}

        data = {
            "mag_x": message2['data_values'][0],
            "mag_y": message2['data_values'][1],
            "mag_z": message2['data_values'][2],
            "acc_x": message1['data_values'][0],
            "acc_y": message1['data_values'][1],
            "acc_z": message1['data_values'][2],
            "ctime": 12348888
        }
        # print(data)
        try:
            requests.post(url, json=data, headers=headers)
        except Exception as e:
            print(e)
            print('Error in sending data to server, retry in 3 seconds...')
            time.sleep(3)
        # print(response.content.decode('utf-8'))

        # Mark the message as consumed
        try:
            accl_queue.task_done()
        except ValueError:
            pass

        try:
            mag_queue.task_done()
        except ValueError:
            pass


async def main():
    # TODO: change to your bangle watch's name
    target_device_name = "Bangle.js 60c6"
    bangle = None

    scanner = BleakScanner()

    while bangle is None:
        logger.info("scanning for 5 seconds, please wait...")
        devices = await scanner.discover(timeout=5, return_adv=True)
        for address, (device, advertisement_data) in devices.items():
            if device.name is not None and target_device_name.lower() in device.name.lower():
                logger.info("---------------")
                logger.info("Device name: " + device.name)
                logger.info("Device address: " + device.address)
                logger.info("Advertisement data:" + str(advertisement_data))
                logger.info("---------------")
                bangle = device
                break

    disconnected_event = asyncio.Event()

    def disconnected_callback(client):
        logger.info("Disconnecting!")
        logger.info("Connected: %r", client.is_connected)
        disconnected_event.set()

    async with BleakClient(
            device, disconnected_callback=disconnected_callback
    ) as client:
        logger.info("Connected: %r", client.is_connected)
        logger.info("Connected to Bangle.js watch: " + bangle.address)
        services = client.services

        for service in services:
            logger.info(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                logger.info(f"  Characteristic: {characteristic.uuid}")
                logger.info(f"  Description: {characteristic.description}")

        logger.info("Receiving data. Press Ctrl+C to stop...")
        await client.start_notify(SERVICE_UUID, handle_data)

        await disconnected_event.wait()
        logger.info("Connected: %r", client.is_connected)

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            print(f"Stop notifing...")
            await client.stop_notify(SERVICE_UUID)


if __name__ == "__main__":

    log_level = logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    consumer_thread = threading.Thread(target=consumer)
    consumer_thread.start()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"Unhandled exception: {e}")
