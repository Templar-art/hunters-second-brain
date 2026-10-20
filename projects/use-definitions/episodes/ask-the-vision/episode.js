// Q&A: "What do I wish more prospects asked me earlier?" (21 Oct clip, 38.1s).
const ASK_IN = 4.4, SCOPE_IN = 9.55, LOST_IN = 14.1, MATCH_IN = 24.5, LOCK_IN = 34.0, END_MOS = 37.8, END_IN = END_MOS + .4;
window.EP = {
  dur: 41.2, voEnd: 37.9,
  punchIns: [[6.8, 9.55]],
  cuts: [ASK_IN, SCOPE_IN, LOST_IN, MATCH_IN, LOCK_IN, END_IN],
  // v2 (redo pass): deliberate transitions the QC continuity check should ignore (hard cuts get ±0.3 s)
  qcAllow: [[0, 0.6], [4.1, 4.8], [6.6, 7.0], [9.1, 10.0], [13.8, 14.5], [24.2, 24.9], [33.7, 34.4], [37.5, 38.6]],
  captions: [[ASK_IN, SCOPE_IN, 1130], [LOCK_IN, END_MOS, 1240]],
  frame(T) {
    if (T < ASK_IN) qOpener(T, 0, ASK_IN, '', ['What do I wish', 'more prospects', 'asked me earlier?']);
    else if (T < SCOPE_IN) sceneAsk(T);
    else if (T < LOST_IN) sceneScope(T);
    else if (T < MATCH_IN) sceneLost(T);
    else if (T < LOCK_IN) sceneMatch(T);
    else if (T < END_IN) sceneLock(T);
    else endCard(T, END_IN, this.dur, 'Q&A', true);   // v2: alive end card
    mosaic(T, END_MOS, 9);
  },
  cues() {
    qOpener.cue(0, ASK_IN); lowerThird.cue(4.5); cue(5.6, 'pop', { f: 800, gain: .22 }); cue(8.22, 'pop', { f: 1000, gain: .22 });
    iris.cue(SCOPE_IN - .45); for (let i = 0; i < 9; i++) cue(10.2 + i * .35, 'pop', { f: 700 + i * 60, d: .05, gain: .12 });
    cue(LOST_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(15.08, 'whoosh', { d: .6, bright: .3, gain: .25 }); cue(22.56, 'typing', { n: 10, cps: 20 });
    cue(MATCH_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(28.94, 'thud', { f: 60, d: .35, gain: .4 }); cue(29.3, 'chime', { f: 1175, gain: .12 });
    cue(LOCK_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(35.4, 'thud', { f: 90, d: .2, gain: .3 }); cue(36.94, 'chime', { f: 1318, gain: .12 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};
function qBubble(txt, x, y, p, dark) { if (p <= 0) return; g.save(); g.translate(x, y); g.scale(p, p); font(700, 52, COND); const w = g.measureText(txt).width + 70;
  g.shadowColor = 'rgba(0,0,0,.25)'; g.shadowBlur = 24; g.fillStyle = dark ? NAVY : WHITE; g.beginPath(); g.roundRect(-w / 2, -50, w, 100, 50); g.fill(); g.shadowColor = 'transparent';
  g.fillStyle = dark ? CYAN : INK; g.textAlign = 'center'; g.fillText(txt, 0, 18); g.textAlign = 'left'; g.restore(); }

// The questions he wishes he got: two bubbles under the chin.
function sceneAsk(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 4.5, 5.5); captions(T);
  qBubble('How will it look?', 540, 1360, back((T - 5.6) / .4), false);
  qBubble('How will it work, end to end?', 540, 1500, back((T - 8.22) / .4), true);
}
// Scoping: a board fills up with sticky notes ("a lot of things to consider").
const NOTES = ['Users', 'Roles', 'Reports', 'Billing', 'Edge cases', 'Imports', 'Alerts', 'Mobile', 'Approvals'];
function sceneScope(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Scoping', 60, 240, T - SCOPE_IN - .1, { size: 30, col: BLUE, track: 6, upper: true, cps: 30 });
  card(60, 300, 960, 1150, WHITE, 26, .1);
  NOTES.forEach((n, i) => { const q = back((T - 10.2 - i * .35) / .35); if (q <= 0) return; const r = rng(i + 3), x = 120 + (i % 3) * 300 + r() * 30, y = 360 + Math.floor(i / 3) * 340 + r() * 30;
    g.save(); g.translate(x + 120, y + 120); g.rotate((r() - .5) * .14); g.scale(q, q); g.fillStyle = ['#FFE7A3', '#BDEFF5', '#D9CCFF'][i % 3];
    g.shadowColor = 'rgba(0,0,0,.12)'; g.shadowBlur = 16; g.shadowOffsetY = 8; g.fillRect(-120, -120, 240, 240); g.shadowColor = 'transparent';
    font(700, 44, COND); g.fillStyle = INK; g.textAlign = 'center'; g.fillText(n, 0, 14); g.textAlign = 'left'; g.restore(); });
  rise('A lot to consider.', 54, 1640, T - 13.4, { size: 120, w: 800, col: INK, dur: .45 });
  faceCircle(910, 1790, 100, back((T - SCOPE_IN - .3) / .6));
}
// Nuance lost: a rich "vision in your head" flows into a plain list and loses its detail.
function sceneLost(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('The vision in your head', 70, 240, T - LOST_IN - .1, { size: 28, col: CYAN, track: 5, upper: true, cps: 36 });
  // thought cloud with rich shapes
  const cp = back((T - 14.4) / .5); if (cp > 0) { g.save(); g.translate(540, 640 + Math.sin(T * 1.8) * 12); g.scale(cp * (1 + Math.sin(T * 2.2) * .025), cp * (1 + Math.sin(T * 2.2) * .025)); g.fillStyle = '#0E3148';   // v2: the vision breathes (old render: still 15.4–24.5 s)
    [[0, 0, 300], [-220, 40, 180], [220, 40, 180], [-120, -120, 170], [130, -120, 170]].forEach(([x, y, r]) => { g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); });
    const r = rng(5); for (let k = 0; k < 18; k++) { const ph = r() * 6.28, x = (r() - .5) * 520 + Math.sin(T * 1.6 + ph) * 34, y = (r() - .5) * 300 + Math.cos(T * 1.3 + ph) * 24, s = 24 + r() * 40, a = T * (r() - .5) * 2;
      g.save(); g.translate(x, y); g.rotate(a); g.fillStyle = TRI[k % 5]; g.globalAlpha = .9; k % 3 ? g.fillRect(-s / 2, -s / 2, s, s) : (g.beginPath(), g.arc(0, 0, s / 2, 0, 7), g.fill()); g.restore(); } g.restore(); }
  // the flow down to the page, shedding detail
  if (T > 15.08) { const r = rng(9); for (let k = 0; k < 18; k++) { const t = ((T - 15.08) * .7 + r()) % 1, x = 540 + (r() - .5) * 420, y = lerp(860, 1330, t), sz = 30 * (1 - t * .6);   // v2: detail falls into the page and loses its colour
    g.globalAlpha = 1 - t * .7; g.fillStyle = t > .55 ? '#7F8C99' : TRI[k % 5]; g.fillRect(x - sz / 2, y, sz, sz); } g.globalAlpha = 1;
    pillPlain('NUANCE GETS LOST', 540, 1000, back((T - 15.08) / .35)); }
  // the plain page list
  const lp = back((T - 18.5) / .45); if (lp > 0) { g.save(); g.translate(540, 1440); g.scale(lp, lp); g.translate(-540, -1440); card(180, 1180, 720, 520, WHITE, 16, .3);
    font(800, 52, COND); g.fillStyle = INK; g.fillText('Requirements', 220, 1260);
    for (let k = 0; k < 5; k++) { const q = expo((T - 22.56 - k * .18) / .3); g.fillStyle = '#C9CDD2'; g.beginPath(); g.arc(240, 1330 + k * 70, 8, 0, 7); g.fill(); g.fillRect(270, 1322 + k * 70, 520 * q * (1 - k * .08), 16); }
    g.restore(); }
  faceCircle(955, 1805, 90, back((T - LOST_IN - .3) / .6));   // v2: clear of the requirements page corner
}
function pillPlain(txt, x, y, p) { if (p <= 0) return; g.save(); g.translate(x, y); g.scale(p, p); font(500, 26, MONO); g.letterSpacing = '3px'; const w = g.measureText(txt).width + 40;
  g.fillStyle = '#F5A524'; g.beginPath(); g.roundRect(-w / 2, -34, w, 68, 34); g.fill(); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(txt, 0, 9); g.textAlign = 'left'; g.letterSpacing = '0px'; g.restore(); }
// Do our visions match? Two circles slide together until they overlap.
function sceneMatch(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Ask me early', 60, 240, T - 24.6, { size: 30, col: BLUE, track: 6, upper: true, cps: 30 });
  const k = inOut((T - 26.6) / 2.2), y = 860;
  [['My head', 27.8, BLUE, -1], ['Your head', 30.12, CYAN, 1]].forEach(([lab, at, col, side]) => { const q = back((T - (side < 0 ? 25.3 : 26.8)) / .45); if (q <= 0) return;
    const x = 540 + side * lerp(260, 120, k), br = side < 0 ? 1 + Math.sin((T - 25.3) * 3.2) * .04 * (1 - k) : 1; g.save(); g.translate(x, y); g.scale(q * br, q * br);   /* v2: my head pulses while it waits */ g.globalAlpha = .85; g.fillStyle = col; g.beginPath(); g.arc(0, 0, 260, 0, 7); g.fill(); g.globalAlpha = 1;
    font(800, 56, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(lab, side * 110, 18); g.textAlign = 'left'; g.restore(); });
  // v2: thoughts stream from your head into mine (old render: still 25.8–34 s)
  if (T > 25.5 && T < 27.2) { const a = clamp((T - 25.5) / .3) * (1 - clamp((T - 26.8) / .3)); g.save(); g.globalAlpha = a; g.translate(800, y); g.rotate((T - 25.5) * 1.2); g.setLineDash([22, 16]); g.strokeStyle = CYAN; g.lineWidth = 6; g.beginPath(); g.arc(0, 0, 260, 0, 7); g.stroke(); g.restore(); }   // the empty slot your head will fill
  if (T > 25.6) { const r = rng(4); for (let n = 0; n < 18; n++) { const t = ((T - 25.6) * .8 + r()) % 1, lane = (r() - .5) * 300, src = T > 26.8 ? 540 + lerp(260, 120, k) : 540 - lerp(260, 120, k), dst = 540 - lerp(260, 120, k);
    const x = T > 26.8 ? lerp(src + 160, dst - 160, t) : src + Math.cos(r() * 6.28) * (280 + t * 260), yy = T > 26.8 ? y + lane * Math.sin(t * Math.PI) * .6 + lane * .3 : y + Math.sin(r() * 6.28) * (280 + t * 260);
    g.globalAlpha = Math.sin(t * Math.PI); g.fillStyle = n % 2 ? BLUE : '#C3A6FF'; g.beginPath(); g.arc(x, yy, 16, 0, 7); g.fill(); } g.globalAlpha = 1; }
  if (T > 29.3) for (let n = 0; n < 2; n++) { const t = ((T - 29.3) / 1.4 + n / 2) % 1; g.strokeStyle = `rgba(0,28,46,${.5 * (1 - t)})`; g.lineWidth = 5; g.beginPath(); g.arc(540, y, 80 + t * 220, 0, 7); g.stroke(); }
  if (T > 28.94) { const q = back((T - 28.94) / .4); g.save(); g.translate(540, y); g.scale(q, q); g.fillStyle = NAVY; g.beginPath(); g.arc(0, 0, 70, 0, 7); g.fill();
    font(800, 64, COND); g.fillStyle = CYAN; g.textAlign = 'center'; g.fillText('✓', 0, 22); g.textAlign = 'left'; g.restore(); }
  rise('Does it match?', 54, 1360, T - 28.94, { size: 140, w: 800, col: INK, dur: .45 });
  rise('Pull me into your space.', 54, 1520, T - 31.08, { size: 90, w: 800, col: BLUE, dur: .45 });
  faceCircle(910, 1780, 100, back((T - MATCH_IN - .3) / .6));
}
// "Sometimes it's hard to force your way in": lock card → "Ask early" prompt, under the chin.
function sceneLock(T) {
  th(FULL, BZ); captions(T);
  const p = back((T - 34.4) / .45); if (p <= 0) return; g.save(); g.translate(540, 1440); g.scale(p, p); card(-420, -140, 840, 280, NAVY, 30, .35);
  const open = expo((T - 36.94) / .4);
  g.strokeStyle = CYAN; g.lineWidth = 10; g.beginPath(); g.arc(-300, -30 - open * 30, 40, Math.PI, 0); g.stroke(); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-350, -30, 100, 90, 12); g.fill();
  font(800, 66, COND); g.fillStyle = WHITE; g.fillText(open > .5 ? 'Ask early.' : 'Hard to see in.', -200, 0);
  font(500, 30, MONO); g.letterSpacing = '3px'; g.fillStyle = '#9FB3C4'; g.fillText(open > .5 ? 'SHOW US YOUR VISION' : 'THEIR VISION', -200, 66); g.letterSpacing = '0px'; g.restore();
}
