import asyncio
import logging

from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from data_processing import process_data
from fall_detector import FallDetector
from bangle_data_sqlite import insert_data

logger = logging.getLogger(__name__)
SERVICE_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"


def handle_data(characteristic: BleakGATTCharacteristic, data: bytearray):
    # logger.info(str(data))
    data_list = process_data(data)
    for data_dict in data_list:
        detect_fall(data_dict)
        insert_data(data_dict)


def detect_fall(data):
    # Fall detection
    # Initialize the fall detector with a threshold value
    threshold = 1.5
    fall_detector = FallDetector(threshold)
    fall_detector.detect_fall(data)


async def main():
    # TODO: change to your bangle watch's name
    target_device_name = "Bangle.js 55a3 or 60c6"
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

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"Unhandled exception: {e}")
