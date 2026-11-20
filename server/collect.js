/* Affil1 — self-hosted analytics endpoint
   Run this on your own host (Node.js, no dependencies). It accepts
   POST /analytics/collect with newline-delimited JSON events and appends
   them to data/events.jsonl. GitHub Pages is static, so this endpoint must
   be self-hosted separately; the client (assets/js/analytics.js) degrades
   silently when the endpoint is unreachable.

   Privacy design:
   - No cookies, no IP addresses, no user identifiers beyond a random
     session id generated in the browser and stored in sessionStorage.
   - Events are append-only; nothing is ever edited or deleted here.
   - Rotate events.jsonl regularly and purge anything that is not needed.

   Usage:
     node server/collect.js        # listens on port 8080 (or $PORT)
*/

var http = require("http");
var fs = require("fs");
var path = require("path");

var PORT = process.env.PORT || 8080;
var DATA_DIR = path.join(__dirname, "..", "data");
var EVENTS_FILE = path.join(DATA_DIR, "events.jsonl");

function ensureDataDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

function appendEvent(line) {
  ensureDataDir();
  fs.appendFileSync(EVENTS_FILE, line + "\n", { encoding: "utf8" });
}

var server = http.createServer(function (req, res) {
  var url = new URL(req.url || "/", "http://localhost");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Cache-Control", "no-store");

  if (req.method === "OPTIONS") {
    res.writeHead(204);
    return res.end();
  }

  if (url.pathname === "/analytics/collect" && req.method === "POST") {
    var body = [];
    req.on("data", function (chunk) { body.push(chunk); });
    req.on("end", function () {
      var text = Buffer.concat(body).toString("utf8").trim();
      if (!text) {
        res.writeHead(400); return res.end("empty body");
      }
      text.split("\n").forEach(function (line) {
        line = line.trim();
        if (line) appendEvent(line);
      });
      res.writeHead(204);
      res.end();
    });
    return;
  }

  if (url.pathname === "/health" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "application/json" });
    return res.end(JSON.stringify({ ok: true }));
  }

  res.writeHead(404);
  res.end("not found");
});

server.listen(PORT, function () {
  console.log("Affil1 analytics collector listening on :%d", PORT);
  console.log("Events append to %s", EVENTS_FILE);
});
