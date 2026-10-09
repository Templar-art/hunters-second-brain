// IDE: integrated development environment (07 Oct clip, 33.9s).
const PIECES_IN = 2.6, IDE_IN = 9.25, FEAT_IN = 18.0, AI_IN = 26.85, END_MOS = 33.6, END_IN = END_MOS + .4;
window.EP = {
  dur: 37.0, voEnd: 33.7,
  punchIns: [[5.0, 7.2], [23.5, 26.85]],
  cuts: [PIECES_IN, IDE_IN, FEAT_IN, AI_IN, END_IN],
  captions: [[PIECES_IN, IDE_IN, 1000], [FEAT_IN, AI_IN, 1780]],
  frame(T) {
    if (T < PIECES_IN) titleCard(T, 'IDE', 2.3);
    else if (T < IDE_IN) scenePieces(T);
    else if (T < FEAT_IN) sceneIDE(T, false);
    else if (T < AI_IN) sceneFeatures(T);
    else if (T < END_IN) sceneIDE(T, true);
    else endCard(T, END_IN, this.dur);
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('IDE', 2.3); lowerThird.cue(2.7);
    PIECES.forEach(([, , , at]) => cue(at, 'whoosh', { d: .3, bright: .45, gain: .22 })); cue(8.58, 'thud', { f: 55, d: .4, gain: .5 }); burst.cue(8.6);
    iris.cue(IDE_IN - .5);
    cue(9.84, 'whoosh', { d: .3, gain: .25 }); cue(11.1, 'typing', { n: 8, cps: 20 }); cue(13.02, 'whoosh', { d: .25, bright: .4, gain: .2 });
    cue(14.4, 'whoosh', { d: .3, gain: .25 }); cue(15.0, 'typing', { n: 8, cps: 20 }); cue(16.5, 'chime', { f: 1175, gain: .1 });
    cue(FEAT_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(21.04, 'pop', { f: 800, gain: .2 }); cue(22.58, 'pop', { f: 950, gain: .2 });
    for (let i = 0; i < 12; i += 3) cue(22.5 + i * .1, 'pop', { f: 900 + i * 40, d: .05, gain: .12 });
    zoomThrough.cue(AI_IN - .3); cue(28.0, 'whoosh', { d: .35, bright: .4, gain: .3 }); cue(29.46, 'pop', { f: 1000, gain: .2 });
    cue(31.0, 'typing', { n: 8, cps: 22 }); cue(32.3, 'chime', { f: 988, gain: .1 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};

// "Pieces together … in one place": four tiles fly in from the corners and lock into one block.
const PIECES = [['Editor', -1, -1, 4.18], ['Files', 1, -1, 4.58], ['Terminal', -1, 1, 5.7], ['Git', 1, 1, 6.52]];
function scenePieces(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 2.7, 4.0); captions(T);
  const join = inOut((T - 8.3) / .35), cx = 540, cy = 1430, s = 200;
  PIECES.forEach(([lab, dx, dy, at], i) => { const p = expo((T - at) / .55); if (p <= 0) return;
    const gap = lerp(26, 0, join), tx = cx + dx * (s / 2 + gap / 2), ty = cy + dy * (s * .42 + gap / 2);
    const x = tx + dx * (1 - p) * 700, y = ty + dy * (1 - p) * 500;
    g.save(); g.translate(x, y); g.rotate((1 - p) * dx * .6);
    card(-s / 2, -s * .42, s, s * .84, i % 3 === 0 ? NAVY : WHITE, 18, .3);
    font(800, 50, COND); g.fillStyle = i % 3 === 0 ? CYAN : INK; g.textAlign = 'center'; g.fillText(lab, 0, 16); g.textAlign = 'left'; g.restore(); });
  if (join > .95) { g.strokeStyle = CYAN; g.lineWidth = 6; g.beginPath(); g.roundRect(cx - s, cy - s * .84, s * 2, s * 1.68, 22); g.stroke();
    font(500, 26, MONO); g.letterSpacing = '5px'; g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('ONE PLACE', cx, cy + s + 30); g.textAlign = 'left'; g.letterSpacing = '0px'; }
  burst(T, 8.6, cx, cy, 22, 5);
  iris(T, IDE_IN - .5, cx, cy, T => sceneIDE(T, false));
}

// The IDE window assembles panel by panel (editor, file tree, terminal), later an AI chat panel.
const SRC = ['function onTime(bus) {', '  const late = bus.eta - bus.due;', '  return late <= 60;', '}'];
function sceneIDE(T, ai) {
  g.fillStyle = '#E9EDF1'; g.fillRect(0, 0, W, H);
  const p = expo((T - (ai ? AI_IN : IDE_IN)) / .55), x = 40, y = 280, w = 1000, h = 1180;
  typeOn(ai ? 'And nowadays' : 'Typically you get', 60, 200, T - (ai ? AI_IN + .1 : 9.36), { size: 28, col: BLUE, track: 6, upper: true, cps: 30 });
  g.save(); g.globalAlpha = clamp(p * 2); g.translate(0, (1 - p) * 120);
  card(x, y, w, h, '#0D1620', 26, .35);
  g.fillStyle = '#16222C'; g.beginPath(); g.roundRect(x, y, w, 64, [26, 26, 0, 0]); g.fill();
  ['#FF6159', '#FFBD2E', '#28C941'].forEach((c, i) => { g.fillStyle = c; g.beginPath(); g.arc(x + 36 + i * 28, y + 32, 9, 0, 7); g.fill(); });
  font(500, 22, MONO); g.fillStyle = GREY; g.fillText('use-project — IDE', x + 420, y + 40);
  // file tree (left)
  const cpA = ai ? expo((T - 28.0) / .5) : 0, ft = ai ? 1 - cpA : expo((T - 13.02) / .45), tw = ai ? 380 * cpA + 260 * (1 - cpA) : 260 * ft;
  if (ft > 0.02) { g.fillStyle = '#111D28'; g.fillRect(x, y + 64, tw, h - 64);
    ['src/', '  app.js', '  bus.js', 'tests/', 'README.md'].forEach((f, i) => { g.globalAlpha = ft; font(500, 24, MONO); g.fillStyle = i === 2 ? CYAN : '#9FB3C4'; g.fillText(f, x + 24, y + 120 + i * 46); });
    g.globalAlpha = 1; }
  // editor (centre)
  const ed = ai ? 1 : expo((T - 9.3) / .35);
  if (ed > 0) { const ex = x + tw + 24; g.globalAlpha = ed; font(500, 22, MONO); g.fillStyle = '#5C7A92'; g.fillText('bus.js', ex, y + 110);
    let chars = ai ? 999 : Math.floor((T - 11.08) * 22);
    SRC.forEach((l, i) => { const n = clamp(chars, 0, l.length); chars -= l.length; font(500, 25, MONO); g.fillStyle = '#3E5466'; g.fillText(String(i + 1), ex, y + 170 + i * 48);
      if (n > 0) { g.fillStyle = i === 0 ? '#7FD6FF' : WHITE; g.fillText(l.slice(0, n), ex + 44, y + 170 + i * 48); } });
    g.globalAlpha = 1; }
  // terminal (bottom)
  const tm = ai ? 1 : expo((T - 14.4) / .45), th2 = 300 * tm;
  if (tm > 0) { const ty = y + h - th2; g.fillStyle = '#081018'; g.fillRect(x + tw, ty, w - tw, th2); g.fillStyle = '#1E2C38'; g.fillRect(x + tw, ty, w - tw, 3);
    font(500, 22, MONO); g.fillStyle = '#5C7A92'; g.fillText('TERMINAL', x + tw + 24, ty + 40);
    typeOn('$ npm test', x + tw + 24, ty + 100, ai ? 9 : T - 15.0, { size: 28, col: WHITE, track: 0, cps: 20, caret: !ai && T < 16.5 });
    if (ai || T > 16.5) { font(500, 28, MONO); g.fillStyle = CYAN; g.fillText('✓ 12 passing', x + tw + 24, ty + 150); } }
  // AI chat panel (right) slides in on "agent or chat window"
  if (ai) { const cp = cpA, cw = 380 * cp, cx = x;
    g.fillStyle = '#132231'; g.fillRect(cx, y + 64, cw, h - 64 - 300); g.fillStyle = CYAN; g.fillRect(cx + cw - 3, y + 64, 3, h - 364);
    if (cp > .6) { font(500, 22, MONO); g.fillStyle = CYAN; g.fillText('AGENT', cx + 24, y + 110);
      const b1 = back((T - 29.46) / .35); if (b1 > 0) { g.save(); g.translate(cx + 30, y + 150); g.scale(b1, b1); g.fillStyle = BLUE; g.beginPath(); g.roundRect(0, 0, 320, 90, 18); g.fill();
        font(600, 26, BODY); g.fillStyle = WHITE; g.fillText('Make late buses', 20, 38); g.fillText('flag after 2 min', 20, 70); g.restore(); }
      const b2 = back((T - 30.6) / .35); if (b2 > 0) { g.save(); g.translate(cx + 30, y + 270); g.scale(b2, b2); g.fillStyle = '#1E3446'; g.beginPath(); g.roundRect(0, 0, 320, 90, 18); g.fill();
        font(600, 26, BODY); g.fillStyle = WHITE; g.fillText('Done: 1 file', 20, 38); g.fillText('changed ✓', 20, 70); g.restore(); }
      // API key field
      const kp = expo((T - 31.0) / .4); if (kp > 0) { g.globalAlpha = kp; g.fillStyle = '#0B1620'; g.strokeStyle = '#2B4A62'; g.lineWidth = 2;
        g.beginPath(); g.roundRect(cx + 30, y + 420, 320, 70, 14); g.fill(); g.stroke(); font(500, 18, MONO); g.fillStyle = GREY; g.fillText('YOUR API KEY', cx + 44, y + 446);
        typeOn('connected ✓', cx + 44, y + 476, T - 31.2, { size: 24, col: CYAN, track: 2, cps: 22 }); g.globalAlpha = 1; }
      if (T > 32.3) { const lp = back((T - 32.3) / .35); g.save(); g.translate(cx + 190, y + 570); g.scale(lp, lp);
        font(500, 22, MONO); g.fillStyle = CYAN; g.textAlign = 'center'; g.fillText('● RUNS LOCALLY', 0, 0); g.textAlign = 'left'; g.restore(); } } }
  g.restore();
  // headline under the window
  if (!ai) { rise('One window.', 54, 1640, T - 9.84, { size: 130, w: 800, col: INK, dur: .45 }); }
  else { rise('AI built in.', 54, 1640, T - 27.3, { size: 130, w: 800, col: INK, dur: .45 }); }
  faceCircle(910, 1700, 120, back((T - (ai ? AI_IN : IDE_IN) - .3) / .6));
}

// Features: speaker column left; right side shows Git branches, then a plugin marketplace.
function sceneFeatures(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  const p = inOut((T - FEAT_IN) / .6), colW = lerp(W, 470, p);
  g.save(); g.beginPath(); g.rect(0, 0, colW, H); g.clip(); th({ x: 0, y: 0, w: colW, h: H }, lerp(BZ, 1.0, p), .3); g.restore();
  g.fillStyle = CYAN; g.fillRect(colW - 4, 0, 4, H);
  const x = 510;
  typeOn('Built-in features', x, 220, T - 18.4, { size: 24, col: CYAN, track: 5, upper: true, cps: 40 });
  // Git branch graph
  const gp = expo((T - 18.6) / .8);
  if (gp > 0) { font(800, 80, COND); g.fillStyle = WHITE; g.globalAlpha = gp; g.fillText('Git', x, 360); g.globalAlpha = 1;
    g.strokeStyle = '#5C7A92'; g.lineWidth = 6; g.lineCap = 'round';
    g.beginPath(); g.moveTo(x + 20, 440); g.lineTo(x + 20 + 480 * gp, 440); g.stroke();
    g.strokeStyle = CYAN; g.beginPath(); g.moveTo(x + 140, 440); g.quadraticCurveTo(x + 180, 520, x + 260, 520); g.lineTo(x + 260 + 120 * clamp(gp * 1.4 - .4), 520); g.stroke();
    [[20, 440], [140, 440], [260, 520], [380, 520], [500, 440]].forEach(([dx, dy], i) => { const q = back((T - 18.8 - i * .3) / .3); if (q <= 0) return;
      g.fillStyle = dy > 440 ? CYAN : WHITE; g.beginPath(); g.arc(x + dx, dy, 14 * q, 0, 7); g.fill(); });
    font(500, 22, MONO); g.fillStyle = GREY; g.fillText('main', x + 20, 420); g.fillStyle = CYAN; g.fillText('feature', x + 270, 560); }
  // plugins
  const pp = expo((T - 22.36) / .5);
  if (pp > 0) { font(800, 80, COND); g.globalAlpha = pp; g.fillStyle = WHITE; g.fillText('Plugins', x, 720); g.globalAlpha = 1; }
  const ICON = ['{ }', '#', '▶', 'Aa', '⚙', '◐', '✓', '⇄', '☁', '⌘', '◆', '✎'];
  ICON.forEach((ic, i) => { const q = back((T - 22.5 - i * .1) / .35); if (q <= 0) return; const cx = x + 60 + (i % 4) * 130, cy = 820 + Math.floor(i / 4) * 140;
    g.save(); g.translate(cx + 50, cy + 50); g.scale(q, q); g.fillStyle = i % 5 ? '#123247' : BLUE; g.beginPath(); g.roundRect(-50, -50, 100, 100, 20); g.fill();
    font(700, 40, BODY); g.fillStyle = i % 5 ? CYAN : WHITE; g.textAlign = 'center'; g.fillText(ic, 0, 14); g.textAlign = 'left'; g.restore(); });
  if (T > 25.0) typeOn('Third-party marketplace', x, 1290, T - 25.22, { size: 24, col: CYAN, track: 4, upper: true, cps: 40 });
  captions(T);
  zoomThrough(T, AI_IN - .3, 700, 1000, () => {}, () => {}, .3);
}
