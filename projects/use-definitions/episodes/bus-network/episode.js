// "Our favourite build": the bus on-time tracking job (22 Oct talking head, ~46s).
// Story beats (VO word times): hook 0–4.2 · transport operator 6.4 · on-time script 7.4–12.2
// · off the beaten track 12.5–16.6 · no system 17.6–21.6 · old system no good 22–26.9
// · quick rebuild 27.5–30.8 · network nuances 31.3–34.2 · accuracy + completeness 34.8–40
// · better outlook 40.4–42.4 · more work 43–46.
const ACC = '#F5A524';                                   // warning amber, only for "bad data" moments
const PANEL_IN = 7.3, NAVY_IN = 12.5, SYS_IN = 17.4, BAD_IN = 21.9, BUILD_IN = 27.7, NET_IN = 31.2, RES_IN = 34.6, OUT_IN = 40.3, MORE_IN = 42.9;
const SHATTER = 46.15, END_IN = 46.55;
const panelTop = (T, a) => lerp(H + 40, PANEL_Y, expo((T - a) / .6));

window.EP = {
  dur: 49.8,
  voEnd: 46.3,
  punchIns: [[4.6, 7.3], [24.3, 27.4], [29.6, 31.2], [43.0, 44.5]],
  // v3 (redo pass): hard scene switches + punch-in edges, so motion blur never straddles them
  cuts: [4.6, 7.3, 24.3, 27.4, 27.7, 29.6, 31.2, 42.9, 43.0, 44.5, 46.55],
  // deliberate transitions the QC continuity check should ignore (iris, whips, glitches, mosaics, zoom-through, shatter)
  qcAllow: [[0, 0.6], [2.0, 2.6], [4.5, 4.8], [7.2, 7.9], [11.5, 13.1], [17.1, 17.8], [19.1, 19.7], [21.8, 22.6], [24.2, 24.8],
            [25.8, 27.2], [27.2, 28.1], [29.5, 29.8], [30.2, 31.9], [34.5, 35.4], [40.0, 40.7], [42.6, 43.2], [44.4, 44.7], [45.9, 47.1]],
  captions: [[0, 4.6, 1200], [4.6, PANEL_IN, 1200], [PANEL_IN, NAVY_IN - .4, T => Math.min(1200, panelTop(T, PANEL_IN) - 80)],
             [SYS_IN, BAD_IN, 1240], [BUILD_IN, NET_IN, 1040], [NET_IN, RES_IN, 1060],
             [OUT_IN, MORE_IN, 1560], [MORE_IN, SHATTER, 1000]],

  frame(T) {
    if (T < 4.6) sceneHook(T);
    else if (T < PANEL_IN) { th(FULL, zoomAt(T)); captions(T); lowerThird(T, 4.8, 7.0); }
    else if (T < NAVY_IN) { scenePanelScript(T); iris(T, NAVY_IN - .55, 194, 1520, sceneOffTrack); }
    else if (T < SYS_IN) sceneOffTrack(T);
    else if (T < BAD_IN) glitch(T, 1 - clamp((T - 19.2) / .35) - (T < 19.2 ? 1 : 0), () => { th(FULL, BZ * 1.14); behindHead(T, 19.04, 20.3, 'SYSTEM', 'NONE'); captions(T); govCard(T); });
    else if (T < BUILD_IN) glitch(T, Math.max(1 - clamp((T - BAD_IN) / .4), T > 25.9 && T < 27.0 && Math.floor(T * 7) % 3 === 0 ? .5 : 0), () => sceneBadData(T));
    else if (T < NET_IN) sceneBuild(T);
    else if (T < RES_IN) sceneNetwork(T);
    else if (T < OUT_IN) zoomThrough(T, RES_IN, 540, 1500, sceneNetwork, sceneResults, .35);
    else if (T < MORE_IN) { th(FULL, BZ); captions(T); outlookCard(T); }
    else if (T < END_IN) { th(FULL, zoomAt(T)); if (T < SHATTER + .1) captions(T); moreCard(T); }
    else endCard(T, END_IN, this.dur, 'Case Study', true);       // v3: alive end card (no dead hold)
    mosaic(T, BUILD_IN - .4, 5);
    mosaic(T, SHATTER - .05, 9);
  },

  cues() {
    cue(.1, 'typing', { n: 30, cps: 26 }); letterDrop.cue(.2, 5, .07); cue(.25, 'shards', { n: 6 }); cue(2.2, 'whoosh', { d: .4, gain: .35 });
    bubble.cue(2.3, 'Which build am I secretly fond of?'); lowerThird.cue(4.8);
    cue(PANEL_IN - .1, 'whoosh', { d: .55, gain: .45 });
    cue(8.0, 'pop', { f: 700, d: .07, gain: .2 }); cue(9.24, 'pop', { f: 800, d: .07, gain: .2 }); cue(9.4, 'typing', { n: 10, cps: 28 });
    flipCard.cue(11.6); cue(11.95, 'chime', { f: 988, gain: .12 }); cue(12.18, 'thud', { f: 90, d: .2, gain: .25 });
    iris.cue(NAVY_IN - .55);
    cue(12.7, 'typing', { n: 17, cps: 30 }); cue(13.2, 'whoosh', { d: .3, gain: .2 });
    cue(14.5, 'riser', { d: 1.4, gain: .15 }); cue(16.0, 'thud', { f: 50, d: .5, gain: .5 });
    whip.cue(SYS_IN - .2);
    behindHead.cue(19.04, 'NONE'); cue(19.2, 'ticks', { n: 8, gap: .03, gain: .3 }); cue(20.3, 'whoosh', { d: .3, gain: .25 }); cue(20.4, 'typing', { n: 30, cps: 40 });
    cue(BAD_IN - .05, 'whoosh', { d: .5, gain: .45 }); cue(BAD_IN, 'ticks', { n: 10, gap: .03, gain: .35 }); cue(22.4, 'typing', { n: 16, cps: 28 });
    for (let i = 0; i < 14; i++) cue(25.9 + i * .07, 'click', { f: 900 + (i % 4) * 300, gain: .15 });
    cue(24.56, 'thud', { f: 45, d: .5, gain: .55 });
    mosaic.cue(BUILD_IN - .4);
    cue(28.0, 'whoosh', { d: .35, bright: .4, gain: .3 }); progress.cue(28.4, 1.8);
    letterPop.cue(30.36, 4); burst.cue(30.78);
    cue(NET_IN - .1, 'whoosh', { d: .55, gain: .45 });
    for (let i = 0; i < 9; i++) cue(31.6 + i * .12, 'pop', { f: 600 + i * 70, d: .05, gain: .1 });
    zoomThrough.cue(RES_IN);
    cue(38.34, 'riser', { d: .5, gain: .12 }); cue(38.34, 'chime', { f: 880, gain: .1 }); cue(39.18, 'chime', { f: 1175, gain: .1 });
    whip.cue(OUT_IN - .1); cue(OUT_IN + .1, 'whoosh', { d: .3, bright: .4, gain: .3 });
    cardStack.cue(MORE_STACK); burst.cue(39.4);
    cue(SHATTER, 'thud', { f: 45, d: .5, gain: .5 }); cue(SHATTER, 'glass', { n: 60, span: .35 });
    mosaic.cue(SHATTER - .05); endCard.cue(END_IN);
  },
};

// ---------- small drawing helpers for this story ----------
function iconBus(cx, cy, r, p, col = BLUE) {
  g.save(); g.globalAlpha *= p; g.translate(cx, cy); const s = lerp(.6, 1, back(p)); g.scale(s, s);
  g.fillStyle = WHITE; g.strokeStyle = col; g.lineWidth = 4; g.beginPath(); g.roundRect(-r, -r, r * 2, r * 2, 22); g.fill(); g.stroke();
  g.strokeStyle = INK; g.lineWidth = 4;
  g.beginPath(); g.roundRect(-r * .5, -r * .5, r, r * .85, 8); g.stroke();
  g.beginPath(); g.moveTo(-r * .5, -r * .05); g.lineTo(r * .5, -r * .05); g.stroke();
  g.fillStyle = INK; [-1, 1].forEach(k => { g.beginPath(); g.arc(k * r * .28, r * .46, r * .09, 0, 7); g.fill(); });
  g.restore();
}
function statusPill(txt, x, y, kind, p = 1, size = 24) {
  if (p <= 0) return 0; font(500, size, MONO); g.letterSpacing = '2px';
  const w = g.measureText(txt).width + 30, h = size * 1.75;
  const C = { ok: [CYAN, NAVY, CYAN], bad: [WHITE, '#9A6200', ACC], off: [WHITE, BLUE, BLUE] }[kind];
  g.save(); g.globalAlpha *= p; g.translate(x + w / 2, y); g.scale(lerp(.6, 1, back(p)), lerp(.6, 1, back(p))); g.translate(-(x + w / 2), -y);
  g.fillStyle = C[0]; g.strokeStyle = C[2]; g.lineWidth = 2.5; g.beginPath(); g.roundRect(x, y - h * .72, w, h, h / 2); g.fill(); g.stroke();
  g.fillStyle = C[1]; g.fillText(txt, x + 15, y); g.restore(); g.letterSpacing = '0px'; return w;
}

function line(x1, y1, x2, y2, p, col = INK, lw = 3) { if (p <= 0) return; g.strokeStyle = col; g.lineWidth = lw; g.beginPath(); g.moveTo(x1, y1); g.lineTo(lerp(x1, x2, p), lerp(y1, y2, p)); g.stroke(); }

// ---------- scenes ----------
// Panel: Bus → script → "On time?" verdict that flips ✓ ON TIME then LATE.
function scenePanelScript(T) {
  th(FULL, BZ); const top = panelTop(T, PANEL_IN);
  captions(T); panel(top);
  const cy = 1520 + top - PANEL_Y;
  g.save(); g.translate(540, cy); g.scale(1.08, 1.08); g.translate(-540, -cy);
  typeOn('What the operator had', 110, cy - 150, T - 7.5, { size: 26, col: BLUE, track: 6, upper: true, cps: 30 });
  iconBus(180, cy, 62, expo((T - 8.0) / .5));
  line(252, cy, 380, cy, expo((T - 8.4) / .4));
  // script card flips over to its verdict on "on time"
  if (T > 9.24) {
    const pin = back((T - 9.24) / .45); g.save(); g.translate(560, cy); g.scale(pin, pin); g.translate(-560, -cy);
    flipCard(T, 11.6, 560, cy, 330, 160,
      (x, y, w, h) => { g.fillStyle = '#3B5266'; [0, 1, 2].forEach(i => { g.beginPath(); g.arc(x + 26 + i * 18, y + 26, 5, 0, 7); g.fill(); });
        typeOn('on_time.py', x + 30, y + 100, T - 9.4, { size: 38, col: WHITE, track: 0, cps: 28, caret: T < 11 }); },
      (x, y, w, h) => { const late = T >= 12.18, sh = late ? Math.sin((T - 12.18) * 60) * 10 * (1 - clamp((T - 12.18) / .3)) : 0;
        font(800, 64, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText(late ? 'LATE ✗' : 'ON TIME ✓', sh, 22); g.textAlign = 'left'; });
    g.restore();
  }
  g.restore();
}
// Navy map: standard grid routes vs one winding route off the beaten track, bus dot travelling.
const ROUTE = [[150, 1760], [260, 1630], [240, 1480], [380, 1390], [470, 1510], [610, 1470], [660, 1310], [820, 1260], [900, 1390], [960, 1560]];
function routePoint(u) {
  const segs = ROUTE.length - 1, f = clamp(u) * segs, i = Math.min(segs - 1, Math.floor(f)), k = f - i;
  return [lerp(ROUTE[i][0], ROUTE[i + 1][0], k), lerp(ROUTE[i][1], ROUTE[i + 1][1], k)];
}
function sceneOffTrack(T) {
  const wy = whip(T, SYS_IN - .2); if (wy < 0) { th(FULL, BZ * 1.14); behindHead(T, 19.04, 20.3, 'SYSTEM', 'NONE'); captions(T); }
  g.save(); g.translate(0, wy);
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('Industry standard', 80, 420, T - 12.6, { size: 30, col: CYAN, track: 6, upper: true, cps: 30 });
  // standard grid: tidy straight routes
  const pg = expo((T - 12.9) / .8);
  g.globalAlpha = .55 * pg;
  for (let i = 0; i < 5; i++) { line(80, 520 + i * 70, 1000, 520 + i * 70, expo((T - 12.9 - i * .06) / .6), '#2B4A62', 6);
    for (let k = 0; k < 6; k++) { g.fillStyle = '#2B4A62'; g.beginPath(); g.arc(120 + k * 170, 520 + i * 70, 9 * pg, 0, 7); g.fill(); } }
  g.globalAlpha = 1;
  rise('Simple.', 80, 960, T - 12.62, { size: 150, w: 800, col: WHITE, dur: .5, exitAt: 14.18, T });
  rise('Standard.', 80, 960, T - 14.0, { size: 150, w: 800, col: '#2B4A62', dur: .4, exitAt: 14.18, T });
  // the off-track route
  if (T > 14.18) {
    rise('Off the', 80, 940, T - 15.66, { size: 150, w: 800, col: WHITE, dur: .5 });
    rise('beaten track.', 80, 1080, T - 16.0, { size: 150, w: 800, col: CYAN, dur: .5 });
    const u = expo((T - 14.3) / 1.6);
    g.save(); g.setLineDash([2, 18]); g.lineCap = 'round'; g.strokeStyle = '#2B4A62'; g.lineWidth = 8;
    g.beginPath(); ROUTE.forEach(([x, y], i) => i ? g.lineTo(x, y) : g.moveTo(x, y)); g.stroke(); g.restore();
    const cam = 1 + .1 * inOut((T - 14.2) / 2.6); g.save(); g.translate(560, 1500); g.scale(cam, cam); g.translate(-560, -1500);   // push the map only, never the text
    g.strokeStyle = CYAN; g.lineWidth = 7; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath();
    const steps = 80; for (let s = 0; s <= steps * u; s++) { const [x, y] = routePoint(s / steps); s ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke();
    ROUTE.forEach(([x, y], i) => { const pp = back((T - 14.3 - i * .16) / .4); if (pp <= 0) return;
      g.fillStyle = NAVY; g.strokeStyle = CYAN; g.lineWidth = 5; g.beginPath(); g.arc(x, y, 14 * pp, 0, 7); g.fill(); g.stroke(); });
    const [bx, by] = routePoint((T - 14.3) / 2.8 % 1);
    g.save(); g.shadowColor = CYAN; g.shadowBlur = 30; g.fillStyle = WHITE; g.beginPath(); g.arc(bx, by, 16, 0, 7); g.fill(); g.restore();
    g.restore();
  }
  faceCircle(880, 230, 130, back((T - 12.8) / .6));
  cluster(61, 980, 1840, 4, 100, 90, T - 12.7, { from: [300, 300] });
  g.restore();
}
// Small card under the head: "Governing body → no system provided".
function govCard(T) {
  const p = expo((T - 20.3) / .45), q = expoIn((T - BAD_IN + .25) / .25); if (p <= 0 || q >= 1) return;
  const x = 60, y = 1400 + (1 - p) * 120 + q * 300, w = 960, h = 170;
  g.save(); g.globalAlpha = clamp(p * 2); card(x, y, w, h, WHITE, 20, .2);
  typeOn('Governing body', x + 36, y + 62, T - 20.32, { size: 30, col: GREY, track: 5, upper: true, cps: 40 });
  statusPill('NO SYSTEM PROVIDED', x + 36, y + 130, 'bad', expo((T - 20.8) / .3), 32);
  g.restore();
}
// Full light slide: the old system's trip log, full of errors and bad data.
const TRIPS = [['R12', '07:40', '07:41', 'ok'], ['R12', '08:10', '—', 'NULL'], ['R7', '08:25', '09:90', 'ERR'], ['R3', '08:40', '08:40', 'ok'], ['R7', '09:05', '??', 'ERR']];
function sceneBadData(T) {
  const top = lerp(H, 0, inOut((T - BAD_IN) / .45)), wy = whip(T, BUILD_IN - .45);
  th(FULL, BZ); g.save(); g.translate(0, wy); panel(top);
  if (top > 4) { g.restore(); return; }
  faceCircle(880, 240, 140, back((T - BAD_IN - .2) / .6));
  typeOn('What they had', 60, 330, T - 22.4, { size: 30, col: BLUE, track: 6, upper: true, cps: 28 });
  rise('Previously…', 54, 560, T - 23.0, { size: 190, w: 800, col: INK, dur: .45, exitAt: 24.5, T });
  rise('No good.', 54, 560, T - 24.56, { size: 230, w: 800, col: INK, dur: .45 });
  // trip log card
  const pt = expo((T - 22.6) / .6), x = 50, y = 700 + (1 - pt) * 80, w = 980;
  g.save(); g.globalAlpha = pt; card(x, y, w, 130 + TRIPS.length * 92, WHITE);
  const C = [x + 40, x + 210, x + 420, x + 650];
  font(500, 24, MONO); g.letterSpacing = '3px'; g.fillStyle = GREY;
  ['ROUTE', 'SCHED', 'ARRIVED', 'STATUS'].forEach((h, i) => g.fillText(h, C[i], y + 62)); g.letterSpacing = '0px';
  g.fillStyle = '#E5E7EA'; g.fillRect(x + 30, y + 90, w - 60, 2);
  TRIPS.forEach((r, i) => {
    const ry = y + 160 + i * 92, bad = r[3] !== 'ok', on = T > 25.92 + i * .12;
    if (bad && on) { g.fillStyle = 'rgba(245,165,36,.12)'; g.fillRect(x + 16, ry - 52, w - 32, 80); }
    const jit = bad && on && Math.floor(T * 30) % 9 === i ? 6 : 0;          // glitch flicker on the bad rows
    font(500, 32, MONO); g.fillStyle = INK; g.fillText(r[0], C[0] + jit, ry);
    g.fillStyle = '#555A60'; g.fillText(r[1], C[1], ry); g.fillStyle = bad && on ? '#9A6200' : '#555A60'; g.fillText(r[2], C[2] - jit, ry);
    statusPill(bad ? r[3] : 'OK', C[3], ry, bad ? (on ? 'bad' : 'off') : 'off', 1, 24);
  });
  g.restore();
  // "errors and bad data" lands as a big amber stamp
  rise('Errors.', 54, 1440, T - 25.92, { size: 130, w: 800, col: ACC, dur: .4 });
  rise('Bad data.', 420, 1440, T - 26.62, { size: 130, w: 800, col: ACC, dur: .4 });
  g.restore();
}
// Bottom panel: the network graph assembling, a bus pulsing along it.
const NODES = [[140, 1480], [300, 1400], [300, 1600], [480, 1500], [640, 1390], [640, 1620], [800, 1500], [950, 1420], [950, 1640]];
const EDGES = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [3, 5], [4, 6], [5, 6], [6, 7], [6, 8]];
function sceneNetwork(T) {
  const t = T - NET_IN, p = expo(t / .6);
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  cluster(71, 980, 160, 4, 90, 80, t - .1, { from: [300, -200] });
  // floating speaker card with a gentle 3D sway
  const cw = 640, ch = 800, cx = 540, cy = 520 + (1 - p) * 900 + Math.sin(t * 1.4) * 8, tilt = Math.sin(t * .9) * .035 - .03;
  g.save(); g.translate(cx, cy); g.rotate(tilt); g.transform(1, 0, Math.sin(t * .7) * .02, 1, 0, 0);
  g.shadowColor = 'rgba(0,0,0,.5)'; g.shadowBlur = 60; g.shadowOffsetY = 30; g.fillStyle = '#0B2A40';
  g.beginPath(); g.roundRect(-cw / 2, -ch / 2, cw, ch, 34); g.fill(); g.shadowColor = 'transparent';
  g.beginPath(); g.roundRect(-cw / 2, -ch / 2, cw, ch, 34); g.clip();
  th({ x: -cw / 2, y: -ch / 2, w: cw, h: ch }, 1.15, .4); g.restore();
  g.strokeStyle = CYAN; g.lineWidth = 3; g.save(); g.translate(cx, cy); g.rotate(tilt); g.beginPath(); g.roundRect(-cw / 2, -ch / 2, cw, ch, 34); g.globalAlpha = .6; g.stroke(); g.restore();
  captions(T);
  typeOn('The nuances of the network', 80, 1210, T - 31.6, { size: 26, col: CYAN, track: 6, upper: true, cps: 30 });
  const oy = 0, wy = 0;
  EDGES.forEach(([a, b], i) => line(NODES[a][0], NODES[a][1] + 40, NODES[b][0], NODES[b][1] + 40, expo((T - 31.6 - i * .1) / .4), '#2B4A62', 5));
  NODES.forEach(([x, y], i) => { const pp = back((T - 31.6 - i * .12) / .4); if (pp <= 0) return; const hub = i === 3 || i === 6;
    g.save(); if (hub) { g.shadowColor = CYAN; g.shadowBlur = 25; } g.fillStyle = NAVY; g.strokeStyle = hub ? CYAN : '#5C7A92'; g.lineWidth = 5;
    g.beginPath(); g.arc(x, y + 40, (hub ? 26 : 18) * pp, 0, 7); g.fill(); g.stroke(); g.restore(); });
  const path = [0, 1, 3, 4, 6, 7], u = ((T - 32.6) / 1.6) % 1;
  if (T > 32.6) { const f = u * (path.length - 1), i = Math.floor(f), k = f - i, A = NODES[path[i]], B = NODES[path[i + 1]];
    g.save(); g.shadowColor = CYAN; g.shadowBlur = 30; g.fillStyle = WHITE; g.beginPath(); g.arc(lerp(A[0], B[0], k), lerp(A[1], B[1], k) + 40, 14, 0, 7); g.fill(); g.restore(); }
}
// Results: before/after bars for accuracy + completeness (no invented numbers).
function sceneResults(T) {
  const wy = whip(T, OUT_IN - .1);
  g.save(); g.translate(0, wy); g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  const tile = (i, x, y, w, h, col, draw) => { const p = back((T - RES_IN - .05 - i * .1) / .5); if (p <= 0) return;
    g.save(); g.translate(x + w / 2, y + h / 2); g.scale(p, p); g.translate(-(x + w / 2), -(y + h / 2)); card(x, y, w, h, col, 28, .1);
    g.beginPath(); g.roundRect(x, y, w, h, 28); g.clip(); draw(x, y, w, h); g.restore(); };
  // headline tile (wide)
  tile(0, 40, 120, 1000, 470, WHITE, (x, y) => {
    typeOn('The result', x + 50, y + 80, T - 35.1, { size: 28, col: BLUE, track: 6, upper: true, cps: 28 });
    rise('Noticeably', x + 44, y + 250, T - 37.16, { size: 170, w: 800, col: INK, dur: .45 });
    rise('better.', x + 44, y + 410, T - 37.4, { size: 170, w: 800, col: BLUE, dur: .45 }); });
  // speaker tile (tall, left)
  tile(1, 40, 620, 480, 860, NAVY, (x, y, w, h) => { th({ x, y, w, h }, 1.25, .38); });
  // stat tiles (right)
  [['Accuracy', 38.34], ['Completeness', 39.18]].forEach(([lab, at], i) => tile(2 + i, 550, 620 + i * 445, 490, 415, i ? NAVY : WHITE, (x, y, w, h) => {
    const dark = i === 1; font(700, 66, COND); g.fillStyle = dark ? WHITE : INK; g.fillText(lab, x + 36, y + 90);
    font(500, 22, MONO); g.letterSpacing = '3px'; g.fillStyle = GREY; g.fillText('BEFORE', x + 36, y + 200); g.fillText('AFTER', x + 36, y + 310); g.letterSpacing = '0px';
    const bw = w - 72, b0 = .38 + i * .06, track = dark ? '#163A55' : '#E5E7EA';
    g.fillStyle = track; g.beginPath(); g.roundRect(x + 36, y + 216, bw, 34, 17); g.fill(); g.beginPath(); g.roundRect(x + 36, y + 326, bw, 34, 17); g.fill();
    g.fillStyle = '#AEB4BA'; g.beginPath(); g.roundRect(x + 36, y + 216, bw * b0 * expo((T - 35.9 - i * .15) / .7) , 34, 17); g.fill();
    const pa = expo((T - at) / .8); if (pa > 0) { const gw = bw * lerp(b0, .94, pa), gr = g.createLinearGradient(x + 36, 0, x + 36 + gw, 0);
      gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN); g.fillStyle = gr; g.beginPath(); g.roundRect(x + 36, y + 326, gw, 34, 17); g.fill(); }
  }));
  // footer tile
  tile(4, 40, 1510, 1000, 170, WHITE, (x, y) => { typeOn('Accuracy + completeness, for the client', x + 44, y + 95, T - 36.2, { size: 30, col: INK, track: 2, cps: 40 }); });
  burst(T, 39.4, 800, 1150, 24, 4);
  g.restore();
}
// Dark card over the head: on-time performance trend line drawing upward.
function outlookCard(T) {
  const p = expo((T - OUT_IN - .1) / .45), q = expoIn((T - MORE_IN + .2) / .2); if (p <= 0 || q >= 1) return;
  const x = 60, w = 960, h = 420, y = 1020 - (1 - p) * 700 - q * 900;
  card(x, y, w, h, NAVY, 20, .35);
  typeOn('On-time performance', x + 40, y + 70, T - OUT_IN - .3, { size: 26, col: GREY, track: 5, upper: true, cps: 40 });
  rise('Clear outlook', x + 40, y + 160, T - 41.16, { size: 80, w: 800, col: WHITE, dur: .45 });
  const pts = [.2, .32, .28, .45, .5, .62, .58, .74, .82, .9], u = expo((T - OUT_IN - .4) / 1.4);
  const gx = x + 40, gy = y + h - 40, gw = w - 80, gh = 180;
  g.strokeStyle = '#163A55'; g.lineWidth = 2; for (let i = 0; i < 4; i++) { g.beginPath(); g.moveTo(gx, gy - i * gh / 3); g.lineTo(gx + gw, gy - i * gh / 3); g.stroke(); }
  g.strokeStyle = CYAN; g.lineWidth = 6; g.lineJoin = 'round'; g.beginPath();
  const n = (pts.length - 1) * u; for (let i = 0; i <= Math.ceil(n); i++) { const k = Math.min(i, n), a = Math.floor(k), f = k - a, v = lerp(pts[a], pts[Math.min(a + 1, pts.length - 1)], f);
    const X = gx + gw * k / (pts.length - 1), Y = gy - gh * v; i ? g.lineTo(X, Y) : g.moveTo(X, Y); } g.stroke();
  // area under the line + live cursor
  const ex = gx + gw * n / (pts.length - 1), a0 = Math.floor(n), ev = lerp(pts[a0], pts[Math.min(a0 + 1, pts.length - 1)], n - a0), ey = gy - gh * ev;
  g.save(); g.lineTo(ex, gy); g.lineTo(gx, gy); g.closePath(); const ag = g.createLinearGradient(0, gy - gh, 0, gy);
  ag.addColorStop(0, 'rgba(18,221,235,.35)'); ag.addColorStop(1, 'rgba(18,221,235,0)'); g.fillStyle = ag; g.fill(); g.restore();
  g.save(); g.shadowColor = CYAN; g.shadowBlur = 24; g.fillStyle = WHITE; g.beginPath(); g.arc(ex, ey, 12, 0, 7); g.fill(); g.restore();
  g.strokeStyle = 'rgba(18,221,235,.5)'; g.lineWidth = 2; g.setLineDash([6, 8]); g.beginPath(); g.moveTo(ex, ey); g.lineTo(ex, gy); g.stroke(); g.setLineDash([]);
}
// "More for the network": headline + a recap card stack, then the stack shatters into the end-card mosaic.
const MORE_STACK = [['Accuracy', 'improved', 43.3, true], ['Completeness', 'improved', 43.7], ['Outlook', 'clearer', 44.1]];
function moreCard(T) {
  if (T >= SHATTER) { okCard(T, MORE_IN, SHATTER, ''); return; }
  const p = expo((T - MORE_IN) / .4);
  g.save(); g.globalAlpha = p; card(40, 1080, 1000, 230, NAVY, 20, .35);
  typeOn('What came next', 80, 1150, T - MORE_IN - .1, { size: 26, col: GREY, track: 5, upper: true, cps: 40 });
  rise('More for the network.', 80, 1260, T - 44.4, { size: 92, w: 800, col: WHITE, dur: .45 });
  g.restore();
  cardStack(T, MORE_STACK, 60, 1340, 960, 110, 14);
}

// Hook: per-letter BUSES drop behind the head, then a speech bubble poses the question.
function sceneHook(T) {
  th(FULL, BZ + T * .01);
  typeOn('Case study · our favourite build', 44, 140, T - .1, { size: 30, track: 2, w: 500, cps: 26 });
  letterDrop('BUSES', 30, 470, T - .2, { size: 300, stagger: .07, exitAt: 2.15, T });
  cutout(BZ + T * .01);
  cluster(21, 960, 860, 6, 130, 90, T - .3, { from: [420, -120], exitAt: 2.2, T, to: [500, -200] });   // v3: off the ear line, to the shoulder
  bubble(T, 2.3, 4.45, 'Which build am I secretly fond of?', 540, 150, { size: 44 });
  captions(T);
}
// Rebuild: dark progress card races to 100%, then COOL pops letter by letter behind the head + burst.
function sceneBuild(T) {
  th(FULL, zoomAt(T));
  const p = expo((T - 28.0) / .45), q = expoIn((T - 30.25) / .25);
  if (p > 0 && q < 1) { const y = 1130 + (1 - p) * 500 + q * 600; card(60, y, 960, 260, NAVY, 20, .35);
    g.save(); g.translate(0, y - 120); progress(T, 28.4, 1.8, 110, 300, 860, 'Rebuild · quick turnaround'); g.restore(); }
  if (T >= 30.36) { letterPop('COOL', 40, 560, T - 30.36, { size: 330, stagger: .07 }); cutout(zoomAt(T)); }
  burst(T, 30.78, 540, 380, 26);
  captions(T);
}
