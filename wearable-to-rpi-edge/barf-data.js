// Replace these UUIDs with your unique UUIDs
var BLE_SERVICE_UUID = 'YOUR_CUSTOM_UUID';
var ACCEL_CHARACTERISTIC_UUID = 'YOUR_ACCEL_UUID';
var MAG_CHARACTERISTIC_UUID = 'YOUR_MAG_UUID';

// Accelerometer characteristic definition
var accelCharacteristic = new BLECharacteristic({
  uuid: ACCEL_CHARACTERISTIC_UUID,
  properties: ['read', 'notify'], // Allow reading and notifications for this characteristic
  onRead: function () {
    // Return accelerometer data as an array of 3 float values (x, y, z)
    return new Float32Array(Bangle.getAccel().values);
  },
});

// Magnetometer characteristic definition
var magCharacteristic = new BLECharacteristic({
  uuid: MAG_CHARACTERISTIC_UUID,
  properties: ['read', 'notify'], // Allow reading and notifications for this characteristic
  onRead: function () {
    // Return magnetometer data as an array of 3 float values (x, y, z)
    return new Float32Array(Bangle.getMag().values);
  },
});

// Custom service definition containing the accelerometer and magnetometer characteristics
var bangleService = new BLEService({
  uuid: BLE_SERVICE_UUID,
  characteristics: [accelCharacteristic, magCharacteristic],
});

// Enable the Bluetooth on the Bangle.js watch
Bangle.setBluetooth(true);

// Remove the default UART service (serial communication) from the watch
NRF.setServices({}, {uart: false});

// Add custom service to the Bangle.js watch
NRF.setServices({
  uuids: [BLE_SERVICE_UUID],
  primary: true,
  visible: true,
  services: [bangleService],
});

// The following lines set up various default BLE services and characteristics,
// which are not strictly necessary for sending accelerometer and magnetometer data,
// but can be useful for identifying the Bangle.js watch and its capabilities.

NRF.setServices({0x1801: {}}, {uart: false});
NRF.setServices({0x1800: {0x2A00: {readable: true, value: 'Bangle'}}}, {uart: false});
NRF.setServices({0x180A: {0x2A29: {readable: true, value: 'Espruino'}}}, {uart: false});
NRF.setServices({0x180F: {0x2A19: {readable: true, value: [95]}}}, {uart: false});
NRF.setServices({0x1802: {0x2A06: {readable: true, value: [0]}}}, {uart: false});
NRF.setServices({0x1805: {0x2A2B: {readable: true, value: [0]}}}, {uart: false});
NRF.setServices({0x1805: {0x2A0F: {readable: true, value: [0]}}}, {uart: false});
NRF.setServices({0x1804: {0x2A07: {readable: true, value: [0]}}}, {uart: false});
NRF.setServices({0x181C: {0x2A9E: {readable: true, value: [0]}}}, {uart: false});
