// Q&A: "What do clients say on the first call that makes me wince?" (18 Oct clip, 21.8s).
const ASK_IN = 3.2, REPLY_IN = 8.2, SHEET_IN = 11.0, RIGHT_IN = 18.0, END_MOS = 21.6, END_IN = END_MOS + .4;
window.EP = {
  dur: 25.0, voEnd: 21.7,
  punchIns: [[6.76, 8.2]],
  cuts: [ASK_IN, REPLY_IN, SHEET_IN, RIGHT_IN, END_IN],
  // v4 (redo pass): deliberate transitions the QC continuity check should ignore (hard cuts get ±0.3 s)
  qcAllow: [[0, 0.6], [2.8, 3.5], [6.5, 7.0], [7.9, 8.5], [10.4, 11.3], [17.7, 18.3], [21.3, 22.3]],
  captions: [[ASK_IN, 8.6, 1240], [RIGHT_IN, END_MOS, 1240]],
  frame(T) {
    if (T < ASK_IN) qOpener(T, 0, ASK_IN, '', ['What makes me wince', 'on a first call?']);
    else if (T < SHEET_IN) sceneChat(T);
    else if (T < RIGHT_IN) sceneSheet(T);
    else if (T < END_IN) sceneRight(T);
    else endCard(T, END_IN, this.dur, 'Q&A', true);   // v4: alive end card
    mosaic(T, END_MOS, 9);
  },
  cues() {
    qOpener.cue(0, ASK_IN); cue(ASK_IN, 'whoosh', { d: .4, gain: .3 }); lowerThird.cue(3.3); bubble.cue(5.32, 'How is this data being tracked?');
    cue(8.64, 'pop', { f: 700, gain: .25 }); cue(10.14, 'thud', { f: 70, d: .3, gain: .4 });
    iris.cue(SHEET_IN - .45); cue(12.74, 'thud', { f: 90, d: .2, gain: .3 }); cue(14.18, 'thud', { f: 80, d: .2, gain: .3 });
    for (let i = 0; i < 6; i++) cue(16.22 + i * .14, 'click', { f: 700 + i * 60, gain: .16 }); cue(17.42, 'thud', { f: 45, d: .4, gain: .4 });
    cue(RIGHT_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(19.5, 'chime', { f: 1175, gain: .12 }); cue(20.5, 'chime', { f: 1318, gain: .1 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};

// His question as a bubble beside the face, then the client's reply bubble + spreadsheet icon.
function sceneChat(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 3.3, 5.1); captions(T);
  const f = faceScreen(zoomAt(T));
  if (T >= 5.32 && T < REPLY_IN) bubble(T, 5.32, REPLY_IN - .1, 'How is this data being tracked?', 540, Math.max(60, f.y - 190), { size: 40 });
  if (T >= 8.64) { const p = back((T - 8.64) / .4); g.save(); g.translate(540, 1500); g.scale(p, p); card(-440, -110, 880, 220, WHITE, 30, .3);
    font(500, 22, MONO); g.letterSpacing = '4px'; g.fillStyle = GREY; g.fillText('THE CLIENT', -400, -60); g.letterSpacing = '0px';
    typeOn('“Well… it all goes into this', -400, 0, T - 8.8, { size: 40, col: INK, w: 600, fam: BODY, track: 0, cps: 30 });
    typeOn('Excel spreadsheet.”', -400, 56, T - 9.9, { size: 40, col: INK, w: 600, fam: BODY, track: 0, cps: 30 }); g.restore();
    const xp = back((T - 10.14) / .4); if (xp > 0) { g.save(); g.translate(860, 1300); g.scale(xp, xp); g.rotate(.12); g.fillStyle = '#1F9D55'; g.beginPath(); g.roundRect(-80, -80, 160, 160, 20); g.fill();
      g.strokeStyle = 'rgba(255,255,255,.7)'; g.lineWidth = 3; for (let k = -1; k <= 1; k++) { g.beginPath(); g.moveTo(-60, k * 34); g.lineTo(60, k * 34); g.moveTo(k * 34, -60); g.lineTo(k * 34, 60); g.stroke(); } g.restore(); } }
  iris(T, SHEET_IN - .45, 860, 1300, sceneSheet);
}

// The ancient spreadsheet: old file, author gone, cells full of errors.
const ERR = ['#REF!', '#VALUE!', '#N/A', '####', '#DIV/0!', '??', 'TBC', 'see Dave'];
function sceneSheet(T) {
  g.fillStyle = '#E9EDF1'; g.fillRect(0, 0, W, H);
  const p = expo((T - SHEET_IN + .3) / .5), push = 1 + .04 * clamp((T - SHEET_IN) / 7); g.save(); g.translate(540, 840); g.scale(push, push); g.translate(-540, -840); g.globalAlpha = p; card(40, 220, 1000, 1040, WHITE, 18, .2);
  g.fillStyle = '#1F7A44'; g.beginPath(); g.roundRect(40, 220, 1000, 90, [18, 18, 0, 0]); g.fill();
  font(500, 26, MONO); g.fillStyle = WHITE; g.fillText('MASTER_tracker_FINAL_v7(2).xlsx', 80, 276);
  const cols = 5, rows = 10, cw = 184, rh = 82, ox = 60, oy = 330; font(500, 24, MONO);
  let rank = 0;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) { const x = ox + c * cw, y = oy + r * rh; if (T < SHEET_IN - .2 + r * .09) continue;
    g.strokeStyle = '#D9DDE1'; g.lineWidth = 1; g.strokeRect(x, y, cw, rh);
    const order = ((r * 7 + c * 3) % 13) / 13 + ((r * 5 + c) % 7) / 70, bad = r > 0 && T > 13.7 + order * 3.6, rr = rng(r * 9 + c);
    if (r === 0) { g.fillStyle = '#F3F3F3'; g.fillRect(x, y, cw, rh); g.fillStyle = INK; g.fillText(['ID', 'Client', 'Due', 'Status', 'Notes'][c], x + 14, y + 50); }
    else if (bad) { g.fillStyle = 'rgba(245,165,36,.18)'; g.fillRect(x, y, cw, rh); g.fillStyle = '#B54708'; g.fillText(ERR[Math.floor(rr() * ERR.length)], x + 14, y + 50); }
    else { g.fillStyle = '#9AA0A6'; g.fillRect(x + 14, y + 34, 40 + rr() * 110, 14); } }
  g.restore();
  // stamps on "10 years ago" and "not even in the company anymore"
  [['BUILT 10 YEARS AGO', 12.74, 300, 1370, -.06], ['AUTHOR LEFT THE COMPANY', 14.18, 640, 1500, .05]].forEach(([txt, at, x, y, rot]) => { const q = back((T - at) / .3); if (q <= 0) return;
    g.save(); g.translate(x, y); g.rotate(rot); g.scale(q * (2 - q), q * (2 - q)); font(800, 46, COND); const w = g.measureText(txt).width + 50;
    g.fillStyle = '#F3F3F3'; g.beginPath(); g.roundRect(-w / 2, -48, w, 96, 12); g.fill(); g.strokeStyle = '#F5A524'; g.lineWidth = 7; g.stroke(); g.fillStyle = '#F5A524'; g.textAlign = 'center'; g.fillText(txt, 0, 18); g.textAlign = 'left'; g.restore(); });
  rise('Complete and utter garbage.', 54, 1650, T - 16.22, { size: 84, w: 800, col: INK, dur: .45 });   // v4: clear of the face circle (v3 overlapped it)
  faceCircle(920, 1790, 100, back((T - SHEET_IN - .2) / .6));
}

// "That's when I know we're talking to the right people": check card + "real difference" chip beside the torso.
function sceneRight(T) {
  th(FULL, BZ); captions(T);
  const p = back((T - 19.45) / .4); if (p > 0) { g.save(); g.translate(300, 1460); g.scale(p, p); card(-230, -110, 460, 220, CYAN, 28, .3);
    font(800, 64, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('Right people ✓', 0, 22); g.textAlign = 'left'; g.restore(); }
  const q = back((T - 20.5) / .45); if (q > 0) { g.save(); g.translate(800, 1460); g.scale(q, q); card(-200, -110, 400, 220, NAVY, 28, .35);
    g.strokeStyle = CYAN; g.lineWidth = 12; g.lineCap = 'round'; g.lineJoin = 'round'; const a = expo((T - 20.6) / .5);
    g.beginPath(); g.moveTo(-140, 30); g.lineTo(-140 + 80 * clamp(a * 3), 30 - 40 * clamp(a * 3)); if (a > .33) g.lineTo(-60 + 60 * clamp(a * 3 - 1), -10 + 20 * clamp(a * 3 - 1)); if (a > .66) g.lineTo(0 + 120 * clamp(a * 3 - 2), 10 - 80 * clamp(a * 3 - 2)); g.stroke();
    if (a > .95) { g.beginPath(); g.moveTo(90, -70); g.lineTo(120, -70); g.lineTo(120, -40); g.stroke(); }
    font(700, 46, COND); g.fillStyle = WHITE; g.fillText('A real difference', -165, 88); g.restore(); }
}
