#!/usr/bin/env node
// Minimal static server for previewing the templates (python http.server breaks on this Mac's hostname).
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { join, extname, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = normalize(join(fileURLToPath(import.meta.url), ".."));
const PORT = Number(process.argv[2]) || 8774;

const TYPES = {
  ".html": "text/html; charset=utf-8", ".css": "text/css",
  ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"
};

createServer(async (req, res) => {
  try {
    const url = new URL(req.url, "http://localhost");
    let path = normalize(join(ROOT, decodeURIComponent(url.pathname)));
    if (!path.startsWith(ROOT)) { res.writeHead(403).end("forbidden"); return; }
    if ((await stat(path)).isDirectory()) path = join(path, "index.html");
    const body = await readFile(path);
    res.writeHead(200, {
      "content-type": TYPES[extname(path).toLowerCase()] || "application/octet-stream",
      "cache-control": "no-store"
    }).end(body);
  } catch {
    res.writeHead(404, { "content-type": "text/plain" }).end("not found");
  }
}).listen(PORT, "127.0.0.1", () => console.log(`serving ${ROOT} on http://localhost:${PORT}`));
