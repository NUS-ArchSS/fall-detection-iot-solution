var ACCEL_PERIOD = 1000; // Accelerometer data send period in milliseconds

// Replace these UUIDs with your unique UUIDs
// var BLE_SERVICE_UUID = '00001800-0000-1000-8000-00805f9b34fb';
var BLE_SERVICE_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e';
var ACCEL_CHARACTERISTIC_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e';
// var MAG_CHARACTERISTIC_UUID = '3834d159-a357-4fc4-80be-091633d1b3fc';

function getAccelData() {
  var accel = Bangle.getAccel();
  return new Float32Array([accel.x, accel.y, accel.z]);
}

function sendAccelData() {
  if (NRF.getSecurityStatus().connected) {
    var update = {};
    update[BLE_SERVICE_UUID] = {};
    update[BLE_SERVICE_UUID][ACCEL_CHARACTERISTIC_UUID] = getAccelData();
    NRF.updateServices(update);
  }
}

function onInit() {
  if (!BLE_SERVICE_UUID || !ACCEL_CHARACTERISTIC_UUID) {
    console.log('Please replace the UUID placeholders with your generated UUIDs.');
    return;
  }

  NRF.setTxPower(4); // Enable Bluetooth by setting the transmission power to a non-zero value (in this case, 4 dBm)

  var services = {};
  services[BLE_SERVICE_UUID] = {};
  services[BLE_SERVICE_UUID][ACCEL_CHARACTERISTIC_UUID] = {
    value: getAccelData(),
    readable: true,
    notify: true,
  };
  NRF.setServices(services, { uart: false });

  Bangle.on('accel', sendAccelData);

  Bangle.setAccelOn(true);
}

onInit();
