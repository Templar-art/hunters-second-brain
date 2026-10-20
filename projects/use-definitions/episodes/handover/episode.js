// Q&A: "What does a client get on the last day / what does a handover look like?" (23 Oct clip, 39.8s).
const ONEOFF_IN = 3.2, EVOLVE_IN = 8.1, LOOP_IN = 14.3, DONE_IN = 23.6, KIT_IN = 27.9, BYE_IN = 34.4, END_MOS = 39.6, END_IN = END_MOS + .4;
window.EP = {
  dur: 43.0, voEnd: 39.7,
  punchIns: [[5.9, 8.1], [36.3, 39.6]],
  cuts: [ONEOFF_IN, EVOLVE_IN, LOOP_IN, DONE_IN, KIT_IN, BYE_IN, END_IN],
  // v2 (redo pass): deliberate transitions the QC continuity check should ignore (hard cuts get ±0.3 s)
  qcAllow: [[0, 0.6], [2.9, 3.6], [5.7, 6.1], [7.6, 8.5], [14.0, 14.6], [23.3, 23.9], [27.6, 28.2], [31.0, 32.4], [33.0, 33.4], [34.1, 34.7], [36.1, 36.5], [39.3, 40.4]],
  captions: [[ONEOFF_IN, EVOLVE_IN, 1080], [DONE_IN, KIT_IN, 1080], [BYE_IN, END_MOS, 1080]],
  frame(T) {
    if (T < ONEOFF_IN) qOpener(T, 0, ONEOFF_IN, '', ['What does a handover', 'look like?']);
    else if (T < EVOLVE_IN) sceneOneOff(T);
    else if (T < LOOP_IN) sceneEvolve(T);
    else if (T < DONE_IN) sceneLoop(T);
    else if (T < KIT_IN) sceneDone(T);
    else if (T < BYE_IN) sceneKit(T);
    else if (T < END_IN) sceneBye(T);
    else endCard(T, END_IN, this.dur, 'Q&A', true);   /* v2: alive end card */
    mosaic(T, END_MOS, 9);
  },
  cues() {
    qOpener.cue(0, ONEOFF_IN); lowerThird.cue(3.3); cue(4.6, 'pop', { f: 800, gain: .22 }); cue(7.26, 'thud', { f: 90, d: .25, gain: .35 });
    iris.cue(EVOLVE_IN - .45); [8.88, 9.6, 10.9, 12.14].forEach((t, i) => cue(t, 'pop', { f: 700 + i * 120, gain: .18 }));
    cue(LOOP_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(15.86, 'pop', { f: 900, gain: .2 }); [18.14, 18.84, 19.4].forEach(t => cue(t, 'click', { gain: .25 })); cue(20.78, 'whoosh', { d: .4, bright: .4, gain: .25 });
    cue(DONE_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(24.58, 'chime', { f: 988, gain: .1 }); cue(26.9, 'click', { gain: .3 }); cue(27.3, 'click', { gain: .3 }); cue(27.62, 'chime', { f: 1175, gain: .1 });
    cue(KIT_IN - .1, 'whoosh', { d: .45, gain: .35 }); KIT.forEach(([, at]) => { cue(at, 'pop', { f: 900, gain: .2 }); cue(at + .3, 'click', { gain: .25 }); }); cue(31.38, 'thud', { f: 60, d: .3, gain: .35 });
    cue(BYE_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(37.52, 'chime', { f: 1318, gain: .12 }); burst.cue(37.6);
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};
// "Not just a one-off event": a single 'LAST DAY' calendar page gets crossed out.
function sceneOneOff(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 3.3, 4.4); captions(T);
  const p = back((T - 4.6) / .45); if (p <= 0) return; g.save(); g.translate(540, 1460); g.scale(p, p); g.rotate(-.04);
  card(-200, -230, 400, 460, WHITE, 24, .3); g.fillStyle = BLUE; g.beginPath(); g.roundRect(-200, -230, 400, 110, [24, 24, 0, 0]); g.fill();
  font(500, 28, MONO); g.letterSpacing = '4px'; g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('LAST DAY', 0, -160); g.letterSpacing = '0px';
  font(800, 200, COND); g.fillStyle = INK; g.fillText('1', 0, 110); g.textAlign = 'left';
  if (T > 7.26) { const k = expo((T - 7.26) / .3); g.strokeStyle = BLUE; g.lineWidth = 14; g.lineCap = 'round'; g.beginPath(); g.moveTo(-160, -60); g.lineTo(-160 + 320 * k, -60 + 260 * k); g.stroke(); }
  g.restore();
  if (T > 7.4) { const q = back((T - 7.4) / .35); g.save(); g.translate(790, 1215); g.scale(q, q); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-230, -55, 460, 110, 55); g.fill();
    font(800, 64, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('Not a one-off', 0, 22); g.textAlign = 'left'; g.restore(); }
}
// "Software is ever-evolving … can't digest everything in a single go": an app keeps growing modules.
function sceneEvolve(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('Ever-evolving', 70, 240, T - 8.3, { size: 30, col: CYAN, track: 6, upper: true, cps: 30 });
  const ver = T > 12.14 ? 'v1.3' : T > 10.9 ? 'v1.2' : T > 9.6 ? 'v1.1' : 'v1.0';
  const MOD = ['Reports', 'Alerts', 'Billing', 'Mobile', 'Exports', 'Roles', 'API', 'Search'];
  MOD.forEach((m, i) => { const at = 8.88 + i * .45, q = back((T - at) / .4); if (q <= 0) return; const spin = .3 * Math.max(0, T - 12.3) * clamp((T - 12.3) / .8), a = -Math.PI / 2 + i / MOD.length * 6.283 + spin, r = 330;   /* v2: the app keeps turning (old render: still 12.5–14.3 s) */
    g.strokeStyle = '#2B4A62'; g.lineWidth = 3; g.beginPath(); g.moveTo(540, 820); g.lineTo(540 + Math.cos(a) * r * clamp(q), 820 + Math.sin(a) * r * clamp(q)); g.stroke();
    if (T > 11.0) { const t = ((T - 11.0) * .9 + i / MOD.length) % 1; g.fillStyle = CYAN; g.beginPath(); g.arc(540 + Math.cos(a) * r * t, 820 + Math.sin(a) * r * t, 9, 0, 7); g.fill(); }
    g.save(); g.translate(540 + Math.cos(a) * r, 820 + Math.sin(a) * r); g.scale(q, q); g.fillStyle = '#0E3148'; g.strokeStyle = CYAN; g.lineWidth = 3; g.beginPath(); g.roundRect(-95, -36, 190, 72, 36); g.fill(); g.stroke();
    font(700, 38, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(m, 0, 13); g.textAlign = 'left'; g.restore(); });
  const core = back((T - 8.3) / .45); if (core > 0) { g.save(); g.translate(540, 820); g.scale(core, core); const gr = g.createLinearGradient(-120, -120, 120, 120); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN);
    g.fillStyle = gr; g.beginPath(); g.roundRect(-130, -130, 260, 260, 60); g.fill(); font(800, 80, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(ver, 0, 28); g.textAlign = 'left'; g.restore(); }
  rise('Too much for a single go.', 70, 1560, T - 12.14, { size: 90, w: 800, col: WHITE, dur: .45 });
  faceCircle(900, 1780, 100, back((T - EVOLVE_IN - .2) / .6));
}
// Build together: a build → test → iterate loop, the client joins, two travellers on a journey path.
function sceneLoop(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('We build it with you', 60, 240, T - LOOP_IN, { size: 30, col: BLUE, track: 6, upper: true, cps: 32 });
  const cx = 540, cy = 760, R = 270, lp = expo((T - LOOP_IN) / .8);
  g.strokeStyle = '#C9CDD2'; g.lineWidth = 10; g.beginPath(); g.arc(cx, cy, R, -Math.PI / 2, -Math.PI / 2 + 6.283 * lp); g.stroke();
  if (T > 15.0) { const a = -Math.PI / 2 + (T - 15.0) * 2.2, tr = Math.min(.9, (T - 15.0) * 2.2);   /* v2: work goes round the loop from the start, with a trail (old render: still 14.9–23.6 s) */
    const sw = g.createRadialGradient(cx, cy, 0, cx, cy, R); sw.addColorStop(0, 'rgba(0,155,232,.05)'); sw.addColorStop(1, 'rgba(0,155,232,.5)'); g.fillStyle = sw; g.beginPath(); g.moveTo(cx, cy); g.arc(cx, cy, R, a - tr * 1.4, a); g.closePath(); g.fill();   /* radar-style sweep: a dot alone is too small to read on the light page */
    g.strokeStyle = CYAN; g.lineWidth = 12; g.lineCap = 'round'; g.beginPath(); g.arc(cx, cy, R, a - tr, a); g.stroke(); g.fillStyle = CYAN; g.beginPath(); g.arc(cx + Math.cos(a) * R, cy + Math.sin(a) * R, 24, 0, 7); g.fill(); }
  [['Build', 16.6, -Math.PI / 2], ['Test', 18.14, Math.PI / 6], ['Iterate', 18.84, Math.PI * 5 / 6]].forEach(([lab, at, a]) => { const q = back((T - at) / .35); if (q <= 0) return;
    g.save(); g.translate(cx + Math.cos(a) * R, cy + Math.sin(a) * R); g.scale(q, q); g.fillStyle = NAVY; g.beginPath(); g.roundRect(-110, -44, 220, 88, 44); g.fill();
    font(800, 50, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(lab, 0, 17); g.textAlign = 'left'; g.restore(); });
  const cl = back((T - 15.86) / .4); if (cl > 0) { g.save(); g.translate(cx, cy + Math.sin(T * 2.6) * 10 * clamp((T - 16.3) / .4)); g.scale(cl, cl); g.fillStyle = BLUE; g.beginPath(); g.arc(0, -20, 46, 0, 7); g.fill(); g.beginPath(); g.arc(0, 80, 80, Math.PI, 0); g.fill();
    font(500, 22, MONO); g.fillStyle = INK; g.textAlign = 'center'; g.fillText('YOU, ON BOARD', 0, 130); g.textAlign = 'left'; g.restore(); }
  // the journey alongside
  const jp = expo((T - 20.42) / 1.4); if (jp > 0) { g.strokeStyle = BLUE; g.lineWidth = 6; g.setLineDash([2, 16]); g.lineCap = 'round'; g.beginPath(); g.moveTo(100, 1260); g.bezierCurveTo(400, 1180, 680, 1360, 980, 1250); g.stroke(); g.setLineDash([]);
    [0, 1].forEach(k => { const u = clamp(jp - k * .05), x = lerp(100, 980, u), y = 1260 + Math.sin(u * Math.PI) * 30 - k * 50 - Math.abs(Math.sin(T * 6 + k * 1.4)) * 18;   /* v2: the two travellers keep walking */ g.fillStyle = k ? CYAN : NAVY; g.beginPath(); g.arc(x, y, 22, 0, 7); g.fill(); });
    font(500, 24, MONO); g.letterSpacing = '4px'; g.fillStyle = BLUE; g.fillText('THE DEVELOPMENT JOURNEY', 100, 1350); g.letterSpacing = '0px'; }
  rise('Delivering what you want.', 54, 1600, T - 22.38, { size: 96, w: 800, col: INK, dur: .45 });
  faceCircle(910, 1790, 100, back((T - LOOP_IN - .3) / .6));
}
// "They're already using it … do we both agree we're done?": in-use pill + two checkboxes tick.
function sceneDone(T) {
  th(FULL, BZ); captions(T);
  const u = back((T - 24.38) / .4); if (u > 0) { g.save(); g.translate(280, 1260); g.scale(u, u); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-200, -40, 400, 80, 40); g.fill();
    font(700, 42, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('● Already in use', 0, 15); g.textAlign = 'left'; g.restore(); }
  const p = back((T - 25.9) / .45); if (p <= 0) return; g.save(); g.translate(540, 1500); g.scale(p, p); card(-430, -150, 860, 300, WHITE, 30, .3);
  font(800, 58, COND); g.fillStyle = INK; g.fillText('Do we both agree we’re done?', -380, -60);
  [['You', 26.9, -380], ['USE', 27.3, 40]].forEach(([who, at, x]) => { const c = back((T - at) / .3); g.strokeStyle = BLUE; g.lineWidth = 5; g.strokeRect(x, 20, 70, 70);
    if (c > 0) { g.save(); g.translate(x + 35, 55); g.scale(c, c); g.strokeStyle = BLUE; g.lineWidth = 9; g.lineCap = 'round'; g.beginPath(); g.moveTo(-20, 0); g.lineTo(-5, 18); g.lineTo(24, -20); g.stroke(); g.restore(); }
    font(700, 52, COND); g.fillStyle = INK; g.fillText(who, x + 100, 76); });
  g.restore();
}
// The handover kit: access, deploy, repo ownership tick off as he names them.
const KIT = [['Access', 30.38, '🔑', 28.6], ['Deploy', 31.02, '↑', 29.0], ['Repo ownership', 32.18, '⇄', 29.4]];
function sceneKit(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('From there, normally', 70, 240, T - 27.95, { size: 30, col: CYAN, track: 6, upper: true, cps: 60 });
  KIT.forEach(([lab, at, ic, ap], i) => { const q = back((T - ap) / .45), done = expo((T - at) / .3); if (q <= 0) return; const y = 480 + i * 280;
    g.save(); g.translate(540, y + Math.sin(T * 2.2 + i * 2.1) * 12 * clamp((T - ap - .5) / .5)); g.scale(q, q); card(-440, -110, 880, 220, done > .5 ? '#0E3A57' : '#0B2233', 26, .3);   /* v2: the kit floats (old render: still 29.9–34.4 s) */
    if (done > .5) { const t = ((T - at) / 1.2) % 1; g.strokeStyle = `rgba(18,221,235,${.6 * (1 - t)})`; g.lineWidth = 4; g.beginPath(); g.arc(-330, 0, 60 + t * 70, 0, 7); g.stroke(); }
    g.fillStyle = done > .5 ? CYAN : '#2B4A62'; g.beginPath(); g.arc(-330, 0, 60, 0, 7); g.fill();
    font(800, 56, BODY); g.fillStyle = done > .5 ? NAVY : WHITE; g.textAlign = 'center'; g.fillText(ic, -330, 20); g.textAlign = 'left';
    font(800, 70, COND); g.fillStyle = WHITE; g.fillText(lab, -230, 25);
    if (done > 0) { g.save(); g.translate(360, 0); g.scale(done, done); g.strokeStyle = CYAN; g.lineWidth = 10; g.lineCap = 'round'; g.beginPath(); g.moveTo(-26, 0); g.lineTo(-6, 22); g.lineTo(30, -24); g.stroke(); g.restore(); }
    g.restore(); });
  // deploy button press on "hitting deploy"
  const dp = back((T - 31.02) / .3); if (dp > 0 && T < 32.18) { const press = T > 31.38 && T < 31.6 ? .06 : 0; g.save(); g.translate(540, 1420); g.scale(dp * (1 - press), dp * (1 - press));
    const dn = BASE_T > 31.5; g.fillStyle = dn ? CYAN : BLUE; g.beginPath(); g.roundRect(-220, -60, 440, 120, 60); g.fill(); font(800, 60, COND); g.fillStyle = dn ? NAVY : WHITE; g.textAlign = 'center'; g.fillText(dn ? 'Deployed ✓' : 'Deploy', 0, 20); g.textAlign = 'left'; g.restore(); }
  if (T > 33.2) { const q = back((T - 33.2) / .3); g.save(); g.translate(540, 1420 + Math.sin(T * 2.6) * 10); g.scale(q, q); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-240, -50, 480, 100, 50); g.fill();
    font(700, 46, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('Repo → your GitHub', 0, 16); g.textAlign = 'left'; g.restore(); }
  faceCircle(900, 1780, 100, back((T - KIT_IN - .3) / .6));
}
// "Job well done for now. See you when you need us."
function sceneBye(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = back((T - 37.26) / .4); if (p > 0) { g.save(); g.translate(540, 1460); g.scale(p, p); card(-400, -130, 800, 260, NAVY, 30, .35);
    font(800, 80, COND); g.fillStyle = WHITE; g.fillText('Job well done ✓', -350, -10);
    if (T > 38.68) { font(700, 52, COND); g.fillStyle = CYAN; g.globalAlpha = expo((T - 38.68) / .3); g.fillText('See you when you need us.', -350, 70); g.globalAlpha = 1; } g.restore(); }
  burst(T, 37.6, 540, 1460, 22, 7);
}
