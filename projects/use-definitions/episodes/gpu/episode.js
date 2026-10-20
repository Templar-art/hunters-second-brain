// GPU: graphical processing unit (09 Oct clip, 49s).
const USES_IN = 2.4, DC_IN = 6.9, CORES_IN = 13.3, RAM_IN = 23.6, XFER_IN = 31.0, NN_IN = 39.5, COST_IN = 46.5, END_MOS = 48.9, END_IN = END_MOS + .4;
window.EP = {
  dur: 52.4, voEnd: 49.0,
  punchIns: [[4.4, 6.9], [26.4, 31.0], [46.5, 48.9]],
  cuts: [USES_IN, DC_IN, CORES_IN, RAM_IN, XFER_IN, NN_IN, COST_IN, END_IN],
  // v2 (redo pass): deliberate transitions the QC continuity check should ignore
  qcAllow: [[0, 0.6], [1.8, 2.7], [4.0, 4.6], [5.0, 5.4], [5.9, 8.1], [9.5, 10.0], [10.7, 11.1], [11.9, 12.3], [12.9, 14.6],
            [15.0, 15.4], [22.4, 23.0], [23.4, 24.0], [26.3, 26.5], [30.7, 31.4], [38.9, 39.8], [42.9, 43.4], [45.1, 45.5],
            [46.3, 47.0], [47.0, 47.6], [48.7, 50.0]],
  captions: [[USES_IN, DC_IN, 1040], [RAM_IN, XFER_IN, 1040], [XFER_IN, NN_IN, 1780], [COST_IN, END_MOS, 1240]],
  frame(T) {
    if (T < USES_IN) titleCard(T, 'GPU', 2.1, 'Definitions', [985, 800]);   // v2: shards off the ear line
    else if (T < DC_IN) sceneUses(T);
    else if (T < CORES_IN) sceneDC(T);
    else if (T < RAM_IN) sceneCores(T);
    else if (T < XFER_IN) sceneRAM(T);
    else if (T < NN_IN) sceneXfer(T);
    else if (T < COST_IN) sceneNN(T);
    else if (T < END_IN) { th(FULL, zoomAt(T)); behindHead(T, 47.2, END_MOS, '$$$', 'EXPENSIVE', zoomAt(T)); captions(T); }
    else endCard(T, END_IN, this.dur, 'Definitions', true);   // v2: alive end card
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('GPU', 2.1); lowerThird.cue(2.5);
    [4.15, 5.15, 6.05].forEach((t, i) => cue(t, 'pop', { f: 700 + i * 120, gain: .2 }));
    iris.cue(DC_IN - .5); cue(9.68, 'thud', { f: 50, d: .5, gain: .45 }); cue(10.84, 'pop', { f: 900, gain: .2 }); cue(12.02, 'pop', { f: 1100, gain: .2 });
    whip.cue(CORES_IN - .2); cue(14.44, 'riser', { d: .8, gain: .14 }); cue(22.64, 'thud', { f: 45, d: .6, gain: .55 }); cue(22.64, 'glass', { n: 40, span: .3 });
    cue(RAM_IN, 'whoosh', { d: .4, gain: .3 }); for (let i = 0; i < 6; i++) cue(27.14 + i * .25, 'click', { f: 1500 + i * 100, gain: .16 });
    cue(XFER_IN - .1, 'whoosh', { d: .45, gain: .35 }); for (let i = 0; i < 6; i++) cue(36.88 + i * .22, 'click', { f: 1200 + (i % 2) * 400, gain: .14 });
    zoomThrough.cue(NN_IN - .3); cue(41.0, 'riser', { d: .6, gain: .12 }); cue(43.14, 'whoosh', { d: .3, bright: .5, gain: .25 }); cue(45.3, 'chime', { f: 1175, gain: .1 });
    behindHead.cue(47.2, 'EXPENSIVE'); mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};

// "Video games, render videos, 3D objects": three tiles under the chin.
function sceneUses(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 2.5, 4.2); captions(T);
  [['Games', 4.15], ['Video', 5.15], ['3D', 6.05]].forEach(([lab, at], i) => { const q = back((T - at) / .45); if (q <= 0) return;
    const x = 70 + i * 320, y = 1140, w = 300, h = 360;
    g.save(); g.translate(x + w / 2, y + h / 2); g.scale(q, q); g.translate(-(x + w / 2), -(y + h / 2)); card(x, y, w, h, NAVY, 26, .35);
    const cx = x + w / 2, cy = y + 150; g.strokeStyle = CYAN; g.lineWidth = 7; g.lineCap = 'round'; g.lineJoin = 'round';
    if (i === 0) { g.beginPath(); g.roundRect(cx - 90, cy - 45, 180, 90, 45); g.stroke(); g.beginPath(); g.moveTo(cx - 50, cy); g.lineTo(cx - 20, cy); g.moveTo(cx - 35, cy - 15); g.lineTo(cx - 35, cy + 15); g.stroke();
      g.fillStyle = CYAN; g.beginPath(); g.arc(cx + 35, cy - 8, 8, 0, 7); g.fill(); g.beginPath(); g.arc(cx + 55, cy + 10, 8, 0, 7); g.fill(); }
    if (i === 1) { g.beginPath(); g.roundRect(cx - 90, cy - 60, 180, 120, 14); g.stroke(); g.fillStyle = CYAN; g.beginPath(); g.moveTo(cx - 20, cy - 30); g.lineTo(cx + 30, cy); g.lineTo(cx - 20, cy + 30); g.fill(); }
    if (i === 2) { const a = (T - at) * 1.6, P = [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]].map(([px, py, pz]) => {
        const x1 = px * Math.cos(a) - pz * Math.sin(a), z1 = px * Math.sin(a) + pz * Math.cos(a), y1 = py * Math.cos(.5) - z1 * Math.sin(.5); return [cx + x1 * 55, cy + y1 * 55]; });
      [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]].forEach(([a1, b1]) => { g.beginPath(); g.moveTo(...P[a1]); g.lineTo(...P[b1]); g.stroke(); }); }
    font(800, 64, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(lab, cx, y + 310); g.textAlign = 'left'; g.restore(); });
  iris(T, DC_IN - .5, 540, 1320, sceneDC);
}

// "Commercial scale … running and training AI": a data centre of racks with blinking LEDs.
function sceneDC(T) {
  const wy = whip(T, CORES_IN - .2); if (wy < 0) sceneCores(T);
  g.save(); g.translate(0, wy);
  g.fillStyle = '#020B12'; g.fillRect(0, 0, W, H);
  typeOn('Nowadays', 70, 260, T - 7.18, { size: 30, col: CYAN, track: 6, upper: true, cps: 30 });
  rise('Commercial scale.', 64, 430, T - 9.68, { size: 140, w: 800, col: WHITE, dur: .45 });
  const scale = expo((T - 9.68) / .8), cols = 3 + Math.round(scale * 3), r = rng(5);
  for (let c = 0; c < cols; c++) { const q = expo((T - 7.3 - c * .15) / .5); if (q <= 0) continue;
    const rw = 860 / cols - 16, x = 110 + c * (rw + 16), y = 560;
    g.save(); g.globalAlpha = q; g.fillStyle = '#0E1C28'; g.beginPath(); g.roundRect(x, y + (1 - q) * 60, rw, 900, 12); g.fill();
    for (let u = 0; u < 16; u++) { const uy = y + 24 + u * 54 + (1 - q) * 60, busy = Math.max(0, Math.sin((T - 7.3) * 5 - u * .55 + c * .9));   // v2: workload sweep through the racks (old render: still holds)
      g.fillStyle = busy > .6 ? `rgba(0,155,232,${.25 + .45 * (busy - .6) / .4})` : '#16293A'; g.fillRect(x + 12, uy, rw - 24, 40);
      for (let k = 0; k < 3; k++) { const on = Math.sin(T * (6 + r() * 10) + r() * 6) > 0; g.fillStyle = on ? (k === 0 ? CYAN : BLUE) : '#24384A'; g.beginPath(); g.arc(x + 30 + k * 18, uy + 20, 5, 0, 7); g.fill(); } }
    g.restore(); }
  [['RUNNING AI', 10.84], ['TRAINING AI', 12.02]].forEach(([lab, at], i) => { const q = back((T - at) / .35); if (q <= 0) return;
    g.save(); g.translate(300 + i * 480, 1580); g.scale(q, q); font(800, 52, COND); const tw = g.measureText(lab).width + 60;
    g.fillStyle = i ? BLUE : CYAN; g.beginPath(); g.roundRect(-tw / 2, -46, tw, 92, 46); g.fill(); g.fillStyle = i ? WHITE : NAVY; g.textAlign = 'center'; g.fillText(lab, 0, 18); g.textAlign = 'left'; g.restore(); });
  faceCircle(900, 1780, 110, back((T - DC_IN - .3) / .6));
  g.restore();
}

// "Lots of really small, really quick processors … all at once": a grid of cores lighting in waves, then together.
function sceneCores(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('Thousands of tiny cores', 70, 260, T - 13.35, { size: 30, col: CYAN, track: 6, upper: true, cps: 30 });
  const N = 24, S = 36, gap = 4, ox = 540 - (N * (S + gap)) / 2, oy = 440, appear = expo((T - 13.35) / 1.2), all = T >= 22.64 ? expo((T - 22.64) / .2) * (1 - clamp((T - 23.2) / .4) * .4) : 0;
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) { const d = Math.hypot(i - N / 2, j - N / 2) / (N * .72); if (d > appear) continue;
    const wave = Math.max(0, Math.sin((T - 17.96) * 7 - d * 9)) * (T > 17.96 && T < 22.5 ? 1 : 0);
    const idle = T < 17.96 && ((i * 73 + j * 151 + Math.floor(T * 7) * 37) % 29) === 0 ? .45 : 0;   // v2: sparse idle twinkle before the waves
    const lit = Math.max(wave, all, idle);
    g.fillStyle = lit > .05 ? `rgba(18,221,235,${.25 + .75 * lit})` : '#0E3148'; g.beginPath(); g.roundRect(ox + i * (S + gap), oy + j * (S + gap), S, S, 6); g.fill(); }
  // tiny maths ops floating up during "small mathematical operations"
  if (T > 19.36 && T < 22.6) { const r = rng(3); for (let k = 0; k < 14; k++) { const t = ((T - 19.36) * .9 + r()) % 1, x = ox + r() * N * (S + gap), y = oy + N * (S + gap) - t * 700;
    g.globalAlpha = Math.sin(t * Math.PI); font(500, 30, MONO); g.fillStyle = WHITE; g.fillText(['2×3', '7+1', '4÷2', '9−5', '3²', '1+1'][k % 6], x, y); } g.globalAlpha = 1; }
  if (T < 22.64) rise('Small. Quick.', 64, 1560, T - 15.14, { size: 140, w: 800, col: WHITE, dur: .45, exitAt: 22.5, T });
  else rise('All at once.', 64, 1560, T - 22.64, { size: 140, w: 800, col: CYAN, dur: .4 });
  faceCircle(900, 1780, 110, back((T - CORES_IN - .2) / .6));
}

// DDR RAM: a memory stick under the chin; cells write in fast bursts.
function sceneRAM(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = expo((T - 24.7) / .5); if (p <= 0) return;
  const x = 60, y = 1180 + (1 - p) * 500, w = 960, h = 380;
  card(x, y, w, h, '#0B3B26', 18, .4);
  g.fillStyle = '#C8A84B'; for (let k = 0; k < 40; k++) g.fillRect(x + 30 + k * 23, y + h - 30, 14, 30);
  typeOn('DDR RAM', x + 30, y + 60, T - 24.8, { size: 28, col: '#A8F0C6', track: 5, cps: 30 });
  const writes = Math.max(0, (T - 27.14) * 26);
  for (let k = 0; k < 8; k++) { const cx = x + 40 + k * 112; g.fillStyle = '#111'; g.fillRect(cx, y + 90, 96, 200);
    for (let c = 0; c < 10; c++) { const idx = k * 10 + c, on = idx < writes % 80 || (writes > 80 && (idx + Math.floor(writes)) % 3 === 0);
      g.fillStyle = on ? CYAN : '#1E2C38'; g.fillRect(cx + 8 + (c % 2) * 44, y + 100 + Math.floor(c / 2) * 38, 36, 30); } }
  if (T > 29.5) { const q = back((T - 29.96) / .35); if (q > 0) { g.save(); g.translate(x + w - 170, y - 40); g.scale(q, q); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-150, -36, 300, 72, 36); g.fill();
    font(800, 44, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('FAST WRITES', 0, 15); g.textAlign = 'left'; g.restore(); } }
}

// Split: speaker left; GPU ↔ RAM packets ping-pong faster and faster on the right.
function sceneXfer(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  const p = inOut((T - XFER_IN) / .6), colW = lerp(W, 470, p);
  g.save(); g.beginPath(); g.rect(0, 0, colW, H); g.clip(); th({ x: 0, y: 0, w: colW, h: H }, lerp(BZ, 1.0, p), .3); g.restore();
  g.fillStyle = CYAN; g.fillRect(colW - 4, 0, 4, H);
  const x = 510; typeOn('Why it’s good for AI', x, 220, T - 31.05, { size: 24, col: CYAN, track: 5, upper: true, cps: 40 });
  const nodes = [['GPU', 400], ['RAM', 1240]], nx = 780;
  nodes.forEach(([lab, ny], i) => { const q = back((T - 31.05 - i * .12) / .4); if (q <= 0) return; g.save(); g.translate(nx, ny); g.scale(q, q);
    g.fillStyle = i ? '#0B3B26' : BLUE; g.beginPath(); g.roundRect(-150, -90, 300, 180, 24); g.fill(); font(800, 90, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(lab, 0, 32); g.textAlign = 'left'; g.restore(); });
  if (T > 32.5) { const speed = 1 + Math.max(0, T - 35.8) * 2.2, n = Math.min(24, 3 + Math.floor((T - 32.5) * 3));
    g.strokeStyle = '#2B4A62'; g.lineWidth = 4; g.setLineDash([8, 10]); g.beginPath(); g.moveTo(nx - 60, 490); g.lineTo(nx - 60, 1150); g.moveTo(nx + 60, 490); g.lineTo(nx + 60, 1150); g.stroke(); g.setLineDash([]);
    for (let k = 0; k < n; k++) { const t = ((T - 32.5) * .5 * speed + k / n) % 1, down = k % 2 === 0, yy = down ? lerp(500, 1140, t) : lerp(1140, 500, t);
      g.save(); g.shadowColor = CYAN; g.shadowBlur = 16; g.fillStyle = down ? CYAN : WHITE; g.beginPath(); g.roundRect(nx + (down ? -60 : 60) - 14, yy - 10, 28, 20, 6); g.fill(); g.restore(); } }
  rise('Back and forth.', x, 1560, T - 36.88, { size: 90, w: 800, col: WHITE, dur: .45 });
  rise('So quickly.', x, 1670, T - 39.0, { size: 90, w: 800, col: CYAN, dur: .45 });
  captions(T);
}

// Neural net: layers build, forward passes fire faster and faster, "no delay" bar fills instantly.
function sceneNN(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Train + run complex models', 60, 260, T - 39.5, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  const L = [3, 5, 6, 5, 2], lx = i => 140 + i * 200, ly = (i, j) => 900 + (j - (L[i] - 1) / 2) * 150;
  const build = expo((T - 39.5) / 1.4), pass = T > 40.2 ? ((T - 40.2) * (T > 43.14 ? 2.4 : 1.0)) % 1 : -1;   // v2: pass starts as soon as the net is built
  L.forEach((n, i) => { if (i < L.length - 1) for (let j = 0; j < n; j++) for (let k = 0; k < L[i + 1]; k++) {
      const vis = clamp(build * L.length - i - .3); if (vis <= 0) continue; const hot = pass >= 0 && Math.abs(pass * (L.length - 1) - i - .5) < .5;
      g.strokeStyle = hot ? 'rgba(0,155,232,.55)' : `rgba(46,49,52,${.12 * vis})`; g.lineWidth = hot ? 3 : 2; g.beginPath(); g.moveTo(lx(i), ly(i, j)); g.lineTo(lx(i + 1), ly(i + 1, k)); g.stroke(); }
    for (let j = 0; j < n; j++) { const q = back(build * L.length - i); if (q <= 0) continue; const hot = pass >= 0 && Math.abs(pass * (L.length - 1) - i) < .45;
      g.save(); g.translate(lx(i), ly(i, j)); g.scale(clamp(q, 0, 1.2), clamp(q, 0, 1.2)); if (hot) { g.shadowColor = CYAN; g.shadowBlur = 24; }
      g.fillStyle = hot ? CYAN : WHITE; g.strokeStyle = BLUE; g.lineWidth = 4; g.beginPath(); g.arc(0, 0, 30, 0, 7); g.fill(); g.stroke(); g.restore(); } });
  // no-delay bar
  if (T > 43.76) { const y = 1430; typeOn('Delay', 120, y - 30, T - 43.76, { size: 26, col: GREY, track: 5, upper: true, cps: 40 });
    g.fillStyle = '#E5E7EA'; g.beginPath(); g.roundRect(120, y, 840, 40, 20); g.fill();
    const f = expo((T - 44.5) / .25), gr = g.createLinearGradient(120, 0, 960, 0); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN);
    g.fillStyle = gr; g.beginPath(); g.roundRect(120, y, Math.max(40, 840 * f), 40, 20); g.fill();
    if (f > .98) statusP('READY · NO WAIT', 120, 1560); }
  rise('No slow delay.', 54, 1720, T - 45.22, { size: 120, w: 800, col: INK, dur: .45 });
  faceCircle(910, 240, 120, back((T - NN_IN - .2) / .6));
}
function statusP(txt, x, y) { font(500, 26, MONO); g.letterSpacing = '2px'; const w = g.measureText(txt).width + 32;
  g.fillStyle = CYAN; g.beginPath(); g.roundRect(x, y - 34, w, 48, 24); g.fill(); g.fillStyle = NAVY; g.fillText(txt, x + 16, y); g.letterSpacing = '0px'; }
