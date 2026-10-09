// ERD: entity relationship diagram (17 Oct clip, 13.4s). Blueprint drafting look, distinct from SQL.
const BP_IN = 1.5, STANDS_IN = 4.35, CARD_IN = 5.85, JOIN_IN = 10.62, END_MOS = 12.9, END_IN = END_MOS + .4;
const STANDS = [['E', 'ntity', 4.48], ['R', 'elationship', 4.76], ['D', 'iagram', 5.3]];
window.EP = {
  dur: 16.3, voEnd: 13.0,
  punchIns: [],
  cuts: [BP_IN, STANDS_IN, CARD_IN, JOIN_IN, END_IN],
  captions: [[JOIN_IN, END_MOS, T => lerp(H + 40, PANEL_Y, expo((T - JOIN_IN) / .5)) - 60]],
  frame(T) {
    if (T < BP_IN) titleCard(T, 'ERD', 1.25);
    else if (T < STANDS_IN) sceneBlueprint(T, false);
    else if (T < CARD_IN) standsFor(T, STANDS_IN, CARD_IN, 'ERD', STANDS);
    else if (T < JOIN_IN) sceneBlueprint(T, true);
    else if (T < END_IN) sceneJoin(T);
    else endCard(T, END_IN, this.dur);
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('ERD', 1.25); iris.cue(BP_IN - .45); cue(2.04, 'typing', { n: 10, cps: 14, gain: .2 }); cue(3.5, 'pop', { f: 900, gain: .2 });
    standsFor.cue(STANDS_IN, CARD_IN, 'ERD', STANDS);
    cue(CARD_IN, 'whoosh', { d: .4, gain: .3 }); cue(7.12, 'pop', { f: 900, gain: .2 }); cue(8.52, 'thud', { f: 70, d: .25, gain: .3 }); cue(9.54, 'thud', { f: 55, d: .25, gain: .3 });
    cue(JOIN_IN - .1, 'whoosh', { d: .45, gain: .35 }); lowerThird.cue(10.6); cue(12.18, 'thud', { f: 60, d: .35, gain: .4 }); cue(12.4, 'chime', { f: 1175, gain: .1 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};
const BP = '#0B3A66', LINE = 'rgba(255,255,255,.9)';
function grid() { g.fillStyle = BP; g.fillRect(0, 0, W, H); g.strokeStyle = 'rgba(255,255,255,.08)'; g.lineWidth = 1;
  for (let x = 0; x < W; x += 40) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); } for (let y = 0; y < H; y += 40) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
  g.strokeStyle = 'rgba(255,255,255,.16)'; for (let x = 0; x < W; x += 200) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); } for (let y = 0; y < H; y += 200) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); } }
// Draw a rectangle outline progressively (drafting pen), p in 0..1.
function trace(x, y, w, h, p) { const L = 2 * (w + h); let d = L * clamp(p); g.beginPath(); g.moveTo(x, y);
  const seg = [[w, 0], [0, h], [-w, 0], [0, -h]]; let cx = x, cy = y; for (const [dx, dy] of seg) { const len = Math.abs(dx + dy), k = Math.min(1, d / len); cx += dx * k; cy += dy * k; g.lineTo(cx, cy); d -= len; if (d <= 0) break; } g.stroke(); }
function table(x, y, name, fields, p, w = 470) { if (p <= 0) return; const h = 110 + fields.length * 74; g.strokeStyle = LINE; g.lineWidth = 4; trace(x, y, w, h, p);
  if (p > .6) { const q = clamp((p - .6) / .4); g.globalAlpha = q; g.beginPath(); g.moveTo(x, y + 100); g.lineTo(x + w, y + 100); g.stroke();
    font(800, 66, COND); g.fillStyle = WHITE; g.fillText(name, x + 30, y + 72); font(500, 40, MONO); fields.forEach((f, i) => { g.fillStyle = i === 0 ? CYAN : 'rgba(255,255,255,.85)'; g.fillText(f, x + 30, y + 162 + i * 74); }); g.globalAlpha = 1; }
  return h; }
// Vertical crow's-foot connector: ONE tick at the top, MANY foot at the bottom.
function crowV(x, y1, y2, p, oneOn, manyOn) {
  const y = lerp(y1, y2, clamp(p)); g.strokeStyle = CYAN; g.lineWidth = 6; g.lineCap = 'round'; g.beginPath(); g.moveTo(x, y1); g.lineTo(x, y); g.stroke();
  if (oneOn > 0) { g.globalAlpha = oneOn; g.beginPath(); g.moveTo(x - 26, y1 + 26); g.lineTo(x + 26, y1 + 26); g.stroke(); font(800, 44, COND); g.fillStyle = CYAN; g.fillText('ONE', x + 44, y1 + 40); g.globalAlpha = 1; }
  if (manyOn > 0) { g.globalAlpha = manyOn; g.beginPath(); g.moveTo(x, y2 - 36); g.lineTo(x - 30, y2); g.moveTo(x, y2 - 36); g.lineTo(x, y2); g.moveTo(x, y2 - 36); g.lineTo(x + 30, y2); g.stroke();
    font(800, 44, COND); g.fillStyle = CYAN; g.fillText('MANY', x + 44, y2 - 10); g.globalAlpha = 1; } }

function sceneBlueprint(T, cardMode) {
  grid();
  const U = { x: 70, y: 340 }, Hs = { x: 540, y: 960 };
  typeOn(cardMode ? 'Cardinality' : 'A diagram of a database', 70, 230, T - (cardMode ? 7.12 : 1.6), { size: 30, col: CYAN, track: 6, upper: true, cps: 36 });
  table(U.x, U.y, 'users', ['id', 'name'], cardMode ? 1 : expo((T - 1.68) / .8));
  table(Hs.x, Hs.y, 'houses', ['id', 'user_id', 'address'], cardMode ? 1 : expo((T - 2.68) / .8));
  // one continuous connector: down from users, across, down into houses
  const P = [[300, 600], [300, 800], [775, 800], [775, 960]], segL = [200, 475, 160], tot = 835;
  let d = tot * (cardMode ? 1 : expo((T - 3.4) / .6));
  const pulse = cardMode && T > 7.12 ? .5 + .5 * Math.sin((T - 7.12) * 7) : 0;
  if (d > 0) { g.save(); if (pulse) { g.shadowColor = CYAN; g.shadowBlur = 24 * pulse; } g.strokeStyle = CYAN; g.lineWidth = 6; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); g.moveTo(...P[0]);
    for (let k = 0; k < 3; k++) { const f = Math.min(1, d / segL[k]); g.lineTo(lerp(P[k][0], P[k + 1][0], f), lerp(P[k][1], P[k + 1][1], f)); d -= segL[k]; if (d <= 0) break; } g.stroke(); g.restore(); }
  // notation draws on "cardinality"; labels on "one" / "another"
  const nt = cardMode ? expo((T - 7.12) / .4) : 0;
  if (nt > 0) { g.save(); g.globalAlpha = nt; g.strokeStyle = CYAN; g.lineWidth = 6; g.beginPath(); g.moveTo(274, 630); g.lineTo(326, 630);
    g.moveTo(775, 924); g.lineTo(745, 960); g.moveTo(775, 924); g.lineTo(775, 960); g.moveTo(775, 924); g.lineTo(805, 960); g.stroke(); g.restore(); }
  if (cardMode) { font(800, 48, COND); g.fillStyle = CYAN; g.globalAlpha = expo((T - 8.52) / .3); g.fillText('ONE', 340, 650); g.globalAlpha = expo((T - 9.54) / .3); g.fillText('MANY', 820, 940); g.globalAlpha = 1; }
  // 1 → many: three house rows fill the lower band from "MANY"
  if (cardMode) for (let k = 0; k < 3; k++) { const q = back((T - 9.54 - k * .1) / .3); if (q <= 0) continue;
    g.save(); g.translate(300, 1360 + k * 120); g.scale(q, q); g.fillStyle = 'rgba(18,221,235,.18)'; g.strokeStyle = CYAN; g.lineWidth = 3; g.beginPath(); g.roundRect(-230, -46, 460, 92, 16); g.fill(); g.stroke();
    font(500, 32, MONO); g.fillStyle = WHITE; g.fillText(`house ${k + 1} → user 1`, -205, 12); g.restore(); }
  if (!cardMode) rise('The structure.', 70, 1640, T - 2.92, { size: 130, w: 800, col: WHITE, dur: .45 });
  else rise('How many own how many.', 70, 1760, T - 8.16, { size: 84, w: 800, col: WHITE, dur: .45 });
  faceCircle(930, 1300, 100, back((T - (cardMode ? CARD_IN : BP_IN) - .3) / .6));
}

// "How you might join those together": two tables slide into one row.
function sceneJoin(T) {
  th(FULL, BZ); const top = lerp(H + 40, PANEL_Y, expo((T - JOIN_IN) / .5)); panel(top); captions(T); const oy = top - PANEL_Y;
  const j = inOut((T - 11.5) / .7);
  lowerThird(T, 10.7, 12.7, 'Sam Bruhn', 'Founder & CEO', 890);
  [['users', 'Sam', BLUE], ['houses', '12 Beach Rd', NAVY]].forEach(([n, v, col], i) => { const x = lerp(i ? 790 : 290, i ? 660 : 420, j);
    g.save(); g.translate(x, 1500 + oy); g.scale(1.4, 1.4); card(-190, -80, 380, 160, col, 20, .2); font(500, 22, MONO); g.fillStyle = WHITE; g.fillText(n.toUpperCase(), -160, -32);
    font(700, 46, COND); g.fillStyle = WHITE; g.fillText(v, -160, 34); g.restore(); });
  if (T > 12.18) { const q = back((T - 12.18) / .35); g.save(); g.translate(540, 1300 + oy); g.scale(q, q); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-110, -40, 220, 80, 40); g.fill();
    font(800, 50, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('JOIN', 0, 18); g.textAlign = 'left'; g.restore(); }
}
