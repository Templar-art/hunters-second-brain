// SDK: software development kit (05 Oct clip, 24.6s).
const PREV_IN = 2.2, WRAP_IN = 5.2, CALLS_IN = 13.8, STACK_IN = 19.9, END_MOS = 23.9, END_IN = END_MOS + .4;
window.EP = {
  dur: 27.4, voEnd: 23.9,
  punchIns: [[3.7, 5.2]],
  captions: [[PREV_IN, WRAP_IN, 1240], [CALLS_IN, STACK_IN, 1000]],
  frame(T) {
    if (T < PREV_IN) titleCard(T, 'SDK', 1.9);
    else if (T < WRAP_IN) scenePrev(T);
    else if (T < CALLS_IN) sceneWrap(T);
    else if (T < STACK_IN) sceneCalls(T);
    else if (T < END_IN) sceneStack(T);
    else endCard(T, END_IN, this.dur);
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('SDK', 1.9); lowerThird.cue(2.4);
    cue(3.3, 'whoosh', { d: .4, bright: .5, gain: .35 }); cue(3.74, 'pop', { f: 900, gain: .25 });
    zoomThrough.cue(WRAP_IN - .35);
    cue(5.6, 'pop', { f: 600, gain: .25 }); [5.9, 7.48, 8.32].forEach((t, i) => { cue(t, 'whoosh', { d: .3, bright: .3, gain: .2 }); cue(t + .2, 'thud', { f: 70 + i * 15, d: .2, gain: .25 }); });
    cue(9.6, 'chime', { f: 988, gain: .1 }); [11.02, 11.2, 11.4].forEach(t => cue(t, 'click', { gain: .25 })); cue(12.02, 'chime', { f: 1318, gain: .1 });
    cue(CALLS_IN - .1, 'whoosh', { d: .5, gain: .4 }); CALLS.forEach(([c, , at]) => { cue(at, 'typing', { n: c.length, cps: 40 }); cue(at + c.length / 40 + .15, 'pop', { f: 1100, gain: .15 }); });
    whip.cue(STACK_IN - .25); LAYERS.forEach(([, , at], i) => cue(at, 'thud', { f: 60 + i * 20, d: .3, gain: .35 })); burst.cue(22.55);
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};

// Callback: "we talked about APIs earlier on this series" → a 'previously' card spins in over the head.
function scenePrev(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 2.4, 3.6); captions(T);
  const p = back((T - 3.3) / .6); if (p <= 0) return;
  const x = 600, y = 140, w = 420, h = 520;
  g.save(); g.translate(x + w / 2, y + h / 2); g.rotate(.06 + (1 - clamp(p)) * .5); g.scale(p, p); g.translate(-(x + w / 2), -(y + h / 2));
  card(x, y, w, h, NAVY, 24, .45);
  typeOn('Previously on', x + 34, y + 70, T - 3.5, { size: 22, col: GREY, track: 4, upper: true, cps: 40 });
  font(800, 64, COND); g.fillStyle = WHITE; g.fillText('Definitions', x + 34, y + 140);
  g.fillStyle = BLUE; g.beginPath(); g.roundRect(x + 110, y + 230, 200, 110, 18); g.fill();
  font(800, 70, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('API', x + 210, y + 310); g.textAlign = 'left';
  g.strokeStyle = '#5C7A92'; g.lineWidth = 3; line2(x + 40, y + 285, x + 110, y + 285); line2(x + 310, y + 285, x + 380, y + 285);
  g.fillStyle = CYAN; g.beginPath(); g.roundRect(x + 34, y + 420, 160, 50, 25); g.fill(); font(500, 22, MONO); g.fillStyle = NAVY; g.fillText('EP · API', x + 56, y + 453);
  g.restore();
}
function line2(a, b, c, d) { g.beginPath(); g.moveTo(a, b); g.lineTo(c, d); g.stroke(); }

// Wrapping: an API block gets wrapped in layered shells → SDK, then developers plug in.
function sceneWrap(T) {
  const wy = whip(T, CALLS_IN - .3);
  g.save(); g.translate(0, wy);
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  const cx = 540, cy = 820;
  typeOn('A way of wrapping', 80, 300, T - 5.62, { size: 30, col: CYAN, track: 6, upper: true, cps: 30 });
  // concentric shells: each wrap layer gets its own outline + tag
  [[8.32, 330, 'SDK', CYAN, 5], [7.48, 250, 'HELPERS', '#5C9DC0', 3], [5.9, 180, 'AUTH', '#3E6E8C', 3]].forEach(([at, r, tag, col, lw], i) => {
    const p = back((T - at) / .5); if (p <= 0) return; const rw = r * 1.45 * p, rh = r * .95 * p;
    g.save(); g.fillStyle = ['#0E3A57', '#0B3048', '#082539'][i]; g.strokeStyle = col; g.lineWidth = lw;
    g.beginPath(); g.roundRect(cx - rw, cy - rh, rw * 2, rh * 2, 36); g.fill(); g.stroke();
    if (i > 0) { font(500, 20, MONO); g.letterSpacing = '3px'; g.fillStyle = col; g.fillText(tag, cx - rw + 22, cy - rh + 36); g.letterSpacing = '0px'; }
    g.restore();
  });
  // API block at the core
  const pa = back((T - 5.6) / .45);
  if (pa > 0) { g.save(); g.translate(cx, cy); g.scale(pa, pa); g.shadowColor = 'rgba(0,155,232,.6)'; g.shadowBlur = 40; g.fillStyle = BLUE;
    g.beginPath(); g.roundRect(-170, -70, 340, 140, 22); g.fill(); g.shadowColor = "transparent";
    font(800, 84, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(T > 8.32 ? 'Backend' : 'API', 0, 30); g.textAlign = 'left'; g.restore(); }
  // SDK label on the outer shell
  if (T > 8.5) { const q = expo((T - 8.5) / .4); g.save(); g.globalAlpha = q; g.fillStyle = CYAN; g.beginPath(); g.roundRect(cx - 80, cy - 345, 160, 64, 32); g.fill();
    font(800, 48, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('SDK', cx, cy - 297); g.textAlign = 'left'; g.restore(); }
  // developers plug in
  [[150, 1380], [540, 1460], [930, 1380]].forEach(([x, y], i) => { const p = back((T - 11.02 - i * .18) / .45); if (p <= 0) return;
    const L = expo((T - 11.2 - i * .18) / .5); g.strokeStyle = CYAN; g.lineWidth = 4; g.setLineDash([10, 10]);
    g.beginPath(); g.moveTo(x, y - 70); g.lineTo(lerp(x, cx + (x - cx) * .3, L), lerp(y - 70, cy + 230, L)); g.stroke(); g.setLineDash([]);
    g.save(); g.translate(x, y); g.scale(p, p); g.fillStyle = WHITE; g.beginPath(); g.arc(0, 0, 62, 0, 7); g.fill();
    g.strokeStyle = INK; g.lineWidth = 5; g.beginPath(); g.arc(0, -12, 16, 0, 7); g.stroke(); g.beginPath(); g.arc(0, 40, 30, Math.PI * 1.1, Math.PI * 1.9); g.stroke();
    font(500, 22, MONO); g.fillStyle = CYAN; g.textAlign = 'center'; g.fillText('DEV', 0, 100); g.textAlign = 'left'; g.restore(); });
  rise('Easier access.', 80, 1700, T - 12.02, { size: 130, w: 800, col: WHITE, dur: .45 });
  g.restore();
}

// Inset layout: speaker in a framed top card, SDK calls type below as he lists them.
const CALLS = [['sdk.records.list({ page: 2 })', '25 records', 15.3], ['sdk.records.get(id)', '1 record', 16.4], ['sdk.bulk.update(rows)', '500 updated', 17.44],
  ['sdk.users.create(user)', 'created', 18.7], ['sdk.users.delete(id)', 'deleted', 19.18]];
function sceneCalls(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  const p = expo((T - CALLS_IN) / .55), r = { x: 60, y: 60 + (1 - p) * -900, w: 960, h: 860 };
  card(r.x, r.y, r.w, r.h, NAVY, 34, .3); g.save(); g.beginPath(); g.roundRect(r.x + 8, r.y + 8, r.w - 16, r.h - 16, 28); g.clip(); th({ x: r.x + 8, y: r.y + 8, w: r.w - 16, h: r.h - 16 }, 1.1, .38); g.restore();
  g.strokeStyle = CYAN; g.lineWidth = 4; g.beginPath(); g.roundRect(r.x, r.y, r.w, r.h, 34); g.stroke();
  const x = 60, y = 1080;
  typeOn('What an SDK makes easy', x, y, T - 14.2, { size: 26, col: BLUE, track: 5, upper: true, cps: 40 });
  CALLS.forEach(([c, out, at], i) => { const ly = y + 90 + i * 150, t = T - at; if (t <= -.3) return;
    const q = expo((t + .3) / .4); g.save(); g.globalAlpha = q; card(x, ly - 70, 960, 120, WHITE, 18, .08); g.restore();
    if (t <= 0) return;
    font(500, 32, MONO); g.fillStyle = BLUE; g.fillText('›', x + 30, ly + 4);
    typeOn(c, x + 64, ly + 4, t, { size: 32, col: INK, track: 0, cps: 40, caret: t < c.length / 40 + .1 });
    const d = t - c.length / 40 - .15; if (d > 0) { const pp = back(d / .35); g.save(); g.translate(x + 870, ly - 6); g.scale(pp, pp);
      font(500, 22, MONO); const w = g.measureText(out).width + 28; g.fillStyle = CYAN; g.beginPath(); g.roundRect(-w / 2, -22, w, 44, 22); g.fill();
      g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText(out, 0, 8); g.textAlign = 'left'; g.restore(); } });
  captions(T);
}

// Layer cake: existing system → SDK → your app dropping on top.
const LAYERS = [['Existing system', '#AEB4BA', 20.4], ['SDK', BLUE, 21.36], ['Your app', CYAN, 22.4]];
function sceneStack(T) {
  g.fillStyle = WHITE; g.fillRect(0, 0, W, H);
  typeOn('Build on top of what exists', 60, 330, T - 20.2, { size: 30, col: BLUE, track: 5, upper: true, cps: 40 });
  rise('On top.', 54, 560, T - 22.4, { size: 200, w: 800, col: INK, dur: .45 });
  LAYERS.forEach(([lab, col, at], i) => { const y = 1500 - i * 230, p = clamp((T - at) / .45), b = back(p), drop = (1 - expo(p)) * -900;
    if (p <= 0) return; const squash = 1 + (1 - clamp(b)) * .2;
    g.save(); g.translate(540, y + 100 + drop); g.scale(1, i < 2 ? 1 : 1 / squash); g.translate(-540, -(y + 100));
    card(140, y, 800, 200, col, 28, .2);
    font(800, 92, COND); g.fillStyle = i === 0 ? INK : (i === 1 ? WHITE : NAVY); g.textAlign = 'center'; g.fillText(lab, 540, y + 132); g.textAlign = 'left'; g.restore(); });
  burst(T, 22.55, 540, 1040, 22, 6);
  faceCircle(900, 200, 120, back((T - STACK_IN) / .6));
}
