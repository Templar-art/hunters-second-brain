// SaaS: software as a service (08 Oct clip, 24.7s).
const SPELL_IN = 1.8, STANDS_IN = 3.0, VALUE_IN = 5.0, BOX_IN = 9.4, MONTH_IN = 14.9, BULK_IN = 19.3, END_MOS = 24.2, END_IN = END_MOS + .4;
const STANDS = [['S', 'oftware', 3.3], ['a', 's', 3.6], ['a', '', 3.85], ['S', 'ervice', 4.1]];
window.EP = {
  dur: 27.6, voEnd: 24.3,
  punchIns: [[11.9, 14.9]],
  cuts: [SPELL_IN, STANDS_IN, VALUE_IN, BOX_IN, MONTH_IN, BULK_IN, END_IN],
  // v2 (redo pass): deliberate transitions the QC continuity check should ignore
  qcAllow: [[0, 0.6], [1.3, 2.3], [2.8, 4.4], [4.7, 5.6], [7.9, 8.6], [9.2, 9.7], [10.9, 11.5], [11.8, 12.0], [13.3, 13.6],
            [14.3, 15.6], [19.1, 19.7], [20.4, 22.2], [22.3, 22.6], [24.0, 25.2]],
  captions: [[SPELL_IN, STANDS_IN, 1070], [BOX_IN, MONTH_IN, 1050]],
  frame(T) {
    if (T < SPELL_IN) titleCard(T, 'SaaS', 1.55, 'Definitions', [985, 800]);   // v2: shards off the ear line
    else if (T < STANDS_IN) sceneSpell(T);
    else if (T < VALUE_IN) sceneStands(T);
    else if (T < BOX_IN) sceneValue(T);
    else if (T < MONTH_IN) sceneBox(T);
    else if (T < BULK_IN) sceneMonthly(T);
    else if (T < END_IN) sceneBulk(T);
    else endCard(T, END_IN, this.dur, 'Definitions', true);   // v2: alive end card
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('SaaS', 1.55);
    cue(SPELL_IN, 'whoosh', { d: .35, gain: .3 }); cue(1.44 + .5, 'chime', { f: 988, gain: .1 }); cue(2.08, 'thud', { f: 90, d: .2, gain: .3 });
    STANDS.forEach(([, , at], i) => cue(at, 'pop', { f: 600 + i * 90, d: .06, gain: .2 }));
    whip.cue(VALUE_IN - .2); cue(5.05, 'pop', { f: 700, gain: .2 }); lowerThird.cue(9.5); cue(8.04, 'riser', { d: .5, gain: .12 }); cue(8.5, 'chime', { f: 1175, gain: .1 });
    cue(11.0, 'whoosh', { d: .4, gain: .3 }); cue(11.24, 'thud', { f: 70, d: .3, gain: .3 }); cue(13.4, 'thud', { f: 50, d: .3, gain: .35 });
    iris.cue(MONTH_IN - .5); for (let i = 0; i < 12; i += 2) cue(15.42 + i * .2, 'click', { f: 1400 + i * 50, gain: .18 });
    cue(BULK_IN - .1, 'whoosh', { d: .45, gain: .35 }); for (let i = 0; i < 12; i += 3) cue(20.48 + i * .14, 'pop', { f: 800 + i * 40, d: .05, gain: .12 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};

// "Two A's, not two S's": spelling card on the chest, wrong spelling struck out.
function sceneSpell(T) {
  th(FULL, BZ); captions(T);
  const p = expo((T - SPELL_IN) / .4), x = 60, y = 1160 + (1 - p) * 400, w = 960, h = 420;
  card(x, y, w, h, WHITE, 24, .3);
  const L = ['S', 'a', 'a', 'S']; font(800, 200, COND);
  let cx = x + 70; L.forEach((ch, i) => { const q = back((T - 1.84 - i * .06) / .35), cw = g.measureText(ch).width; if (q > 0) {
    const hot = (i === 1 || i === 2) && T > 1.9; g.save(); g.translate(cx + cw / 2, y + 230); g.scale(q, q);
    if (hot) { g.fillStyle = CYAN; g.beginPath(); g.roundRect(-cw / 2 - 8, -150, cw + 16, 170, 14); g.fill(); }
    g.fillStyle = hot ? NAVY : INK; g.fillText(ch, -cw / 2, 0); g.restore(); } cx += cw + 6; });
  statusPill('TWO A’S ✓', x + 560, y + 120, expo((T - 1.95) / .3));
  const ps = expo((T - 2.08) / .3); if (ps > 0) { g.globalAlpha = ps; font(800, 90, COND); g.fillStyle = '#AEB4BA'; g.fillText('SASS', x + 560, y + 290);
    g.fillStyle = '#F5A524'; g.fillRect(x + 550, y + 255, 220 * expo((T - 2.2) / .3), 9); g.globalAlpha = 1; }
  typeOn('To be clear', x + 70, y + 360, T - 2.5, { size: 26, col: GREY, track: 5, upper: true, cps: 40 });
}
function statusPill(txt, x, y, p) {
  if (p <= 0) return; font(500, 26, MONO); g.letterSpacing = '2px'; const w = g.measureText(txt).width + 32;
  g.save(); g.globalAlpha *= clamp(p); g.fillStyle = CYAN; g.beginPath(); g.roundRect(x, y - 34, w, 48, 24); g.fill();
  g.fillStyle = NAVY; g.fillText(txt, x + 16, y); g.restore(); g.letterSpacing = '0px';
}
function sceneStands(T) {
  const wy = whip(T, VALUE_IN - .2); if (wy < 0) sceneValue(T);
  g.save(); g.translate(0, wy); standsFor(T, STANDS_IN, VALUE_IN + 1, 'SaaS', STANDS); g.restore();
}

// "Built software they think has a lot of value": product card assembles, value meter fills.
function sceneValue(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Someone builds software', 60, 300, T - 5.0, { size: 30, col: BLUE, track: 6, upper: true, cps: 32 });
  const p = back((T - 5.05) / .5), cx = 540, cy = 860 + Math.sin((T - VALUE_IN) * 2.0) * 12 * clamp((T - 5.6) / .5);   // v2: app card floats (old render: still 5.7–9.4 s)
  if (p > 0) { g.save(); g.translate(cx, cy); g.scale(p, p); card(-300, -300, 600, 600, WHITE, 40, .15);
    const gr = g.createLinearGradient(-200, -200, 200, 200); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN);
    g.fillStyle = gr; g.beginPath(); g.roundRect(-150, -210, 300, 300, 70); g.fill();
    font(800, 150, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('App', 0, -10);
    font(700, 56, COND); g.fillStyle = INK; g.fillText('Your product', 0, 190); g.textAlign = 'left'; g.restore(); }
  // value meter
  const vm = expo((T - 8.04) / 1.0);
  if (T > 7.6) { const y = 1300; typeOn('Value', 140, y - 30, T - 7.7, { size: 26, col: GREY, track: 5, upper: true, cps: 40 });
    g.fillStyle = '#E5E7EA'; g.beginPath(); g.roundRect(140, y, 800, 40, 20); g.fill();
    const gr = g.createLinearGradient(140, 0, 940, 0); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN);
    g.fillStyle = gr; g.beginPath(); g.roundRect(140, y, Math.max(40, 800 * vm * .92), 40, 20); g.fill(); }
  rise('A lot of value.', 54, 1560, T - 8.04, { size: 140, w: 800, col: INK, dur: .45 });
  faceCircle(910, 1760, 110, back((T - VALUE_IN - .2) / .6));
}

// "One-time licence … decades ago": retro boxed software under the head, price tag, 1998 stamp.
function sceneBox(T) {
  th(FULL, zoomAt(T)); captions(T); lowerThird(T, 9.5, 10.85);
  const p = expo((T - 11.0) / .5), cx = 540, cy = 1500 + (1 - p) * 600; if (T < 11.0) return;
  g.save(); g.globalAlpha = clamp(p * 1.5);
  // 3D box: front + side + top
  g.save(); g.translate(cx, cy); g.rotate(-.05);
  g.fillStyle = '#C9B48A'; g.beginPath(); g.moveTo(160, -200); g.lineTo(230, -250); g.lineTo(230, 170); g.lineTo(160, 220); g.fill();
  g.fillStyle = '#E3D2A8'; g.beginPath(); g.moveTo(-160, -200); g.lineTo(-90, -250); g.lineTo(230, -250); g.lineTo(160, -200); g.fill();
  g.fillStyle = '#F2E6C9'; g.fillRect(-160, -200, 320, 420);
  g.fillStyle = '#7A3E9D'; g.fillRect(-160, -200, 320, 120); font(800, 54, COND); g.fillStyle = '#FFE9A8'; g.fillText('SOFTWARE', -140, -125);
  font(700, 40, BODY); g.fillStyle = '#7A3E9D'; g.fillText('Deluxe Edition', -140, -30); font(500, 22, MONO); g.fillStyle = '#6B5A3A'; g.fillText('CD-ROM · WIN 98', -140, 20);
  g.fillStyle = '#B7A27A'; g.beginPath(); g.arc(0, 120, 60, 0, 7); g.fill(); g.fillStyle = '#F2E6C9'; g.beginPath(); g.arc(0, 120, 16, 0, 7); g.fill();
  g.restore();
  // price tag on "license"
  const tp = back((T - 11.24) / .4); if (tp > 0) { g.save(); g.translate(cx + 240, cy - 230); g.rotate(.18); g.scale(tp, tp);
    g.fillStyle = WHITE; g.beginPath(); g.roundRect(-10, -50, 280, 100, 14); g.fill(); g.strokeStyle = INK; g.lineWidth = 3; g.stroke();
    font(800, 52, COND); g.fillStyle = INK; g.fillText('$499', 20, 10); font(500, 18, MONO); g.fillStyle = GREY; g.fillText('ONE-TIME', 150, 2); g.fillText('LICENCE', 150, 26); g.restore(); }
  // 1998 stamp on "decades ago"
  const sp = back((T - 13.36) / .3); if (sp > 0) { g.save(); g.translate(cx - 230, cy + 120); g.rotate(-.22); g.scale(sp * (2 - sp), sp * (2 - sp));
    g.strokeStyle = '#F5A524'; g.lineWidth = 8; g.beginPath(); g.roundRect(-150, -60, 300, 120, 16); g.stroke();
    font(800, 90, COND); g.fillStyle = '#F5A524'; g.textAlign = 'center'; g.fillText('1998', 0, 32); g.textAlign = 'left'; g.restore(); }
  g.restore();
}

// "Pay monthly for access": month tiles light up in turn, recurring loop arrow, navy.
function sceneMonthly(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('Instead, you pay', 80, 300, T - MONTH_IN - .1, { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  rise('Monthly.', 70, 500, T - 15.42, { size: 200, w: 800, col: WHITE, dur: .45 });
  const M = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
  M.forEach((m, i) => { const x = 80 + (i % 4) * 235, y = 640 + Math.floor(i / 4) * 230, on = T > 15.42 + i * .2, q = back((T - 15.42 - i * .2) / .3);
    g.save(); g.translate(x + 105, y + 100); g.scale(on ? lerp(.9, 1, clamp(q)) : .9, on ? lerp(.9, 1, clamp(q)) : .9);
    g.fillStyle = on ? BLUE : '#0E3148'; g.beginPath(); g.roundRect(-105, -100, 210, 200, 22); g.fill();
    font(800, 80, COND); g.fillStyle = on ? WHITE : '#2B4A62'; g.textAlign = 'center'; g.fillText(m, 0, 10);
    if (on) { font(500, 22, MONO); g.fillStyle = CYAN; g.fillText('PAID ✓', 0, 60); } g.textAlign = 'left'; g.restore(); });
  // v2: once the year is paid, a 'this month' ring keeps stepping through the calendar (recurring, never dead)
  if (T > 17.75) { const k = Math.floor((T - 17.75) / .22) % 12, x = 80 + (k % 4) * 235, y = 640 + Math.floor(k / 4) * 230;
    g.save(); g.strokeStyle = CYAN; g.lineWidth = 7; g.shadowColor = CYAN; g.shadowBlur = 20; g.beginPath(); g.roundRect(x - 6, y - 6, 222, 212, 26); g.stroke(); g.restore(); }
  // recurring loop
  const lp = expo((T - 16.32) / .8); if (lp > 0) { g.save(); g.translate(540, 1500); g.rotate(T * 1.5); g.strokeStyle = CYAN; g.lineWidth = 10; g.lineCap = 'round';
    g.beginPath(); g.arc(0, 0, 90, 0, 5.5 * lp); g.stroke(); g.restore();
    font(500, 26, MONO); g.letterSpacing = '5px'; g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('ACCESS, EVERY MONTH', 540, 1670); g.textAlign = 'left'; g.letterSpacing = '0px'; }
  faceCircle(900, 1760, 110, back((T - MONTH_IN - .2) / .6));
}

// "Developing in bulk": one product fans out to many companies; cost-per-company bar shrinks.
function sceneBulk(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Built once, in bulk', 60, 260, T - BULK_IN - .1, { size: 30, col: BLUE, track: 6, upper: true, cps: 32 });
  const hx = 540, hy = 760, N = 12;
  let joined = 0;
  for (let i = 0; i < N; i++) { const at = 20.48 + i * .14, q = back((T - at) / .35); if (q <= 0) continue; joined++;
    const a = -Math.PI / 2 + (i / N) * 6.283, r = 340, x = hx + Math.cos(a) * r, y = hy + Math.sin(a) * r * .8;
    g.strokeStyle = '#C9CDD2'; g.lineWidth = 3; g.beginPath(); g.moveTo(hx, hy); g.lineTo(lerp(hx, x, clamp(q)), lerp(hy, y, clamp(q))); g.stroke();
    g.save(); g.translate(x, y); g.scale(q, q); g.fillStyle = WHITE; g.strokeStyle = BLUE; g.lineWidth = 3; g.beginPath(); g.roundRect(-46, -40, 92, 80, 14); g.fill(); g.stroke();
    g.fillStyle = INK; g.fillRect(-20, -14, 40, 34); g.fillStyle = WHITE; for (let k = 0; k < 3; k++) g.fillRect(-14 + k * 11, -6, 6, 6); g.restore(); }
  // v2: built once, shipped to all — update packets run out from the app along every spoke
  if (T > 22.1) for (let i = 0; i < N; i++) { const a = -Math.PI / 2 + (i / N) * 6.283, u = ((T - 22.1) / .8 + i * .37) % 1;
    g.fillStyle = BLUE; g.beginPath(); g.arc(hx + Math.cos(a) * 340 * u, hy + Math.sin(a) * 272 * u, 11, 0, 7); g.fill(); }
  const hp = back((T - BULK_IN) / .45); if (hp > 0) { g.save(); g.translate(hx, hy); g.scale(hp, hp);
    const gr = g.createLinearGradient(-90, -90, 90, 90); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN); g.fillStyle = gr;
    g.beginPath(); g.roundRect(-90, -90, 180, 180, 44); g.fill(); font(800, 64, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('App', 0, 22); g.textAlign = 'left'; g.restore(); }
  // cost per company shrinks as companies join
  const y = 1380; typeOn('Cost per company', 120, y - 30, T - 22.0, { size: 26, col: GREY, track: 5, upper: true, cps: 40 });
  if (T > 22.0) { g.fillStyle = '#E5E7EA'; g.beginPath(); g.roundRect(120, y, 840, 40, 20); g.fill();
    const share = 1 / Math.max(1, joined * .6), gr = g.createLinearGradient(120, 0, 960, 0); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN);
    g.fillStyle = gr; g.beginPath(); g.roundRect(120, y, Math.max(40, 840 * share), 40, 20); g.fill(); }
  rise('Cheaper for everyone.', 54, 1620, T - 22.4, { size: 110, w: 800, col: INK, dur: .45 });
  faceCircle(910, 1780, 100, back((T - BULK_IN - .3) / .6));
}
