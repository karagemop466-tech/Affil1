#!/usr/bin/env node
// Local preview server. Serves the built static site with directory indexes,
// so /shop/ resolves to shop/index.html exactly as GitHub Pages does.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const PORT = Number(process.env.PORT || 4321);
const BASE = "/Affil1"; // mirrors the GitHub Pages project path

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
};

const server = http.createServer((req, res) => {
  let urlPath = decodeURIComponent((req.url || "/").split("?")[0]);

  // Accept both the bare path and the /Affil1 project prefix.
  if (urlPath.startsWith(BASE)) urlPath = urlPath.slice(BASE.length) || "/";
  if (!urlPath.startsWith("/")) urlPath = "/" + urlPath;

  let file = path.join(ROOT, urlPath);
  if (!file.startsWith(ROOT)) {
    res.writeHead(403).end("Forbidden");
    return;
  }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) {
    file = path.join(file, "index.html");
  }
  if (!fs.existsSync(file)) {
    const notFound = path.join(ROOT, "404.html");
    res.writeHead(404, { "Content-Type": "text/html; charset=utf-8" });
    res.end(fs.existsSync(notFound) ? fs.readFileSync(notFound) : "Not found");
    return;
  }
  res.writeHead(200, {
    "Content-Type": TYPES[path.extname(file)] || "application/octet-stream",
    "Cache-Control": "no-store",
  });
  fs.createReadStream(file).pipe(res);
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`Serving ${ROOT}`);
  console.log(`  http://localhost:${PORT}/`);
  console.log(`  http://localhost:${PORT}${BASE}/`);
});
