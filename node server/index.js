var express = require("express");
var app = express();
const expressMonitorStatus = require('express-status-monitor');
app.use(expressMonitorStatus());

app.listen(3000, function () {
  console.log("listening on 3000");
});

app.get("/", (req, res) => {
  res.send("Users are being Shown");
});

app.get("/memory", (req, res) => {
  for (let i = 0; i < 4; i++) {
	const x = new Uint8Array(1024 * 1024 * 1024 * 1).fill(255); // 1GiB
}  
  res.send("memory load");
});

app.get("/cpu", (req, res) => {
  res.send("cpu load");
});

app.get("/monitor", (req, res) => {
  res.send("Insert User");
});
