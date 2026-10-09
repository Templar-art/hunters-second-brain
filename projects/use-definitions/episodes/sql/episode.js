// SQL: structured query language (16 Oct clip, 40.6s).
const OLD_IN = 2.2, QUERY_IN = 7.5, CLEAN_IN = 12.2, NOSQL_IN = 16.4, TABLE_IN = 24.9, REL_IN = 31.3, END_MOS = 40.4, END_IN = END_MOS + .4;
window.EP = {
  dur: 43.8, voEnd: 40.5,
  punchIns: [[4.9, 7.5], [20.0, 24.9]],
  cuts: [OLD_IN, QUERY_IN, CLEAN_IN, NOSQL_IN, TABLE_IN, REL_IN, END_IN],
  captions: [[OLD_IN, QUERY_IN, 1040], [NOSQL_IN, TABLE_IN, 1040]],
  frame(T) {
    if (T < OLD_IN) titleCard(T, 'SQL', 1.95);
    else if (T < QUERY_IN) sceneOld(T);
    else if (T < CLEAN_IN) sceneQuery(T);
    else if (T < NOSQL_IN) sceneClean(T);
    else if (T < TABLE_IN) sceneNoSQL(T);
    else if (T < REL_IN) sceneTable(T);
    else if (T < END_IN) sceneRel(T);
    else endCard(T, END_IN, this.dur);
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('SQL', 1.95); lowerThird.cue(2.3); cue(3.04, 'whoosh', { d: .4, bright: .4, gain: .25 }); cue(4.46, 'pop', { f: 900, gain: .2 }); cue(5.3, 'thud', { f: 60, d: .3, gain: .35 });
    iris.cue(QUERY_IN - .5); cue(7.6, 'typing', { n: 14, cps: 30 }); cue(10.46, 'riser', { d: .4, gain: .12 }); [10.5, 10.6, 10.7, 10.8].forEach((t, i) => cue(t, 'pop', { f: 700 + i * 100, d: .05, gain: .14 }));
    cue(11.34, 'whoosh', { d: .3, bright: .5, gain: .25 });
    whip.cue(CLEAN_IN - .2); cue(14.18, 'thud', { f: 90, d: .2, gain: .25 }); cue(14.8, 'whoosh', { d: .4, gain: .3 }); cue(15.3, 'chime', { f: 988, gain: .1 });
    cue(NOSQL_IN - .1, 'whoosh', { d: .45, gain: .35 }); cue(18.74, 'thud', { f: 100, d: .2, gain: .25 }); cue(20.34, 'pop', { f: 1000, gain: .2 });
    cue(TABLE_IN - .1, 'whoosh', { d: .45, gain: .35 }); [25.76, 27.34, 28.5, 29.9].forEach(t => cue(t, 'click', { gain: .25 }));
    zoomThrough.cue(REL_IN - .3); [34.46, 36.68, 38.94].forEach(t => cue(t, 'thud', { f: 70, d: .25, gain: .3 }));
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};
function pillS(txt, x, y, p, bg = CYAN, fg = NAVY, size = 28) { if (p <= 0) return; g.save(); g.translate(x, y); g.scale(p, p); font(500, size, MONO); g.letterSpacing = '2px';
  const w = g.measureText(txt).width + 40; g.fillStyle = bg; g.beginPath(); g.roundRect(-w / 2, -size, w, size * 2, size); g.fill(); g.fillStyle = fg; g.textAlign = 'center'; g.fillText(txt, 0, size * .35); g.textAlign = 'left'; g.letterSpacing = '0px'; g.restore(); }

// "Very old but still very popular and powerful": 1970s → today timeline under the chin.
function sceneOld(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 2.3, 3.0); captions(T);
  const p = expo((T - 3.04) / .5); if (p <= 0) return;
  g.save(); g.globalAlpha = p; card(60, 1180, 960, 360, NAVY, 26, .35);
  g.strokeStyle = '#2B4A62'; g.lineWidth = 8; g.lineCap = 'round'; g.beginPath(); g.moveTo(130, 1330); g.lineTo(950, 1330); g.stroke();
  g.strokeStyle = CYAN; g.beginPath(); g.moveTo(130, 1330); g.lineTo(130 + 820 * expo((T - 3.2) / 1.2), 1330); g.stroke();
  font(800, 54, COND); g.fillStyle = WHITE; g.fillText('1970s', 110, 1420); g.textAlign = 'right'; g.fillText('Today', 970, 1420); g.textAlign = 'left';
  g.fillStyle = CYAN; g.beginPath(); g.arc(130 + 820 * expo((T - 3.2) / 1.2), 1330, 18, 0, 7); g.fill();
  pillS('STILL POPULAR', 330, 1250, back((T - 4.46) / .35)); pillS('POWERFUL', 760, 1250, back((T - 5.3) / .35), BLUE, WHITE);
  g.restore();
}

// Reading data for analytics: a query types, then a result chart builds. "Transforming" swaps the verb.
function sceneQuery(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn(T < 11.34 ? 'Reading data' : 'Transforming data', 70, 250, T - (T < 11.34 ? 7.5 : 11.34), { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  card(60, 320, 960, 300, '#020B12', 22, .4);
  const q = T < 11.34 ? ['SELECT city, COUNT(*)', 'FROM users', 'GROUP BY city;'] : ['UPDATE users', 'SET city = TRIM(city)', 'WHERE city IS NOT NULL;'];
  let chars = Math.floor((T - (T < 11.34 ? 7.6 : 11.4)) * 34);
  q.forEach((l, i) => { const n = clamp(chars, 0, l.length); chars -= l.length; if (n <= 0) return; font(500, 38, MONO);
    const kw = /^(SELECT|FROM|GROUP BY|UPDATE|SET|WHERE)/.exec(l); g.fillStyle = BLUE; const s = l.slice(0, n);
    if (kw && n >= kw[0].length) { g.fillText(kw[0], 100, 410 + i * 70); g.fillStyle = WHITE; g.fillText(s.slice(kw[0].length), 100 + g.measureText(kw[0]).width, 410 + i * 70); } else { g.fillText(s, 100, 410 + i * 70); } });
  if (T < 11.34) { const bars = [['Gold Coast', .9], ['Brisbane', .7], ['Sydney', .5], ['Perth', .3]];
    bars.forEach(([c, v], i) => { const p = expo((T - 9.9 - i * .1) / .45); if (p <= 0) return; const y = 760 + i * 170;
      font(700, 44, COND); g.fillStyle = WHITE; g.fillText(c, 80, y + 50); const gr = g.createLinearGradient(380, 0, 1000, 0); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN);
      g.fillStyle = gr; g.beginPath(); g.roundRect(380, y, 600 * v * p, 70, 14); g.fill(); });
    rise('For analytics.', 70, 1600, T - 10.46, { size: 130, w: 800, col: WHITE, dur: .45 }); }
  else { rise('And transforming.', 70, 1600, T - 11.34, { size: 130, w: 800, col: CYAN, dur: .45 });
    pillS('✓ 1,204 ROWS UPDATED', 540, 800, back((T - 11.9) / .35)); }
  faceCircle(900, 1790, 100, back((T - QUERY_IN - .3) / .6));
}

// Raw, unclean data funnels into a clean table.
function sceneClean(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Loading raw data', 60, 240, T - 12.5, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  const raw = ['  sam BRUHN ,gold coast', 'NULL, , brisbane!!', 'Jo lee;;  SYDNEY', 'alex kim ,  perth  '], clean = ['Sam Bruhn · Gold Coast', 'Jo Lee · Sydney', 'Alex Kim · Perth'];
  raw.forEach((r, i) => { const p = expo((T - 12.5 - i * .15) / .4), fall = clamp((T - 14.8 - i * .1) / .5); if (p <= 0 || fall >= 1) return;
    g.save(); g.globalAlpha = p * (1 - fall); g.translate((Math.sin(T * 3 + i) * 10), fall * 300); g.rotate((i % 2 ? .03 : -.03)); card(70, 340 + i * 110, 940, 90, '#FFF6E5', 14, .08);
    font(500, 32, MONO); g.fillStyle = '#9A6200'; g.fillText(r, 100, 398 + i * 110); g.restore(); });
  if (T > 14.18) pillS('RAW · UNCLEAN', 540, 820, back((T - 14.18) / .35), '#F5A524', WHITE);
  // funnel
  g.fillStyle = '#C9CDD2'; g.beginPath(); g.moveTo(240, 900); g.lineTo(840, 900); g.lineTo(620, 1080); g.lineTo(460, 1080); g.closePath(); g.fill();
  font(800, 44, COND); g.fillStyle = INK; g.textAlign = 'center'; g.fillText('SQL', 540, 985); g.textAlign = 'left';
  if (T > 15.2) pillS('CLEAN ✓', 870, 1110, back((T - 15.3) / .35));
  clean.forEach((c, i) => { const p = back((T - 15.2 - i * .08) / .3); if (p <= 0) return; g.save(); g.translate(540, 1200 + i * 120); g.scale(p, p);
    card(-440, -45, 880, 90, WHITE, 14, .08); g.fillStyle = CYAN; g.fillRect(-440, -45, 10, 90); font(600, 36, BODY); g.fillStyle = INK; g.fillText(c, -400, 12); g.restore(); });
  rise('Into the database.', 54, 1700, T - 15.46, { size: 110, w: 800, col: INK, dur: .45 });
}

// "Some people hate it … NoSQL, less structured": structured grid vs loose blob.
function sceneNoSQL(T) {
  th(FULL, zoomAt(T)); captions(T);
  [['SQL', 60, 16.6, true], ['NoSQL', 560, 20.34, false]].forEach(([lab, x, at, structured]) => { const p = back((T - at) / .45); if (p <= 0) return;
    g.save(); g.translate(x + 230, 1360); g.scale(p, p); card(-230, -190, 460, 380, structured ? NAVY : WHITE, 26, .3);
    if (structured) { g.strokeStyle = CYAN; g.lineWidth = 3; for (let r = 0; r < 4; r++) for (let c = 0; c < 3; c++) g.strokeRect(-170 + c * 115, -130 + r * 50, 110, 44); }
    else { const r = rng(4); for (let k = 0; k < 7; k++) { g.fillStyle = [CYAN, BLUE, '#C3A6FF'][k % 3]; g.beginPath(); g.roundRect(-170 + r() * 260, -140 + r() * 150, 50 + r() * 80, 30 + r() * 20, 14); g.fill(); } }
    font(800, 70, COND); g.fillStyle = structured ? WHITE : INK; g.textAlign = 'center'; g.fillText(lab, 0, 150); g.textAlign = 'left'; g.restore(); });
  if (T > 18.74) pillS('NOT FOR EVERYONE', 290, 1120, back((T - 18.74) / .35), '#F5A524', WHITE, 30);
  if (T > 22.4) pillS('LESS STRUCTURED', 790, 1600, back((T - 22.58) / .35), '#F5A524', WHITE, 24);
  if (T > 24.0) pillS('VERY STRUCTURED', 290, 1600, back((T - 24.26) / .35), CYAN, NAVY, 24);
}

// Define a table: name, set columns, set data types, then rows drop in.
function sceneTable(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Define a table', 60, 240, T - TABLE_IN - .1, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  const tp = expo((T - 25.0) / .4); if (tp <= 0) return; card(60, 330, 960, 1100, WHITE, 26, .12 * tp);
  g.save(); g.globalAlpha = tp; font(800, 72, COND); g.fillStyle = INK; g.fillText('users', 110, 430); g.restore();
  const COLS = [['id', 'INT'], ['name', 'TEXT'], ['email', 'TEXT'], ['joined', 'DATE']];
  COLS.forEach(([c, ty], i) => { const p = back((T - 27.34 - i * .12) / .35), x = 110 + i * 230; if (p <= 0) return;
    g.save(); g.translate(x + 100, 520); g.scale(p, p); g.fillStyle = NAVY; g.beginPath(); g.roundRect(-100, -40, 210, 80, 12); g.fill();
    font(700, 42, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(c, 5, 14); g.textAlign = 'left'; g.restore();
    const tq = back((T - 28.5 - i * .1) / .35); if (tq > 0) { g.save(); g.translate(x + 100, 600); g.scale(tq, tq); font(500, 24, MONO); g.fillStyle = BLUE; g.textAlign = 'center'; g.fillText(ty, 5, 8); g.textAlign = 'left'; g.restore(); } });
  const ROWS = [['1', 'Sam', 'sam@…', '2024'], ['2', 'Jo', 'jo@…', '2025'], ['3', 'Alex', 'alex@…', '2025']];
  ROWS.forEach((r, i) => { const p = clamp((T - 29.7 - i * .12) / .25), drop = (1 - expo(p)) * -200; if (p <= 0) return;
    g.save(); g.globalAlpha = p; const y = 700 + i * 120 + drop; g.fillStyle = i % 2 ? '#F6F8FA' : WHITE; g.fillRect(90, y - 50, 900, 100);
    r.forEach((v, k) => { font(500, 32, MONO); g.fillStyle = INK; g.fillText(v, 120 + k * 230, y + 10); }); g.restore(); });
  rise('Set columns. Set types.', 54, 1600, T - 27.34, { size: 100, w: 800, col: INK, dur: .45 });
  faceCircle(910, 1780, 100, back((T - TABLE_IN - .3) / .6));
}

// Relational: users own many houses, houses own many rooms.
function sceneRel(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('Often relational', 70, 240, T - REL_IN - .1, { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  const T3 = [['Users', 34.46, 420, 31.3], ['Houses', 36.68, 900, 33.0], ['Rooms', 38.94, 1380, 33.3]];
  T3.forEach(([lab, at, y, ap], i) => { const p = back((T - ap) / .5); if (p <= 0) return; const lit = i === 0 ? expo((T - 31.3) / .3) : expo((T - at) / .3);
    g.save(); g.translate(540, y); g.scale(p, p); g.globalAlpha = lit > .5 ? 1 : .45; g.fillStyle = lit > .5 ? BLUE : '#0E3148'; g.strokeStyle = lit > .5 ? CYAN : '#2B4A62'; g.lineWidth = 4;
    g.beginPath(); g.roundRect(-300, -130, 600, 260, 24); g.fill(); g.stroke();
    font(800, 84, COND); g.fillStyle = WHITE; g.fillText(lab, -260, -30);
    for (let k = 0; k < 3; k++) { g.fillStyle = 'rgba(255,255,255,.18)'; g.fillRect(-260, 10 + k * 34, 520 - k * 80, 18); } g.restore();
    if (i > 0) { const lp = expo((T - at + .2) / .5); g.strokeStyle = CYAN; g.lineWidth = 6; g.beginPath(); g.moveTo(540, y - 350); g.lineTo(540, lerp(y - 350, y - 130, lp)); g.stroke();
      if (lp > .9) { g.beginPath(); g.moveTo(540, y - 150); g.lineTo(510, y - 130); g.moveTo(540, y - 150); g.lineTo(540, y - 130); g.moveTo(540, y - 150); g.lineTo(570, y - 130); g.stroke();
        font(500, 22, MONO); g.fillStyle = CYAN; g.fillText('ONE → MANY', 570, y - 230); } } });
  rise('And so on.', 70, 1730, T - 39.64, { size: 110, w: 800, col: WHITE, dur: .45 });
  faceCircle(900, 1780, 90, back((T - REL_IN - .3) / .6));
}
