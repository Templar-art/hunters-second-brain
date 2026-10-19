#!/usr/bin/env node
// SFX sorter: moves finished sound downloads out of ~/Downloads into ~/Music/SFX Library.
//
//   zip that is mostly audio  -> extracted to SFX Library/Ocular Sounds/<pack>/  (if "ocular"
//                                appears in the zip name or its contents), else
//                                SFX Library/_Incoming/<pack>/;
//                                the original zip is kept in SFX Library/_Archives/
//
// Only sound-pack zips (>= MIN_AUDIO audio files) downloaded after the sorter was installed
// (SFX Library/.sorter-since) are touched. Loose audio files are left alone on purpose:
// Downloads also holds music tracks and client VO. RAWs, videos, PDFs, other zips: untouched.
// Nothing is deleted; name clashes get a " (2)" suffix. Run by launchd on every change
// to ~/Downloads (com.10x.sfx-sorter), or by hand: node sfx-sorter.mjs [--dry-run]

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const HOME = os.homedir();
const DOWNLOADS = process.env.SFX_DOWNLOADS || path.join(HOME, "Downloads");
const LIBRARY = process.env.SFX_LIBRARY || path.join(HOME, "Music", "SFX Library");
const DRY = process.argv.includes("--dry-run");

const AUDIO = new Set([".wav", ".aif", ".aiff", ".mp3", ".flac", ".ogg", ".m4a", ".caf", ".bwf"]);
const DOCS = new Set([".pdf", ".txt", ".csv", ".rtf", ".md", ".html", ".png", ".jpg", ".jpeg", ".xml", ".json"]);
const PARTIAL = /\.(crdownload|download|part|partial|tmp)$/i;
const MIN_AUDIO = 5;            // fewer audio files than this = a song/VO, not a sound pack
const SETTLE_MS = 20_000;       // a file must be untouched this long before we move it
const MAX_WAIT_MS = 4 * 60_000; // keep rechecking fresh files this long, then exit

const log = (msg) => {
  const line = `${new Date().toISOString()} ${DRY ? "[dry] " : ""}${msg}`;
  console.log(line);
  if (!DRY) fs.appendFileSync(path.join(LIBRARY, "_sorter.log"), line + "\n");
};

const ext = (p) => path.extname(p).toLowerCase();

function freePath(dir, name) {
  const { name: base, ext: e } = path.parse(name);
  let candidate = path.join(dir, name);
  for (let i = 2; fs.existsSync(candidate); i++) candidate = path.join(dir, `${base} (${i})${e}`);
  return candidate;
}

function move(src, destDir) {
  fs.mkdirSync(destDir, { recursive: true });
  const dest = freePath(destDir, path.basename(src));
  if (!DRY) fs.renameSync(src, dest);
  return dest;
}

function zipEntries(zip) {
  try {
    return execFileSync("/usr/bin/unzip", ["-Z1", zip], { encoding: "utf8", maxBuffer: 64 << 20 })
      .split("\n").filter((e) => e && !e.endsWith("/") && !e.startsWith("__MACOSX/") && !path.basename(e).startsWith("._"));
  } catch {
    return null; // not a readable zip (yet)
  }
}

function classifyZip(zip) {
  const entries = zipEntries(zip);
  if (!entries?.length) return null;
  const audio = entries.filter((e) => AUDIO.has(ext(e))).length;
  const other = entries.filter((e) => !AUDIO.has(ext(e)) && !DOCS.has(ext(e))).length;
  if (audio < MIN_AUDIO || audio < other) return null; // not a sound pack
  const ocular = /ocular/i.test(path.basename(zip)) || entries.some((e) => /ocular/i.test(e));
  return { ocular, audio };
}

function packName(zip) {
  return path.basename(zip, path.extname(zip)).replace(/\s*\(\d+\)$/, "").trim() || "Pack";
}

function extractPack(zip, info) {
  const base = path.join(LIBRARY, info.ocular ? "Ocular Sounds" : "_Incoming");
  const dest = freePath(base, packName(zip));
  if (DRY) return log(`would extract ${path.basename(zip)} (${info.audio} audio) -> ${dest}`);

  const tmp = path.join(LIBRARY, ".extracting", path.basename(dest));
  fs.rmSync(tmp, { recursive: true, force: true });
  fs.mkdirSync(tmp, { recursive: true });
  execFileSync("/usr/bin/ditto", ["-x", "-k", zip, tmp]);
  fs.rmSync(path.join(tmp, "__MACOSX"), { recursive: true, force: true });

  // Unwrap a lone top-level folder only when it is just the pack's own name (Pack/Pack/…);
  // a lone category folder like "Impacts" is kept.
  const top = fs.readdirSync(tmp).filter((n) => !n.startsWith("."));
  const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, "");
  const pack = norm(packName(zip));
  const wrapper = top.length === 1 && fs.statSync(path.join(tmp, top[0])).isDirectory() &&
    (norm(top[0]).includes(pack) || pack.includes(norm(top[0])) || /ocular/i.test(top[0]));
  const root = wrapper ? path.join(tmp, top[0]) : tmp;
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.renameSync(root, dest);
  fs.rmSync(path.join(LIBRARY, ".extracting"), { recursive: true, force: true });

  const kept = move(zip, path.join(LIBRARY, "_Archives"));
  log(`extracted ${path.basename(zip)} (${info.audio} audio) -> ${dest}; zip kept at ${kept}`);
}

const SINCE_FILE = path.join(LIBRARY, ".sorter-since");

function pass(since) {
  let waiting = 0;
  for (const name of fs.readdirSync(DOWNLOADS)) {
    if (name.startsWith(".") || PARTIAL.test(name)) continue;
    const p = path.join(DOWNLOADS, name);
    let st;
    try { st = fs.statSync(p); } catch { continue; }
    if (!st.isFile()) continue;
    const e = ext(name);
    if (e !== ".zip" || st.birthtimeMs < since) continue;
    if (Date.now() - st.mtimeMs < SETTLE_MS) { waiting++; continue; }

    try {
      const info = classifyZip(p);
      if (info) extractPack(p, info);
    } catch (err) {
      log(`ERROR on ${name}: ${err.message}`);
    }
  }
  return waiting;
}

fs.mkdirSync(LIBRARY, { recursive: true });
if (!fs.existsSync(SINCE_FILE) && !DRY) fs.writeFileSync(SINCE_FILE, new Date().toISOString() + "\n");
const since = fs.existsSync(SINCE_FILE) ? Date.parse(fs.readFileSync(SINCE_FILE, "utf8").trim()) : Date.now();
const started = Date.now();
while (pass(since) > 0 && Date.now() - started < MAX_WAIT_MS) {
  await new Promise((r) => setTimeout(r, 15_000));
}
