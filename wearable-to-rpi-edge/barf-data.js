var ACCEL_PERIOD = 1000; // Accelerometer data send period in milliseconds
var MAG_PERIOD = 1000; // Magnetometer data send period in milliseconds

// Replace these UUIDs with your unique UUIDs
var BLE_SERVICE_UUID = '9d9cd999-7277-4580-8d28-83dffc56dc1b';
var ACCEL_CHARACTERISTIC_UUID = '93940fa7-ea5f-4c38-9e63-a0271cca3fac';
var MAG_CHARACTERISTIC_UUID = '3834d159-a357-4fc4-80be-091633d1b3fc';

function getAccelData() {
  return new Float32Array(Bangle.getAccel().values);
}

function getMagData() {
  return new Float32Array(Bangle.getMag().values);
}

function sendAccelData() {
  if (NRF.getSecurityStatus().connected) {
    var update = {};å
    update[BLE_SERVICE_UUID] = {};
    update[BLE_SERVICE_UUID][ACCEL_CHARACTERISTIC_UUID] = getAccelData();
    NRF.updateServices(update);
  }
}

function sendMagData() {
  if (NRF.getSecurityStatus().connected) {
    var update = {};
    update[BLE_SERVICE_UUID] = {};
    update[BLE_SERVICE_UUID][MAG_CHARACTERISTIC_UUID] = getMagData();
    NRF.updateServices(update);
  }
}

function onInit() {
  NRF.setTxPower(4); // Enable Bluetooth by setting the transmission power to a non-zero value (in this case, 4 dBm)

  var services = {};
  services[BLE_SERVICE_UUID] = {};
  services[BLE_SERVICE_UUID][ACCEL_CHARACTERISTIC_UUID] = {
    value: getAccelData(),
    readable: true,
    notify: true,
  };
  services[BLE_SERVICE_UUID][MAG_CHARACTERISTIC_UUID] = {
    value: getMagData(),
    readable: true,
    notify: true,
  };
  NRF.setServices(services, { uart: false });

  Bangle.on('accel', sendAccelData);
  Bangle.on('mag', sendMagData);

  Bangle.setAccelOn(true);
  Bangle.setMagOn(true);
}

onInit();
