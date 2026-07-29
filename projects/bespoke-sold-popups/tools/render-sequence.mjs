#!/usr/bin/env node
/**
 * Render the pop-ups to a frame sequence + MP4.
 *
 * One headless Chrome, one page load: each frame is set by calling the page's own
 * renderFrame(scene, ms) over the DevTools Protocol, then captured. Roughly 50x
 * faster than launching Chrome per frame.
 *
 *   node tools/render-sequence.mjs [169|916] [outDir]
 *
 * Needs the `bespoke-popups` server running (http://localhost:8773).
 */
import { spawn } from "node:child_process";
import { mkdir, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";

const AR      = process.argv[2] || "169";
const OUT     = process.argv[3] || `/tmp/bespoke-popups-${AR}`;
const [W, H]  = AR === "169" ? [1920, 1080] : [1080, 1920];
const URL_    = `http://localhost:8773/popups.html?ar=${AR}&bg=plate`;
const CHROME  = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT    = 9333;
const FPS     = 25;
const STEP    = 1000 / FPS;

/* scene → last millisecond to shoot (in + hold, before the out) */
const SCENES = [[1, 2800], [2, 2200], [3, 4600]];

const sleep = ms => new Promise(r => setTimeout(r, ms));

/* own profile dir — otherwise this fights the user's running Chrome for the profile lock */
const PROFILE = `/tmp/bespoke-render-profile-${process.pid}`;

const chrome = spawn(CHROME, [
  "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
  "--no-default-browser-check", `--user-data-dir=${PROFILE}`,
  "--force-device-scale-factor=1", `--window-size=${W},${H}`,
  `--remote-debugging-port=${PORT}`, "--remote-allow-origins=*",
  "about:blank"
], { stdio: "ignore" });

/* wait for the debugger, then find the page target */
let wsUrl;
for (let i = 0; i < 60 && !wsUrl; i++){
  await sleep(250);
  try {
    const targets = await fetch(`http://127.0.0.1:${PORT}/json/list`).then(r => r.json());
    wsUrl = targets.find(t => t.type === "page")?.webSocketDebuggerUrl;
  } catch {}
}
if (!wsUrl) { chrome.kill(); throw new Error("Chrome DevTools never came up"); }

const ws = new WebSocket(wsUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

let id = 0;
const pending = new Map();
ws.onmessage = e => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)){
    const { res, rej } = pending.get(m.id); pending.delete(m.id);
    m.error ? rej(new Error(m.error.message)) : res(m.result);
  }
};
const send = (method, params = {}) => new Promise((res, rej) => {
  const msgId = ++id;
  pending.set(msgId, { res, rej });
  ws.send(JSON.stringify({ id: msgId, method, params }));
});

const evaluate = async expression => {
  const { result, exceptionDetails } =
    await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
  if (exceptionDetails) throw new Error(exceptionDetails.text + " " + (exceptionDetails.exception?.description || ""));
  return result.value;
};

await send("Page.enable");
await send("Runtime.enable");
/* NB: no Emulation.setDeviceMetricsOverride and no fromSurface on the capture —
   either one wedges Page.captureScreenshot in headless=new. --window-size is enough. */
await send("Page.navigate", { url: URL_ });
for (let i = 0; i < 80; i++){                       // wait for fonts + first paint
  await sleep(150);
  if (await evaluate("!!window.renderFrame && document.fonts.status === 'loaded'").catch(() => false)) break;
}

await rm(OUT, { recursive: true, force: true });
await mkdir(OUT, { recursive: true });

let n = 0;
for (const [scene, end] of SCENES){
  for (let ms = 0; ms <= end; ms += STEP){
    await evaluate(`window.renderFrame(${scene}, ${Math.round(ms)}, {ar:"${AR}"})`);
    const { data } = await send("Page.captureScreenshot", { format: "png" });
    await writeFile(join(OUT, String(n++).padStart(4, "0") + ".png"), Buffer.from(data, "base64"));
  }
  process.stdout.write(`scene ${scene} done (${n} frames)\n`);
}

ws.close(); chrome.kill();
await rm(PROFILE, { recursive: true, force: true });

const mp4 = `${OUT}.mp4`;
await new Promise((res, rej) => {
  const ff = spawn("ffmpeg", [
    "-y", "-v", "error", "-framerate", String(FPS), "-i", join(OUT, "%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-r", "30", mp4
  ], { stdio: "inherit" });
  ff.on("exit", code => code === 0 ? res() : rej(new Error("ffmpeg exit " + code)));
});
console.log(`${n} frames -> ${mp4}`);
