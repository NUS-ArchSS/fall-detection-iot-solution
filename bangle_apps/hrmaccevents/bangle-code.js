// var method = document.getElementById("chkLocal").checked ? 2 : 1;
var method = 1;
var accData = [];
var maxSize = 0;
var filename = "log.csv";

var gotHRMraw = false;
var gotBTHRM = false;
var gotHRM = false;
var gotAcc = false;

var events = -1;
var hrmRaw, hrmPulse, bthrmPulse;

function gotAll() {
  return gotBTHRM && gotHRM && gotHRMraw && gotAcc;
}

let bthrmSettings = require("Storage").readJSON("bthrm.json", 1) || {};

Bangle.setHRMPower(1);

if (bthrmSettings.replace) Bangle.origSetHRMPower(1);

if (Bangle.setBTHRMPower) {
  Bangle.setBTHRMPower(1);
} else {
  gotBTHRM = true;
}

var write = null;

if (method == 2) {
  var f = require("Storage").open(filename, "w");
  f.erase();
  f = require("Storage").open(filename, "a");
  write = function (str) {
    f.write(str);
    events++;
  };
} else if (method == 1) {
  write = function (str) {
    Bluetooth.print("DATA: " + str);
    events++;
  };
}

write("Time,Acc_x,Acc_y,Acc_z,HRM_b,HRM_c,HRM_r,HRM_f,PPG_r,PPG_o,BTHRM\n");

function writeAcc(e) {
  gotAcc = true;
  acc = e;
  e.date = Date.now();
  accData.push(e);
  accData.splice(0, accData.length - maxSize);
}

function writeAccDirect(e) {
  gotAcc = true;
  acc = e;
  if (!gotAll()) return;
  write(Date.now() + "," + e.x + "," + e.y + "," + e.z + ",,,,,,,,\n");
}

function writeBTHRM(e) {
  gotBTHRM = true;
  bthrmPulse = e.bpm;
  if (!gotAll()) return;
  write(Date.now() + ",,,,,,,,,," + e.bpm + "\n");
}

function writeHRM(e) {
  gotHRM = true;
  hrmPulse = e.bpm;
  if (!gotAll()) return;
  while (accData.length > 0) {
    var c = accData.shift();
    if (c) write(c.date + "," + c.x + "," + c.y + "," + c.z + ",,,,,,,,\n");
  }
  write(Date.now() + ",,,," + e.bpm + "," + e.confidence + ",,,,\n");
}

function writeHRMraw(e) {
  gotHRMraw = true;
  hrmRaw = e.raw;
  if (!gotAll()) return;
  write(
    Date.now() +
      ",,,,,," +
      e.raw +
      "," +
      e.filt +
      "," +
      e.vcPPG +
      "," +
      e.vcPPGoffs +
      ",\n"
  );
}

if (maxSize) {
  Bangle.on("accel", writeAcc);
} else {
  Bangle.on("accel", writeAccDirect);
}
Bangle.on("HRM-raw", writeHRMraw);
if (bthrmSettings.replace) {
  Bangle.origOn("HRM", writeHRM);
} else {
  Bangle.on("HRM", writeHRM);
}
Bangle.on("BTHRM", writeBTHRM);

g.clear();

function drawStatusText(name, y) {
  g.setFont12x20();
  g.setColor(g.theme.fg);
  g.drawString(name, 24, y * 22 + 2);
}

function drawStatus(isOk, y, value) {
  g.setFont12x20();
  if (isOk) g.setColor(0, 1, 0);
  else g.setColor(1, 0, 0);
  g.fillRect(0, y * 22, 20, y * 22 + 20);
  g.setColor(g.theme.bg);
  let x = 120;
  g.fillRect(x, y * 22, g.getWidth(), y * 22 + 20);
  g.setColor(g.theme.fg);
  if (value) g.drawString(value, x, y * 22 + 2);
}

function updateStatus() {
  let h = 1;
  drawStatus(gotAcc, h++);
  drawStatus(gotBTHRM, h++, bthrmPulse);
  bthrmPulse = null;
  drawStatus(gotHRM, h++, hrmPulse);
  hrmPulse = null;
  drawStatus(gotHRMraw, h++, hrmRaw);
  hrmRaw = null;
  drawStatus(events > 0, h++, Math.max(events, 0));
  if (method == 2) {
    let free = require("Storage").getFree();
    drawStatus(
      free > 0.25 * process.env.STORAGE,
      h++,
      Math.floor(free / 1024) + "K"
    );
  }
}

var intervalId = -1;

g.setFont12x20();
g.setColor(g.theme.fg);
g.drawString("Target " + (method == 2 ? "log.csv" : "Bluetooth"), 0, 2);

let h = 1;
drawStatusText("Acc", h++);
drawStatusText("BTHRM", h++);
drawStatusText("HRM", h++);
drawStatusText("HRM_r", h++);
drawStatusText("Events", h++);
if (method == 2) drawStatusText("Storage", h++);
updateStatus();

intervalId = setInterval(() => {
  updateStatus();
}, 1000);

if (Bangle.setBTHRMPower) {
  intervalId = setInterval(() => {
    if (!Bangle.isBTHRMOn()) Bangle.setBTHRMPower(1);
  }, 5000);
}
