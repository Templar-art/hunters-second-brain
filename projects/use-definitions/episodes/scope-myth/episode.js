// Q&A: "What do people presume about software shops that isn't true?" (19 Oct clip, 35.6s).
const MYTH_IN = 4.9, SCOPE_IN = 13.4, LOVE_IN = 23.2, TRUTH_IN = 28.7, END_MOS = 35.9, END_IN = END_MOS + .4;
window.EP = {
  dur: 39.3, voEnd: 36.0,
  punchIns: [[9.0, 13.4], [26.0, 28.7]],
  cuts: [MYTH_IN, SCOPE_IN, LOVE_IN, TRUTH_IN, END_IN],
  captions: [[MYTH_IN, SCOPE_IN, 1240], [LOVE_IN, TRUTH_IN, 1240], [TRUTH_IN, END_MOS, T => lerp(H + 40, PANEL_Y, expo((T - TRUTH_IN) / .6)) - 60]],
  frame(T) {
    if (T < MYTH_IN) qOpener(T, 0, MYTH_IN, '', ['What do people wrongly', 'assume about', 'software shops?']);
    else if (T < SCOPE_IN) sceneMyth(T);
    else if (T < LOVE_IN) sceneScope(T);
    else if (T < TRUTH_IN) sceneOver(T);
    else if (T < END_IN) sceneTruth(T);
    else endCard(T, END_IN, this.dur, 'Q&A');
    mosaic(T, END_MOS, 9);
  },
  cues() {
    qOpener.cue(0, MYTH_IN); cue(MYTH_IN, 'whoosh', { d: .4, gain: .3 }); lowerThird.cue(5.0);
    cue(7.92, 'thud', { f: 60, d: .35, gain: .4 }); INV.forEach(([, at]) => cue(at, 'click', { f: 1300, gain: .2 })); cue(12.74, 'thud', { f: 45, d: .4, gain: .45 });
    iris.cue(SCOPE_IN - .45); cue(15.58, 'chime', { f: 988, gain: .1 }); EXTRA.forEach(([, at]) => { cue(at - .1, 'whoosh', { d: .3, bright: .5, gain: .22 }); cue(at + .2, 'pop', { f: 1000, gain: .18 }); });
    cue(LOVE_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(28.36, 'riser', { d: .4, gain: .14 }); burst.cue(28.5);
    cue(TRUTH_IN - .1, 'whoosh', { d: .5, gain: .4 }); cue(32.76, 'thud', { f: 80, d: .25, gain: .3 }); cue(35.36, 'chime', { f: 1318, gain: .12 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};
function stamp(txt, x, y, at, T, col = '#F5A524', rot = -.12, size = 70) { const q = back((T - at) / .3); if (q <= 0) return;
  g.save(); g.translate(x, y); g.rotate(rot); g.scale(q * (2 - q), q * (2 - q)); font(800, size, COND); const w = g.measureText(txt).width + 60;
  g.fillStyle = '#F3F3F3'; g.beginPath(); g.roundRect(-w / 2, -size * .75, w, size * 1.4, 12); g.fill(); g.strokeStyle = col; g.lineWidth = 8; g.stroke();
  g.fillStyle = col; g.textAlign = 'center'; g.fillText(txt, 0, size * .32); g.textAlign = 'left'; g.restore(); }

// The myth: an invoice that keeps growing with "scope extension" lines.
const INV = [['+ scope extension', 11.02], ['+ scope extension', 11.46], ['+ scope extension', 12.04], ['+ scope extension', 12.6]];
function sceneMyth(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 5.0, 7.0); captions(T);
  const p = expo((T - 7.6) / .5); if (p <= 0) return;
  const rows = INV.filter(([, at]) => T > at).length, h = 200 + rows * 70;
  g.save(); g.globalAlpha = p; card(120, 1320, 840, h, WHITE, 18, .3);
  font(500, 24, MONO); g.letterSpacing = '4px'; g.fillStyle = GREY; g.fillText('INVOICE', 160, 1380); g.letterSpacing = '0px';
  font(600, 36, BODY); g.fillStyle = INK; g.fillText('Agreed project', 160, 1450); g.textAlign = 'right'; g.fillText('$', 920, 1450); g.textAlign = 'left';
  INV.forEach(([lab, at], i) => { const q = expo((T - at) / .25); if (q <= 0) return; g.globalAlpha = q; font(600, 34, BODY); g.fillStyle = '#B54708'; g.fillText(lab, 160, 1520 + i * 70); g.textAlign = 'right'; g.fillText('$$', 920, 1520 + i * 70); g.textAlign = 'left'; });
  g.restore();
  stamp('MYTH', 820, 1290, 12.74, T);
}

// Scopes keep it manageable; then the extensions he says yes to fly in and get packed.
const EXTRA = [['Extra report', 20.12], ['New button', 20.92], ['One more page', 21.56], ['Bonus export', 22.38]];
function sceneScope(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn(T < 18.36 ? 'We set scopes' : 'If it’s up to me', 60, 250, T - (T < 18.36 ? 13.4 : 18.4), { size: 30, col: BLUE, track: 6, upper: true, cps: 32 });
  const bp = expo((T - 13.45) / .5); g.save(); g.setLineDash([16, 12]); g.lineDashOffset = -T * 30; g.strokeStyle = BLUE; g.lineWidth = 5; g.globalAlpha = bp;
  g.beginPath(); g.roundRect(80, 360, 920, 920, 30); g.stroke(); g.restore(); g.setLineDash([]);
  if (bp > .5) { font(500, 24, MONO); g.letterSpacing = '4px'; g.fillStyle = BLUE; g.fillText('SCOPE', 110, 400); g.letterSpacing = '0px'; }
  const CORE = ['Login', 'Dashboard', 'Reports', 'Admin'];
  CORE.forEach((c, i) => { const q = back((T - 14.4 - i * .15) / .4); if (q <= 0) return; const x = 140 + (i % 2) * 430, y = 450 + Math.floor(i / 2) * 200;
    g.save(); g.translate(x + 190, y + 80); g.scale(q, q); card(-190, -80, 380, 160, NAVY, 20, .2); font(700, 54, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(c, 0, 18); g.textAlign = 'left'; g.restore(); });
  if (T > 15.58 && T < 18.36) { const q = back((T - 15.58) / .35); g.save(); g.translate(540, 1150); g.scale(q, q); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-220, -44, 440, 88, 44); g.fill();
    font(800, 54, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('Manageable ✓', 0, 18); g.textAlign = 'left'; g.restore(); }
  EXTRA.forEach(([c, at], i) => { const k = expo(clamp((T - at) / .5)); if (T < at) return; const tx = 140 + (i % 2) * 430, ty = 870 + Math.floor(i / 2) * 170;
    const x = lerp(i % 2 ? 1300 : -500, tx, k), y = lerp(ty - 300, ty, k);
    g.save(); g.translate(x + 190, y + 70); g.rotate((1 - k) * (i % 2 ? .4 : -.4)); card(-190, -70, 380, 140, CYAN, 20, .2);
    font(700, 46, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText(c, 0, 16); g.textAlign = 'left'; g.restore();
    if (k > .9) stamp('YES', tx + 340, ty + 10, at + .45, T, '#1F9D55', .15, 40); });
  rise(T < 18.36 ? 'Something manageable.' : 'Pack it all in.', 54, 1600, T - (T < 18.36 ? 15.58 : 22.38), { size: 110, w: 800, col: INK, dur: .45 });
  faceCircle(910, 1780, 100, back((T - SCOPE_IN - .3) / .6));
}

// "Feels good to over-deliver": a delivery bar that overflows past 100%.
function sceneOver(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = expo((T - 24.3) / .45); if (p <= 0) return;
  g.save(); g.globalAlpha = p; card(60, 1340, 960, 300, NAVY, 26, .35);
  font(500, 24, MONO); g.letterSpacing = '4px'; g.fillStyle = GREY; g.fillText('DELIVERED', 100, 1400); g.letterSpacing = '0px';
  const fill = clamp((T - 24.5) / 3.8) * 1.18, bx = 100, bw = 880;
  g.fillStyle = '#163A55'; g.beginPath(); g.roundRect(bx, 1450, bw, 50, 25); g.fill();
  const gr = g.createLinearGradient(bx, 0, bx + bw, 0); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN); g.fillStyle = gr; g.beginPath(); g.roundRect(bx, 1450, Math.min(bw, bw * fill), 50, 25); g.fill();
  if (fill > 1) { g.fillStyle = '#28C941'; g.beginPath(); g.roundRect(bx + bw - 30, 1450, 30 + (fill - 1) * bw, 50, 25); g.fill(); }
  g.strokeStyle = WHITE; g.lineWidth = 3; g.beginPath(); g.moveTo(bx + bw * .85, 1430); g.lineTo(bx + bw * .85, 1520); g.stroke(); font(500, 22, MONO); g.fillStyle = WHITE; g.fillText('PROMISED', bx + bw * .85 - 60, 1555);
  g.restore();
  if (T > 28.36) { const q = back((T - 28.36) / .35); g.save(); g.translate(800, 1290); g.scale(q, q); g.fillStyle = '#28C941'; g.beginPath(); g.roundRect(-190, -40, 380, 80, 40); g.fill();
    font(800, 48, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('Over-delivered', 0, 16); g.textAlign = 'left'; g.restore(); }
  burst(T, 28.5, 960, 1475, 18, 6);
}

// Myth vs reality, on a panel under the head.
function sceneTruth(T) {
  th(FULL, BZ); const top = lerp(H + 40, PANEL_Y, expo((T - TRUTH_IN) / .6)); panel(top); captions(T); const oy = top - PANEL_Y;
  const a = expo((T - 29.6) / .4); if (a > 0) { g.save(); g.globalAlpha = a; font(500, 24, MONO); g.letterSpacing = '4px'; g.fillStyle = '#B54708'; g.fillText('THE MYTH', 80, 1340 + oy); g.letterSpacing = '0px';
    font(800, 66, COND); g.fillStyle = INK; g.fillText('“In it for the money.”', 80, 1420 + oy);
    if (T > 32.76) { g.fillStyle = '#F5A524'; g.fillRect(76, 1396 + oy, (g.measureText('“In it for the money.”').width + 8) * expo((T - 32.76) / .35), 9); } g.restore(); }
  const r = expo((T - 33.64) / .45); if (r > 0) { g.save(); g.globalAlpha = r; font(500, 24, MONO); g.letterSpacing = '4px'; g.fillStyle = BLUE; g.fillText('THE REALITY', 80, 1520 + oy); g.letterSpacing = '0px';
    font(800, 66, COND); g.fillStyle = INK; g.fillText('We love making', 80, 1600 + oy); g.fillStyle = BLUE; g.fillText('really cool software.', 80, 1672 + oy); g.restore(); }
  if (T > 35.36) burst(T, 35.36, 700, 1640 + oy, 18, 2);
}
