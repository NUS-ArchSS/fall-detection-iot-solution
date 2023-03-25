from bluepy.btle import DefaultDelegate, Peripheral, Scanner, UUID
import struct

BLE_SERVICE_UUID = "YOUR_CUSTOM_UUID"  # Replace with your custom UUID
ACCEL_CHARACTERISTIC_UUID = "YOUR_ACCEL_UUID"
MAG_CHARACTERISTIC_UUID = "YOUR_MAG_UUID"

class BangleDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        if cHandle == accel_char.getHandle():
            accel_data = struct.unpack('<fff', data)
            print("Accelerometer data:", accel_data)  # Print accelerometer data
        elif cHandle == mag_char.getHandle():
            mag_data = struct.unpack('<fff', data)
            print("Magnetometer data:", mag_data)  # Print magnetometer data

def discover_bangle_device():
    scanner = Scanner()
    devices = scanner.scan(10.0)  # Scan for 10 seconds
    bangle_device = None
    for dev in devices:
        for (adtype, desc, value) in dev.getScanData():
            if adtype == 9 and value == 'Bangle':
                bangle_device = dev
                break
        if bangle_device:
            break
    return bangle_device

bangle_device = discover_bangle_device()

if bangle_device:
    print(f"Found Bangle device: {bangle_device.addr}")
    bangle_peripheral = Peripheral(bangle_device)
    bangle_peripheral.setDelegate(BangleDelegate())

    bangle_service = bangle_peripheral.getServiceByUUID(UUID(BLE_SERVICE_UUID))
    accel_char = bangle_service.getCharacteristics(UUID(ACCEL_CHARACTERISTIC_UUID))[0]
    mag_char = bangle_service.getCharacteristics(UUID(MAG_CHARACTERISTIC_UUID))[0]

    bangle_peripheral.writeCharacteristic(
        accel_char.valHandle + 1,
        struct.pack('<bb', 0x01, 0x00),
    )

    bangle_peripheral.writeCharacteristic(
        mag_char.valHandle + 1,
        struct.pack('<bb', 0x01, 0x00),
    )

    while True:
        if bangle_peripheral.waitForNotifications(1.0):
            continue
        print("Waiting for notifications...")
else:
    print("Bangle device not found.")
