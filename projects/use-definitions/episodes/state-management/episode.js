// State management (15 Oct clip, 25s).
const LT_IN = 1.3, STORE_IN = 2.6, PAGES_IN = 7.9, PERSIST_IN = 15.4, REQ_IN = 20.8, END_MOS = 24.9, END_IN = END_MOS + .4;
window.EP = {
  dur: 28.3, voEnd: 25.0,
  punchIns: [],
  cuts: [LT_IN, STORE_IN, PAGES_IN, PERSIST_IN, REQ_IN, END_IN],
  captions: [[LT_IN, STORE_IN, 1040], [PERSIST_IN, REQ_IN, T => lerp(H + 40, PANEL_Y - 120, expo((T - PERSIST_IN) / .6)) - 60]],
  frame(T) {
    if (T < LT_IN) titleCard(T, 'STATE', 1.1);
    else if (T < STORE_IN) { th(FULL, BZ); lowerThird(T, 1.4, 2.45); captions(T); }
    else if (T < PAGES_IN) sceneStore(T);
    else if (T < PERSIST_IN) scenePages(T);
    else if (T < REQ_IN) scenePersist(T);
    else if (T < END_IN) sceneRequests(T);
    else endCard(T, END_IN, this.dur);
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('STATE', 1.1); lowerThird.cue(1.4); cue(STORE_IN, 'whoosh', { d: .4, gain: .3 });
    VARS.forEach((v, i) => cue(STORE_IN + i * .1, 'pop', { f: 700 + i * 80, d: .05, gain: .14 })); cue(4.74, 'whoosh', { d: .4, bright: .5, gain: .3 }); cue(5.04, 'chime', { f: 988, gain: .1 });
    whip.cue(PAGES_IN - .2); PAGES.forEach(([, at]) => cue(at, 'click', { gain: .3 })); cue(12.9, 'thud', { f: 90, d: .2, gain: .25 });
    cue(PERSIST_IN - .1, 'whoosh', { d: .5, gain: .4 }); cue(17.96, 'pop', { f: 900, gain: .2 }); cue(18.74, 'pop', { f: 1050, gain: .2 });
    zoomThrough.cue(REQ_IN - .3); cue(22.22, 'riser', { d: .5, gain: .12 }); cue(23.68, 'chime', { f: 1175, gain: .1 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};
const VARS = [['user', '"Sam"'], ['cart', '3'], ['theme', '"dark"'], ['page', '"/home"'], ['loggedIn', 'true']];
function chip(x, y, k, v, p, glow = 0) { if (p <= 0) return; font(500, 30, MONO); const w = g.measureText(`${k}: ${v}`).width + 44;
  g.save(); g.translate(x, y); g.scale(p, p); if (glow) { g.shadowColor = CYAN; g.shadowBlur = 20 * glow; }
  g.fillStyle = '#0E3148'; g.strokeStyle = glow ? CYAN : '#2B4A62'; g.lineWidth = 3; g.beginPath(); g.roundRect(-w / 2, -32, w, 64, 32); g.fill(); g.stroke();
  g.fillStyle = CYAN; g.fillText(k + ':', -w / 2 + 22, 10); g.fillStyle = WHITE; g.fillText(' ' + v, -w / 2 + 22 + g.measureText(k + ':').width, 10); g.restore(); }

// Variables scattered across the app snap into one store and stay consistent.
function sceneStore(T) {
  const wy = whip(T, PAGES_IN - .2); g.save(); g.translate(0, wy);
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('All the variables in your app', 70, 250, T - STORE_IN, { size: 28, col: CYAN, track: 5, upper: true, cps: 36 });
  const snap = inOut((T - 4.74) / .6), sp = back((T - 4.5) / .45);
  if (sp > 0) { g.save(); g.translate(540, 1060); g.scale(sp, sp); g.strokeStyle = CYAN; g.lineWidth = 6; g.fillStyle = '#082539';
    g.beginPath(); g.roundRect(-380, -330, 760, 660, 34); g.fill(); g.stroke(); font(500, 24, MONO); g.letterSpacing = '5px'; g.fillStyle = CYAN; g.fillText('STATE STORE', -340, -280); g.letterSpacing = '0px'; g.restore(); }
  const r = rng(3);
  VARS.forEach(([k, v], i) => { const sx = 150 + r() * 780, sy = 420 + r() * 1100, tx = 540, ty = 860 + i * 100;
    const x = lerp(sx, tx, snap) + Math.sin(T * 2 + i) * 14 * (1 - snap), y = lerp(sy, ty, snap) + Math.cos(T * 2 + i) * 14 * (1 - snap);
    chip(x, y, k, v, back((T - STORE_IN - i * .1) / .4), expo((T - 5.04 - i * .08) / .3)); });
  rise('Kept consistent.', 70, 1640, T - 5.04, { size: 130, w: 800, col: WHITE, dur: .45 });
  faceCircle(900, 1790, 100, back((T - STORE_IN - .3) / .6));
  g.restore();
}

// Moving between pages: each switch would re-fetch… but with state, the log entries aren't needed.
const PAGES = [['Home', 8.4], ['Profile', 8.92], ['Settings', 9.76]];
function scenePages(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Moving between pages', 60, 230, T - PAGES_IN - .1, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  let pi = 0; PAGES.forEach(([, at], i) => { if (T >= at) pi = i; });
  const bp = expo((T - PAGES_IN - .05) / .45); g.save(); g.globalAlpha = bp; card(60, 300, 960, 720, WHITE, 28, .12);
  g.fillStyle = '#E9EDF1'; g.beginPath(); g.roundRect(60, 300, 960, 80, [28, 28, 0, 0]); g.fill();
  PAGES.forEach(([lab, at], i) => { const on = i === pi; g.fillStyle = on ? WHITE : '#E9EDF1'; g.beginPath(); g.roundRect(90 + i * 230, 316, 210, 64, [14, 14, 0, 0]); g.fill();
    font(600, 30, BODY); g.fillStyle = on ? INK : GREY; g.fillText(lab, 120 + i * 230, 360); });
  const sl = T - PAGES[pi][1], off = (1 - expo(sl / .3)) * 300;
  g.save(); g.beginPath(); g.rect(60, 380, 960, 640); g.clip(); g.translate(off, 0);
  font(800, 90, COND); g.fillStyle = INK; g.fillText(PAGES[pi][0], 120, 520);
  for (let k = 0; k < 3; k++) { g.fillStyle = '#EEF1F4'; g.beginPath(); g.roundRect(120, 580 + k * 130, 840, 100, 18); g.fill();
    g.fillStyle = [CYAN, BLUE, '#C3A6FF'][(k + pi) % 3]; g.beginPath(); g.arc(180, 630 + k * 130, 28, 0, 7); g.fill(); }
  g.restore(); g.restore();
  // request log
  const lp = expo((T - 10.36) / .4); if (lp > 0) { g.save(); g.globalAlpha = lp; card(60, 1080, 960, 520, NAVY, 26, .3);
    font(500, 22, MONO); g.letterSpacing = '4px'; g.fillStyle = GREY; g.fillText('WITHOUT STATE, EVERY PAGE WOULD…', 100, 1140); g.letterSpacing = '0px';
    [['GET /api/user', 10.96], ['GET /api/cart', 11.96], ['GET /api/settings', 12.64], ['SELECT * FROM users', 13.8]].forEach(([req, at], i) => { const q = expo((T - at) / .3); if (q <= 0) return;
      const y = 1220 + i * 90; g.globalAlpha = q; font(500, 32, MONO); g.fillStyle = '#F5A524'; g.fillText('↻ ' + req, 100, y);
      if (T > 14.4) { g.fillStyle = CYAN; g.fillRect(96, y - 12, (g.measureText('↻ ' + req).width + 10) * expo((T - 14.4 - i * .08) / .3), 5); } });
    g.globalAlpha = 1; if (T > 14.1) { const q = back((T - 14.1) / .3); g.save(); g.translate(800, 1545); g.scale(q, q); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-190, -40, 380, 80, 40); g.fill();
      font(500, 40, MONO); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('NOT NEEDED ✓', 0, 14); g.textAlign = 'left'; g.restore(); } g.restore(); }
  faceCircle(920, 1760, 100, back((T - PAGES_IN - .3) / .6));
}

// Persistent store: a panel under the head holding users + items that survive page changes.
function scenePersist(T) {
  th(FULL, BZ); const top = lerp(H + 40, PANEL_Y - 120, expo((T - PERSIST_IN) / .6)); panel(top); captions(T); const oy = top - (PANEL_Y - 120);
  typeOn('Persistent state', 80, 1220 + oy, T - 16.0, { size: 26, col: BLUE, track: 6, upper: true, cps: 36 });
  const sh = expo((T - 16.0) / .45); if (sh > 0) { g.save(); g.globalAlpha = sh; g.setLineDash([14, 10]); g.lineDashOffset = -T * 30; g.strokeStyle = BLUE; g.lineWidth = 4;
    g.beginPath(); g.roundRect(40, 1260 + oy, 1000, 420, 30); g.stroke(); g.setLineDash([]); font(500, 22, MONO); g.fillStyle = BLUE; g.textAlign = 'right'; g.fillText('IN MEMORY', 1030, 1245 + oy); g.textAlign = 'left'; g.restore(); }
  const users = back((T - 17.96) / .4), items = back((T - 18.74) / .4);
  if (users > 0) { g.save(); g.translate(300, 1460 + oy); g.scale(users, users); card(-230, -170, 460, 340, WHITE, 24, .1);
    font(700, 44, COND); g.fillStyle = INK; g.fillText('Users', -190, -110); for (let k = 0; k < 4; k++) { g.fillStyle = [CYAN, BLUE, '#C3A6FF', '#7FD6FF'][k]; g.beginPath(); g.arc(-150 + k * 100, 0, 38, 0, 7); g.fill(); }
    font(500, 22, MONO); g.fillStyle = GREY; g.fillText('KEPT IN MEMORY', -190, 120); g.restore(); }
  if (items > 0) { g.save(); g.translate(780, 1460 + oy); g.scale(items, items); card(-230, -170, 460, 340, WHITE, 24, .1);
    font(700, 44, COND); g.fillStyle = INK; g.fillText('Items', -190, -110); for (let k = 0; k < 3; k++) { g.fillStyle = '#EEF1F4'; g.beginPath(); g.roundRect(-190, -60 + k * 64, 380, 48, 12); g.fill(); }
    font(500, 22, MONO); g.fillStyle = GREY; g.fillText('KEPT IN MEMORY', -190, 150); g.restore(); }
}

// "Without thousands of requests": a swarm of requests vs a calm few.
function sceneRequests(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('Just navigating around', 70, 250, T - REQ_IN - .1, { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  [['Without state', 520, 1.0, '#F5A524'], ['With state', 1040, .13, CYAN]].forEach(([lab, y, amt, col], row) => { const q = expo((T - 21.28 - row * .3) / .4); if (q <= 0) return;
    g.save(); g.globalAlpha = q; font(800, 64, COND); g.fillStyle = WHITE; g.fillText(lab, 80, y - 60);
    const n = row ? 4 : Math.round(160 * expo((T - 21.3) / 1.2)), r = rng(row + 7);
    for (let k = 0; k < n; k++) { const t = ((T - 21.3) * (row ? .5 : 1.2 + r()) + (row ? k / 4 : r())) % 1; g.fillStyle = col; g.beginPath(); g.arc(80 + t * 920, y + 40 + (row ? 0 : (r() - .5) * 220), row ? 16 : 7, 0, 7); g.fill(); }
    g.fillStyle = '#163A55'; g.beginPath(); g.roundRect(80, y + 200, 920, 36, 18); g.fill();
    g.fillStyle = col; g.beginPath(); g.roundRect(80, y + 200, Math.max(36, 920 * amt * expo((T - 21.6) / .8)), 36, 18); g.fill(); g.restore(); });
  if (T > 22.22) { font(500, 26, MONO); g.fillStyle = '#F5A524'; g.fillText('THOUSANDS OF REQUESTS', 80, 820); }
  if (T > 21.6) { font(500, 26, MONO); g.fillStyle = CYAN; g.fillText('A HANDFUL OF REQUESTS', 80, 1340); }
  rise('Way fewer requests.', 70, 1600, T - 20.94, { size: 110, w: 800, col: WHITE, dur: .45 });
  faceCircle(900, 1790, 100, back((T - REQ_IN - .3) / .6));
}
