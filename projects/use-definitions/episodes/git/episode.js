// Git: version control (11 Oct clip, 42.8s).
const HUB_IN = 2.1, TEAM_IN = 10.2, MERGE_IN = 23.7, TREE_IN = 30.1, END_MOS = 42.6, END_IN = END_MOS + .4;
window.EP = {
  dur: 46.0, voEnd: 42.7,
  punchIns: [[6.0, 10.2]],
  cuts: [HUB_IN, TEAM_IN, MERGE_IN, TREE_IN, END_IN],
  captions: [[HUB_IN, TEAM_IN, 1040]],
  frame(T) {
    if (T < HUB_IN) titleCard(T, 'GIT', 1.85);
    else if (T < TEAM_IN) sceneHub(T);
    else if (T < MERGE_IN) sceneTeam(T);
    else if (T < TREE_IN) sceneMerge(T);
    else if (T < END_IN) sceneTree(T);
    else endCard(T, END_IN, this.dur);
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('GIT', 1.85); lowerThird.cue(2.3);
    cue(3.7, 'pop', { f: 600, gain: .22 }); cue(5.4, 'pop', { f: 900, gain: .22 }); cue(9.48, 'thud', { f: 70, d: .3, gain: .35 });
    iris.cue(TEAM_IN - .5); cue(10.4, 'pop', { f: 700, gain: .2 }); DEVS.forEach((d, i) => cue(15.46 + i * .15, 'click', { f: 1300 + i * 100, gain: .2 }));
    cue(21.0, 'thud', { f: 90, d: .25, gain: .35 }); cue(23.4, 'chime', { f: 1175, gain: .1 });
    whip.cue(MERGE_IN - .2); cue(26.82, 'whoosh', { d: .5, bright: .5, gain: .35 }); cue(27.4, 'thud', { f: 60, d: .3, gain: .3 }); cue(28.92, 'chime', { f: 988, gain: .1 });
    zoomThrough.cue(TREE_IN - .3); LANES.forEach(([, at]) => cue(at, 'pop', { f: 800, gain: .2 })); cue(40.24, 'pop', { f: 1100, gain: .18 }); cue(42.28, 'chime', { f: 1318, gain: .12 }); burst.cue(42.3);
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};

// Git (the method) vs GitHub (one place it lives), owned by Microsoft.
function sceneHub(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 2.3, 3.6); captions(T);
  const p = back((T - 3.7) / .5); if (p <= 0) return;
  const cx = 540, cy = 1430;
  g.save(); g.translate(cx, cy); g.scale(p, p);
  g.fillStyle = 'rgba(0,28,46,.9)'; g.beginPath(); g.arc(0, 0, 330, 0, 7); g.fill(); g.strokeStyle = CYAN; g.lineWidth = 5; g.stroke();
  font(800, 90, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('Git', 0, -180);
  font(500, 22, MONO); g.fillStyle = CYAN; g.fillText('THE METHOD', 0, -140); g.restore();
  const q = back((T - 5.4) / .45); if (q > 0) { g.save(); g.translate(cx + 40, cy + 50); g.scale(q, q); g.fillStyle = BLUE; g.beginPath(); g.arc(0, 0, 150, 0, 7); g.fill();
    font(800, 70, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('GitHub', 0, 12); font(500, 20, MONO); g.fillText('ONE PLACE IT LIVES', 0, 50); g.restore(); }
  const m = back((T - 9.48) / .35); if (m > 0) { g.save(); g.translate(cx + 250, cy + 230); g.rotate(-.15); g.scale(m * (2 - m), m * (2 - m));
    g.fillStyle = WHITE; g.beginPath(); g.roundRect(-150, -36, 300, 72, 36); g.fill(); font(500, 22, MONO); g.fillStyle = INK; g.textAlign = 'center'; g.fillText('OWNED BY MICROSOFT', 0, 8); g.textAlign = 'left'; g.restore(); }
  g.textAlign = 'left';
}

// One codebase, many developers on separate machines; two edits collide, Git catches it.
const DEVS = [[150, 520], [930, 520], [150, 1420], [930, 1420]];
function laptop(x, y, s, p, hot) { if (p <= 0) return; g.save(); g.translate(x, y); g.scale(p * s, p * s);
  g.fillStyle = hot ? '#F5A524' : '#123247'; g.beginPath(); g.roundRect(-90, -70, 180, 120, 12); g.fill(); g.fillStyle = hot ? '#FFE3B0' : '#0B2233'; g.fillRect(-78, -58, 156, 96);
  g.fillStyle = '#5C7A92'; g.beginPath(); g.moveTo(-110, 55); g.lineTo(110, 55); g.lineTo(95, 72); g.lineTo(-95, 72); g.fill();
  g.fillStyle = hot ? '#9A6200' : CYAN; for (let k = 0; k < 3; k++) g.fillRect(-60, -42 + k * 26, 60 + k * 20, 10); g.restore(); }
function sceneTeam(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('One codebase', 70, 230, T - 10.3, { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  const cx = 540, cy = 970, rp = back((T - 10.4) / .45);
  DEVS.forEach(([x, y], i) => { const q = back((T - 15.46 - i * .15) / .45); if (q <= 0) return;
    const sync = ((T - 17.6) * .9 + i * .25) % 1;
    g.strokeStyle = '#2B4A62'; g.lineWidth = 4; g.setLineDash([10, 10]); g.beginPath(); g.moveTo(x, y); g.lineTo(cx, cy); g.stroke(); g.setLineDash([]);
    if (T > 17.6 && T < 21.6) { g.fillStyle = CYAN; g.beginPath(); g.arc(lerp(x, cx, sync), lerp(y, cy, sync), 9, 0, 7); g.fill(); }
    const clash = T > 21.0 && T < 23.4 && i < 2; laptop(x, y, 1, q, clash);
    font(500, 20, MONO); g.fillStyle = GREY; g.textAlign = 'center'; g.fillText(`DEV ${i + 1}`, x, y + 110); g.textAlign = 'left'; });
  if (rp > 0) { g.save(); g.translate(cx, cy); g.scale(rp, rp); g.shadowColor = 'rgba(0,155,232,.5)'; g.shadowBlur = 40;
    g.fillStyle = BLUE; g.beginPath(); g.roundRect(-170, -120, 340, 240, 28); g.fill(); g.shadowColor = 'transparent';
    font(800, 72, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('app/', 0, -10); font(500, 22, MONO); g.fillText('SAME CODE', 0, 40); g.textAlign = 'left'; g.restore(); }
  // collision → caught
  if (T > 20.82) { const k = back((T - 21.0) / .35); if (k > 0 && T < 23.4) { g.save(); g.translate(cx, 640); g.scale(k, k); g.fillStyle = '#F5A524'; g.beginPath(); g.roundRect(-230, -40, 460, 80, 40); g.fill();
      font(500, 26, MONO); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('SAME LINE, SAME TIME', 0, 9); g.textAlign = 'left'; g.restore(); }
    const ok = back((T - 23.4) / .35); if (ok > 0) { g.save(); g.translate(cx, 640); g.scale(ok, ok); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-230, -40, 460, 80, 40); g.fill();
      font(500, 26, MONO); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('CONFLICT CAUGHT ✓', 0, 9); g.textAlign = 'left'; g.restore(); } }
  rise('Without stepping on toes.', 70, 1720, T - 20.82, { size: 84, w: 800, col: WHITE, dur: .45 });
  faceCircle(540, 1420, 110, back((T - TEAM_IN - .3) / .6));
}

// Separate versions, all at once → zip back together on "merge", reviewed.
function sceneMerge(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Separate versions, all at once', 60, 260, T - 24.16, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  const merge = inOut((T - 26.82) / .8), cols = [CYAN, BLUE, '#C3A6FF'];
  ['you', 'sam', 'alex'].forEach((who, i) => { const q = back((T - 24.58 - i * .15) / .45); if (q <= 0) return;
    const y = lerp(520 + i * 260, 760, merge), x = 90;
    g.save(); g.globalAlpha = i === 0 ? 1 : 1 - clamp((merge - .6) / .4); g.translate(540, y + 100); g.scale(q, q); g.translate(-540, -(y + 100));
    card(x, y, 900, 200, WHITE, 22, .1); g.fillStyle = cols[i]; g.fillRect(x, y, 14, 200);
    font(700, 52, COND); g.fillStyle = INK; g.fillText(i === 0 && merge > .5 ? 'main · merged' : `version · ${who}`, x + 50, y + 80);
    for (let k = 0; k < 3; k++) { g.fillStyle = merge > .5 ? cols[k] : '#E5E7EA'; g.beginPath(); g.roundRect(x + 50 + k * 260, y + 120, 220, 26, 13); g.fill(); }
    g.restore(); });
  rise('Merged back together.', 54, 1130, T - 27.58, { size: 110, w: 800, col: INK, dur: .45 });
  const rv = back((T - 28.92) / .3); if (rv > 0) { g.save(); g.translate(250, 1280); g.scale(rv, rv); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-190, -40, 380, 80, 40); g.fill();
    font(500, 26, MONO); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('REVIEWED ✓', 0, 9); g.textAlign = 'left'; g.restore(); }
  faceCircle(910, 1720, 110, back((T - MERGE_IN - .2) / .6));
}

// The branching tree: feature → development → test → production, all live at once.
const LANES = [['New features', 35.36, '#C3A6FF'], ['Development', 36.62, CYAN], ['Test', 38.06, BLUE], ['Production', 39.58, '#28C941']];
function sceneTree(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('One branching tree', 70, 230, T - 30.5, { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  const trunkX = 160, grow = expo((T - 30.4) / 1.2);
  g.strokeStyle = '#2B4A62'; g.lineWidth = 10; g.lineCap = 'round'; g.beginPath(); g.moveTo(trunkX, 1650); g.lineTo(trunkX, lerp(1650, 380, grow)); g.stroke();
  LANES.forEach(([lab, at, col], i) => { const y = 1500 - i * 300, sprout = expo((T - 31.9 - i * .45) / .6), lit = expo((T - at) / .4), q = sprout; if (q <= 0) return;
    col = lit > .5 ? col : '#3E5A70';
    g.strokeStyle = col; g.lineWidth = 10; g.beginPath(); g.moveTo(trunkX, y + 80); g.quadraticCurveTo(trunkX, y, trunkX + 120, y); g.lineTo(trunkX + 120 + 700 * q, y); g.stroke();
    for (let k = 0; k < 4; k++) { const cx = trunkX + 220 + k * 180; if (cx > trunkX + 120 + 700 * q) continue; g.fillStyle = WHITE; g.beginPath(); g.arc(cx, y, 16, 0, 7); g.fill(); g.strokeStyle = col; g.lineWidth = 5; g.stroke(); }
    // commits flowing up the tree
    if (T > at + .4 && i < 3 && lit > .5) { const t = ((T - at) * .8) % 1; g.fillStyle = col; g.beginPath(); g.arc(trunkX, lerp(y, y - 300, t), 10, 0, 7); g.fill(); }
    if (lit > 0) { g.globalAlpha = lit; font(800, 64, COND); g.fillStyle = WHITE; g.fillText(lab, trunkX + 140, y - 40); g.globalAlpha = 1; } });
  // customers on production
  for (let k = 0; k < 5; k++) { const q = back((T - 40.24 - k * .05) / .3); if (q <= 0) continue; g.save(); g.translate(690 + k * 76, 470); g.scale(q * .85, q * .85);
    g.fillStyle = WHITE; g.beginPath(); g.arc(0, -14, 14, 0, 7); g.fill(); g.beginPath(); g.arc(0, 26, 24, Math.PI, 0); g.fill(); g.restore(); }
  if (T > 40.24) typeOn('Customers', 650, 400, T - 40.3, { size: 22, col: GREY, track: 4, upper: true, cps: 40 });
  const nc = back((T - 42.28) / .35); if (nc > 0) { g.save(); g.translate(540, 1780); g.scale(nc, nc); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-230, -44, 460, 88, 44); g.fill();
    font(800, 54, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('No conflicts ✓', 0, 18); g.textAlign = 'left'; g.restore(); }
  burst(T, 42.3, 540, 1780, 20, 8);
  faceCircle(900, 260, 110, back((T - TREE_IN - .3) / .6));
}
