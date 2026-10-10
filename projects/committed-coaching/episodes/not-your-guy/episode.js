// Committed Coaching: "Don't work with me if…" anti-pitch (7 takes joined, 31.4s).
// Take starts: 0, 2.84, 7.44, 12.4, 16.86, 21.22, 25.86 (jump cuts; alternate takes punch in).
const S2 = 2.84, S3 = 7.44, S4 = 12.4, S5 = 16.86, S6 = 21.22, S7 = 25.86, END_MOS = 31.25, END_IN = END_MOS + .4;
window.EP = {
  dur: 34.8, voEnd: 31.4,
  punchIns: [[S2, S3], [S4, S5], [S7, END_MOS]],
  cuts: [S2, S3, S4, S5, S6, S7, END_IN],
  captions: [[S2, S3, 1040], [S4, S5, 1040], [S6, S7, 1040], [S7, END_MOS, 1040]],
  frame(T) {
    if (T < S2) sceneHook(T);
    else if (T < S3) sceneShred(T);
    else if (T < S4) scenePDF(T);
    else if (T < S5) sceneCheckin(T);
    else if (T < S6) sceneBut(T);
    else if (T < S7) sceneDeal(T);
    else if (T < END_IN) sceneCTA(T);
    else endCard(T, END_IN, this.dur);
    mosaic(T, END_MOS, 9);
  },
  cues() {
    cue(0, 'whoosh', { d: .4, gain: .35 }); cue(.05, 'thud', { f: 50, d: .5, gain: .55 }); cue(.9, 'thud', { f: 60, d: .4, gain: .45 }); cue(1.76, 'pop', { f: 900, gain: .22 }); lowerThird.cue(.6);
    cue(3.5, 'pop', { f: 800, gain: .2 }); cue(4.6, 'whoosh', { d: .4, bright: .5, gain: .25 }); stampCue(6.8);
    iris.cue(S3 - .45); cue(8.42, 'pop', { f: 900, gain: .2 }); cue(9.22, 'riser', { d: .5, gain: .12 }); cue(9.96, 'whoosh', { d: .6, bright: .2, gain: .2 }); stampCue(11.66);
    cue(S4, 'whoosh', { d: .35, gain: .3 }); cue(13.2, 'pop', { f: 900, gain: .2 }); cue(14.12, 'thud', { f: 90, d: .2, gain: .3 }); cue(14.74, 'pop', { f: 1000, gain: .2 }); stampCue(16.1);
    whip.cue(S5 - .2); cue(S5, 'thud', { f: 40, d: .6, gain: .6 }); cue(17.92, 'pop', { f: 800, gain: .2 }); cue(19.0, 'pop', { f: 1000, gain: .2 }); cue(20.2, 'chime', { f: 988, gain: .12 });
    cue(S6, 'whoosh', { d: .35, gain: .3 }); STEPS.forEach(([, at]) => { cue(at, 'pop', { f: 900, gain: .22 }); cue(at + .25, 'click', { gain: .3 }); }); cue(24.98, 'thud', { f: 60, d: .35, gain: .4 });
    cue(S7, 'whoosh', { d: .35, gain: .3 }); cue(27.5, 'pop', { f: 1000, gain: .25 }); cue(29.88, 'chime', { f: 1175, gain: .12 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};
function stampCue(t) { cue(t, 'thud', { f: 55, d: .4, gain: .5 }); cue(t, 'glass', { n: 20, span: .2 }); }
// Red ✗ "not your guy" stamp, always placed below the chin (y given).
function noStamp(T, at, txt, y) { const q = back((T - at) / .3); if (q <= 0) return; g.save(); g.translate(540, y); g.rotate(-.06); g.scale(q * (2 - q), q * (2 - q));
  font(900, 74, COND); const w = g.measureText(txt).width + 150; g.fillStyle = BLUE; g.beginPath(); g.roundRect(-w / 2, -58, w, 116, 18); g.fill();
  g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('✗  ' + txt, 0, 26); g.textAlign = 'left'; g.restore(); }

// Hook: "DON'T WORK WITH ME" behind his head + name card + "if this sounds like you".
function sceneHook(T) {
  th(FULL, BZ + T * .01);
  // hook as a type block on the chest (he stands centred, so text behind the head would be hidden)
  const hp = expo(T / .3); g.save(); g.globalAlpha = .88 * hp; g.fillStyle = NAVY; g.beginPath(); g.roundRect(30, 880, 1020, 520, 26); g.fill(); g.restore(); g.save();
  rise("DON'T WORK", 60, 1050, T - .02, { size: 165, w: 900, col: WHITE, dur: .4 });
  rise('WITH ME', 60, 1200, T - .9, { size: 165, w: 900, col: BLUE, dur: .4 }); g.restore();
  if (T > 1.76) { const q = back((T - 1.76) / .35); g.save(); g.translate(60, 1260); g.scale(q, q); font(700, 46, BODY); const w = g.measureText('IF THIS SOUNDS LIKE YOU…').width + 56;
    g.fillStyle = WHITE; g.beginPath(); g.roundRect(0, 0, w, 90, 45); g.fill(); g.fillStyle = INK; g.fillText('IF THIS SOUNDS LIKE YOU…', 28, 61); g.restore(); }
  cluster(21, 990, 820, 4, 60, 56, T - .2, { from: [400, -100] });
  lowerThird(T, .6, 2.7, 'Jackson Farrier', 'Committed Coaching', 1450);
}

// 30-day shred: weight drops then rebounds straight after Christmas.
function sceneShred(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = expo((T - S2 - .1) / .45); if (p <= 0) return;
  const x = 70, y = 1120 + (1 - p) * 500, w = 940, h = 420;
  card(x, y, w, h, WHITE, 26, .35);
  font(900, 54, COND); g.fillStyle = INK; g.fillText('30-DAY SHRED', x + 40, y + 76);
  typeOn('Body weight', x + 40, y + 124, T - 3.6, { size: 30, col: GREY, track: 4, upper: true, cps: 40 });
  const gx = x + 40, gy = y + 180, gw = w - 80, gh = 190, dr = clamp((T - 3.5) / 1.2), rb = clamp((T - 5.5) / .9);
  const pt = u => u < .55 ? [gx + gw * u, gy + gh * (.15 + .65 * (u / .55))] : [gx + gw * u, gy + gh * (.8 - .7 * ((u - .55) / .45))];
  g.strokeStyle = '#E5E5E8'; g.lineWidth = 2; for (let k = 0; k < 4; k++) { g.beginPath(); g.moveTo(gx, gy + k * gh / 3); g.lineTo(gx + gw, gy + k * gh / 3); g.stroke(); }
  const upto = .55 * dr + .45 * rb; g.lineWidth = 8; g.lineCap = 'round'; g.lineJoin = 'round';
  g.strokeStyle = INK; g.beginPath(); for (let k = 0; k <= 50 * Math.min(upto, .55) / .55; k++) { const [px, py] = pt(k / 50 * Math.min(upto, .55)); k ? g.lineTo(px, py) : g.moveTo(px, py); } g.stroke();
  if (rb > 0) { g.strokeStyle = BLUE; g.beginPath(); for (let k = 0; k <= 30; k++) { const [px, py] = pt(.55 + .45 * rb * k / 30); k ? g.lineTo(px, py) : g.moveTo(px, py); } g.stroke();
    font(700, 38, BODY); g.fillStyle = BLUE; g.fillText('After Christmas', gx + gw * .5, gy - 16); }
  noStamp(T, 6.8, 'NOT YOUR GUY', 1700);
}

// PDF to download and forget: file downloads, gathers dust, 0 opens.
function scenePDF(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('If you want a', 60, 260, T - S3, { size: 34, col: BLUE, track: 6, upper: true, cps: 40 });
  rise('PDF to download', 54, 440, T - 8.42, { size: 120, w: 900, col: INK, dur: .45 });
  rise('and forget.', 54, 580, T - 9.96, { size: 120, w: 900, col: GREY, dur: .45 });
  const p = back((T - 8.42) / .45), dust = clamp((T - 9.96) / 1.2), cx = 540, cy = 1040;
  if (p > 0) { g.save(); g.translate(cx, cy); g.scale(p, p); g.rotate(dust * -.05); g.globalAlpha = 1 - dust * .45;
    g.fillStyle = WHITE; g.shadowColor = 'rgba(0,0,0,.15)'; g.shadowBlur = 30; g.shadowOffsetY = 12; const f = 60;
    g.beginPath(); g.moveTo(-170, -220); g.lineTo(170 - f, -220); g.lineTo(170, -220 + f); g.lineTo(170, 220); g.lineTo(-170, 220); g.closePath(); g.fill(); g.shadowColor = 'transparent';
    g.fillStyle = BLUE; g.beginPath(); g.roundRect(-130, 110, 260, 80, 12); g.fill(); font(900, 50, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('PDF', 0, 168); g.textAlign = 'left';
    g.fillStyle = '#DADADF'; for (let k = 0; k < 4; k++) g.fillRect(-120, -150 + k * 50, 240 - k * 30, 16);
    if (dust > 0) { const r = rng(5); for (let k = 0; k < 60 * dust; k++) { g.fillStyle = 'rgba(140,130,110,.5)'; g.fillRect(-170 + r() * 340, -220 + r() * 440, 3 + r() * 4, 3 + r() * 4); } }
    g.restore(); }
  // download progress then "0 opens"
  const dl = clamp((T - 9.22) / .7); if (T > 9.22) { g.fillStyle = '#DADADF'; g.beginPath(); g.roundRect(240, 1330, 600, 22, 11); g.fill(); g.fillStyle = INK; g.beginPath(); g.roundRect(240, 1330, 600 * dl, 22, 11); g.fill();
    font(700, 44, BODY); g.fillStyle = GREY; g.fillText(dl < 1 ? 'Downloading…' : 'Opened 0 times', 240, 1420); }
  noStamp(T, 11.66, 'ALSO NOT YOUR GUY', 1600);
  faceCircle(920, 1800, 90, back((T - S3 - .3) / .6));
}

// Check-ins: a weekly check-in where the answer and the truth don't match.
function sceneCheckin(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = expo((T - S4 - .05) / .45); if (p <= 0) return;
  const x = 70, y = 1120 + (1 - p) * 500, w = 940, h = 440;
  card(x, y, w, h, WHITE, 26, .35);
  font(900, 50, COND); g.fillStyle = INK; g.fillText('WEEKLY CHECK-IN', x + 40, y + 72);
  [['Followed plan?', 'Yes, 100%', 13.2], ['Hit protein?', 'Every day', 14.74]].forEach(([q, a, at], i) => { const r = expo((T - at) / .3); if (r <= 0) return; const ry = y + 160 + i * 130;
    g.globalAlpha = r; font(600, 42, BODY); g.fillStyle = GREY; g.fillText(q, x + 40, ry); font(700, 42, BODY); g.fillStyle = INK; g.fillText(a, x + 560, ry);
    if (T > at + .5) { g.fillStyle = BLUE; g.fillRect(x + 556, ry - 14, g.measureText(a).width + 8, 6); font(700, 36, BODY); g.fillText(['(really: 3 of 7)', '(really: twice)'][i], x + 560, ry + 48); } g.globalAlpha = 1; });
  noStamp(T, 16.1, "WE'RE NOT GOING TO WORK", 1700);
}

// BUT: slam on black, then business KPIs vs body KPIs, treated the same way.
function sceneBut(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  letterDrop('BUT', 60, 420, T - S5, { size: 300, col: BLUE, stagger: .06 });
  typeOn('If you’re a business owner…', 66, 570, T - 17.3, { size: 48, col: WHITE, track: 2, w: 700, fam: BODY, cps: 34 });
  [['YOUR BUSINESS', 17.92, [.3, .38, .5, .62, .78, .9]], ['YOUR BODY', 19.0, [.25, .3, .42, .55, .7, .85]]].forEach(([lab, at, pts], i) => {
    const q = back((T - at) / .45); if (q <= 0) return; const x = 60 + i * 500, y = 700, w = 460, h = 560;
    g.save(); g.translate(x + w / 2, y + h / 2); g.scale(q, q); g.translate(-(x + w / 2), -(y + h / 2)); card(x, y, w, h, '#151518', 26, .4);
    font(900, 44, COND); g.fillStyle = WHITE; g.fillText(lab, x + 30, y + 70);
    const gx = x + 30, gy = y + 480, gw = w - 60, gh = 320, u = expo((T - at - .2) / 1.0);
    g.strokeStyle = i ? BLUE : WHITE; g.lineWidth = 8; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath();
    const n = (pts.length - 1) * u; for (let k = 0; k <= Math.ceil(n); k++) { const kk = Math.min(k, n), a0 = Math.floor(kk), f = kk - a0, v = lerp(pts[a0], pts[Math.min(a0 + 1, pts.length - 1)], f);
      const X = gx + gw * kk / (pts.length - 1), Y = gy - gh * v; k ? g.lineTo(X, Y) : g.moveTo(X, Y); } g.stroke();
    font(700, 32, BODY); g.fillStyle = GREY; g.fillText(i ? 'Training · food' : 'Systems · numbers', x + 30, y + 530); g.restore(); });
  rise('Same standard.', 60, 1460, T - 20.2, { size: 120, w: 900, col: WHITE, dur: .45 });
  faceCircle(910, 1760, 110, back((T - S5 - .3) / .6));
}

// The deal: three steps tick off under the chin, then "I'll handle the rest".
const STEPS = [['SHOW UP', 21.22], ['FOLLOW THE PLAN', 22.28], ['TELL THE TRUTH, WEEKLY', 23.34]];
function sceneDeal(T) {
  th(FULL, BZ); captions(T);
  STEPS.forEach(([lab, at], i) => { const q = back((T - at) / .35); if (q <= 0) return; const y = 1160 + i * 140;
    g.save(); g.translate(70, y); g.scale(q, q); card(0, 0, 940, 112, '#0A0A0A', 20, .4);
    g.fillStyle = BLUE; g.beginPath(); g.arc(60, 56, 30, 0, 7); g.fill(); g.strokeStyle = WHITE; g.lineWidth = 7; g.lineCap = 'round';
    if (T > at + .25) { g.beginPath(); g.moveTo(46, 56); g.lineTo(56, 67); g.lineTo(76, 44); g.stroke(); }
    font(900, 48, COND); g.fillStyle = WHITE; g.fillText(lab, 115, 74); g.restore(); });
  const r = back((T - 24.98) / .35); if (r > 0) { g.save(); g.translate(540, 1640); g.scale(r, r); font(900, 60, COND); const w = g.measureText("I'LL HANDLE THE REST.").width + 80;
    g.fillStyle = BLUE; g.beginPath(); g.roundRect(-w / 2, -54, w, 108, 54); g.fill(); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText("I'LL HANDLE THE REST.", 0, 22); g.textAlign = 'left'; g.restore(); }
}

// CTA: free video in bio, arrow bouncing, "we'll know quick if we're a fit".
function sceneCTA(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = back((T - 27.04) / .4); if (p <= 0) return; g.save(); g.translate(540, 1480); g.scale(p, p);
  card(-440, -170, 880, 340, BLUE, 30, .4); font(900, 84, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('FREE VIDEO', 0, -40);
  font(900, 52, BODY); g.fillText('in my bio', 0, 24); const b = Math.sin((T - 27.5) * 7) * 14;
  g.strokeStyle = WHITE; g.lineWidth = 10; g.lineCap = 'round'; g.beginPath(); g.moveTo(0, 60 + b); g.lineTo(0, 120 + b); g.moveTo(-26, 96 + b); g.lineTo(0, 124 + b); g.lineTo(26, 96 + b); g.stroke();
  g.textAlign = 'left'; g.restore();
  if (T > 29.88) { const q = expo((T - 29.88) / .35); g.save(); g.globalAlpha = q; font(700, 32, BODY); g.fillStyle = WHITE; g.textAlign = 'center';
    font(700, 48, BODY); g.fillText('We’ll know quick if we’re a fit.', 540, 1730); g.textAlign = 'left'; g.restore(); }
}
