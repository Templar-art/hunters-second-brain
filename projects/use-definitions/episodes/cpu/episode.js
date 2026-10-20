// CPU: central processing unit (10 Oct clip, 35.6s). Sister episode to GPU, deliberately different visuals.
const VS_IN = 1.65, CORES_IN = 3.85, BRAIN_IN = 9.3, BOARD_IN = 14.4, FLOW_IN = 19.0, OUT_IN = 28.0, END_MOS = 35.3, END_IN = END_MOS + .4;
window.EP = {
  dur: 38.8, voEnd: 35.4,
  punchIns: [[11.0, 14.4], [31.2, 35.3]],
  cuts: [VS_IN, CORES_IN, BRAIN_IN, BOARD_IN, FLOW_IN, OUT_IN, END_IN],
  // v3 (redo pass): deliberate transitions the QC continuity check should ignore (hard cuts get ±0.3 s)
  qcAllow: [[0, 0.6], [1.3, 2.1], [2.7, 3.1], [3.5, 4.6], [5.4, 6.4], [7.0, 7.6], [9.0, 9.7], [10.7, 11.3], [13.1, 15.0],
            [16.4, 17.1], [18.7, 19.9], [20.2, 20.6], [21.2, 21.5], [22.4, 23.1], [23.2, 23.4], [25.7, 26.4], [27.7, 28.8],
            [30.4, 30.7], [30.9, 31.5], [32.8, 33.1], [34.9, 36.5]],
  captions: [[VS_IN, CORES_IN, 1040], [BRAIN_IN, BOARD_IN, 1240], [OUT_IN, END_MOS, T => lerp(H + 40, PANEL_Y, expo((T - OUT_IN) / .6)) - 60]],
  frame(T) {
    if (T < VS_IN) titleCard(T, 'CPU', 1.4, 'Definitions', [985, 800]);   // v3: shards off the ear line
    else if (T < CORES_IN) sceneVS(T);
    else if (T < BRAIN_IN) sceneCores(T);
    else if (T < BOARD_IN) { th(FULL, zoomAt(T)); lowerThird(T, 9.5, 11.6); behindHead(T, 13.24, BOARD_IN, 'BRAIN', null, zoomAt(T)); brainChip(T); captions(T); }
    else if (T < FLOW_IN) sceneBoard(T);
    else if (T < OUT_IN) sceneFlow(T);
    else if (T < END_IN) sceneOut(T);
    else endCard(T, END_IN, this.dur, 'Definitions', true);   // v3: alive end card
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('CPU', 1.4); cue(VS_IN, 'whoosh', { d: .35, gain: .3 }); cue(2.84, 'thud', { f: 70, d: .3, gain: .35 });
    whip.cue(CORES_IN - .15); cue(4.76, 'pop', { f: 500, gain: .25 }); cue(7.14, 'thud', { f: 45, d: .5, gain: .5 });
    cue(BRAIN_IN, 'whoosh', { d: .3, gain: .25 }); lowerThird.cue(9.5); behindHead.cue(13.24, null);
    iris.cue(BOARD_IN - .45); cue(16.1, 'riser', { d: .6, gain: .12 }); cue(16.96, 'chime', { f: 988, gain: .1 });
    cue(FLOW_IN - .1, 'whoosh', { d: .45, gain: .35 }); [21.32, 22.52, 25.78].forEach(t => cue(t, 'pop', { f: 900, gain: .2 }));
    cue(OUT_IN - .1, 'whoosh', { d: .5, gain: .4 }); OUTS.forEach(([, at]) => cue(at, 'pop', { f: 1000, gain: .2 })); cue(35.06, 'chime', { f: 1175, gain: .1 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};

// "A little different from a GPU": VS card below the chin.
function sceneVS(T) {
  th(FULL, BZ); captions(T);
  const p = expo((T - VS_IN) / .4), y = 1130 + (1 - p) * 500;
  [['CPU', BLUE, 60], ['GPU', '#0E3148', 560]].forEach(([lab, col, x], i) => { const q = expo((T - VS_IN - i * .1) / .4);
    g.save(); g.globalAlpha = q; card(x, y, 460, 380, col, 26, .35); font(800, 160, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(lab, x + 230, y + 250); g.textAlign = 'left'; g.restore(); });
  const v = back((T - 2.84) / .35); if (v > 0) { g.save(); g.translate(540, y + 190); g.scale(v, v); g.rotate(-.1);
    g.fillStyle = CYAN; g.beginPath(); g.arc(0, 0, 70, 0, 7); g.fill(); font(800, 70, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('VS', 0, 25); g.textAlign = 'left'; g.restore(); }
}

// Fewer, more powerful cores (CPU) vs a swarm of tiny ones (GPU).
function sceneCores(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('Fewer cores', 70, 260, T - CORES_IN, { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  rise('More powerful.', 64, 430, T - 7.14, { size: 140, w: 800, col: WHITE, dur: .45 });
  // CPU: 4 big cores
  const pulse = T > 7.14 ? .5 + .5 * Math.sin((T - 7.14) * 8) : 0;
  for (let i = 0; i < 4; i++) { const q = back((T - 4.0 - i * .12) / .4); if (q <= 0) continue; const x = 90 + (i % 2) * 230, y = 800 + Math.floor(i / 2) * 230;
    g.save(); g.translate(x + 100, y + 100); g.scale(q * (1 + pulse * .05), q * (1 + pulse * .05)); if (pulse) { g.shadowColor = CYAN; g.shadowBlur = 30 * pulse; }
    const turn = T > 4.5 && T < 7.14 && Math.floor((T - 4.5) * 3) % 4 === i;   // v3: the few big cores take turns working (old render: still 5–7.1 s)
    if (turn) { g.shadowColor = CYAN; g.shadowBlur = 36; }
    g.fillStyle = turn ? '#3FC3F5' : BLUE; g.beginPath(); g.roundRect(-100, -100, 200, 200, 26); g.fill(); g.shadowColor = 'transparent';
    font(800, 56, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('CORE', 0, 20); g.textAlign = 'left'; g.restore(); }
  font(800, 60, COND); g.fillStyle = WHITE; g.globalAlpha = expo((T - 4.3) / .4); g.fillText('CPU', 90, 1320); g.globalAlpha = 1;
  // GPU: many tiny cores
  const appear = expo((T - 5.58) / .8);
  for (let j = 0; j < 12; j++) for (let i = 0; i < 10; i++) { if ((i + j) / 22 > appear || appear < .05) continue; g.fillStyle = '#1E4A66'; g.beginPath(); g.roundRect(600 + i * 40, 800 + j * 36, 30, 28, 5); g.fill(); }
  g.globalAlpha = appear; font(800, 60, COND); g.fillStyle = '#5C7A92'; g.fillText('GPU', 600, 1320); g.globalAlpha = 1;
  [['4 big cores', 90], ['many tiny ones', 600]].forEach(([l, x], i) => typeOn(l, x, 1380, T - 5.0 - i * .6, { size: 24, col: GREY, track: 4, upper: true, cps: 40 }));
  faceCircle(900, 1700, 120, back((T - CORES_IN - .3) / .6));
}

// "Makes all the main operations within the machine": motherboard traces light out from the chip.
function sceneBoard(T) {
  g.fillStyle = '#04141E'; g.fillRect(0, 0, W, H);
  typeOn('Inside the machine', 70, 260, T - 14.4, { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  const cx = 540, cy = 980, r = rng(9), grow = expo((T - 15.0) / 2.0);   // v3: traces start as soon as the chip lands
  for (let k = 0; k < 28; k++) { const a = (k / 28) * 6.283, len = 260 + r() * 260, bend = (r() - .5) * 1.2, L = len * grow;
    const x1 = cx + Math.cos(a) * 130, y1 = cy + Math.sin(a) * 130, x2 = x1 + Math.cos(a) * L * .6, y2 = y1 + Math.sin(a) * L * .6, x3 = x2 + Math.cos(a + bend) * L * .4, y3 = y2 + Math.sin(a + bend) * L * .4;
    g.strokeStyle = 'rgba(18,221,235,.55)'; g.lineWidth = 4; g.beginPath(); g.moveTo(x1, y1); g.lineTo(x2, y2); g.lineTo(x3, y3); g.stroke();
    if (grow > .9) { g.fillStyle = CYAN; g.beginPath(); g.arc(x3, y3, 7, 0, 7); g.fill(); }
    const pulseT = ((T - 15.9) * 1.3 + r()) % 1; if (T > 15.9) { const px = pulseT < .6 ? lerp(x1, x2, pulseT / .6) : lerp(x2, x3, (pulseT - .6) / .4), py = pulseT < .6 ? lerp(y1, y2, pulseT / .6) : lerp(y2, y3, (pulseT - .6) / .4);
      g.save(); g.shadowColor = CYAN; g.shadowBlur = 14; g.fillStyle = WHITE; g.beginPath(); g.arc(px, py, 5, 0, 7); g.fill(); g.restore(); } }
  const cp = back((T - 14.4) / .45); if (cp > 0) { g.save(); g.translate(cx, cy); g.scale(cp, cp);
    g.fillStyle = '#1A2B38'; g.beginPath(); g.roundRect(-150, -150, 300, 300, 24); g.fill(); g.fillStyle = '#9FB3C4'; for (let i = 0; i < 8; i++) { g.fillRect(-130 + i * 34, -170, 14, 20); g.fillRect(-130 + i * 34, 150, 14, 20); g.fillRect(-170, -130 + i * 34, 20, 14); g.fillRect(150, -130 + i * 34, 20, 14); }
    const gr = g.createLinearGradient(-100, -100, 100, 100); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN); g.fillStyle = gr; g.beginPath(); g.roundRect(-100, -100, 200, 200, 16); g.fill();
    font(800, 80, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('CPU', 0, 28); g.textAlign = 'left'; g.restore(); }
  rise('All the main operations.', 64, 1640, T - 16.54, { size: 96, w: 800, col: WHITE, dur: .45 });
}

// Memory ⇄ CPU loop: a data packet loads into memory, gets processed, written back.
function sceneFlow(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Inside the machine', 60, 260, T - FLOW_IN - .1, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  const M = { x: 270, y: 900 }, C = { x: 810, y: 900 };
  [[M, 'Memory', 19.2], [C, 'CPU', 19.4]].forEach(([n, lab, at], i) => { const q = back((T - at) / .45); if (q <= 0) return;
    const fl = Math.sin((T - FLOW_IN) * 2.0 + i * Math.PI) * 12 * clamp((T - 19.9) / .5);   // v3: cards float in opposite phase (old render: still 20.6–28 s)
    g.save(); g.translate(n.x, n.y + fl); g.scale(q, q); card(-190, -170, 380, 340, i ? NAVY : WHITE, 30, .15);
    font(800, 76, COND); g.fillStyle = i ? WHITE : INK; g.textAlign = 'center'; g.fillText(lab, 0, 26); g.textAlign = 'left'; g.restore(); });
  // arrows
  const la = expo((T - 19.6) / .4); g.globalAlpha = la;
  g.strokeStyle = '#AEB4BA'; g.lineWidth = 5; g.beginPath(); g.moveTo(480, 840); g.lineTo(600, 840); g.moveTo(600, 960); g.lineTo(480, 960); g.stroke(); g.globalAlpha = 1;
  // packet journey: into memory (21.3) → CPU (22.5) → processed (23.3) → back to memory (25.8)
  let px = 70, py = 900, label = 'data';
  if (T > 20.28) { const k = clamp((T - 20.28) / 1.0); px = lerp(-60, M.x, expo(k)); }
  if (T > 22.52) { const k = clamp((T - 22.52) / .5); px = lerp(M.x, C.x, inOut(k)); py = 840; }
  if (T > 23.26) label = 'result';
  if (T > 25.78) { const k = clamp((T - 25.78) / .5); px = lerp(C.x, M.x, inOut(k)); py = 960; }
  if (T > 20.28) { g.save(); g.translate(px, py - 230 + Math.sin(T * 3.1) * 8); g.shadowColor = CYAN; g.shadowBlur = 24; g.fillStyle = label === 'result' ? CYAN : BLUE; g.beginPath(); g.roundRect(-80, -34, 160, 68, 34); g.fill();
    font(500, 26, MONO); g.fillStyle = label === 'result' ? NAVY : WHITE; g.textAlign = 'center'; g.fillText(label, 0, 9); g.textAlign = 'left'; g.restore(); }
  // operations spark inside the CPU
  if (T > 23.0 && T < 25.6) { const r = rng(Math.floor(T * 12)); for (let k = 0; k < 6; k++) { font(500, 30, MONO); g.fillStyle = CYAN; g.globalAlpha = .8; g.fillText(['+', '×', '÷', '−'][k % 4], C.x - 120 + r() * 240, C.y - 120 + r() * 60); } g.globalAlpha = 1; }
  [['Load', 20.28], ['Process', 22.78], ['Write back', 25.78]].forEach(([s, at], i) => { const q = expo((T - at) / .4); if (q <= 0) return;
    g.save(); g.globalAlpha = q; font(800, 72, COND); g.fillStyle = i === 2 ? BLUE : INK; g.fillText(`${i + 1}. ${s}`, 80, 1250 + i * 110); g.restore(); });
  faceCircle(910, 1720, 110, back((T - FLOW_IN - .2) / .6));
}

// Then it goes somewhere: panel under the head branches to drive / network / GPU → display.
const OUTS = [['Drive', 28.25], ['Network', 30.52], ['GPU', 32.9], ['Display', 35.06]];
function sceneOut(T) {
  th(FULL, zoomAt(T)); const top = lerp(H + 40, PANEL_Y, expo((T - OUT_IN) / .6));
  panel(top); captions(T); const oy = top - PANEL_Y;
  typeOn('Then it might go to', 80, 1330 + oy, T - OUT_IN - .3, { size: 26, col: BLUE, track: 6, upper: true, cps: 36 });
  OUTS.forEach(([lab, at], i) => { const q = back((T - at) / .4); if (q <= 0) return; const x = 150 + i * 260, y = 1560 + oy;
    if (i > 0 && i < 3) { g.strokeStyle = '#C9CDD2'; g.lineWidth = 3; g.setLineDash([8, 8]); g.beginPath(); g.moveTo(x - 260 + 80, y); g.lineTo(x - 80, y); g.stroke(); g.setLineDash([]); }
    if (i === 3) { g.strokeStyle = CYAN; g.lineWidth = 4; g.beginPath(); g.moveTo(x - 180, y); g.lineTo(x - 80, y); g.stroke(); }
    g.save(); g.translate(x, y); g.scale(q, q); g.fillStyle = i === 3 ? CYAN : WHITE; g.strokeStyle = BLUE; g.lineWidth = 4; g.beginPath(); g.roundRect(-75, -75, 150, 150, 24); g.fill(); g.stroke();
    g.strokeStyle = INK; g.lineWidth = 5;
    if (i === 0) { g.beginPath(); g.ellipse(0, -25, 40, 14, 0, 0, 7); g.stroke(); g.beginPath(); g.moveTo(-40, -25); g.lineTo(-40, 25); g.moveTo(40, -25); g.lineTo(40, 25); g.stroke(); g.beginPath(); g.ellipse(0, 25, 40, 14, 0, 0, Math.PI); g.stroke(); }
    if (i === 1) { g.beginPath(); g.arc(0, 0, 40, 0, 7); g.stroke(); g.beginPath(); g.ellipse(0, 0, 18, 40, 0, 0, 7); g.moveTo(-40, 0); g.lineTo(40, 0); g.stroke(); }
    if (i === 2) { g.beginPath(); g.roundRect(-40, -30, 80, 60, 8); g.stroke(); g.fillStyle = INK; for (let k = 0; k < 4; k++) g.fillRect(-30 + k * 18, 38, 8, 12); }
    if (i === 3) { g.beginPath(); g.roundRect(-45, -32, 90, 58, 6); g.stroke(); g.beginPath(); g.moveTo(-15, 40); g.lineTo(15, 40); g.stroke(); }
    font(700, 36, COND); g.fillStyle = INK; g.textAlign = 'center'; g.fillText(lab, 0, 120); g.textAlign = 'left'; g.restore(); });
}

// "The brain of a computer": a chip with pulse rings beside the face (never over it).
function brainChip(T) {
  const q = back((T - 13.3) / .4); if (q <= 0) return; const f = faceScreen(zoomAt(T)), cx = Math.min(W - 130, f.x + f.w + 150), cy = f.y + f.h * .45;
  for (let k = 0; k < 3; k++) { const t = ((T - 13.3) * 1.4 + k / 3) % 1; g.strokeStyle = `rgba(18,221,235,${1 - t})`; g.lineWidth = 4; g.beginPath(); g.arc(cx, cy, 70 + t * 70, 0, 7); g.stroke(); }
  g.save(); g.translate(cx, cy); g.scale(q, q); g.fillStyle = '#1A2B38'; g.beginPath(); g.roundRect(-70, -70, 140, 140, 16); g.fill();
  g.fillStyle = '#9FB3C4'; for (let i = 0; i < 4; i++) { g.fillRect(-55 + i * 34, -84, 10, 14); g.fillRect(-55 + i * 34, 70, 10, 14); g.fillRect(-84, -55 + i * 34, 14, 10); g.fillRect(70, -55 + i * 34, 14, 10); }
  const gr = g.createLinearGradient(-45, -45, 45, 45); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN); g.fillStyle = gr; g.beginPath(); g.roundRect(-46, -46, 92, 92, 10); g.fill();
  font(800, 40, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('CPU', 0, 14); g.textAlign = 'left'; g.restore();
}
