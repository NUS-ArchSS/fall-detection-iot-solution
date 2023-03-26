import asyncio
from bleak import BleakClient, BleakScanner

# Replace these UUIDs with your unique UUIDs
BLE_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
ACCEL_CHARACTERISTIC_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

def handle_accel_data(sender: int, data: bytearray):
    accel_values = [float(x) for x in data]
    print(f"Accelerometer data: x={accel_values[0]}, y={accel_values[1]}, z={accel_values[2]}")

async def run(address):
    async with BleakClient(address) as client:
        await client.start_notify(ACCEL_CHARACTERISTIC_UUID, handle_accel_data)
        print("Subscribed to accelerometer notifications.")
        await asyncio.sleep(30)
        await client.stop_notify(ACCEL_CHARACTERISTIC_UUID)
        print("Unsubscribed from accelerometer notifications.")

async def get_services_and_characteristics(address):
    async with BleakClient(address) as client:
        services = await client.get_services()
        
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid}")

            
async def discover_bangle():
    devices = await BleakScanner.discover()
    bangle_device = None

    for device in devices:
        if "Bangle.js" in device.name:
            print(device.metadata)
            bangle_device = device
            break

    if bangle_device:
        print(f"Found Bangle device: {bangle_device.address}")
        await get_services_and_characteristics(bangle_device.address)
        while True:
            pass
        # await run(bangle_device.address)
    else:
        print("Bangle.js device not found. Make sure it is powered on and advertising.")

loop = asyncio.get_event_loop()
loop.run_until_complete(discover_bangle())


