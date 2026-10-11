// Committed Coaching: "Don't work with me if…" PREMIUM cut (face-on).
// Restraint over effects: his face and the captions carry it. Graphic moments: a scale widget on the whiteboard beside him,
// the three-step deal as plain type, and one CTA pill. The three "not your guy" lines share one quiet verdict treatment;
// the "But" turn is a black type card. Type: Inter for the voice, Instrument Serif italic for one key word per line.
// Captions are hand-set phrase lines (whole lines in, whole lines out), not word-by-word karaoke.
// Nothing sits on the COMMITTED print on his shirt (≈ y 1000–1200): type lives below it, the widget beside his head.
const S2 = 2.84, S3 = 7.44, S4 = 12.4, S5 = 16.86, S6 = 21.22, S7 = 25.86, BACK = 18.9, END = 31.75;   // no end card: it ends on his face + the CTA and loops straight back into the hook
const STARTS = [0, S2, S3, S4, S5, S6, S7], ZOOMS = [1.06, 1.0, 1.0, 1.08, 1.08, 1.0, 1.08];   // takes 2–3 wide: the widget slot left of his head   // alternate wide / tight per take so jump cuts read as intentional
// B-roll slots (Jackson's own footage; see SHOTLIST.md). A slot with no footage falls back to him on camera, so clips just drop in:
//   python3 tools/broll.py episodes/not-your-guy-premium broll/<slot> <clip> <start_s> <dur_s> [x_center]
const BROLL = [   // two cutaways. The list, the verdicts and the CTA always stay on his face.
  ['broll/D_train', BACK, 20.0],    // "to treat your body": one heavy, controlled rep; back to his face on "way you treat your business"
  ['broll/H_rest', 24.56, 25.86],   // "and I'll handle the rest": the hero shot, his forearm on the bar / a client's back
];
const OFF = '#F4F1EA', MUTED = 'rgba(244,241,234,.62)', RED = '#E0352B', INKD = '#121214';
const sansF = (w, s) => `${w} ${s}px Inter, sans-serif`, serifF = s => `italic 400 ${s}px "Instrument Serif", Georgia, serif`;

window.EP = {
  dur: END, voEnd: 31.4,
  cuts: [...new Set([S2, S3, S4, S5, BACK, S6, S7, ...BROLL.flatMap(([, a, b]) => [a, b])])].sort((x, y) => x - y),
  broll: BROLL.map(([dir, a, b]) => ({ dir, a, b, n: Math.ceil((b - a) * 50) + 2 })),
  frame(T) {
    if (T < S2) sceneHook(T);
    else if (T < S3) sceneShred(T);
    else if (T < S4) scenePDF(T);
    else if (T < S5) { plate(T); caps(T); verdict(T, 15.78, 'Not going to work.', S5); }
    else if (T < S6) sceneBut(T);
    else if (T < S7) sceneDeal(T);
    else sceneCTA(T);
  },
  cues() {
    cue(0, 'sub', { gain: .38 }); cue(.55, 'soft', { gain: .12 });
    cue(3.3, 'soft', { gain: .22 }); cue(8.25, 'soft', { gain: .2 }); cue(9.9, 'click', { gain: .1 }); cue(6.68, 'thud', { f: 60, d: .3, gain: .17 });
    cue(11.34, 'thud', { f: 60, d: .3, gain: .17 }); cue(15.78, 'thud', { f: 60, d: .3, gain: .17 });
    cue(S5, 'sub', { gain: .42 }); cue(BACK, 'soft', { gain: .12 });
    STEPS.forEach(([, at]) => cue(at, 'click', { gain: .08 }));
    cue(27.04, 'soft', { gain: .22 }); cue(28.58, 'ding', { gain: .13 });
  },
};

// ---------- camera: native frames, one slow push per take, a gentle grade, a legibility gradient low in frame ----------
function plate(T) {
  let i = STARTS.filter(s => BASE_T >= s).length - 1, a = STARTS[i], b = STARTS[i + 1] || END;
  if (i === 4) a = BACK;
  const sl = BR && EP.broll.find(s => BASE_T >= s.a && BASE_T < s.b);
  if (sl) { const z = 1.02 + .006 * (T - sl.a);   // same slow push rate as the talking head, so a cut to B-roll never feels like a zoom bump
    g.save(); g.filter = 'contrast(1.06) saturate(.88) brightness(.96)';   // B-roll: matched grade, slow push
    g.drawImage(BR, (W - W * z) / 2, (H - H * z) / 2, W * z, H * z); g.restore(); }
  else { const punch = BASE_T >= 14.5 && BASE_T < S5 ? .1 : 0;   // one camera punch on "in your check-ins": the last long shot gets a beat
    g.save(); g.filter = 'contrast(1.05) saturate(.93)'; th(FULL, ZOOMS[i] + punch + .025 * clamp((T - a) / (b - a))); g.restore(); }
  const gr = g.createLinearGradient(0, 1180, 0, H); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(.3, 'rgba(0,0,0,.38)'); gr.addColorStop(1, 'rgba(0,0,0,.66)'); g.fillStyle = gr; g.fillRect(0, 1180, W, H - 1180);   // starts below the shirt print
}

// ---------- primitives ----------
// Soft text entrance: opacity + small rise + blur that clears. Returns width.
function softText(txt, x, y, t, { font, col = OFF, d = .55, dy = 18, blur = 10, align = 'left', track = 0, alpha = 1, maxW = 940, shadow = 0 } = {}) {
  if (t <= 0 || alpha <= 0) return 0; const p = expo(t / d);
  g.save(); g.font = font; g.letterSpacing = track + 'px'; g.textAlign = align;
  let w = g.measureText(txt).width; if (w > maxW) { g.font = font.replace(/(\d+(\.\d+)?)px/, m => (parseFloat(m) * maxW / w) + 'px'); w = maxW; }
  g.globalAlpha = alpha * Math.min(1, p * 1.25); if (p < .98 && blur) g.filter = `blur(${(1 - p) * blur}px)`;
  g.fillStyle = col; const yy = y + (1 - p) * dy;
  if (shadow) { g.shadowColor = `rgba(0,0,0,${shadow})`; g.shadowBlur = 22; g.shadowOffsetY = 2; g.fillText(txt, x, yy); g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 5; g.shadowOffsetY = 1; }   // halo + tight contact shadow
  g.fillText(txt, x, yy); g.restore(); g.letterSpacing = '0px'; return w;
}
// Drop shadow for a rounded shape without drawing the shape (it's drawn off-canvas; only its shadow lands).
function softShadow(x, y, w, h, r, a, blur = 60, oy = 22) { g.save(); g.globalAlpha = a; g.shadowColor = 'rgba(0,0,0,.4)'; g.shadowBlur = blur; g.shadowOffsetY = oy; g.shadowOffsetX = 5000;
  g.fillStyle = '#000'; g.beginPath(); g.roundRect(x - 5000, y, w, h, r); g.fill(); g.restore(); }
// Tabular numerals: fixed-width digit cells so a counting number never jitters.
function tnum(txt, x, y, size, col) { g.font = sansF(600, size); g.fillStyle = col; g.textAlign = 'center'; let cx = x;
  for (const c of txt) { const cw = c === '.' ? size * .3 : size * .62; g.fillText(c, cx + cw / 2, y); cx += cw; } g.textAlign = 'left'; return cx - x; }

// ---------- captions: hand-set phrase lines. '/' = line break, *word* = serif-italic accent ----------
const LINES = [
  [2.84, 4.10, 'If you want a / 30-day *shred*'],
  [4.10, 6.60, 'so you can rebound / straight after *Christmas*'],
  [7.44, 8.68, 'If you want a *PDF*'],
  [8.68, 11.30, 'to download / and *forget* about it'],
  [12.40, 14.50, 'And if you’re not willing / to be *honest*'],
  [14.50, 15.70, 'in your check-ins'],
  [BACK, 19.72, 'ready to treat your *body*'],
  [19.72, S6, 'the way you treat / your *business*'],
  [S7, 27.00, 'If that’s you,'],
  [28.94, END + 1, 'I’ll tell you pretty quick / if we’re a *fit.*'],   // held to the last frame
];
function caps(T, y0 = 1440) {
  T = BASE_T; const L = LINES.find(([a, b]) => win(T, a, b)); if (!L) return;
  const [a, b, txt] = L, SZ = 60, lh = 76, rows = txt.split(' / '), p = expo((T - a) / .32), fo = clamp((b - T) / .14);
  const y = y0 - (rows.length - 1) * lh + (1 - p) * 6;   // two-line captions grow upward, so the bottom line never nears Instagram's UI
  g.save(); g.shadowColor = 'rgba(0,0,0,.55)'; g.shadowBlur = 24; g.shadowOffsetY = 2; g.globalAlpha = Math.min(1, p * 1.4) * fo;
  if (p < .9) g.filter = `blur(${(1 - p) * 6}px)`;
  rows.forEach((row, r) => {
    const parts = row.split(/(\*[^*]+\*)/).filter(Boolean).map(s => ({ em: s.startsWith('*'), s: s.replace(/\*/g, '') }));
    const setF = (pt, k) => { g.font = pt.em ? serifF(SZ * 1.26 * k) : sansF(600, SZ * k); g.letterSpacing = pt.em ? '0px' : `${-.6 * k}px`; };
    parts.forEach(pt => { setF(pt, 1); pt.w = g.measureText(pt.s).width; });
    const tot = parts.reduce((s, pt) => s + pt.w, 0), k = Math.min(1, 900 / tot); let x = W / 2 - tot * k / 2;
    const xs = []; let xx = x; parts.forEach((pt, j) => { const prev = parts[j - 1];   // optical spacing at sans/serif joins
      if (prev && pt.em && prev.s.endsWith(" ")) xx -= .04 * SZ * k; if (prev && !pt.em && prev.em) xx -= .06 * SZ * k; xs.push(xx); xx += pt.w * k; });
    x -= (xx - x - tot * k) / 2;   // re-centre after the adjustments
    const draw = () => parts.forEach((pt, j) => { setF(pt, k); g.fillStyle = OFF; g.fillText(pt.s, xs[j] + (x - (W / 2 - tot * k / 2)), y + r * lh); });
    draw(); g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 5; g.shadowOffsetY = 1; draw(); g.shadowColor = 'rgba(0,0,0,.55)'; g.shadowBlur = 24; g.shadowOffsetY = 2;
  });
  g.restore(); g.letterSpacing = '0px';
}

// ---------- the verdict: one quiet treatment for all three "not your guy" lines ----------
function verdict(T, a, txt, end, y = 1470) {
  const t = T - a; if (t <= 0) return; const al = 1 - clamp((T - (end - .12)) / .12);
  const d = expo(t / .5); g.save(); g.globalAlpha = al; g.fillStyle = RED; g.fillRect(540 - 20 * d, y - 130, 40 * d, 3); g.restore();   // a short red rule draws in, centred above the line
  softText(txt, 549, y, t, { align: 'center',   // +9: optical centre (italic slant + trailing period) under the rule
    font: serifF(128), col: '#FFFFFF', d: .6, dy: 16, blur: 12, alpha: al, maxW: 820, shadow: .5 });
}

// ---------- hook: the thumbnail. Set from frame 0; it settles rather than appears ----------
function sceneHook(T) {
  plate(T);
  const al = 1 - clamp((T - 2.6) / .24), s = 1 + .025 * T / S2;
  g.save(); g.translate(540, 1460); g.scale(s, s); g.translate(-540, -1460); g.globalAlpha = al; g.textAlign = 'center';
  g.shadowColor = 'rgba(0,0,0,.5)'; g.shadowBlur = 30;
  g.font = sansF(700, 136); g.letterSpacing = `${lerp(-1, -4, expo(T / 1.2))}px`; g.fillStyle = OFF; g.fillText('Don’t work', 540, 1352);
  g.font = serifF(178); g.letterSpacing = '0px'; g.fillStyle = '#FFFFFF'; g.fillText('with me', 540, 1496);
  g.restore(); g.textAlign = 'left'; g.letterSpacing = '0px';
  g.save(); g.globalAlpha = al; g.font = serifF(64); g.textAlign = 'center'; g.fillStyle = 'rgba(244,241,234,.92)'; g.shadowColor = 'rgba(0,0,0,.5)'; g.shadowBlur = 22;
  g.fillText('if this sounds like you.', 540, 1596); g.restore(); g.textAlign = 'left';   // part of the thumbnail: set from frame 0
  // audience kicker: near-black on the white wall, left of his head, below Instagram's top bar
  const p = expo((T + .3) / .8), na = 1 - clamp((T - 2.5) / .3);
  if (na > 0) { g.save(); g.globalAlpha = na; g.fillStyle = RED; g.fillRect(64, 318, 48 * p, 3); g.restore();
    softText('FOR BUSINESS OWNERS', 64, 376, T + .3, { font: sansF(600, 38), col: INKD, track: 6, alpha: na, blur: 6 }); }
}

// ---------- shred: a compact scale widget on the whiteboard, beside his head; the line drops, then rebounds red ----------
function sceneShred(T) {
  plate(T);
  const p = clamp((BASE_T - 3.3) / .5), q = clamp((BASE_T - 6.4) / .32);   // wipe runs on frame time: a crisp edge, no stepped motion-blur bands
  if (p > 0 && q < 1) {
    const x = 64, w = 346, h = 400, y = 470, r = 30, rev = inOut(p), hide = inOut(q), a = 1;   // content is opaque and rides the wipe: no separate fade
    const top = y + h * hide, bot = y + h * rev;   // opaque card, revealed and removed by a vertical wipe: nothing ever shows through it
    softShadow(x, y, w, h, r, .8 * clamp((T - 3.8) / .3) * (1 - clamp(q * 4)));   // shadow only once the card is fully in, gone before it leaves
    g.save(); g.beginPath(); g.rect(x - 2, top, w + 4, Math.max(0, bot - top)); g.clip(); g.fillStyle = '#111111'; g.beginPath(); g.roundRect(x, y, w, h, r); g.fill();
    g.globalAlpha = a; g.strokeStyle = 'rgba(255,255,255,.08)'; g.lineWidth = 1.5; g.beginPath(); g.roundRect(x + .75, y + .75, w - 1.5, h - 1.5, r); g.stroke();
    g.font = sansF(600, 22); g.letterSpacing = '3.5px'; g.fillStyle = MUTED; g.fillText('30-DAY SHRED', x + 40, y + 56); g.letterSpacing = '0px';
    const cs = v => .5 - .5 * Math.cos(Math.PI * clamp(v)), dr = cs((BASE_T - 3.84) / .76), rb = cs((BASE_T - 4.6) / .9), K = .78;   // frame-centre time: every subframe shows the same number, so digits never ghost
    const val = u => u <= K ? 96 - 8 * cs(u / K) + .3 * Math.sin(u * 40) * Math.sin(Math.PI * u / K) : 88 + 7.5 * cs((u - K) / (1 - K));   // wiggle vanishes at both ends: never above 96
    const upto = K * dr + (1 - K) * rb, kg = val(upto), hot = rb > 0;
    tnum(kg.toFixed(1), x + 38, y + 146, 80, hot ? RED : OFF);
    g.font = sansF(500, 28); g.fillStyle = MUTED; g.fillText('kg', x + 46 + 80 * .62 * 3 + 80 * .3, y + 146);   // pinned: never moves with the number
    g.font = sansF(600, 24); if (hot) { g.fillStyle = RED; g.fillText(`+${(kg - 88).toFixed(1)} kg after Christmas`, x + 40, y + 194, w - 80); }
    else if (96 - kg >= .1) { g.fillStyle = MUTED; g.fillText(`\u2212${Math.max(0, 96 - kg).toFixed(1)} kg`, x + 40, y + 194); }
    const gx = x + 40, gw = w - 80, gy = y + 236, gh = 124, Y = v => gy + (96.6 - v) / 9.2 * gh;
    g.fillStyle = 'rgba(255,255,255,.07)'; for (let k = 0; k < 3; k++) g.fillRect(gx, gy + k * gh / 2, gw, 1.5);
    const seg = (u0, u1, col, glow) => { if (u1 <= u0) return; g.save(); g.strokeStyle = col; g.lineWidth = 4; g.lineCap = 'round'; g.lineJoin = 'round';
      if (glow) { g.shadowColor = col; g.shadowBlur = 14; } g.beginPath(); const n = 70;
      for (let k = 0; k <= n; k++) { const u = u0 + (u1 - u0) * k / n, X = gx + gw * u, Yv = Y(val(u)); k ? g.lineTo(X, Yv) : g.moveTo(X, Yv); } g.stroke(); g.restore(); };
    seg(0, Math.min(upto, K), OFF, false); seg(K, upto, RED, true);
    if (T > 5.66) { const mx = gx + gw * K; g.save(); g.globalAlpha = a * expo((T - 5.66) / .5); g.strokeStyle = 'rgba(255,255,255,.3)'; g.lineWidth = 1.5; g.setLineDash([4, 6]);
      g.beginPath(); g.moveTo(mx, gy - 4); g.lineTo(mx, gy + gh); g.stroke(); g.restore(); }   // the Christmas line: unlabelled, the caption says it
    if (upto > 0) { const X = gx + gw * upto, Yv = Y(kg), c = hot ? RED : OFF, pu = (T * 1.6) % 1;
      g.fillStyle = c; g.beginPath(); g.arc(X, Yv, 6.5, 0, 7); g.fill(); g.globalAlpha = a * (1 - pu) * .6; g.strokeStyle = c; g.lineWidth = 2; g.beginPath(); g.arc(X, Yv, 6.5 + pu * 14, 0, 7); g.stroke(); }
    g.restore();
  }
  caps(T);
  verdict(T, 6.68, 'Not your guy.', S3);
}

// ---------- PDF: the same widget slot; the file downloads, then sits there unopened ----------
function scenePDF(T) {
  plate(T);
  const p = clamp((BASE_T - 8.25) / .5), q = clamp((BASE_T - 10.95) / .32);
  if (p > 0 && q < 1) {
    const grow = inOut(clamp((BASE_T - 9.96) / .45)), h = 252 + 148 * grow;   // compact (file + progress) until "forget", then it opens to reveal the payoff
    const x = 64, w = 346, y = 470, r = 30, top = y + h * inOut(q), bot = y + h * inOut(p);
    softShadow(x, y, w, h, r, .8 * clamp((T - 8.75) / .3) * (1 - clamp(q * 4)));
    g.save(); g.beginPath(); g.rect(x - 2, top, w + 4, Math.max(0, bot - top)); g.clip(); g.fillStyle = '#111111'; g.beginPath(); g.roundRect(x, y, w, h, r); g.fill();
    g.strokeStyle = 'rgba(255,255,255,.08)'; g.lineWidth = 1.5; g.beginPath(); g.roundRect(x + .75, y + .75, w - 1.5, h - 1.5, r); g.stroke();
    g.save(); g.beginPath(); g.roundRect(x, y, w, h, r); g.clip();
    g.font = sansF(600, 22); g.letterSpacing = '3.5px'; g.fillStyle = MUTED; g.fillText('DOWNLOADS', x + 40, y + 56); g.letterSpacing = '0px';
    const fg = clamp((BASE_T - 10.1) / .4), dim = 1 - .55 * clamp((BASE_T - 9.96) / .5);   // "forget": the file greys out
    g.globalAlpha = dim; g.fillStyle = RED; g.beginPath(); g.roundRect(x + 40, y + 84, 54, 66, 8); g.fill();
    g.font = sansF(700, 18); g.fillStyle = '#FFFFFF'; g.textAlign = 'center'; g.fillText('PDF', x + 67, y + 124); g.textAlign = 'left';
    g.font = sansF(600, 28); g.letterSpacing = '-.3px'; g.fillStyle = OFF; g.fillText('meal-plan.pdf', x + 110, y + 114); g.letterSpacing = '0px';
    g.font = sansF(500, 22); g.fillStyle = MUTED; g.fillText('2.4 MB', x + 110, y + 144);
    const dl = clamp((BASE_T - 9.22) / .6);
    g.fillStyle = 'rgba(255,255,255,.1)'; g.beginPath(); g.roundRect(x + 40, y + 182, w - 80, 5, 2.5); g.fill();
    if (dl > 0) { g.fillStyle = OFF; g.beginPath(); g.roundRect(x + 40, y + 182, (w - 80) * inOut(dl), 5, 2.5); g.fill(); }
    g.font = sansF(500, 22); g.fillStyle = MUTED; g.fillText(dl >= 1 ? 'Downloaded' : dl > 0 ? 'Downloading…' : 'Ready', x + 40, y + 222);
    g.globalAlpha = 1;
    if (fg > 0) { g.globalAlpha = Math.min(1, fg * 1.5); g.font = sansF(600, 22); g.letterSpacing = '3.5px'; g.fillStyle = MUTED; g.fillText('OPENED', x + 40, y + 282); g.letterSpacing = '0px';
      const nw = tnum('0', x + 38, y + 360, 80, RED); g.font = sansF(500, 28); g.fillStyle = MUTED; g.fillText('times', x + 48 + nw, y + 360); g.globalAlpha = 1; }
    g.restore(); g.restore();
  }
  caps(T); verdict(T, 11.34, 'Also not your guy.', S4);
}

// ---------- the turn: a black type card on "But", held through "business owner…", back to him on "to treat" ----------
function sceneBut(T) {
  if (T >= BACK) { plate(T); caps(T); return; }
  g.fillStyle = '#0B0B0C'; g.fillRect(0, 0, W, H);
  const rg = g.createRadialGradient(540, 920, 40, 540, 920, 900); rg.addColorStop(0, 'rgba(255,238,220,.07)'); rg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = rg; g.fillRect(0, 0, W, H);
  const s = 1 + .02 * (T - S5) / (BACK - S5); g.save(); g.translate(540, 960); g.scale(s, s); g.translate(-540, -960);
  softText('But', 540, 860, T - S5 + .1, { font: serifF(300), col: '#FFFFFF', align: 'center', d: .5, blur: 14, dy: 10 });
  softText('if you’re a', 540, 1004, T - 17.26, { font: sansF(500, 46), col: 'rgba(244,241,234,.78)', align: 'center', track: -.4 });
  softText('business owner\u2026', 540, 1128, T - 17.92, { font: serifF(104), col: '#FFFFFF', align: 'center', d: .6 });
  g.restore();
}

// ---------- the deal: three steps as plain type below the shirt print, then "I'll handle the rest." ----------
const STEPS = [['Show up', 21.22], ['Follow the plan', 22.28], ['Tell the truth, weekly', 23.34]];
function sceneDeal(T) {
  plate(T);
  g.font = sansF(600, 52); g.letterSpacing = '-.8px'; const mw = Math.max(...STEPS.map(([l]) => g.measureText(l).width)); g.letterSpacing = '0px';
  const x0 = 540 - mw / 2 - 64;   // centre the labels; the small numerals hang into the margin
  const lo = BR && BASE_T >= 24.56 ? 0 : 1 - clamp((T - 24.72) / .22);   // the list clears before the promise: "I'll handle the rest." reads on its own
  if (lo > 0) STEPS.forEach(([lab, at], i) => { const t = T - at, ry = 1316 + i * 84;
    softText(String(i + 1).padStart(2, '0'), x0, ry - 4, t, { font: sansF(600, 26), col: 'rgba(244,241,234,.72)', track: 3, shadow: .6, alpha: lo });
    softText(lab, x0 + 64, ry + 4, t - .04, { font: sansF(600, 52), track: -.8, shadow: .6, alpha: lo }); });
  softText('I’ll handle the rest.', 547, 1470, T - 24.98, { font: serifF(96), col: '#FFFFFF', align: 'center', shadow: .5 });
}

// ---------- CTA: one white pill below the print, "link in bio" under it, a single sheen on "bio" ----------
function sceneCTA(T) {
  plate(T); caps(T, 1600);
  const t = T - 27.04; if (t <= 0) return;
  const p = expo(t / .6), pw = 652, ph = 124, px = 540 - pw / 2, py = 1236 + (1 - p) * 24, a = Math.min(1, p * 1.3);
  softShadow(px, py, pw, ph, ph / 2, a * .9, 50, 18);
  g.save(); g.globalAlpha = a; g.fillStyle = OFF; g.beginPath(); g.roundRect(px, py, pw, ph, ph / 2); g.fill();
  const sh = clamp((T - 28.58) / .8); if (sh > 0 && sh < 1) { g.save(); g.beginPath(); g.roundRect(px, py, pw, ph, ph / 2); g.clip();
    const sxp = px - 200 + (pw + 400) * inOut(sh), lg = g.createLinearGradient(sxp - 110, 0, sxp + 110, 0);
    lg.addColorStop(0, 'rgba(255,255,255,0)'); lg.addColorStop(.5, 'rgba(255,255,255,.95)'); lg.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = lg; g.fillRect(px, py, pw, ph); g.restore(); }
  g.font = sansF(600, 44); g.letterSpacing = '-.5px'; g.fillStyle = INKD; g.fillText('Watch the free video', px + 60, py + 78); g.letterSpacing = '0px';
  const cx = px + pw - 62, cy = py + ph / 2; g.fillStyle = RED; g.beginPath(); g.arc(cx, cy, 40, 0, 7); g.fill();
  const n = -2 + Math.sin(Math.max(0, T - 27.6) * 2.2) * 2; g.strokeStyle = '#FFFFFF'; g.lineWidth = 5; g.lineCap = 'round'; g.lineJoin = 'round';
  g.beginPath(); g.moveTo(cx - 14 + n, cy); g.lineTo(cx + 14 + n, cy); g.moveTo(cx + 3 + n, cy - 11); g.lineTo(cx + 14 + n, cy); g.lineTo(cx + 3 + n, cy + 11); g.stroke();
  g.restore();
  softText('LINK IN BIO', 543, 1418, T - 28.06, { font: sansF(600, 28), col: 'rgba(244,241,234,.82)', track: 6, align: 'center', shadow: .6 });
}
