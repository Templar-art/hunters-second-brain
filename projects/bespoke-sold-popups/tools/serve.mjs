#!/usr/bin/env node
/**
 * Minimal static server for this folder.
 *
 * Replaces `python3 -m http.server`, which dies on this Mac with
 * "'idna' codec can't encode character '\x83'" — http.server calls
 * socket.getfqdn() on bind and the machine's hostname isn't ASCII-clean.
 *
 *   node tools/serve.mjs [port]
 */
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { join, extname, normalize } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = normalize(join(fileURLToPath(import.meta.url), "..", ".."));
const PORT = Number(process.argv[2]) || 8773;

const TYPES = {
  ".html":"text/html; charset=utf-8", ".js":"text/javascript", ".mjs":"text/javascript",
  ".css":"text/css", ".svg":"image/svg+xml", ".png":"image/png", ".jpg":"image/jpeg",
  ".jpeg":"image/jpeg", ".webm":"video/webm", ".mp4":"video/mp4", ".mov":"video/quicktime",
  ".woff2":"font/woff2", ".woff":"font/woff", ".ttf":"font/ttf", ".otf":"font/otf",
  ".json":"application/json", ".md":"text/markdown; charset=utf-8"
};

createServer(async (req, res) => {
  try {
    const url  = new URL(req.url, "http://localhost");
    let path   = normalize(join(ROOT, decodeURIComponent(url.pathname)));
    if (!path.startsWith(ROOT)) { res.writeHead(403).end("forbidden"); return; }
    if ((await stat(path)).isDirectory()) path = join(path, "popups.html");

    const body = await readFile(path);
    res.writeHead(200, {
      "content-type": TYPES[extname(path).toLowerCase()] || "application/octet-stream",
      "cache-control": "no-store"
    }).end(body);
  } catch {
    res.writeHead(404, { "content-type":"text/plain" }).end("not found");
  }
}).listen(PORT, "127.0.0.1", () => console.log(`serving ${ROOT} on http://localhost:${PORT}`));
