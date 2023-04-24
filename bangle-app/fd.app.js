var APP_NAME = "FallDetect";

var events = -1;
var hrmRaw, hrmPulse;

var gotHRMraw = false;
var gotHRM = false;
var gotAcc = false;
var gotMag = false;

write = function (str) { Bluetooth.print(str); events++; };

function writeAcc(e) {
  gotAcc = true;
  write(Date.now() + ",Accel," + e.x + "," + e.y + "," + e.z + ",\n");
}

function writeMag(e) {
  gotMag = true;
  write(Date.now() + ",Mag," + e.x + "," + e.y + "," + e.z + ",\n");
}

function writeHRM(e) {
  gotHRM = true;
  hrmPulse = e.bpm;
  // write(Date.now() + ",HRM," + e.bpm + "," + e.confidence + ",\n");
}

function writeHRMraw(e) {
  gotHRMraw = true;
  hrmRaw = e.raw;
  // write(Date.now() + ",HRMraw," + e.raw + "," + e.filt + "," + e.vcPPG + "," + e.vcPPGoffs + ",\n");
}

Bangle.setHRMPower(1);
Bangle.setCompassPower(1);

Bangle.on("accel", writeAcc);
Bangle.on("mag", writeMag);
Bangle.on("HRM-raw", writeHRMraw);
Bangle.on("HRM", writeHRM);

function drawStatus(isOk, y, value) {
  g.setFont12x20();
  if (isOk) g.setColor(0, 1, 0); else g.setColor(1, 0, 0);
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
  drawStatus(gotMag, h++);
  drawStatus(gotHRM, h++, hrmPulse); hrmPulse = null;
  drawStatus(gotHRMraw, h++, hrmRaw); hrmRaw = null;
  drawStatus(events > 0, h++, Math.max(events, 0));
}

function drawStatusText(name, y) {
  g.setFont12x20();
  g.setColor(g.theme.fg);
  g.drawString(name, 24, y * 22 + 2);
}

g.clear();
g.setFont12x20();
g.setColor(g.theme.fg);
g.drawString("Target Bluetooth", 0, 2);

let h = 1;
drawStatusText("Acc", h++);
drawStatusText("Mag", h++);
drawStatusText("HRM", h++);
drawStatusText("HRM_r", h++);
drawStatusText("Events", h++);

updateStatus();

var intervalId = -1;
intervalId = setInterval(() => {
  updateStatus();
}, 1000);