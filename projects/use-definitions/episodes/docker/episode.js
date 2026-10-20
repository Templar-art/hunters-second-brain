// Docker / containers (12 Oct clip, 40s). Shipping-container metaphor throughout.
const VM_IN = 2.5, BOX_IN = 6.0, CLONE_IN = 13.4, SETUP_IN = 19.5, SHIP_IN = 30.8, SEC_IN = 35.1, END_MOS = 39.9, END_IN = END_MOS + .4;
window.EP = {
  dur: 43.3, voEnd: 40.0,
  punchIns: [[33.0, 35.1]],
  cuts: [VM_IN, BOX_IN, CLONE_IN, SETUP_IN, SHIP_IN, SEC_IN, END_IN],
  // v2 (redo pass): deliberate transitions the QC continuity check should ignore (hard cuts get ±0.3 s)
  qcAllow: [[0, 0.6], [1.9, 2.8], [5.4, 6.6], [13.0, 13.8], [18.5, 19.8], [27.6, 28.3], [30.5, 31.2], [34.8, 35.5], [39.6, 40.6]],
  captions: [[VM_IN, BOX_IN, 1040], [SHIP_IN, SEC_IN, T => lerp(H + 40, PANEL_Y, expo((T - SHIP_IN) / .6)) - 60]],
  frame(T) {
    if (T < VM_IN) titleCard(T, 'DOCKER', 2.2, 'Definitions', [985, 800]);   // v2: shards off the ear line
    else if (T < BOX_IN) sceneVM(T);
    else if (T < CLONE_IN) sceneBox(T);
    else if (T < SETUP_IN) sceneClone(T);
    else if (T < SHIP_IN) sceneSetup(T);
    else if (T < SEC_IN) sceneShip(T);
    else if (T < END_IN) sceneSecure(T);
    else endCard(T, END_IN, this.dur, 'Definitions', true);   // v2: alive end card
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('DOCKER', 2.2); lowerThird.cue(2.6); cue(3.58, 'pop', { f: 800, gain: .22 });
    iris.cue(BOX_IN - .5); cue(6.5, 'whoosh', { d: .4, bright: .4, gain: .25 }); [11.18, 11.66, 12.56].forEach((t, i) => cue(t, 'thud', { f: 90 + i * 15, d: .2, gain: .25 }));
    whip.cue(CLONE_IN - .2); [15.34, 16.64, 17.26].forEach(t => cue(t, 'whoosh', { d: .3, bright: .5, gain: .25 })); cue(18.6, 'chime', { f: 1175, gain: .12 });
    cue(SETUP_IN, 'whoosh', { d: .4, gain: .3 }); for (let i = 0; i < 6; i++) cue(25.0 + i * .3, 'click', { f: 900, gain: .14 }); cue(27.76, 'whoosh', { d: .5, bright: .5, gain: .4 });
    cue(SHIP_IN - .1, 'whoosh', { d: .5, gain: .4 }); cue(31.5, 'thud', { f: 50, d: .5, gain: .5 }); [34.3, 34.54, 34.84].forEach(t => cue(t, 'pop', { f: 1100, gain: .16 }));
    cue(SEC_IN, 'whoosh', { d: .35, gain: .3 }); cue(36.0, 'thud', { f: 80, d: .3, gain: .35 }); cue(39.08, 'chime', { f: 1318, gain: .12 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};
function pillC(txt, x, y, p, bg = CYAN, fg = NAVY, size = 26) { if (p <= 0) return; g.save(); g.translate(x, y); g.scale(p, p); font(500, size, MONO); g.letterSpacing = '2px';
  const w = g.measureText(txt).width + 40; g.fillStyle = bg; g.beginPath(); g.roundRect(-w / 2, -size, w, size * 2, size); g.fill(); g.fillStyle = fg; g.textAlign = 'center'; g.fillText(txt, 0, size * .35); g.textAlign = 'left'; g.letterSpacing = '0px'; g.restore(); }
function cargo(x, y, w, h, p, label = 'USE', col = BLUE) {   // ribbed shipping container
  if (p <= 0) return; g.save(); g.translate(x, y); g.scale(p, p);
  g.fillStyle = col; g.beginPath(); g.roundRect(-w / 2, -h / 2, w, h, 10); g.fill();
  g.fillStyle = 'rgba(0,0,0,.18)'; for (let k = 0; k < 14; k++) g.fillRect(-w / 2 + 20 + k * (w - 40) / 14, -h / 2 + 14, 8, h - 28);
  g.fillStyle = 'rgba(255,255,255,.9)'; font(800, h * .32, COND); g.textAlign = 'center'; g.fillText(label, 0, h * .12); g.textAlign = 'left'; g.restore(); }

// "A little like a virtual machine": screen-in-a-screen card under the chin.
function sceneVM(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 2.6, 3.4); captions(T);
  const p = back((T - 3.58) / .45); if (p <= 0) return; g.save(); g.translate(540, 1400); g.scale(p, p);
  card(-300, -200, 600, 360, NAVY, 26, .35); g.strokeStyle = CYAN; g.lineWidth = 6; g.beginPath(); g.roundRect(-220, -150, 440, 250, 16); g.stroke();
  g.strokeStyle = WHITE; g.lineWidth = 4; g.beginPath(); g.roundRect(-120, -90, 240, 130, 10); g.stroke();
  font(800, 54, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('≈ virtual machine', 0, 210); g.textAlign = 'left'; g.restore();
}

// "Virtually contained part of your computer with its own tooling": container glows inside a laptop.
function sceneBox(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('Inside your computer', 70, 250, T - 6.1, { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  g.strokeStyle = '#5C7A92'; g.lineWidth = 8; g.beginPath(); g.roundRect(100, 420, 880, 640, 30); g.stroke(); g.beginPath(); g.moveTo(40, 1110); g.lineTo(1040, 1110); g.stroke();
  const c = expo((T - 6.5) / 1.0);
  if (c > 0) { g.save(); g.setLineDash([16, 12]); g.lineDashOffset = -T * 40; g.strokeStyle = CYAN; g.lineWidth = 6; g.shadowColor = CYAN; g.shadowBlur = 24 * c;
    g.beginPath(); g.roundRect(540 - 330 * c, 740 - 230 * c, 660 * c, 460 * c, 22); g.stroke(); g.restore();
    font(500, 24, MONO); g.globalAlpha = c; g.fillStyle = CYAN; g.fillText('CONTAINER', 230, 550); g.globalAlpha = 1; }
  [['node', 11.18], ['python', 11.66], ['database', 12.56]].forEach(([lab, at], i) => { const q = back((T - at) / .4), drop = (1 - expo(clamp((T - at) / .4))) * -300; if (q <= 0) return;
    g.save(); g.translate(330 + i * 210, 760 + drop); g.scale(q, q); g.fillStyle = [BLUE, '#3E7CB1', '#1F9D55'][i]; g.beginPath(); g.roundRect(-90, -70, 180, 140, 18); g.fill();
    font(700, 40, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(lab, 0, 14); g.textAlign = 'left'; g.restore(); });
  rise('Its own tooling.', 70, 1360, T - 11.18, { size: 120, w: 800, col: WHITE, dur: .45 });
  rise('Its own environment.', 70, 1490, T - 12.56, { size: 90, w: 800, col: CYAN, dur: .45 });
  faceCircle(900, 1730, 110, back((T - BOX_IN - .2) / .6));
}

// "Identical environment on any machine, immediately": the container copies onto three machines.
function sceneClone(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Same environment, any machine', 60, 250, T - 13.5, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  const sy = 520 + Math.sin((T - 13.6) * 2.6) * 16;   // v2: source container floats (old render: still 14–19.5 s)
  [[200, 15.34], [540, 16.64], [880, 17.26]].forEach(([x, at]) => { if (T < 13.9 || T > at) return;   // v2: copy beams reach for each machine until it lands
    g.save(); g.globalAlpha = clamp((T - 13.9) / .4); g.setLineDash([14, 12]); g.lineDashOffset = -T * 90; g.strokeStyle = BLUE; g.lineWidth = 5; g.beginPath(); g.moveTo(540, sy + 85); g.lineTo(x, 1000); g.stroke(); g.restore(); });
  cargo(540, sy, 420, 170, back((T - 13.6) / .45));
  if (T > 14.0) { const sx = ((T - 14.0) * 700) % 1400 - 400; g.save(); g.beginPath(); g.roundRect(330, sy - 85, 420, 170, 10); g.clip(); g.fillStyle = 'rgba(255,255,255,.35)'; g.beginPath(); g.moveTo(330 + sx, sy - 85); g.lineTo(450 + sx, sy - 85); g.lineTo(390 + sx, sy + 85); g.lineTo(270 + sx, sy + 85); g.fill(); g.restore(); }   // v2: image shine sweeps
  [['Laptop', 200, 15.34], ['Server', 540, 16.64], ['Cloud', 880, 17.26]].forEach(([lab, x, at], i) => { const q = expo((T - at) / .5), bob = Math.sin(T * 2.4 + i * 2.1) * 12 * clamp((T - at - .5) / .4);
    g.fillStyle = WHITE; g.strokeStyle = '#C9CDD2'; g.lineWidth = 3; g.beginPath(); g.roundRect(x - 150, 1000, 300, 360, 24); g.fill(); g.stroke();
    font(700, 48, COND); g.fillStyle = INK; g.textAlign = 'center'; g.fillText(lab, x, 1320); g.textAlign = 'left';
    if (q > 0) { const yy = lerp(520, 1130, q) + bob, xx = lerp(540, x, q); cargo(xx, yy, 230, 100, lerp(.6, 1, q)); }
    if (q > .95) pillC('✓', x + 120, 1030, back((T - at - .5) / .3), CYAN, NAVY, 22); });
  const im = expo((T - 18.6) / .2); if (im > 0) { g.fillStyle = `rgba(255,255,255,${.6 * (1 - clamp((T - 18.7) / .3))})`; g.fillRect(0, 0, W, H); }
  rise('Immediately.', 54, 1600, T - 18.6, { size: 150, w: 800, col: INK, dur: .4 });
}

// "You and I … not worried about setting that all up": two machines, mismatched installs, then swept away.
const DEPS = [['node', 'v18', 'v20'], ['python', '3.9', '3.12'], ['libssl', '1.1', '3.0'], ['postgres', '13', '16']];
function sceneSetup(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Without containers', 60, 250, T - SETUP_IN - .1, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  const sweep = inOut((T - 27.76) / .5);
  [['Your computer', 60], ['My computer', 560]].forEach(([lab, x], side) => { const q = expo((T - 19.72 - side * .2) / .45); if (q <= 0) return;
    const pulse = Math.max(0, 1 - Math.abs(T - (side ? 30.0 : 29.4)) / .3);
    const fy = Math.sin((T - 19.7) * 2 + side * Math.PI) * 12 * clamp((T - 20.2) / .5);   // v2: machines float in opposite phase (old render: still 20.3–29 s)
    g.save(); g.globalAlpha = q; g.translate(0, fy); card(x, 340, 460, 900, pulse > 0 ? lerpC(WHITE, '#DFF8FB', pulse) : WHITE, 26, .1); font(800, 60, COND); g.fillStyle = INK; g.fillText(lab, x + 34, 430);
    DEPS.forEach(([d, a, b], i) => { const at = [22.44, 22.84, 24.08, 25.04][i], r = expo((T - at) / .3); if (r <= 0) return; const y = 540 + i * 150, off = sweep * (side ? 600 : -600);
      g.save(); g.globalAlpha = q * r * (1 - sweep * .5);
      font(500, 30, MONO); g.fillStyle = INK; g.fillText(d, x + 34, y); g.fillStyle = side ? '#9A6200' : BLUE; g.fillText(side ? b : a, x + 300, y);
      if (side) { g.fillStyle = '#F5A524'; g.beginPath(); g.arc(x + 420, y - 10, 18 + Math.max(0, Math.sin(T * 5 - i)) * 6 * (1 - sweep), 0, 7); g.fill(); font(800, 26, COND); g.fillStyle = WHITE; g.fillText('✗', x + 411, y - 1); }
      if (sweep > 0) { g.globalAlpha = 1; g.fillStyle = CYAN; g.fillRect(x + 30, y - 12, 400 * sweep, 5); }
      g.restore(); });
    g.restore(); });
  pillC('SAME APP', 540, 320 + Math.sin(T * 2.6) * 8, back((T - 21.18) / .35), BLUE, WHITE, 26);
  if (T > 25.2 && sweep < .5) pillC('VERSIONS DON’T MATCH', 540, 1340, back((T - 25.5) / .35), '#F5A524', WHITE);
  rise('Not worried.', 54, 1560, T - 27.88, { size: 160, w: 800, col: INK, dur: .45 });
  faceCircle(910, 1740, 110, back((T - SETUP_IN - .2) / .6));
}

// "It all lives in this Docker image … same every single time": cargo container under the head, identical runs.
function sceneShip(T) {
  th(FULL, zoomAt(T)); const top = lerp(H + 40, PANEL_Y, expo((T - SHIP_IN) / .6));
  panel(top); captions(T); const oy = top - PANEL_Y;
  cargo(540 - (1 - expo((T - 31.3) / .6)) * 800, 1440 + oy, 520, 200, 1, 'DOCKER IMAGE');
  ['run 1 ✓', 'run 2 ✓', 'run 3 ✓'].forEach((r, i) => pillC(r, 250 + i * 290, 1680 + oy, back((T - [34.3, 34.54, 34.84][i]) / .3), CYAN, NAVY, 32));
}

// "Doesn't get access to higher-level functions … more secure": shield blocks the container.
function sceneSecure(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('And it’s isolated', 70, 250, T - SEC_IN - .1, { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  cargo(540, 1300 + Math.sin((T - SEC_IN) * 2.2) * 12, 460, 180, back((T - SEC_IN - .1) / .45));   // v2: container bobs (old render: still 36.3–39 s)
  const sys = back((T - 35.2) / .45); if (sys > 0) { g.save(); g.translate(540, 520); g.scale(sys, sys); card(-260, -110, 520, 220, '#0E3148', 22, .3);
    font(800, 64, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('Your system', 0, 0); font(500, 22, MONO); g.fillStyle = GREY; g.fillText('HIGHER-LEVEL FUNCTIONS', 0, 50); g.textAlign = 'left'; g.restore(); }
  // arrow up from the container, stopped by a shield
  const sh = back((T - 36.0) / .35), a = expo((T - 36.3) / .5); g.strokeStyle = '#F5A524'; g.lineWidth = 8; g.lineCap = 'round'; g.beginPath(); g.moveTo(540, 1200); g.lineTo(540, lerp(1200, 1000, a)); g.stroke(); if (sh > 0) { g.save(); g.translate(540, 880); g.scale(sh, sh);
    g.fillStyle = CYAN; g.beginPath(); g.moveTo(0, -90); g.lineTo(80, -60); g.lineTo(70, 30); g.quadraticCurveTo(40, 80, 0, 100); g.quadraticCurveTo(-40, 80, -70, 30); g.lineTo(-80, -60); g.closePath(); g.fill();
    g.strokeStyle = NAVY; g.lineWidth = 10; g.beginPath(); g.moveTo(-30, 0); g.lineTo(-5, 28); g.lineTo(35, -25); g.stroke(); g.restore(); }
  // v2: repeated escape attempts fire up from the container and bounce off the shield
  if (T > 36.8) for (let k = 0; k < 3; k++) { const t = ((T - 36.8) * .9 + k / 3) % 1, x = 540 + (k - 1) * 120, up = t < .6, yy = up ? lerp(1180, 990, t / .6) : lerp(990, 1120, (t - .6) / .4), xx = up ? x * .3 + 540 * .7 + (x - 540) * .7 * (t / .6) : x + (x - 540) * (t - .6) * 1.5;
    g.save(); g.globalAlpha = up ? 1 : 1 - (t - .6) / .4; g.shadowColor = '#F5A524'; g.shadowBlur = 16; g.fillStyle = '#F5A524'; g.beginPath(); g.arc(xx, yy, 13, 0, 7); g.fill(); g.restore();
    if (!up) { const r = (t - .6) / .4; g.strokeStyle = `rgba(18,221,235,${.6 * (1 - r)})`; g.lineWidth = 5; g.beginPath(); g.arc(540, 880, 110 + r * 120, 0, 7); g.stroke(); } }
  rise('More secure.', 70, 1640, T - 39.08, { size: 150, w: 800, col: WHITE, dur: .45 });
  faceCircle(900, 1780, 100, back((T - SEC_IN - .2) / .6));
}

function lerpC(a, b, p) { const pa = [1, 3, 5].map(i => parseInt(a.slice(i, i + 2), 16)), pb = [1, 3, 5].map(i => parseInt(b.slice(i, i + 2), 16)); return `rgb(${pa.map((v, i) => Math.round(lerp(v, pb[i], clamp(p)))).join(',')})`; }
