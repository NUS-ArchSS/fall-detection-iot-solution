function saveCSV(filename, csvData) {
  let a = document.createElement("a"),
    file = new Blob([csvData], { type: "Comma-separated value file" });
  let url = URL.createObjectURL(file);
  a.href = url;
  a.download = filename + ".csv";
  document.body.appendChild(a);
  a.click();
  setTimeout(function () {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 0);
}

function createCode() {
  //modes: 1 BT, 2 File
  return (
    "var method=" +
    (document.getElementById("chkLocal").checked ? 2 : 1) +
    ";\n" +
    String.raw`
  var accData=[];
  var maxSize=0;
  var filename="log.csv";

  var gotHRMraw = false;
  var gotBTHRM = false;
  var gotHRM = false;
  var gotAcc = false;
  
  var events = -1;
  var hrmRaw,hrmPulse,bthrmPulse

  function gotAll(){
    return gotHRM && gotAcc;
  }

  let bthrmSettings = (require("Storage").readJSON("bthrm.json",1) || {});

  Bangle.setHRMPower(1);
  
  if (bthrmSettings.replace) Bangle.origSetHRMPower(1);
  
  if (Bangle.setBTHRMPower){
    Bangle.setBTHRMPower(1);
  } else {
    gotBTHRM = true;
  }

  var write=null;

  if (method == 2){
    var f = require('Storage').open(filename,"w");
    f.erase();
    f = require('Storage').open(filename,"a");
    write = function(str){f.write(str);events++;};
  } else if (method == 1){
    write = function(str){Bluetooth.print("DATA: " + str);events++;};
  }

  write("Time,Acc_x,Acc_y,Acc_z,HRM_b,HRM_c\n");

  function writeAcc(e){
    gotAcc = true;
    acc = e;
    e.date=Date.now();
    accData.push(e);
    accData.splice(0, accData.length - maxSize);
  }

  function writeAccDirect(e){
    gotAcc = true;
    acc = e;
    if (!gotAll()) return;
    var x = Math.round(e.x*100);
    var y = Math.round(e.y*100);
    var z = Math.round(e.z*100);
    write(Date.now()+","+x+","+y+","+z+",,,\n");
  }

  function writeHRM(e){
    gotHRM = true;
    hrmPulse = e.bpm;
    if (!gotAll()) return;
    while(accData.length > 0){
      var c = accData.shift();
      if (c) write(c.date+","+c.x+","+c.y+","+c.z+",,,\n");
    }
    write(Date.now()+",,,,"+e.bpm+","+e.confidence+"\n");
  }

  if(maxSize){
    Bangle.on("accel", writeAcc);
  } else {
    Bangle.on("accel", writeAccDirect);
  }
  if (bthrmSettings.replace){
    Bangle.origOn("HRM", writeHRM);
  } else {
    Bangle.on("HRM", writeHRM);
  }

  g.clear();

  function drawStatusText(name, y){
    g.setFont12x20();
    g.setColor(g.theme.fg);
    g.drawString(name, 24, y * 22 + 2);
  }

  function drawStatus(isOk, y, value){
    g.setFont12x20();
    if (isOk) g.setColor(0,1,0); else g.setColor(1,0,0);
    g.fillRect(0,y * 22, 20, y * 22 + 20);
    g.setColor(g.theme.bg);
    let x = 120
    g.fillRect(x,y*22,g.getWidth(),y*22+20);
    g.setColor(g.theme.fg);
    if (value) g.drawString(value, x, y * 22 + 2);
  }

  function updateStatus(){
    let h = 1;
    drawStatus(gotAcc, h++);
    drawStatus(gotHRM, h++, hrmPulse); hrmPulse = null;
    drawStatus(events>0, h++, Math.max(events,0));
    if (method == 2){
      let free = require('Storage').getFree();
      drawStatus(free>0.25*process.env.STORAGE, h++, Math.floor(free/1024) + "K");
    }
  }
  
  var intervalId = -1;

  g.setFont12x20();
  g.setColor(g.theme.fg);
  g.drawString("Target " + (method==2?"log.csv":"Bluetooth"), 0, 2);

  let h = 1;
  drawStatusText("Acc", h++);
  drawStatusText("HRM", h++);
  drawStatusText("Events", h++);
  if (method == 2) drawStatusText("Storage", h++);
  updateStatus();
  
  intervalId = setInterval(()=>{
    updateStatus();
  }, 1000);

  if (Bangle.setBTHRMPower){
    intervalId = setInterval(()=>{
      if (!Bangle.isBTHRMOn()) Bangle.setBTHRMPower(1);
    }, 5000);
  }
  `
  );
}

var connection;
var lineCount = -1;

function stop() {
  connection.reconnect((c) => {
    c.write("load();\n");
    c.close();
    connection = undefined;
  });
}

function updateButtons() {
  document.getElementById("btnSave").disabled =
    document.getElementById("chkLocal").checked;
  document.getElementById("btnDownload").disabled =
    !document.getElementById("chkLocal").checked;
  document.getElementById("btnReset").disabled =
    document.getElementById("chkLocal").checked;
  document.getElementById("btnStop").disabled =
    document.getElementById("chkLocal").checked;
}

updateButtons();

document.getElementById("chkLocal").addEventListener("click", function () {
  reset();
  updateButtons();
});

window.addEventListener(
  "message",
  function (event) {
    let msg = event.data;
    if (msg.type == "readstoragefilersp") {
      saveCSV("log.csv", msg.data);
    }
  },
  false
);

document.getElementById("btnDownload").addEventListener("click", function () {
  if (connection) {
    stop();
  }
  console.log("Loading data from BangleJs...");
  try {
    window.postMessage({ type: "readstoragefile", data: "log.csv", id: 0 });
  } catch (ex) {
    console.log("(Warning) Could not load apikey from BangleJs.");
    console.log(ex);
  }
});

document.getElementById("btnSave").addEventListener("click", function () {
  saveCSV("log.csv", localStorage.getItem("data"));
});

function reset() {
  document.getElementById("result").innerText = "";
}

document.getElementById("btnReset").addEventListener("click", function () {
  if (connection) {
    stop();
  }
  lineCount = -1;
  localStorage.removeItem("data");
  reset();
});

document.getElementById("btnStop").addEventListener("click", function () {
  if (connection) {
    stop();
  }
});

function connect(connectionHandler) {
  Puck.connect(function (c) {
    if (!c) {
      console.log("Couldn't connect!\n");
      return;
    }
    connection = c;
    connectionHandler(c);
  });
}

document.getElementById("btnConnect").addEventListener("click", function () {
  localStorage.setItem("data", "");
  lineCount = -1;
  if (connection) {
    stop();
    document.getElementById("result").innerText = "0";
  }
  connect(function (connection) {
    var buf = "";
    connection.on("data", function (d) {
      buf += d;
      var l = buf.split("\n");
      buf = l.pop();
      l.forEach(onLine);
    });
    connection.write("reset();\n", function () {
      setTimeout(function () {
        connection.write("\x03\x10if(1){" + createCode() + "}\n", function () {
          console.log("Ready...");
        });
      }, 1500);
    });
  });
});

function onLine(line) {
  console.log("RECEIVED:" + line);
  if (line.startsWith("DATA:")) {
    localStorage.setItem(
      "data",
      localStorage.getItem("data") + line.substr(5) + "\n"
    );
    lineCount++;
    document.getElementById("result").innerText =
      "Captured events: " + lineCount;

    var dataArray = line.split(",");
    renderBar(dataArray);
    renderChart(dataArray);
  }

  // When we get a line of data, check it and if it's
  // from the accelerometer, update it

  function renderBar(data) {
    // we have an accelerometer reading
    if (data[1] && data[2] && data) {
      var accel = {
        x: parseInt(data[1]),
        y: parseInt(data[2]),
        z: parseInt(data[3]),
      };
      // Update bar positions
      setBarPos("barX", accel.x);
      setBarPos("barY", accel.y);
      setBarPos("barZ", accel.z);

      // calculate fall
      calculateFall(accel.x, accel.y, accel.z);
    }
  }
}

// When we get a line of data, check it and if it's
// from the heart rate monitor, update it
function renderChart(data) {
  // we have an HR monitor reading
  if (data[4]) {
    var hr_data = {
      hr: parseInt(data[4]),
      conf: parseInt(data[5]),
    };
    updateChart(hr_data.hr);
  }
}

// Set the position of each bar
function setBarPos(id, d) {
  var s = document.getElementById(id).style;
  if (d > 150) d = 150;
  if (d < -150) d = -150;
  if (d >= 0) {
    s.left = "150px";
    s.width = d + "px";
  } else {
    // less than 0
    s.left = 150 + d + "px";
    s.width = -d + "px";
  }
}

//Chart Setup
var dps = []; // dataPoints
var chart = new CanvasJS.Chart("chartContainer", {
  title: {
    text: "Bangle.js HeartRate Monitoring Over Time",
  },
  axisY: {
    title: "Heart Rate",
  },
  axisX: {
    title: "Time",
    valueFormatString: "HH:mm:ss",
  },
  data: [
    {
      type: "spline",
      indexLabel: "{y}",
      dataPoints: dps,
    },
  ],
});

chart.render();
var dataLength = 20; // number of dataPoints visible at any point

var updateChart = function (hr) {
  if (dps.length <= dataLength) {
    labelVal = new Date().toISOString();
    xVal = new Date();
    yVal = hr;
    dps.push({
      x: xVal,
      y: yVal,
    });
  }

  if (dps.length > dataLength) {
    dps.shift();
  }

  chart.render();
};

//Use this function to calculate
function calculateFall(accelX, accelY, accelZ) {
  pitch =
    (Math.atan2(accelX, Math.sqrt(accelY * accelY + accelZ * accelZ)) * 180) /
    Math.PI;
  roll =
    (Math.atan2(accelY, Math.sqrt(accelX * accelX + accelZ * accelZ)) * 180) /
    Math.PI;

  if (pitch > 35 || pitch < -35 || roll > 35 || roll < -35) {
    console.log("Fall detected. " + "picth: " + pitch + " ,roll: " + roll);
  } else {
    // console.log(pitch + ":" + roll + "No Fall - Normal");
  }
}
