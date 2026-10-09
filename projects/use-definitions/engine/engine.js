// USE Software "Definitions" engine. Every reusable piece of the series look lives here;
// an episode (episodes/<name>/episode.js) only supplies timings, words and its own scenes.
// Rendered frame-by-frame by tools/render.cjs via window.seek(t). Pure function of time.
'use strict';
const W = 1080, H = 1920, FPS = 30;
const out = document.getElementById('c').getContext('2d');
const off = Object.assign(document.createElement('canvas'), { width: W, height: H });
let g = off.getContext('2d');

// ---------- brand ----------
const NAVY = '#001C2E', LIGHT = '#F3F3F3', BLUE = '#009BE8', CYAN = '#12DDEB', INK = '#2E3134', GREY = '#8A9099', WHITE = '#FFFFFF';
const TRI = ['#0B5E91', '#0A86CC', '#009BE8', '#00B9EE', '#12DDEB'];
const COND = '"Barlow Condensed", sans-serif', BODY = 'Barlow, sans-serif', MONO = '"JetBrains Mono", monospace';

// ---------- maths ----------
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, p) => a + (b - a) * p;
const expo = x => { x = clamp(x); return x === 1 ? 1 : 1 - Math.pow(2, -10 * x); };     // the series' entrance curve
const expoIn = x => { x = clamp(x); return x === 0 ? 0 : Math.pow(2, 10 * x - 10); };   // whips / exits
const inOut = x => { x = clamp(x); return x < .5 ? 16 * x ** 5 : 1 - Math.pow(-2 * x + 2, 5) / 2; };
const back = x => { x = clamp(x); const c = 1.5; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
function rng(seed) { return () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0;
  let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const win = (T, a, b) => T >= a && T < b;

// ---------- sound cues (collected by render.cjs, synthesised by tools/sfx.py) ----------
// Components register their own cues so the SFX always line up with the motion.
const CUES = [];
const cue = (t, type, opts = {}) => CUES.push({ t, type, ...opts });

// ---------- footage ----------
const img = src => new Promise(r => { const i = new Image(); i.onload = () => r(i); i.onerror = () => r(null); i.src = src; });
let FR = null, MT = null, LOGO = null, META = { frames: 1 }, EP_DIR = '', TRACK = null, FBOX = null;
// Past the last source frame, ping-pong the final 12 frames so the speaker never freezes.
function fidx(T) {
  const n = META.frames; let i = Math.floor(T * FPS) + 1;
  if (i > n) { const L = 12, k = (i - n) % (2 * L); i = n - (k < L ? k : 2 * L - k); }
  return clamp(i, 1, n);
}
const pad = n => String(n).padStart(4, '0');
async function load(T) {
  const i = fidx(T);
  FR = await img(`${EP_DIR}/build/frames/f${pad(i)}.jpg`);
  MT = await img(`${EP_DIR}/build/matte/m${pad(i)}.png`);
  // tracked face for this frame (falls back to the fixed box); FACE follows it so crops stay centred
  if (TRACK) { const b = TRACK[i - 1]; FBOX = { x: b[0], y: b[1], w: b[2], h: b[3] }; FACE = { x: b[0] + b[2] / 2, y: b[1] + b[3] * .5 }; }
}
// FACE: where the face sits in the 1080x1920 source. Episodes can override (EP.face).
let FACE = { x: 545, y: 540 };
const BZ = 1.22, BAY = .25;                                   // series framing: cut at thighs, face a quarter down
function xf(rect, zoom, ay) {
  const s = Math.max(rect.w / W, rect.h / H) * zoom;
  let ox = rect.x + rect.w / 2 - FACE.x * s, oy = rect.y + rect.h * ay - FACE.y * s;
  ox = clamp(ox, rect.x + rect.w - W * s, rect.x); oy = clamp(oy, rect.y + rect.h - H * s, rect.y);
  return [ox, oy, W * s, H * s];
}
const FULL = { x: 0, y: 0, w: W, h: H };
// Face keep-out (Hunter's rule: never cover the face). Source-frame face box, 1080x1920.
const BODY_BOX = { x: 260, y: 1000, w: 560, h: 420 };   // torso: used to tell a full-slide takeover from a face overlay
const FACE_BOX = { x: 465, y: 370, w: 180, h: 330 };   // inner face: brow to chin, cheek to cheek
let FACE_SNAPS = [], FACE_CHECK = false;
function th(rect = FULL, zoom = BZ, ay = BAY) {
  if (!FR) return; const r = xf(rect, zoom, ay); g.drawImage(FR, ...r);
  if (!FACE_CHECK) return;
  snapBox(r, rect, FBOX || FACE_BOX, 'face'); snapBox(r, rect, BODY_BOX, 'body');
}
function snapBox(r, rect, B, kind) {
  const s = r[2] / W, fx = r[0] + B.x * s, fy = r[1] + B.y * s, fw = B.w * s, fh = B.h * s;
  // only the visible part of the face inside the rect (and on canvas)
  const x0 = Math.max(fx, rect.x, 0), y0 = Math.max(fy, rect.y, 0), x1 = Math.min(fx + fw, rect.x + rect.w, W), y1 = Math.min(fy + fh, rect.y + rect.h, H);
  if (x1 - x0 < 20 || y1 - y0 < 20) return;
  const m = g.getTransform(), p0 = m.transformPoint({ x: x0, y: y0 }), p1 = m.transformPoint({ x: x1, y: y1 });
  const bx = Math.round(Math.min(p0.x, p1.x)), by = Math.round(Math.min(p0.y, p1.y)), bw = Math.round(Math.abs(p1.x - p0.x)), bh = Math.round(Math.abs(p1.y - p0.y));
  if (bw < 20 || bh < 20 || bx < 0 || by < 0 || bx + bw > W || by + bh > H) return;
  FACE_SNAPS.push({ kind, bx, by, bw, bh, d: g.getImageData(bx, by, bw, bh).data });
}
// Fraction of face pixels changed by later drawing (0 = untouched). Cut-outs redraw the face, so they pass.
function faceCovered() {
  let worst = 0, body = 1, sawBody = false;
  for (const f of FACE_SNAPS.filter(f => f.kind === 'body')) { sawBody = true; const now = g.getImageData(f.bx, f.by, f.bw, f.bh).data; let bad = 0, n = 0;
    for (let i = 0; i < now.length; i += 16) { n++; if (Math.abs(now[i] - f.d[i]) + Math.abs(now[i + 1] - f.d[i + 1]) + Math.abs(now[i + 2] - f.d[i + 2]) > 60) bad++; }
    body = Math.min(body, bad / n); }
  for (const f of FACE_SNAPS.filter(f => f.kind === 'face')) { const now = g.getImageData(f.bx, f.by, f.bw, f.bh).data; let bad = 0, n = 0;
    for (let i = 0; i < now.length; i += 16) { n++; if (Math.abs(now[i] - f.d[i]) + Math.abs(now[i + 1] - f.d[i + 1]) + Math.abs(now[i + 2] - f.d[i + 2]) > 60) bad++; }
    worst = Math.max(worst, bad / n); }
  // full takeover (slide replaces the shot): face AND torso both hidden → not an overlay
  if (worst > .9 && sawBody && body > .9) return 0;
  return worst;
}
// Speaker cut out over whatever was drawn (text behind the head). Same transform as th().
function cutout(zoom = BZ, ay = BAY) {
  if (!MT || !FR) return;
  const c = cutout.c || (cutout.c = Object.assign(document.createElement('canvas'), { width: W, height: H }));
  const x = c.getContext('2d'), r = xf(FULL, zoom, ay);
  x.globalCompositeOperation = 'source-over'; x.clearRect(0, 0, W, H);
  x.drawImage(FR, ...r); x.globalCompositeOperation = 'destination-in'; x.drawImage(MT, ...r);
  g.drawImage(c, 0, 0);
  // face is back on top: re-baseline the face check so only overlays drawn after this count
  if (FACE_CHECK) FACE_SNAPS.forEach(f => { f.d = g.getImageData(f.bx, f.by, f.bw, f.bh).data; });
}
// Screen-space face box for the current frame under a full-frame th(zoom, ay).
function faceScreen(zoom = BZ, ay = BAY) { const r = xf(FULL, zoom, ay), s = r[2] / W, b = FBOX || FACE_BOX;
  return { x: r[0] + b.x * s, y: r[1] + b.y * s, w: b.w * s, h: b.h * s }; }
// Punch-in cuts: zoomAt(T) returns BZ, or BZ*1.12 inside any EP.punchIns window.
let BASE_T = 0;   // centre time of the frame being drawn (subframes share it for cut decisions)
const zoomAt = T => (EP.punchIns || []).some(([a, b]) => win(BASE_T, a, b)) ? BZ * 1.12 : BZ;

// ---------- type ----------
function font(w, size, fam) { g.font = `${w} ${size}px ${fam}`; }
// Masked rise: the standard text entrance. exitAt → rises out the top.
function rise(txt, x, y, t, { size, w = 800, fam = COND, col = WHITE, dur = .5, exitAt = Infinity, T = 0, align = 'left', track = 0 }) {
  const p = expo(t / dur); if (p <= 0) return 0;
  const q = inOut((T - exitAt) / .24);
  font(w, size, fam); g.letterSpacing = track + 'px'; g.textAlign = align;
  g.save(); g.beginPath(); g.rect(0, y - size * 1.0, W, size * 1.25); g.clip();
  g.fillStyle = col; g.fillText(txt, x, y + (1 - p) * size * 1.1 - q * size * 1.2);
  g.restore(); g.letterSpacing = '0px'; g.textAlign = 'left';
  return g.measureText(txt).width;
}
function typeOn(txt, x, y, t, { size = 30, col = WHITE, w = 500, cps = 24, track = 4, fam = MONO, caret = false, upper = false }) {
  if (t <= 0) return; const n = Math.floor(clamp(t * cps, 0, txt.length));
  font(w, size, fam); g.letterSpacing = track + 'px'; g.fillStyle = col;
  const s = upper ? txt.toUpperCase() : txt; g.fillText(s.slice(0, n), x, y);
  if (caret && (n < s.length || Math.floor(t * 2.4) % 2 === 0)) { const cw = g.measureText(s.slice(0, n)).width;
    g.fillStyle = CYAN; g.fillRect(x + cw + 4, y - size * .8, size * .55, size); }
  g.letterSpacing = '0px';
}

// ---------- triangle shards ----------
function shard(cx, cy, s, rot, col, t, { from = [300, -200], spin = .25, dur = .7, exitAt = Infinity, T = 0, to = [400, -300] } = {}) {
  const p = expo(t / dur); if (p <= 0) return;
  const q = expoIn((T - exitAt) / .4); if (q >= 1) return;
  const x = cx + from[0] * (1 - p) + to[0] * q, y = cy + from[1] * (1 - p) + to[1] * q;
  const r = rot + (1 - p) * 2.2 + t * spin * .2 + q * 2;
  g.save(); g.translate(x, y); g.rotate(r); g.scale(s, s); g.fillStyle = col;
  g.beginPath(); g.moveTo(0, -1); g.lineTo(.95, .7); g.lineTo(-.85, .55); g.closePath(); g.fill(); g.restore();
}
function cluster(seed, cx, cy, n, spread, size, t, opts = {}) {
  const r = rng(seed);
  for (let i = 0; i < n; i++) {
    const a = r() * 6.283, d = Math.sqrt(r()) * spread;
    shard(cx + Math.cos(a) * d, cy + Math.sin(a) * d * .9, size * (.45 + r() * .75), r() * 6.28, TRI[Math.floor(r() * TRI.length)],
      t - i * .03, { ...opts, from: [(opts.from || [320, -260])[0] * (.6 + r()), (opts.from || [320, -260])[1] * (.6 + r())] });
  }
}

// ---------- triangle mosaic wipe ----------
// Covers over [a, a+.4], uncovers over [a+.4, a+.8]. Cut the scene underneath at a+.4.
function mosaic(T, a, seed = 3) {
  const t = T < a + .4 ? (T - a) / .4 : 1 + (T - a - .4) / .4;
  if (t <= 0 || t >= 2) return;
  const r = rng(seed), C = 135, cols = Math.ceil(W / C), rows = Math.ceil(H / C);
  for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) for (let k = 0; k < 2; k++) {
    const d = (i / cols * .35 + j / rows * .65) * .55 + r() * .25, col = TRI[Math.floor(r() * TRI.length)];
    const p = t < 1 ? expo((t - d) / .35) : 1 - expo((t - 1 - d) / .35); if (p <= 0) continue;
    const x = i * C, y = j * C, flip = (i + j) % 2;
    const pts = k ? (flip ? [[x, y], [x + C, y], [x, y + C]] : [[x, y], [x + C, y], [x + C, y + C]])
                  : (flip ? [[x + C, y], [x + C, y + C], [x, y + C]] : [[x, y], [x + C, y + C], [x, y + C]]);
    const mx = (pts[0][0] + pts[1][0] + pts[2][0]) / 3, my = (pts[0][1] + pts[1][1] + pts[2][1]) / 3;
    g.fillStyle = col; g.beginPath();
    pts.forEach(([px, py], n) => { const X = mx + (px - mx) * p * 1.02, Y = my + (py - my) * p * 1.02; n ? g.lineTo(X, Y) : g.moveTo(X, Y); });
    g.closePath(); g.fill();
  }
}
mosaic.cue = a => { cue(a + .05, 'riser', { d: .6, gain: .2 }); cue(a - .08, 'whoosh', { d: .6, gain: .55 }); cue(a, 'glass', { n: 30, span: .4 }); cue(a + .4, 'glass', { n: 30, span: .4 }); cue(a + .45, 'thud', { f: 48, d: .6, gain: .5 }); };

// ---------- captions (auto-chunked from words.json) ----------
// Chunk rules: break on punctuation, a pause > .35s, 3 words, or 20 characters.
let CHUNKS = [];
function chunkWords(words) {
  // whisper splits hyphenated words ("third -party") → join them back
  words = words.reduce((acc, w) => { if (w.w.startsWith('-') && acc.length) acc[acc.length - 1] = { ...acc[acc.length - 1], w: acc[acc.length - 1].w + w.w, e: w.e }; else acc.push({ ...w }); return acc; }, []);
  const out = []; let cur = [];
  words.forEach((w, i) => {
    cur.push(w);
    const next = words[i + 1], chars = cur.map(x => x.w).join(' ').length;
    if (!next || /[.,?!]$/.test(w.w) || next.s - w.e > .35 || cur.length >= 3 || chars >= 20) { out.push(cur); cur = []; }
  });
  return out;
}
// Draw the active chunk if T sits inside a caption window [a, b, y].
function captions(T) {
  T = BASE_T;   // captions are sharp: drawn at the frame centre, never blended across a chunk switch
  const wnd = (EP.captions || []).find(([a, b]) => win(T, a, b)); if (!wnd) return;
  const [wa, wb, yy, style] = wnd, SZ = 66, y = typeof yy === 'function' ? yy(T) : yy, dark = style === 'dark';
  for (let c = 0; c < CHUNKS.length; c++) {
    const ch = CHUNKS[c], carried = ch[0].s < wa, st = carried ? wa : Math.max(ch[0].s, wa + .15), last = ch[ch.length - 1];   // mid-sentence cut: chunk carries over settled; otherwise first caption after a cut waits .15s
    const en = Math.min(CHUNKS[c + 1] ? CHUNKS[c + 1][0].s : 1e9, last.e + .45, wb);
    if (!win(T, st, en) || ch[0].s >= wb || (carried && last.e < wa)) continue;   // finished lines don't carry across a cut
    font(800, SZ, COND); g.letterSpacing = '0.5px';
    const sp = 16, ws = ch.map(w => g.measureText(w.w).width), total = ws.reduce((a, b) => a + b, 0) + sp * (ch.length - 1);
    const xs = []; let x = W / 2 - total / 2; ws.forEach(w => { xs.push(x); x += w + sp; });
    let a = 0; ch.forEach((w, i) => { if (T >= w.s) a = i; });
    const pa = Math.max(0, a - 1), k = a === 0 ? 1 : expo((T - ch[a].s) / .16);
    const hx = lerp(xs[pa], xs[a], k) - 10, hw = lerp(ws[pa], ws[a], k) + 20;
    const p = carried ? 1 : expo((T - st) / .32), dy = (1 - p) * SZ * 1.2;
    g.save(); g.beginPath(); g.rect(0, y - SZ * 1.1, W, SZ * 1.5); g.clip();
    g.fillStyle = CYAN; g.beginPath(); g.roundRect(hx, y - SZ * .82 + dy, hw, SZ * 1.0, 8); g.fill();
    if (!dark) { g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 10; g.shadowOffsetY = 2; }
    ch.forEach((w, i) => { g.fillStyle = dark ? (i === a ? NAVY : INK) : WHITE; g.fillText(w.w, xs[i], y + dy); });   // dark: light slides
    g.restore(); g.letterSpacing = '0px';
  }
}
captions.cue = () => {};                                       // captions are silent: SFX only on real motion

// ---------- small parts ----------
function iconUser(cx, cy, r, p) {
  g.save(); g.globalAlpha *= p; g.translate(cx, cy); g.scale(lerp(.6, 1, back(p)), lerp(.6, 1, back(p)));
  g.fillStyle = WHITE; g.strokeStyle = BLUE; g.lineWidth = 4; g.beginPath(); g.arc(0, 0, r, 0, 7); g.fill(); g.stroke();
  g.strokeStyle = INK; g.lineWidth = 4; g.beginPath(); g.arc(0, -r * .18, r * .22, 0, 7); g.stroke();
  g.beginPath(); g.arc(0, r * .55, r * .42, Math.PI * 1.1, Math.PI * 1.9); g.stroke(); g.restore();
}
function iconDB(cx, cy, r, p) {
  g.save(); g.globalAlpha *= p; g.translate(cx, cy); g.scale(lerp(.6, 1, back(p)), lerp(.6, 1, back(p)));
  g.fillStyle = WHITE; g.strokeStyle = BLUE; g.lineWidth = 4; g.beginPath(); g.roundRect(-r, -r, r * 2, r * 2, 22); g.fill(); g.stroke();
  g.strokeStyle = INK; g.lineWidth = 4; const w = r * .5, h = r * .16;
  for (const yy of [-r * .32, 0, r * .32]) { g.beginPath(); g.ellipse(0, yy, w, h, 0, 0, Math.PI * (yy === -r * .32 ? 2 : 1)); g.stroke(); }
  g.beginPath(); g.moveTo(-w, -r * .32); g.lineTo(-w, r * .32); g.moveTo(w, -r * .32); g.lineTo(w, r * .32); g.stroke(); g.restore();
}
function pill(txt, x, y, { size = 28, padX = 18, h = 52, fam = MONO, w = 500 } = {}) {
  font(w, size, fam); g.letterSpacing = '2px'; const tw = g.measureText(txt).width + padX * 2;
  g.lineWidth = 2.5; g.strokeStyle = '#C9CDD2'; g.fillStyle = WHITE;
  g.beginPath(); g.roundRect(x, y, tw, h, h / 2); g.fill(); g.stroke();
  g.fillStyle = INK; g.fillText(txt, x + padX, y + h * .68); g.letterSpacing = '0px'; return tw;
}
// Light panel with rounded top edge (rises under the talking head; can grow to full screen).
const PANEL_Y = 1230;
function panel(top) {
  g.save(); g.shadowColor = 'rgba(0,0,0,.25)'; g.shadowBlur = 40; g.fillStyle = LIGHT;
  g.beginPath(); g.roundRect(0, top, W, H - top + 60, [44, 44, 0, 0]); g.fill(); g.restore();
}
// Circular face, white rim (light slides).
function faceCircle(cx, cy, r, p) {
  if (p <= 0 || !FR) return; g.save(); g.translate(cx, cy); g.scale(p, p);
  g.shadowColor = 'rgba(0,0,0,.18)'; g.shadowBlur = 30; g.shadowOffsetY = 10;
  g.beginPath(); g.arc(0, 0, r, 0, 7); g.fillStyle = WHITE; g.fill(); g.shadowColor = 'transparent';
  g.beginPath(); g.arc(0, 0, r - 8, 0, 7); g.clip();
  g.drawImage(FR, FACE.x - 260, FACE.y - 250, 520, 520, -(r - 8), -(r - 8), (r - 8) * 2, (r - 8) * 2); g.restore();
}
// Vertical whip: returns the y offset for a layer leaving upward at time a (0 before).
const whip = (T, a, d = .2) => -H * expoIn((T - a) / d);
whip.cue = a => cue(a - .05, 'whoosh', { d: .3, bright: .5, gain: .45 });

// =====================================================================================
// SERIES COMPONENTS
// =====================================================================================
// Title: "Definitions" label + giant TERM behind the speaker's head, shard clusters. 0 → out.
function titleCard(T, term, out = 2.0, label = 'Definitions') {
  th(FULL, BZ + T * .012);
  typeOn(label, 44, 140, T - .1, { size: 34, track: 2, w: 500, cps: 22 });
  const size = Math.min(330, 900 / Math.max(1, term.length) * 1.55);
  rise(term, 26, 470, T - .15, { size, w: 800, dur: .6, exitAt: out, T });
  cutout(BZ + T * .012);
  cluster(21, 900, 520, 7, 150, 95, T - .25, { from: [420, -120], exitAt: out + .05, T, to: [500, -200] });
  cluster(22, 70, 820, 3, 70, 70, T - .4, { from: [-300, 80], exitAt: out + .05, T, to: [-400, 100] });
}
titleCard.cue = (term, out = 2.0, label = 'Definitions') => { cue(.1, 'typing', { n: label.length, cps: 22 }); cue(.12, 'whoosh', { d: .4, gain: .35 }); cue(.25, 'thud', { f: 60, d: .35, gain: .45 });
  cue(.25, 'shards', { n: 7 }); cue(.4, 'shards', { n: 3 }); cue(out, 'whoosh', { d: .35, gain: .3 }); };

// Lower third: logo | name / role. Shown a → b.
function lowerThird(T, a, b, name = 'Sam Bruhn', role = 'Founder & CEO', y = 1330) {
  const p = expo((T - a) / .55), q = expoIn((T - b) / .3); if (p <= 0 || q >= 1) return;
  const x = 64 - (1 - p) * 120 - q * 700, w = 640, h = 180;
  g.save(); g.globalAlpha = clamp(p * 2) * (1 - q);
  g.shadowColor = 'rgba(0,0,0,.18)'; g.shadowBlur = 30; g.shadowOffsetY = 10;
  g.fillStyle = WHITE; g.beginPath(); g.roundRect(x, y, w * lerp(.5, 1, p), h, 14); g.fill(); g.restore();
  g.save(); g.globalAlpha = clamp((T - a - .03) * 6) * (1 - q); g.beginPath(); g.rect(x, y, w * p, h); g.clip();
  if (LOGO) { const lh = 86, lw = lh * LOGO.width / LOGO.height; g.drawImage(LOGO, x + 34, y + h / 2 - lh / 2, lw, lh); }
  g.fillStyle = '#D9DDE1'; g.fillRect(x + 262, y + 34, 2, (h - 68) * expo((T - a - .25) / .4));
  rise(name, x + 290, y + 92, T - a - .06, { size: 76, w: 700, col: INK, dur: .5 });
  typeOn(role, x + 292, y + 140, T - a - .2, { size: 24, col: BLUE, track: 5, upper: true, cps: 30 });
  g.restore();
  const wob = Math.sin((T - a) * 3) * .25;
  shard(x + 40, y + 6, 46, -.4 + wob, CYAN, T - a - .1, { from: [-140, -160], exitAt: b, T, to: [-300, -200], spin: 1.2 });
  shard(x + 22, y + 40, 34, 1.2 - wob, '#0B5E91', T - a - .16, { from: [-160, -100], exitAt: b, T, to: [-300, -100], spin: 1.6 });
  shard(x + 64, y - 10, 26, 2.4 + wob, BLUE, T - a - .2, { from: [-100, -200], exitAt: b, T, to: [-200, -300], spin: 2 });
}
lowerThird.cue = (a, role = 'Founder & CEO') => { cue(a, 'whoosh', { d: .3, bright: .4, gain: .3 }); cue(a + .4, 'typing', { n: role.length, cps: 30 }); cue(a + .1, 'shards', { n: 2 }); };

// Dictionary card: DEFINITIONS · NOUN pill, giant term, "say:" pronunciation. a → whip out at b.
function defCard(T, a, b, term, say, under) {
  const wy = whip(T, b); if (wy < 0 && under) under(T);
  g.save(); g.translate(0, wy);
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  const t = T - a, p = expo(t / .5);
  g.save(); g.globalAlpha = p; g.strokeStyle = BLUE; g.lineWidth = 3; font(500, 30, MONO); g.letterSpacing = '4px';
  const pw = g.measureText('DEFINITIONS').width + 40; g.beginPath(); g.roundRect(92, 470, pw, 56, 28); g.stroke();
  g.fillStyle = BLUE; g.fillText('DEFINITIONS', 112, 509); g.fillStyle = GREY; g.fillText('NOUN', 92 + pw + 20, 509);
  g.letterSpacing = '0px'; g.restore();
  g.fillStyle = '#D7D9DC'; g.fillRect(92, 570, 870 * expo((t - .1) / .6), 2);
  const size = Math.min(470, 880 / Math.max(1, term.length) * 2.0);
  rise(term, 80, 1010, t - .12, { size, w: 800, col: INK, dur: .6 });
  typeOn('say: ' + say, 96, 1140, t - .42, { size: 44, col: '#555A60', track: 2, w: 400, cps: 30 });
  g.fillStyle = BLUE; g.fillRect(96, 1180, 150 * expo((t - .5) / .5), 9);
  cluster(31, 860, 1560, 8, 230, 120, t - .1, { from: [380, 420] });
  g.restore();
}
defCard.cue = (a, b, say) => { cue(a + .42, 'typing', { n: say.length + 5, cps: 30 }); cue(a + .1, 'shards', { n: 8 }); whip.cue(b); };

// Navy "X stands for" slide: speaker in an inset card, words land on the VO, inset expands at the end.
// words: [[letter, rest, time], ...]
const INSET = { x: 60, y: 120, w: 960, h: 880 };
function standsFor(T, a, b, label, words) {
  const t = T - a, p = expo(t / .55), e = inOut((T - b + .3) / .3);
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  const r0 = { x: INSET.x, y: INSET.y + (1 - p) * 500, w: INSET.w, h: INSET.h };
  const r = { x: lerp(r0.x, 0, e), y: lerp(r0.y, 0, e), w: lerp(r0.w, W, e), h: lerp(r0.h, H, e) };
  g.save(); g.translate(0, e * 400);
  typeOn(label + ' stands for', 100, 1120, t - .2, { size: 34, col: CYAN, track: 6, upper: true, cps: 30 });
  const size = words.length > 4 ? 130 : 160, gap = size + 5;
  words.forEach(([L, rest, at], i) => {
    const y = 1290 + i * gap, tt = T - at; if (tt <= 0) return;
    font(800, size, COND); const lw = g.measureText(L).width;
    rise(L, 98, y, tt, { size, w: 800, col: CYAN, dur: .45 });
    rise(rest, 98 + lw, y, tt - .04, { size, w: 800, col: WHITE, dur: .45 });
    const full = lw + g.measureText(rest).width;
    g.fillStyle = CYAN; g.fillRect(98, y + 20, full * expo((tt - .1) / .5), 5);
  });
  cluster(41, 880, 1640, 5, 140, 120, t - .3, { from: [300, 300] });
  g.restore();
  g.save(); g.beginPath(); g.roundRect(r.x, r.y, r.w, r.h, 36 * (1 - e)); g.clip(); th(r, lerp(1.0, BZ * 1.14, e), lerp(.45, BAY, e)); g.restore();
}
standsFor.cue = (a, b, label, words) => { cue(a + .4, 'typing', { n: label.length + 11, cps: 30 });
  words.forEach(([, , at], i) => { cue(at, 'pop', { f: 600 + i * 90, d: .06, gain: .22 }); cue(at, 'whoosh', { d: .18, bright: .4, gain: .12 }); });
  cue(b - .32, 'whoosh', { d: .4, gain: .4 }); };

// Big word behind the head on the talking head (e.g. "REST"), optional cyan tag pill.
function behindHead(T, a, b, word, tag, z = BZ * 1.14) {
  if (T < a || T >= b) return;
  // fit the word fully left of the tracked face (60px gap) so it reads whole behind the head
  const fs = faceScreen(z); font(800, 100, COND); const w100 = g.measureText(word).width;
  const size = clamp((fs.x - 100) / w100 * 100, 120, Math.min(360, 1300 / word.length));
  rise(word, 40, 560, T - a, { size, w: 800, dur: .5, exitAt: b - .15, T });
  cutout(z);
  if (tag && T > a + .16) { const p = back((T - a - .16) / .45), f = faceScreen(z); font(800, 70, COND);
    const tw0 = g.measureText(tag).width + 50, tx = Math.min(W - tw0 / 2 - 20, f.x + f.w + tw0 / 2 + 50), ty = Math.max(70, f.y - 30);
    g.save(); g.translate(tx, ty); g.scale(p, p); g.rotate(-.06);
    font(800, 70, COND); const tw = g.measureText(tag).width + 50;
    g.fillStyle = CYAN; g.beginPath(); g.roundRect(-tw / 2, -45, tw, 90, 14); g.fill();
    g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText(tag, 0, 25); g.textAlign = 'left'; g.restore(); }
}
behindHead.cue = (a, tag) => { cue(a - .03, 'whoosh', { d: .3, bright: .4, gain: .3 }); cue(a, 'thud', { f: 48, d: .5, gain: .6 }); if (tag) cue(a + .16, 'pop', { f: 1000, d: .06, gain: .2 }); };

// Dark terminal card over the talking head, types two lines.
function terminal(T, a, b, l1, l2) {
  const p = expo((T - a) / .45), q = expoIn((T - b + .2) / .2); if (p <= 0 || q >= 1) return;
  const x = 44, y = 70 - (1 - p) * 260 - q * 400, w = 600, h = 190;
  g.save(); g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 40; g.shadowOffsetY = 14;
  g.fillStyle = NAVY; g.beginPath(); g.roundRect(x, y, w, h, 18); g.fill(); g.restore();
  g.fillStyle = '#3B5266'; [0, 1, 2].forEach(i => { g.beginPath(); g.arc(x + 30 + i * 22, y + 28, 6, 0, 7); g.fill(); });
  const t = T - a - .3, n1 = l1.length / 34;
  typeOn('$', x + 30, y + 92, t, { size: 30, col: CYAN, track: 0, cps: 34 });
  typeOn(l1, x + 30 + 36, y + 92, t - 1 / 34, { size: 30, col: WHITE, track: 0, cps: 34, caret: t < n1 });
  typeOn(l2, x + 30, y + 140, t - n1, { size: 30, col: WHITE, track: 0, cps: 34, caret: t >= n1 });
}
terminal.cue = (a, l1, l2) => { cue(a, 'whoosh', { d: .3, bright: .4, gain: .25 }); cue(a + .3, 'typing', { n: l1.length + l2.length, cps: 34 }); };

// "200 OK" response card on the talking head: drops in, code rolls, JSON types, shatters at sh.
function okCard(T, a, sh, json, status = 200, label = 'OK') {
  if (T < a) return;
  const p = expo((T - a) / .4), x = 60, w = 960, h = 330, y = 900 - (1 - p) * 700;
  if (T < sh) {
    g.save(); g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 50; g.shadowOffsetY = 18;
    g.fillStyle = NAVY; g.beginPath(); g.roundRect(x, y, w, h, 20); g.fill(); g.restore();
    const roll = clamp((T - a - .15) / .35), code = roll >= 1 ? status : status + Math.round((1 - roll) ** 2 * 48 + (Math.floor(T * 30) % 7));
    font(800, 120, COND); g.fillStyle = CYAN; g.fillText(String(code), x + 40, y + 125);
    g.fillStyle = WHITE; if (roll >= 1) { const cw = g.measureText(status + ' ').width; g.fillText(label, x + 40 + cw, y + 125); }
    typeOn('To: you', x + w - 200, y + 100, T - a - .15, { size: 26, col: GREY, track: 5, upper: true, cps: 30 });
    g.fillStyle = '#163A55'; g.fillRect(x + 40, y + 160, w - 80, 2);
    typeOn(json, x + 40, y + 240, T - a - .4, { size: 34, col: WHITE, track: 0, cps: 60, caret: true });
    return;
  }
  const r = rng(77), t = T - sh;                              // shatter
  for (let j = 0; j < 6; j++) for (let i = 0; i < 14; i++) for (let k = 0; k < 2; k++) {
    const cw = w / 14, chh = h / 6, cx0 = x + i * cw, cy0 = y + j * chh;
    const pts = k ? [[cx0, cy0], [cx0 + cw, cy0], [cx0, cy0 + chh]] : [[cx0 + cw, cy0], [cx0 + cw, cy0 + chh], [cx0, cy0 + chh]];
    const mx = (pts[0][0] + pts[1][0] + pts[2][0]) / 3, my = (pts[0][1] + pts[1][1] + pts[2][1]) / 3;
    const vx = (mx - 540) * (1.5 + r() * 2) + (r() - .5) * 900, vy = (my - 1065) * (2 + r() * 3) + 600 * r() - 300;
    const rot = (r() - .5) * 10 * t, sc = 1 - clamp(t / .6) * r() * .5, col = r() < .55 ? NAVY : TRI[Math.floor(r() * TRI.length)];
    const ox = vx * t + 900 * t * t * (r() - .5), oy = vy * t + 1400 * t * t;
    g.save(); g.translate(mx + ox, my + oy); g.rotate(rot); g.scale(sc, sc); g.fillStyle = col; g.beginPath();
    pts.forEach(([px, py], n) => n ? g.lineTo(px - mx, py - my) : g.moveTo(px - mx, py - my)); g.closePath(); g.fill(); g.restore();
  }
}
okCard.cue = (a, sh, json) => { cue(a, 'whoosh', { d: .3, bright: .4, gain: .3 }); cue(a + .35, 'thud', { f: 70, d: .2, gain: .25 });
  cue(a + .15, 'ticks', { n: 10, gap: .035 }); cue(a + .5, 'chime', { f: 1175, gain: .1 }); cue(a + .4, 'typing', { n: json.length, cps: 60 });
  cue(sh, 'thud', { f: 45, d: .5, gain: .5 }); cue(sh, 'glass', { n: 60, span: .35 }); };

// White end card: logo, "Definitions", tagline, URL. Fades to white over the last .4s.
function endCard(T, a, dur, title = 'Definitions') {
  const t = T - a; g.fillStyle = WHITE; g.fillRect(0, 0, W, H);
  if (LOGO) { const p = expo(t / .6), lw = 620, lh = lw * LOGO.height / LOGO.width;
    g.save(); g.beginPath(); g.rect(70, 600, lw * p + 4, lh + 10); g.clip(); g.drawImage(LOGO, 70, 605, lw, lh); g.restore(); }
  rise(title, 76, 1010, t - .2, { size: 150, w: 700, col: INK, dur: .5 });
  typeOn('understand · solve · execute', 82, 1110, t - .25, { size: 38, col: '#0B6FA8', track: 5, w: 500, cps: 30 });
  typeOn('usesoftware.com.au', 82, 1175, t - .6, { size: 32, col: '#555A60', track: 2, w: 400, cps: 30 });
  cluster(51, 900, 160, 7, 180, 120, t - .05, { from: [300, -300] });
  cluster(52, 760, 1620, 4, 140, 150, t - .15, { from: [200, 400] });
  cluster(53, 620, 1920, 6, 260, 110, t - .25, { from: [0, 300] });
  const f = clamp((T - dur + .4) / .4); if (f > 0) { g.fillStyle = `rgba(255,255,255,${f})`; g.fillRect(0, 0, W, H); }
}
endCard.cue = a => { cue(a + .1, 'swell', { d: 2.2, gain: .18 }); cue(a + .45, 'typing', { n: 28, cps: 30 }); cue(a + 1.1, 'typing', { n: 18, cps: 30 }); cue(a, 'shards', { n: 8 }); };

// =====================================================================================
// ANIMATION KIT v2: more vocabulary, so episodes don't repeat the same moves.
// =====================================================================================
// Per-letter drop: each glyph falls from above with overshoot + slight rotation, staggered.
function letterDrop(txt, x, y, t, { size = 300, w = 800, col = WHITE, stagger = .05, exitAt = Infinity, T = 0 } = {}) {
  font(w, size, COND); let cx = x; const q = inOut((T - exitAt) / .3);
  [...txt].forEach((ch, i) => {
    const p = back((t - i * stagger) / .55), cw = g.measureText(ch).width; if (p <= 0) { cx += cw; return; }
    g.save(); g.translate(cx + cw / 2, y - size * .35); g.rotate((1 - clamp(p)) * (i % 2 ? .35 : -.35) + q * (i % 2 ? .6 : -.6));
    g.translate(0, -(1 - p) * size * 1.4 - q * size * 2); g.globalAlpha *= clamp(p * 3) * (1 - q);
    g.fillStyle = col; g.fillText(ch, -cw / 2, size * .35); g.restore(); cx += cw;
  });
}
letterDrop.cue = (a, n, stagger = .05) => { for (let i = 0; i < n; i++) cue(a + i * stagger + .2, 'pop', { f: 500 + i * 60, d: .06, gain: .16 }); };
// Per-letter pop: glyphs scale up from 0 one by one (springy). For short punchy words.
function letterPop(txt, x, y, t, { size = 300, w = 800, col = WHITE, stagger = .06 } = {}) {
  font(w, size, COND); let cx = x;
  [...txt].forEach((ch, i) => { const p = back((t - i * stagger) / .4), cw = g.measureText(ch).width;
    if (p > 0) { g.save(); g.translate(cx + cw / 2, y - size * .35); g.scale(p, p); g.fillStyle = col; g.fillText(ch, -cw / 2, size * .35); g.restore(); }
    cx += cw; });
}
letterPop.cue = (a, n, stagger = .06) => { for (let i = 0; i < n; i++) cue(a + i * stagger, 'pop', { f: 800 + i * 90, d: .05, gain: .15 }); };
// Speech bubble near the head; text types in, bubble springs from its tail.
function bubble(T, a, b, txt, x, y, { size = 40 } = {}) {
  const p = back((T - a) / .45), q = expoIn((T - b) / .25); if (p <= 0 || q >= 1) return;
  font(600, size, BODY); const tw = Math.min(g.measureText(txt).width, 760), w = tw + 60, h = size + 50;
  g.save(); g.translate(x, y + h); g.scale(p * (1 - q), p * (1 - q)); g.translate(-x, -(y + h));
  g.shadowColor = 'rgba(0,0,0,.25)'; g.shadowBlur = 30; g.shadowOffsetY = 10; g.fillStyle = WHITE;
  g.beginPath(); g.roundRect(x - w / 2, y, w, h, h / 2); g.fill();
  g.beginPath(); g.moveTo(x - 18, y + h - 2); g.lineTo(x, y + h + 26); g.lineTo(x + 18, y + h - 2); g.fill(); g.restore();
  g.save(); g.globalAlpha = 1 - q; typeOn(txt, x - w / 2 + 30, y + h / 2 + size * .35, T - a - .15, { size, col: INK, w: 600, fam: BODY, track: 0, cps: 40 }); g.restore();
}
bubble.cue = (a, txt) => { cue(a, 'pop', { f: 700, d: .08, gain: .25 }); cue(a + .15, 'typing', { n: Math.min(txt.length, 40), cps: 40, gain: .2 }); };
// 3D flip: draws front() then back() on a card that rotates around its vertical axis at time a.
function flipCard(T, a, cx, cy, w, h, front, backFn, col = NAVY) {
  const p = inOut((T - a) / .5), ang = p * Math.PI, sx = Math.abs(Math.cos(ang)), showBack = ang > Math.PI / 2;
  g.save(); g.translate(cx, cy); g.scale(Math.max(sx, .001), 1 + Math.sin(ang) * .06);
  g.shadowColor = 'rgba(0,0,0,.3)'; g.shadowBlur = 40; g.shadowOffsetY = 14; g.fillStyle = showBack ? CYAN : col;
  g.beginPath(); g.roundRect(-w / 2, -h / 2, w, h, 18); g.fill(); g.shadowColor = 'transparent';
  (showBack ? backFn : front)(-w / 2, -h / 2, w, h); g.restore();
}
flipCard.cue = a => { cue(a, 'whoosh', { d: .4, bright: .5, gain: .25 }); cue(a + .5, 'click', { f: 1600, gain: .3 }); };
// Iris: a growing circle reveals `inner` (drawn by a callback) over the current frame.
function iris(T, a, cx, cy, inner, d = .55) {
  const p = inOut((T - a) / d); if (p <= 0) return false;
  g.save(); g.beginPath(); g.arc(cx, cy, p * Math.hypot(W, H), 0, 7); g.clip(); inner(T); g.restore();
  if (p < 1) { g.strokeStyle = CYAN; g.lineWidth = 10 * (1 - p); g.beginPath(); g.arc(cx, cy, p * Math.hypot(W, H), 0, 7); g.stroke(); }
  return p >= 1;
}
iris.cue = a => { cue(a, 'riser', { d: .4, gain: .15 }); cue(a, 'whoosh', { d: .55, bright: .3, gain: .4 }); };
// Zoom-through: scale the outgoing layer up hard toward (cx,cy) and fade, revealing `under`.
function zoomThrough(T, a, cx, cy, outgoing, under, d = .4) {
  const p = expoIn((T - a) / d); if (p <= 0) { outgoing(T); return; }
  under(T); if (p >= 1) return;
  g.save(); g.globalAlpha = 1 - p; g.translate(cx, cy); g.scale(1 + p * 5, 1 + p * 5); g.translate(-cx, -cy); outgoing(T); g.restore();
}
zoomThrough.cue = a => { cue(a, 'whoosh', { d: .45, bright: .6, gain: .5 }); cue(a + .38, 'thud', { f: 60, d: .3, gain: .35 }); };
// Glitch: draws fn three times with RGB offsets + horizontal slice tears, intensity k (0..1).
function glitch(T, k, fn) {
  if (k <= 0) { fn(); return; }
  const c = glitch.c || (glitch.c = Object.assign(document.createElement('canvas'), { width: W, height: H })), x = c.getContext('2d');
  const sv = g; x.clearRect(0, 0, W, H);
  // render fn into the temp canvas
  const gg = g; g = x; fn(); g = gg;
  const r = rng(Math.floor(T * 24)), off = 14 * k;
  g.save(); g.globalCompositeOperation = 'lighter'; g.globalAlpha = .55;
  g.filter = 'sepia(1) saturate(8) hue-rotate(160deg)'; g.drawImage(c, -off, 0);
  g.filter = 'sepia(1) saturate(8) hue-rotate(-40deg)'; g.drawImage(c, off, 0); g.restore(); g.filter = 'none';
  for (let i = 0; i < 7; i++) { const y = r() * H, h = 10 + r() * 50, dx = (r() - .5) * 80 * k; g.drawImage(c, 0, y, W, h, dx, y, W, h); }
  g.drawImage(c, 0, 0);
}
// Progress race: a bar fills with an eased ticker + label, shimmer sweep on completion.
function progress(T, a, d, x, y, w, label) {
  const p = expo((T - a) / d); if (T < a) return;
  typeOn(label, x, y - 24, T - a, { size: 26, col: GREY, track: 5, upper: true, cps: 40 });
  g.fillStyle = '#163A55'; g.beginPath(); g.roundRect(x, y, w, 30, 15); g.fill();
  const gr = g.createLinearGradient(x, 0, x + w, 0); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN);
  g.fillStyle = gr; g.beginPath(); g.roundRect(x, y, Math.max(30, w * p), 30, 15); g.fill();
  if (p > .98) { const s = ((T - a - d) * 1.2) % 1.5; const sx = x + w * s; const sg = g.createLinearGradient(sx - 80, 0, sx + 80, 0);
    sg.addColorStop(0, 'rgba(255,255,255,0)'); sg.addColorStop(.5, 'rgba(255,255,255,.7)'); sg.addColorStop(1, 'rgba(255,255,255,0)');
    g.save(); g.beginPath(); g.roundRect(x, y, w, 30, 15); g.clip(); g.fillStyle = sg; g.fillRect(sx - 80, y, 160, 30); g.restore(); }
  font(800, 64, COND); g.fillStyle = WHITE; g.textAlign = 'right'; g.fillText(Math.round(p * 100) + '%', x + w, y - 18); g.textAlign = 'left';
}
progress.cue = (a, d) => { for (let i = 0; i < 16; i++) cue(a + d * (1 - Math.pow(1 - i / 16, 3)), 'click', { f: 1200 + i * 60, gain: .14 }); cue(a + d * .9, 'chime', { f: 1318, gain: .12 }); };
// Card stack: cards slide in from the right one after another and stack with depth (ref "REST API / HTTP / TCP" stack).
function cardStack(T, items, x, y, w, h, gap = 22) {
  items.forEach(([title, sub, at, dark], i) => {
    const p = expo((T - at) / .5); if (p <= 0) return;
    const yy = y + i * (h + gap), xx = x + (1 - p) * 900;
    g.save(); g.globalAlpha = clamp(p * 2); card(xx, yy, w, h, dark ? '#2B2E33' : WHITE, 16, .2);
    font(800, h * .48, COND); g.fillStyle = dark ? WHITE : INK; g.fillText(title, xx + 32, yy + h * .66);
    typeOn(sub, xx + w - 32 - sub.length * 17, yy + h * .6, T - at - .2, { size: 24, col: dark ? CYAN : BLUE, track: 4, upper: true, cps: 40 });
    g.restore();
  });
}
cardStack.cue = items => items.forEach(([, , at]) => { cue(at, 'whoosh', { d: .3, bright: .45, gain: .3 }); cue(at + .3, 'click', { f: 1400, gain: .25 }); });
// Triangle burst: shards explode radially from a point (celebration / emphasis).
function burst(T, a, cx, cy, n = 22, seed = 9) {
  const t = T - a; if (t <= 0 || t > 1.2) return; const r = rng(seed);
  for (let i = 0; i < n; i++) { const ang = r() * 6.28, sp = 300 + r() * 700, s = 14 + r() * 26, col = TRI[Math.floor(r() * TRI.length)];
    const d = sp * expo(t / .9), x = cx + Math.cos(ang) * d, y = cy + Math.sin(ang) * d + 300 * t * t;
    g.save(); g.globalAlpha = 1 - clamp((t - .6) / .6); g.translate(x, y); g.rotate(r() * 6 + t * 8); g.scale(s, s); g.fillStyle = col;
    g.beginPath(); g.moveTo(0, -1); g.lineTo(.95, .7); g.lineTo(-.85, .55); g.closePath(); g.fill(); g.restore(); }
}
burst.cue = a => { cue(a, 'thud', { f: 70, d: .25, gain: .3 }); cue(a, 'glass', { n: 24, span: .3 }); };
// Shared card helper (rounded, soft shadow).
function card(x, y, w, h, col = WHITE, r = 20, sh = .12) {
  g.save(); g.shadowColor = `rgba(0,0,0,${sh})`; g.shadowBlur = 40; g.shadowOffsetY = 14; g.fillStyle = col;
  g.beginPath(); g.roundRect(x, y, w, h, r); g.fill(); g.restore();
}

// =====================================================================================
// RUNTIME
// =====================================================================================
// Motion blur: average SUB subframes across a full-frame shutter.
const SUB = +(new URLSearchParams(location.search).get("sub") || 8);
function draw(T) {
  out.globalAlpha = 1; BASE_T = T;
  for (let k = 0; k < SUB; k++) {
    g.globalAlpha = 1; g.clearRect(0, 0, W, H);
    // subframes never straddle a scene cut (EP.cuts), so cuts stay hard instead of dissolving
    let t = T + (k / SUB - .5) * (1 / FPS); for (const c of EP.cuts || []) { if (T >= c && t < c) t = c; if (T < c && t >= c) t = c - 1e-4; }
    EP.frame(t);
    out.globalAlpha = 1 / (k + 1); out.drawImage(off, 0, 0);
  }
  out.globalAlpha = 1;
}
window.seek = async t => { await load(t); draw(t); return true; };
// Face audit: single-subframe render of time t; returns share of the face area covered by graphics.
window.faceAudit = async t => { await load(t); BASE_T = t; FACE_CHECK = true; FACE_SNAPS = []; g.globalAlpha = 1; g.clearRect(0, 0, W, H); EP.frame(t);
  const c = faceCovered(); FACE_CHECK = false; FACE_SNAPS = []; return c; };
window.cues = () => CUES;
window.ready = (async () => {
  EP_DIR = new URLSearchParams(location.search).get('ep') || '.';
  await document.fonts.ready;
  await Promise.all(['800 40px "Barlow Condensed"', '700 40px "Barlow Condensed"', '600 40px "Barlow Condensed"', '600 40px Barlow',
    '500 40px "JetBrains Mono"', '400 40px "JetBrains Mono"'].map(f => document.fonts.load(f)));
  LOGO = await img('../brand/use-logo-short.png');
  META = await fetch(`${EP_DIR}/build/meta.json`).then(r => r.json());
  TRACK = await fetch(`${EP_DIR}/build/face.json`).then(r => r.ok ? r.json() : null).catch(() => null);
  const words = await fetch(`${EP_DIR}/words.json`).then(r => r.json());
  await new Promise((res, rej) => { const s = document.createElement('script'); s.src = `${EP_DIR}/episode.js`; s.onload = res; s.onerror = rej; document.body.appendChild(s); });
  if (EP.face) FACE = EP.face;
  CHUNKS = chunkWords(words.filter(w => !(EP.dropWords || []).some(([a, b]) => w.s >= a && w.s < b)));
  captions.cue(); EP.cues && EP.cues();
  return { dur: EP.dur };
})();
if (!navigator.webdriver) window.ready.then(async () => { const t0 = performance.now();
  (async function loop() { const t = ((performance.now() - t0) / 1000) % EP.dur; await load(t); draw(t); requestAnimationFrame(loop); })(); });
