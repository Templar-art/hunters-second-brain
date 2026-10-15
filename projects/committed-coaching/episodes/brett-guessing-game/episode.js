// Committed Coaching: "Brett and the guessing game" — CLONE format (Jackson plays both Brett and the coach).
// Source is a clone composite built by tools/clone.py from a locked-off camera: coach left, Brett right, in one frame.
// Premium system (same as not-your-guy-premium): Inter for the voice, Instrument Serif italic for one key word per line,
// hand-set phrase captions on the dark table, editorial ink type on the white wall above their heads, slow expo motion.
// Nothing ever sits in the face band (y ≈ 580–1080): type lives on the wall above it or on the table below it.
const A = 0, B = 5.58, C = 10.48, D = 18.48, D2 = 20.18, E = 27.22, F = 30.82, END = 36.72, OUT = END + 1.0;   // clone.json segment starts
const QUOTE = 17.5, BR0 = D2;   // quote card ("In his words…") on the 1s held beat after "structure"; B-roll from "Every rep"
// framing per line: alternate wide / slightly tight so jump cuts read as edits; two gentle punch-ins (1.07, centred so both faces stay whole)
const STARTS = [0, 2.42, 3.08, B, C, 12.6, QUOTE, D, D2, E, F, 32.1];
const ZOOMS  = [1.0, 1.05, 1.0, 1.05, 1.0, 1.07, 1.0, 1.05, 1.0, 1.05, 1.0, 1.07];
const OFF = '#F4F1EA', MUTED = 'rgba(244,241,234,.62)', RED = '#E0352B', INKD = '#121214';
const sansF = (w, s) => `${w} ${s}px Inter, sans-serif`, serifF = s => `italic 400 ${s}px "Instrument Serif", Georgia, serif`;

// B-roll from Jackson's library (cut in with tools/broll.py). Captions stay on; the chapter kicker sits top-left.
const BROLL = [   // no faces that could read as a third character: the rep is side-on and distant, the rest is hands / screens / food
  ['broll/rep', D2, 21.6],          // "Every rep, every set"
  ['broll/app', 21.6, 23.3],        // "laid out on the app": at his desk from behind, the plan on screen
  ['broll/weigh', 23.3, 24.13],     // "nutrition to follow": portions weighed into containers
  ['broll/macros', 24.13, 25.45],   // "so we understood these macros": close-up across the portions
];   // "and check-ins every week" returns to the coach on camera

window.EP = {
  dur: OUT, voEnd: END,
  cuts: [...new Set([B, C, D, E, F, END, ...BROLL.flatMap(([, a, b]) => [a, b])])].sort((x, y) => x - y),
  broll: BROLL.map(([dir, a, b]) => ({ dir, a, b, n: Math.ceil((b - a) * 50) + 2 })),
  frame(T) {
    if (T < END) { plate(T); scene(T); caps(T); }
    else endCard(T);
  },
  cues() {
    cue(0, 'sub', { gain: .34 });
    cue(QUOTE, 'soft', { gain: .16 }); cue(29.95, 'click', { gain: .08 });
    cue(BR0, 'soft', { gain: .2 });
    cue(END, 'sub', { gain: .3 }); cue(END + .55, 'ding', { gain: .12 });
  },
};

// ---------- camera: the clone plate (or B-roll), one slow push per line, gentle grade, legibility gradient on the table ----------
function plate(T) {
  const i = STARTS.filter(s => BASE_T >= s).length - 1, a = STARTS[i], b = STARTS[i + 1] || END;
  const sl = BR && EP.broll.find(s => BASE_T >= s.a && BASE_T < s.b);
  if (sl) { const z = 1.02 + .006 * (T - sl.a); g.save(); g.filter = 'contrast(1.06) saturate(.9) brightness(.97)';
    g.drawImage(BR, (W - W * z) / 2, (H - H * z) / 2, W * z, H * z); g.restore();
    const tg = g.createLinearGradient(0, 0, 0, 560); tg.addColorStop(0, 'rgba(0,0,0,.55)'); tg.addColorStop(.7, 'rgba(0,0,0,.35)'); tg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = tg; g.fillRect(0, 0, W, 560); }
  else { g.save(); g.filter = 'contrast(1.05) saturate(.94)'; th(FULL, ZOOMS[i] + .02 * clamp((T - a) / (b - a)), .41); g.restore(); }
  const gr = g.createLinearGradient(0, 1200, 0, H); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(.35, 'rgba(0,0,0,.4)'); gr.addColorStop(1, 'rgba(0,0,0,.66)');
  g.fillStyle = gr; g.fillRect(0, 1200, W, H - 1200);
}

// ---------- primitives (shared with the premium cut) ----------
function softText(txt, x, y, t, { font, col = OFF, d = .55, dy = 18, blur = 10, align = 'left', track = 0, alpha = 1, maxW = 940, shadow = 0 } = {}) {
  if (t <= 0 || alpha <= 0) return 0; const p = expo(t / d);
  g.save(); g.font = font; g.letterSpacing = track + 'px'; g.textAlign = align;
  let w = g.measureText(txt).width; if (w > maxW) { g.font = font.replace(/(\d+(\.\d+)?)px/, m => (parseFloat(m) * maxW / w) + 'px'); w = maxW; }
  g.globalAlpha = alpha * Math.min(1, p * 1.25); if (p < .98 && blur) g.filter = `blur(${(1 - p) * blur}px)`;
  g.fillStyle = col; const yy = y + (1 - p) * dy;
  if (shadow) { g.shadowColor = `rgba(0,0,0,${shadow})`; g.shadowBlur = 22; g.shadowOffsetY = 2; g.fillText(txt, x, yy); g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 5; g.shadowOffsetY = 1; }
  g.fillText(txt, x, yy); g.restore(); g.letterSpacing = '0px'; return w;
}
// Mixed sans + serif line (*word* = serif italic accent), centred at cx. Used for the wall headlines.
function mixedLine(txt, cx, y, t, { SZ, col, accent, alpha = 1, d = .6, shadow = 0, weight = 700, align = 'center' }) {
  if (t <= 0 || alpha <= 0) return; const p = expo(t / d);
  const parts = txt.split(/(\*[^*]+\*|[\u201C\u201D])/).filter(Boolean).map(s => ({ em: s.startsWith('*'), q: /^[\u201C\u201D]$/.test(s), s: s.replace(/\*/g, '') }));
  const setF = pt => { g.font = pt.em || pt.q ? serifF(SZ * 1.28) : sansF(weight, SZ); g.letterSpacing = pt.em || pt.q ? '0px' : `${-.025 * SZ}px`; };   // quote marks in the serif: Inter's read as primes
  parts.forEach(pt => { setF(pt); pt.w = g.measureText(pt.s).width; });
  const tot = parts.reduce((s, pt) => s + pt.w, 0), last = parts[parts.length - 1], prev = parts[parts.length - 2];
  const hl = parts[0].q ? parts[0].w : 0, hr = last.q ? last.w + (prev && !prev.em && /^[.,]$/.test(prev.s) ? prev.w : 0) : 0;   // hang the punctuation
  let x = align === 'left' ? cx - hl : cx - (tot - hl - hr) / 2 - hl;
  g.save(); g.globalAlpha = alpha * Math.min(1, p * 1.25); if (p < .98) g.filter = `blur(${(1 - p) * 10}px)`;
  if (shadow) { g.shadowColor = `rgba(0,0,0,${shadow})`; g.shadowBlur = 24; }
  parts.forEach(pt => { setF(pt); g.fillStyle = pt.em ? accent : col; g.fillText(pt.s, x, y + (1 - p) * 16); x += pt.w; });
  g.restore(); g.letterSpacing = '0px';
}

// ---------- captions: hand-set phrase lines on the dark table. '/' = line break, *word* = serif accent ----------
const LINES = [
  [0.25, 2.42, 'I sit behind a laptop all day.'],
  [2.42, 4.4, 'I train, but honestly,'],
  [4.4, B, 'I\u2019m just always *guessing.*'],
  [B + .12, 6.85, 'Guessing what, bro?'],
  [6.85, C, 'Sets, reps, macros, / all of it?'],
  [C, 12.6, 'That\u2019s Brett. / When he started,'],
  [12.6, 15.7, 'he told me the one thing / that had always thrown him off'],
  [15.7, QUOTE, 'was not having *structure.*'],
  [D, D2, 'So we took the *guessing* away.'],
  [D2, 23.3, 'Every rep, every set / laid out on the app,'],
  [23.3, 25.45, 'nutrition to follow, / so we understood these *macros,*'],
  [25.45, E, 'and check-ins every week.'],
  [E + .02, F, 'So I just open the app / and do it?'],
  [F, 32.1, 'Desk job or not,'],
  [32.1, 35.32, 'structure beats *guesswork* / every time.'],
  [35.32, END, 'Follow for *more.*'],
];
function caps(T, y0 = 1470) {
  T = BASE_T; const L = LINES.find(([a, b]) => win(T, a, b)); if (!L) return;
  const [a, b, txt] = L, SZ = 60, lh = 76, rows = txt.split(' / '), p = expo((T - a) / .32), fo = clamp((b - T) / .14);
  const y = y0 - (rows.length - 1) * lh + (1 - p) * 6;
  g.save(); g.shadowColor = 'rgba(0,0,0,.55)'; g.shadowBlur = 24; g.shadowOffsetY = 2; g.globalAlpha = Math.min(1, p * 1.4) * fo;
  if (p < .9) g.filter = `blur(${(1 - p) * 6}px)`;
  rows.forEach((row, r) => {
    const parts = row.split(/(\*[^*]+\*)/).filter(Boolean).map(s => ({ em: s.startsWith('*'), s: s.replace(/\*/g, '') }));
    const setF = (pt, k) => { g.font = pt.em ? serifF(SZ * 1.26 * k) : sansF(600, SZ * k); g.letterSpacing = pt.em ? '0px' : `${-.6 * k}px`; };
    parts.forEach(pt => { setF(pt, 1); pt.w = g.measureText(pt.s).width; });
    const tot = parts.reduce((s, pt) => s + pt.w, 0), k = Math.min(1, 900 / tot);
    const xs = []; let xx = 0; parts.forEach((pt, j) => { const prev = parts[j - 1];
      if (prev && pt.em && prev.s.endsWith(' ')) xx -= .04 * SZ * k; if (prev && !pt.em && prev.em) xx -= .06 * SZ * k; xs.push(xx); xx += pt.w * k; });
    const x0 = W / 2 - xx / 2;
    const draw = () => parts.forEach((pt, j) => { setF(pt, k); g.fillStyle = OFF; g.fillText(pt.s, x0 + xs[j], y + r * lh); });
    draw(); g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 5; g.shadowOffsetY = 1; draw(); g.shadowColor = 'rgba(0,0,0,.55)'; g.shadowBlur = 24; g.shadowOffsetY = 2;
  });
  g.restore(); g.letterSpacing = '0px';
}

// ---------- name labels: dark ink on the wall, just above each head, on first appearance ----------
function label(T, a, b, name, role, x, align) {
  const p = expo((T - a) / .6), q = clamp((T - b) / .3), al = 1 - q; if (p <= 0 || al <= 0) return;
  const rx = align === 'right' ? x - 44 * p : x;
  g.save(); g.globalAlpha = al; g.fillStyle = RED; g.fillRect(rx, 438, 44 * p, 3); g.restore();
  softText(name, x, 500, T - a - .08, { font: sansF(600, 44), col: INKD, track: -.4, align, alpha: al, blur: 6 });
  softText(role, align === 'right' ? x + 5 : x, 542, T - a - .2, { font: sansF(600, 26), col: 'rgba(18,18,20,.75)', track: 5, align, alpha: al, blur: 6 });
}

// ---------- the beats ----------
function scene(T) {
  // hook (the thumbnail): set from frame 0 on the white wall, dark ink, above their heads
  const hk = 1 - clamp((T - 2.7) / .3);
  if (hk > 0) { mixedLine('\u201CThe guessing', 540, 404, T + 1, { SZ: 92, col: INKD, accent: INKD, alpha: hk });
    mixedLine('becomes too *hard*.\u201D', 540, 508, T + 1, { SZ: 92, col: INKD, accent: RED, alpha: hk }); }
  label(T, 3.0, 5.4, 'Brett', 'CLIENT \u00B7 RE-ENACTED', 1016, 'right');   // Jackson plays him: say so
  label(T, B + .1, 9.9, 'Jackson', 'COACH', 64, 'left');
  // quote card on the held beat after "structure": his words, on the wall
  const qa = T - QUOTE, qo = 1 - clamp((T - 18.84) / .16);   // screen-fixed: holds through the cut into D, like the hook
  if (qa > 0 && qo > 0) {
    softText('IN HIS WORDS', 543.5, 318, qa, { font: sansF(600, 28), col: 'rgba(18,18,20,.75)', track: 7, align: 'center', alpha: qo, blur: 6, d: .45 });
    mixedLine('\u201CThe guessing becomes', 540, 424, qa - .05, { SZ: 68, col: INKD, accent: INKD, alpha: qo, weight: 600, d: .45 });
    mixedLine('too *hard*.\u201D', 540, 514, qa - .1, { SZ: 68, col: INKD, accent: RED, alpha: qo, weight: 600, d: .45 });
  }
  // the answer: wall type above the coach, from just after "do it?" through "Desk job or not,"
  const an = T - 29.95, ao = 1 - clamp((T - (F - .3)) / .18);   // a silent beat in the hold after Brett's question, cleared before the coach speaks
  if (an > 0 && ao > 0) { mixedLine('Open the app.', 100, 404, an, { SZ: 68, col: INKD, accent: INKD, alpha: ao, weight: 600, d: .4, align: 'left' });
    mixedLine('Do *it*.', 100, 484, an - .06, { SZ: 68, col: INKD, accent: RED, alpha: ao, weight: 600, d: .4, align: 'left' }); }
  // chapter kicker across the B-roll run: "No more guessing."
  const ka = T - BR0, ko = 1 - clamp((T - 23.1) / .2);
  if (BR && ka > 0 && ko > 0) { g.save(); g.globalAlpha = ko; g.fillStyle = RED; g.fillRect(64, 318, 48 * expo(ka / .6), 3); g.restore();
    softText('NO MORE GUESSING', 64, 372, ka, { font: sansF(600, 30), col: OFF, track: 6, alpha: ko, blur: 6, shadow: .5 }); }
}

// ---------- end card: the last frame softens behind the CTA ----------
let LOGO_P = null, LAST = null;
function endCard(T) {
  const t = T - END;
  if (FR) { const s = 1.04 + .01 * t; g.save(); g.filter = `blur(${Math.min(24, t * 70)}px) brightness(${1 - Math.min(.8, t * 2.3)}) saturate(${1 - Math.min(.4, t)})`;
    g.drawImage(FR, (W - W * s) / 2, (H - H * s) / 2, W * s, H * s); g.restore(); }
  if (LOGO && !LOGO_P) { LOGO_P = Object.assign(document.createElement('canvas'), { width: LOGO.width, height: LOGO.height }); const x = LOGO_P.getContext('2d');
    x.drawImage(LOGO, 0, 0); x.globalCompositeOperation = 'source-in'; x.fillStyle = OFF; x.fillRect(0, 0, LOGO.width, LOGO.height); }
  if (LOGO_P) { const p = expo((t - .1) / .6), lw = 560, lh = lw * LOGO.height / LOGO.width; if (p > 0) { g.save(); g.globalAlpha = Math.min(1, p * 1.3);
    if (p < .98) g.filter = `blur(${(1 - p) * 10}px)`; g.drawImage(LOGO_P, 540 - lw / 2, 770 - lh / 2, lw, lh); g.restore(); } }
  const l = expo((t - .3) / .6); if (l > 0) { g.fillStyle = RED; g.fillRect(540 - 36 * l, 890, 72 * l, 3); }
  g.save(); g.shadowColor = 'rgba(0,0,0,.4)'; g.shadowBlur = 20;
  mixedLine('Follow for *more.*', 540, 1030, t - .25, { SZ: 84, col: OFF, accent: OFF, weight: 600 });
  softText('@jacksonfarrier', 541, 1122, t - .4, { font: sansF(600, 34), col: 'rgba(244,241,234,.8)', align: 'center', track: 2 });
  g.restore();
  const f = clamp((T - OUT + .3) / .3); if (f > 0) { g.fillStyle = `rgba(0,0,0,${f})`; g.fillRect(0, 0, W, H); }
}
