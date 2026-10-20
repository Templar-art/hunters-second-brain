// JSON: JavaScript Object Notation (04 Oct clip, 33s).
const JASON_IN = 1.95, STANDS_IN = 5.0, FILES_IN = 7.6, CODE_IN = 14.3, TYPES_IN = 22.6, SEMI_IN = 26.5, END_MOS = 32.5, END_IN = END_MOS + .4;
const STANDS = [['J', 'ava', 5.64], ['S', 'cript', 5.9], ['O', 'bject', 6.22], ['N', 'otation', 6.9]];
window.EP = {
  dur: 36.0, voEnd: 32.7,
  punchIns: [[29.9, 32.5]],
  captions: [[JASON_IN, STANDS_IN, 1600], [CODE_IN, TYPES_IN, 1760], [SEMI_IN, END_MOS, 1170]],
  cuts: [JASON_IN, STANDS_IN, FILES_IN, CODE_IN, TYPES_IN, SEMI_IN, END_IN],
  // v4 (redo pass): deliberate transitions the QC continuity check should ignore
  qcAllow: [[0, 0.6], [1.5, 2.4], [3.6, 4.4], [4.8, 5.4], [7.4, 8.1], [13.3, 13.7], [14.1, 14.8], [22.4, 23.0], [23.3, 23.8],
            [24.9, 25.4], [25.8, 26.9], [27.4, 27.9], [29.2, 29.6], [29.8, 30.1], [32.3, 33.5]],
  frame(T) {
    if (T < JASON_IN) titleCard(T, 'JSON', 1.7, 'Definitions', [985, 800]);   // v4: shards off the ear line
    else if (T < STANDS_IN) sceneJason(T);
    else if (T < FILES_IN) standsFor(T, STANDS_IN, FILES_IN, 'JSON', STANDS);
    else if (T < CODE_IN) sceneFiles(T);
    else if (T < TYPES_IN) sceneCode(T);
    else if (T < SEMI_IN) sceneTypes(T);
    else if (T < END_IN) sceneSemi(T);
    else endCard(T, END_IN, this.dur, 'Definitions', true);   // v4: alive end card
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('JSON', 1.7);
    cue(JASON_IN, 'whoosh', { d: .4, gain: .4 }); cue(2.3, 'typing', { n: 5, cps: 20 }); cue(3.68, 'thud', { f: 40, d: .6, gain: .7 }); cue(3.68, 'glass', { n: 40, span: .3 });
    cue(4.32, 'whoosh', { d: .3, bright: .5, gain: .3 }); cue(4.6, 'pop', { f: 900, gain: .25 });
    standsFor.cue(STANDS_IN, FILES_IN, 'JSON', STANDS);
    cue(FILES_IN, 'whoosh', { d: .4, gain: .35 }); FILES.forEach(([, , at]) => { cue(at, 'thud', { f: 90, d: .2, gain: .25 }); cue(at, 'pop', { f: 800, gain: .15 }); });
    cue(13.4, 'whoosh', { d: .35, gain: .25 });
    cue(CODE_IN - .1, 'whoosh', { d: .5, gain: .4 }); cue(14.9, 'typing', { n: 90, cps: 16, gain: .2 }); cue(20.78, 'chime', { f: 988, gain: .1 }); cue(21.14, 'chime', { f: 1318, gain: .1 });
    cue(TYPES_IN - .1, 'whoosh', { d: .4, gain: .35 }); TYPES.forEach(([, , at]) => flipCard.cue(at));
    cue(SEMI_IN, 'whoosh', { d: .3, gain: .3 }); behindHead.cue(27.54, 'STRUCTURED?');
    SEMIROWS.forEach(([, ok, at]) => cue(at, ok ? 'chime' : 'thud', ok ? { f: 1175, gain: .1 } : { f: 90, d: .2, gain: .3 }));
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};

// "Not to be confused with JASON": film-strip card, screen cracks on "hatchets", JSON stamp.
function sceneJason(T) {
  const shake = T > 3.68 && T < 4.1 ? Math.sin(T * 90) * 18 * (1 - (T - 3.68) / .42) : 0;
  g.save(); g.translate(shake, shake * .4);
  th(FULL, BZ * 1.05);
  const p = expo((T - JASON_IN) / .45), x = 60, y = 1180 + (1 - p) * 500, w = 960, h = 560;
  card(x, y, w, h, '#0A0A0A', 18, .5);
  g.fillStyle = '#1E1E1E'; for (let i = 0; i < 14; i++) { g.fillRect(x + 30 + i * 68, y + 18, 34, 22); g.fillRect(x + 30 + i * 68, y + h - 40, 34, 22); }
  typeOn('Not to be confused with', x + 60, y + 120, T - 2.0, { size: 28, col: GREY, track: 5, upper: true, cps: 40 });
  letterDrop('JASON', x + 60, y + 340, T - 2.3, { size: 230, col: WHITE, stagger: .06 });
  if (T > 4.32) { const q = expo((T - 4.32) / .3); g.fillStyle = CYAN; g.fillRect(x + 50, y + 260, 560 * q, 14); }
  if (T > 4.6) { const q = back((T - 4.6) / .35); g.save(); g.translate(x + 760, y + 300); g.rotate(-.18); g.scale(q, q);
    g.strokeStyle = CYAN; g.lineWidth = 8; g.beginPath(); g.roundRect(-150, -80, 300, 160, 16); g.stroke();
    font(800, 120, COND); g.fillStyle = CYAN; g.textAlign = 'center'; g.fillText('JSON', 0, 42); g.textAlign = 'left'; g.restore(); }
  typeOn('the guy from the movie', x + 60, y + 470, T - 2.6, { size: 26, col: '#666', track: 5, upper: true, cps: 40 });
  // crack lines across the frame on "hatchets"
  if (T > 3.68) { const r = rng(13), q = expo((T - 3.68) / .25);
    g.strokeStyle = 'rgba(255,255,255,.85)'; g.lineWidth = 3;
    for (let k = 0; k < 6; k++) { let cx = 540, cy = 760; g.beginPath(); g.moveTo(cx, cy); const a = r() * 6.28;
      for (let s = 0; s < 6 * q; s++) { cx += Math.cos(a + (r() - .5) * 1.2) * 90; cy += Math.sin(a + (r() - .5) * 1.2) * 90; g.lineTo(cx, cy); } g.stroke(); }
    g.globalAlpha = 1 - clamp((T - 3.68) / .15); g.fillStyle = WHITE; g.fillRect(0, 0, W, H); g.globalAlpha = 1; }
  captions(T);
  g.restore();
}

// File formats: folded-corner document cards land as he names them.
const FILES = [['JSON', '.json', 7.88, BLUE], ['CSV', '.csv', 10.38, '#1F9D55'], ['XLSX', '.xlsx', 11.78, '#127A3E']];
function fileIcon(x, y, w, h, label, ext, col, p) {
  if (p <= 0) return; g.save(); g.translate(x + w / 2, y + h); g.rotate((1 - clamp(p)) * .4); g.scale(p, p); g.translate(-(x + w / 2), -(y + h));
  g.shadowColor = 'rgba(0,0,0,.15)'; g.shadowBlur = 30; g.shadowOffsetY = 12; g.fillStyle = WHITE; const f = w * .26;
  g.beginPath(); g.moveTo(x, y); g.lineTo(x + w - f, y); g.lineTo(x + w, y + f); g.lineTo(x + w, y + h); g.lineTo(x, y + h); g.closePath(); g.fill();
  g.shadowColor = 'transparent'; g.fillStyle = '#E5E7EA'; g.beginPath(); g.moveTo(x + w - f, y); g.lineTo(x + w - f, y + f); g.lineTo(x + w, y + f); g.fill();
  g.fillStyle = col; g.beginPath(); g.roundRect(x + 24, y + h - 120, w - 48, 80, 12); g.fill();
  font(800, 56, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(label, x + w / 2, y + h - 60);
  font(500, 24, MONO); g.fillStyle = GREY; g.fillText(ext, x + w / 2, y + 120); g.textAlign = 'left';
  g.fillStyle = '#E5E7EA'; for (let i = 0; i < 3; i++) g.fillRect(x + 30, y + 160 + i * 30, (w - 60) * (1 - i * .2), 12);
  g.restore();
}
function sceneFiles(T) {
  const wy = whip(T, CODE_IN - .3);
  th(FULL, BZ); g.save(); g.translate(0, wy);
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('A file format', 60, 330, T - 8.24, { size: 30, col: BLUE, track: 6, upper: true, cps: 30 });
  rise('Like a CSV,', 54, 540, T - 8.5, { size: 150, w: 800, col: INK, dur: .45 });
  rise('or an XLSX.', 54, 690, T - 11.52, { size: 150, w: 800, col: INK, dur: .45 });
  FILES.forEach(([l, ext, at, col], i) => fileIcon(60 + i * 330, 860 + Math.sin(T * 2.1 + i * 1.4) * 12 /* v4: idle float */, 300, 400, l, ext, col, back((T - at) / .5)));
  // bracket: "something else that stores information"
  const pb = expo((T - 13.4) / .5);
  if (pb > 0) { g.strokeStyle = BLUE; g.lineWidth = 5; g.beginPath(); g.moveTo(60, 1310); g.lineTo(60, 1340); g.lineTo(60 + 960 * pb, 1340); g.lineTo(60 + 960 * pb, 1310); g.stroke();
    typeOn('All of them store information', 60, 1420, T - 13.5, { size: 34, col: INK, track: 2, cps: 40 }); }
  faceCircle(900, 1700, 130, back((T - 8.0) / .6));
  g.restore();
}

// Split layout: speaker in a tall left column, live JSON on navy to the right.
const CODE = [['{', 0], ['  "users": [', 0], ['    {', 0], ['      "name": "Sam",', 1], ['      "role": "Founder",', 1], ['      "id": 101', 2], ['    }', 0], ['  ]', 0], ['}', 0]];
function sceneCode(T) {
  const t = T - CODE_IN, p = inOut(t / .6), wy = whip(T, TYPES_IN - .42, .4);
  if (wy < 0) sceneTypes(T);
  g.save(); g.translate(0, wy);
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  const colW = lerp(W, 400, p);
  g.save(); g.beginPath(); g.rect(0, 0, colW, H); g.clip(); th({ x: 0, y: 0, w: colW, h: H }, lerp(BZ, 1.0, p), .3); g.restore();
  g.fillStyle = CYAN; g.fillRect(colW - 4, 0, 4, H * p);
  const x = 440;
  typeOn('Lists + objects', x, 260, T - 14.6, { size: 26, col: CYAN, track: 5, upper: true, cps: 40 });
  let chars = Math.floor((T - 14.9) * 16);
  const keyGlow = expo((T - 20.78) / .3) * (1 - clamp((T - 21.6) / .3)), valGlow = expo((T - 21.14) / .3);
  CODE.forEach(([line, kind], i) => { const n = clamp(chars, 0, line.length); chars -= line.length; if (n <= 0) return;
    const y = 380 + i * 70, s = line.slice(0, n), m = s.match(/^(\s*)("[^"]*")(:\s*)(.*)$/);
    font(500, 34, MONO); let cx = x;
    const put = (txt, col, glow) => { if (glow > 0) { g.save(); g.shadowColor = col; g.shadowBlur = 30 * glow; } g.fillStyle = col; g.fillText(txt, cx, y); if (glow > 0) g.restore(); cx += g.measureText(txt).width; };
    if (m) { put(m[1], WHITE); put(m[2], keyGlow > .1 ? CYAN : '#7FD6FF', keyGlow); put(m[3], GREY); put(m[4], valGlow > .1 ? '#FFD580' : (kind === 2 ? '#C3A6FF' : '#A8F0C6'), valGlow); }
    else put(s, WHITE); });
  // key/value legend
  if (T > 20.6) { statusPill('KEY', x, 1080, 'ok', expo((T - 20.78) / .3), 26); statusPill('VALUE', x + 150, 1080, 'off', expo((T - 21.14) / .3), 26); }
  rise('Key-value', x, 1300, T - 20.78, { size: 120, w: 800, col: WHITE, dur: .45 });
  rise('attributes.', x, 1430, T - 21.62, { size: 120, w: 800, col: CYAN, dur: .45 });
  g.restore();
  if (wy === 0) { const save = EP.captions; captions(T); }
}
function statusPill(txt, x, y, kind, p = 1, size = 24) {
  if (p <= 0) return 0; font(500, size, MONO); g.letterSpacing = '2px';
  const w = g.measureText(txt).width + 30, h = size * 1.75, C = { ok: [CYAN, NAVY, CYAN], off: [NAVY, CYAN, CYAN], bad: [WHITE, '#9A6200', '#F5A524'] }[kind];
  g.save(); g.globalAlpha *= clamp(p); g.fillStyle = C[0]; g.strokeStyle = C[2]; g.lineWidth = 2.5; g.beginPath(); g.roundRect(x, y - h * .72, w, h, h / 2); g.fill(); g.stroke();
  g.fillStyle = C[1]; g.fillText(txt, x + 15, y); g.restore(); g.letterSpacing = '0px'; return w;
}

// Data types: three cards flip from the type to an example value.
const TYPES = [['Text', '"Sam"', 23.36], ['Integer', '42', 24.96], ['Decimal', '3.14', 25.9]];
function sceneTypes(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Values can be', 60, 380, T - 22.8, { size: 30, col: BLUE, track: 6, upper: true, cps: 30 });
  TYPES.forEach(([type, ex, at], i) => { const cy = 640 + i * 400 + Math.sin(T * 2.3 + i * 1.3) * 12, pin   /* v4: idle float between flips */ = back((T - TYPES_IN - .1 - i * .1) / .5); if (pin <= 0) return;
    g.save(); g.translate(540, cy); g.scale(pin, pin); g.translate(-540, -cy);
    flipCard(T, at, 540, cy, 900, 320,
      (x, y, w, h) => { font(800, 130, COND); g.fillStyle = WHITE; g.fillText(type, x + 60, y + 205); },
      (x, y, w, h) => { font(500, 120, MONO); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText(ex, 0, 42); g.textAlign = 'left'; }, NAVY);
    g.restore(); });
  faceCircle(910, 200, 110, back((T - TYPES_IN - .2) / .6));
}

// Semi-structured: SEMI behind the head, then a checklist that fails on enforcement.
const SEMIROWS = [['Has a structure', true, 29.46], ['Structure enforced', false, 30.36], ['Schema validated', false, 31.86]];
function sceneSemi(T) {
  th(FULL, zoomAt(T));
  behindHead(T, 27.54, 29.4, 'SEMI', 'STRUCTURED', zoomAt(T));
  const p = expo((T - 29.2) / .45);
  if (p > 0) { const x = 60, y = 1330 + (1 - p) * 300, w = 960, h = 420; card(x, y, w, h, WHITE, 22, .25);
    SEMIROWS.forEach(([lab, ok, at], i) => { const ry = y + 110 + i * 120, q = back((T - at) / .4);
      font(700, 56, COND); g.fillStyle = INK; g.fillText(lab, x + 50, ry);
      if (q > 0) { g.save(); g.translate(x + w - 90, ry - 18); g.scale(q, q); g.fillStyle = ok ? CYAN : '#F5A524'; g.beginPath(); g.arc(0, 0, 34, 0, 7); g.fill();
        font(800, 46, COND); g.fillStyle = ok ? NAVY : WHITE; g.textAlign = 'center'; g.fillText(ok ? '✓' : '✗', 0, 16); g.textAlign = 'left'; g.restore(); }
      if (i < 2) { g.fillStyle = '#EEF0F2'; g.fillRect(x + 40, ry + 45, w - 80, 2); } }); }
  captions(T);
}
