// Q&A: "What do clients worry about that never actually happens?" (20 Oct clip, 19.9s).
const WORRY_IN = 1.95, DEAL_IN = 4.2, KEEP_IN = 12.7, END_MOS = 19.8, END_IN = END_MOS + .4;
window.EP = {
  dur: 23.2, voEnd: 19.9,
  punchIns: [[15.3, 17.6]],
  cuts: [WORRY_IN, DEAL_IN, KEEP_IN, END_IN],
  // v3 (redo pass): deliberate transitions the QC continuity check should ignore (hard cuts get ±0.3 s)
  qcAllow: [[0, 0.6], [1.6, 2.3], [3.7, 4.6], [12.4, 13.0], [15.1, 15.5], [17.4, 17.8], [18.6, 19.0], [19.5, 20.8]],
  captions: [[WORRY_IN, DEAL_IN, 1240], [KEEP_IN, END_MOS, 1240]],
  frame(T) {
    if (T < WORRY_IN) qOpener(T, 0, WORRY_IN + .9, '', ['What do clients worry', 'about that never', 'actually happens?']);
    else if (T < DEAL_IN) sceneWorry(T);
    else if (T < KEEP_IN) sceneDeal(T);
    else if (T < END_IN) sceneKeep(T);
    else endCard(T, END_IN, this.dur, 'Q&A', true);   // v3: alive end card
    mosaic(T, END_MOS, 9);
  },
  cues() {
    qOpener.cue(0, WORRY_IN + .9); lowerThird.cue(2.0); cue(2.7, 'pop', { f: 700, gain: .25 }); cue(3.92, 'thud', { f: 90, d: .2, gain: .3 });
    iris.cue(DEAL_IN - .45); cue(5.66, 'typing', { n: 10, cps: 30 }); SCEN.forEach(([, at]) => cue(at, 'pop', { f: 800, gain: .16 })); cue(8.36, 'whoosh', { d: .4, bright: .5, gain: .3 }); cue(8.8, 'chime', { f: 988, gain: .1 });
    cue(11.9, 'click', { gain: .3 }); cue(9.8, 'pop', { f: 1100, gain: .2 }); cue(KEEP_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(14.02, 'riser', { d: .5, gain: .12 }); cue(16.18, 'pop', { f: 900, gain: .2 }); cue(17.3, 'thud', { f: 90, d: .2, gain: .25 }); cue(19.02, 'thud', { f: 45, d: .5, gain: .5 }); cue(19.46, 'chime', { f: 1318, gain: .12 }); burst.cue(19.5);
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};
// The worry: a card under the chin asking "not delivering what we said?"
function sceneWorry(T) {
  th(FULL, BZ); lowerThird(T, 2.0, 2.65); captions(T);
  const p = back((T - 2.7) / .45); if (p <= 0) return; g.save(); g.translate(540, 1480); g.scale(p, p); card(-420, -130, 840, 260, WHITE, 30, .3);
  g.fillStyle = '#F5A524'; g.beginPath(); g.arc(-320, 0, 56, 0, 7); g.fill(); font(800, 70, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('?', -320, 25); g.textAlign = 'left';
  font(500, 22, MONO); g.letterSpacing = '4px'; g.fillStyle = GREY; g.fillText('THE WORRY', -230, -40); g.letterSpacing = '0px';
  font(700, 52, COND); g.fillStyle = INK; g.fillText('Not delivering', -230, 18); g.fillText('what was promised.', -230, 74); g.restore();
}
// The agreement: clauses type, worst-case scenarios pop, it gets signed.
const SCEN = [['If the deadline slips…', 6.76], ['If the scope changes…', 7.02], ['If something breaks…', 7.54]];
function sceneDeal(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Every commercial agreement', 60, 230, T - DEAL_IN - .1, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  const p = expo((T - DEAL_IN) / .5); g.save(); g.globalAlpha = p; g.translate(0, (1 - p) * 80); card(90, 300, 900, 1180, WHITE, 18, .15);
  font(800, 64, COND); g.fillStyle = INK; g.fillText('Agreement', 140, 400);
  for (let k = 0; k < 4; k++) { const q = expo((T - DEAL_IN - .1 - k * .15) / .35), lw = 800 * (k === 3 ? .6 : 1), hl = inOut((T - 4.9 - k * .45) / .5);
    if (hl > 0) { g.fillStyle = `rgba(18,221,235,${hl < 1 ? .6 : .25})`; g.fillRect(132, 444 + k * 46, (lw + 16) * hl, 28); }   // v3: a highlighter reads each clause (old render: still 5–6.8 s)
    g.fillStyle = '#E5E7EA'; g.fillRect(140, 450 + k * 46, lw * q, 16); }
  SCEN.forEach(([s, at], i) => { const q = back((T - at) / .35); if (q <= 0) return; const y = 720 + i * 120; g.save(); g.translate(140, y); g.scale(q, q);
    const pl = inOut((T - 10.3 - i * .45) / .5);   // v3: each worst case gets a plan, swept and ticked (old render: still 10.6–11.9 s)
    g.fillStyle = 'rgba(245,165,36,.15)'; g.beginPath(); g.roundRect(0, -46, 800, 92, 16); g.fill();
    if (pl > 0) { g.fillStyle = 'rgba(18,221,235,.28)'; g.beginPath(); g.roundRect(0, -46, 800 * pl, 92, 16); g.fill(); }
    if (pl < 1) { g.fillStyle = '#F5A524'; g.beginPath(); g.moveTo(40, -24); g.lineTo(64, 20); g.lineTo(16, 20); g.closePath(); g.fill(); }
    else { g.fillStyle = CYAN; g.beginPath(); g.arc(40, 0, 26, 0, 7); g.fill(); g.strokeStyle = NAVY; g.lineWidth = 6; g.lineCap = 'round'; g.beginPath(); g.moveTo(28, 0); g.lineTo(37, 10); g.lineTo(53, -10); g.stroke(); }
    font(600, 38, BODY); g.fillStyle = INK; g.fillText(s, 90, 12); g.restore(); });
  // the plan answer on "you know what's gonna happen"
  if (T > 11.9) { const q = back((T - 11.9) / .35); g.save(); g.translate(540, 1110); g.scale(q, q); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-330, -44, 660, 88, 44); g.fill();
    font(700, 44, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('→ Everyone knows the plan', 0, 15); g.textAlign = 'left'; g.restore(); }
  // signature on "agreement"
  g.strokeStyle = '#C9CDD2'; g.lineWidth = 3; g.beginPath(); g.moveTo(140, 1370); g.lineTo(640, 1370); g.stroke();
  const sg = clamp((T - 8.36) / .7); if (sg > 0) { g.strokeStyle = BLUE; g.lineWidth = 5; g.lineCap = 'round'; g.beginPath();
    for (let k = 0; k <= 60 * sg; k++) { const u = k / 60, x = 160 + u * 440, y = 1340 + Math.sin(u * 18) * 22 * (1 - u * .5) - u * 10; k ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); }
  font(500, 22, MONO); g.fillStyle = T > 9.8 ? BLUE : GREY; g.fillText(T > 9.8 ? 'SIGNED · AGREED ✓' : 'SIGNED', 140, 1410);
  // v3: a seal stamps beside the signature and keeps turning (old render: still 8.8–10.2 s)
  const se = back((T - 9.0) / .35); if (se > 0) { g.save(); g.translate(820, 1350); g.scale(se, se); g.fillStyle = BLUE; g.beginPath(); g.arc(0, 0, 70, 0, 7); g.fill();
    g.rotate((T - 9.0) * 1.6); g.setLineDash([14, 10]); g.strokeStyle = CYAN; g.lineWidth = 6; g.beginPath(); g.arc(0, 0, 92, 0, 7); g.stroke(); g.setLineDash([]); g.rotate(-(T - 9.0) * 1.6);
    g.strokeStyle = WHITE; g.lineWidth = 9; g.lineCap = 'round'; g.beginPath(); g.moveTo(-26, 2); g.lineTo(-6, 22); g.lineTo(28, -20); g.stroke(); g.restore(); }
  // v3: the pen glides in, signs, then lifts and hovers (old render: still 7.9–8.8 s)
  if (T > 4.5 && T < 12.2) { let px, py; const u = clamp((T - 8.36) / .7), LW = [800, 800, 800, 480];
    if (T < 4.9) { const m = inOut((T - 4.5) / .4); px = lerp(1060, 140, m); py = lerp(560, 458, m); }   // pen reads along the highlighter
    else if (T < 6.7) { const k = Math.min(3, Math.floor((T - 4.9) / .45)), hl = inOut((T - 4.9 - k * .45) / .5); px = 140 + LW[k] * hl; py = 458 + k * 46; }
    else if (T < 7.6) { px = 620; py = 596 + Math.sin((T - 6.7) * 3) * 14; }
    else if (T < 8.36) { const m = inOut((T - 7.6) / .76); px = lerp(620, 160, m); py = lerp(596, 1340, m); }
    else if (u < 1) { px = 160 + u * 440; py = 1340 + Math.sin(u * 18) * 22 * (1 - u * .5) - u * 10; }
    else { const m = inOut((T - 9.06) / .6), ex = inOut((T - 11.5) / .5); px = lerp(lerp(600, 560, m), 1260, ex); py = lerp(lerp(1330, 1220, m) + Math.sin((T - 9.06) * 2.4) * 12 * m, 1000, ex); }   // exits before the plan pill lands
    g.save(); g.translate(px, py); g.rotate(.55); g.fillStyle = NAVY; g.beginPath(); g.roundRect(-11, -150, 22, 124, 8); g.fill(); g.fillStyle = BLUE; g.beginPath(); g.moveTo(-11, -26); g.lineTo(11, -26); g.lineTo(0, 0); g.closePath(); g.fill(); g.restore(); }
  SCEN.forEach(([, at], i) => { const pulse = Math.max(0, 1 - Math.abs(T - (10.1 + i * .3)) / .2); if (pulse > 0) { g.strokeStyle = `rgba(245,165,36,${pulse})`; g.lineWidth = 4; g.beginPath(); g.roundRect(140, 674 + i * 120, 800, 92, 16); g.stroke(); } });
  g.restore();
  faceCircle(920, 1760, 100, back((T - DEAL_IN - .3) / .6));
}
// "We make a promise, we keep it": promise made → promise kept stamp, on the card under the chin.
function sceneKeep(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = back((T - 14.02) / .45); if (p <= 0) return;
  g.save(); g.translate(540, 1470); g.scale(p, p); card(-430, -150, 860, 300, NAVY, 30, .35);
  font(500, 24, MONO); g.letterSpacing = '4px'; g.fillStyle = T > 14.02 ? CYAN : GREY; g.fillText('ABOVE', -380, -80);
  g.fillStyle = T > 14.66 ? CYAN : GREY; g.fillText(' AND BEYOND', -380 + g.measureText('ABOVE').width, -80); g.letterSpacing = '0px';
  const fadeOld = 1 - clamp((T - 18.74) / .2), fadeNew = expo((T - 18.74) / .25);
  if (fadeOld > 0) { g.globalAlpha = fadeOld; typeOn('Whatever we’ve said…', -380, 10, T - 15.34, { size: 76, col: WHITE, w: 800, fam: COND, track: 0, cps: 26 });
    if (T > 16.18) { g.globalAlpha = fadeOld * expo((T - 16.18) / .3); font(800, 76, COND); g.fillStyle = CYAN; g.fillText('…happens.', -380, 100); } g.globalAlpha = 1; }
  if (fadeNew > 0) { g.globalAlpha = fadeNew; font(800, 76, COND); g.fillStyle = WHITE; g.fillText('Promise made.', -380, 10 + (1 - fadeNew) * 30);
    if (T > 19.46) { g.globalAlpha = expo((T - 19.46) / .25); g.fillStyle = CYAN; g.fillText('Promise kept.', -380, 100); } g.globalAlpha = 1; }
  // KEPT stamp on the card's right half
  const q = back((T - 19.46) / .3); if (q > 0) { g.save(); g.translate(280, 40); g.rotate(-.15); g.scale(q * (2 - q) * .8, q * (2 - q) * .8);
    g.fillStyle = '#F3F3F3'; g.beginPath(); g.roundRect(-140, -50, 280, 100, 14); g.fill(); g.strokeStyle = '#28C941'; g.lineWidth = 8; g.stroke();
    font(800, 60, COND); g.fillStyle = '#1F9D55'; g.textAlign = 'center'; g.fillText('KEPT ✓', 0, 22); g.textAlign = 'left'; g.restore(); }
  g.restore();
  if (T > 17.3 && T < 18.94) { const k = back((T - 17.3) / .35) * (1 - clamp((T - 18.74) / .2)); g.save(); g.translate(540, 1680); g.scale(k, k); g.fillStyle = '#F5A524'; g.beginPath(); g.roundRect(-200, -38, 400, 76, 38); g.fill();
    font(500, 28, MONO); g.letterSpacing = '3px'; g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('EVEN AT OUR COST', 0, 10); g.textAlign = 'left'; g.letterSpacing = '0px'; g.restore(); }
  burst(T, 19.5, 820, 1510, 20, 3);
}
