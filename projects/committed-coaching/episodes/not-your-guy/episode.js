// Committed Coaching: "Don't work with me if…" anti-pitch (7 takes joined, 31.4s). v2: gym look.
// Take starts: 0, 2.84, 7.44, 12.4, 16.86, 21.22, 25.86 (jump cuts punch in; alternate takes zoom).
const S2 = 2.84, S3 = 7.44, S4 = 12.4, S5 = 16.86, S6 = 21.22, S7 = 25.86, END_MOS = 31.25, END_IN = END_MOS + .4;
window.EP = {
  dur: 34.8, voEnd: 31.4,
  punchIns: [[S2, S3], [S4, S5], [S7, END_MOS]],
  cuts: [S2, S3, S4, S5, S6, S7, END_IN],
  captions: [[S2, S3, 1000], [S4, S5, 1000], [S6, S7, 1000], [S7, END_MOS, 1000]],
  frame(T) {
    if (T < S2) sceneHook(T);
    else if (T < S3) sceneShred(T);
    else if (T < S4) scenePDF(T);
    else if (T < S5) sceneCheckin(T);
    else if (T < S6) sceneBut(T);
    else if (T < S7) sceneDeal(T);
    else if (T < END_IN) sceneCTA(T);
    else endCard(T, END_IN, this.dur);
    if (T < S2) gymClock(T); if (T >= S7 && T < END_IN) gymClock(T, expo((T - S7) / .3));
    slash(T, END_MOS - .35);
  },
  cues() {
    cue(0, 'thud', { f: 45, d: .5, gain: .55 }); cue(1.34, 'click', { gain: .3 }); lowerThird.cue(.6);
    cue(3.45, 'thud', { f: 110, d: .14, gain: .25 }); cue(4.6, 'click', { gain: .3 }); cue(5.66, 'click', { gain: .2 }); stamp.cue(6.92);
    cue(S3, 'thud', { f: 70, d: .3, gain: .35 }); cue(8.42, 'whoosh', { d: .3, bright: .3, gain: .15 }); cue(9.6, 'whoosh', { d: .3, bright: .3, gain: .15 }); cue(11.0, 'thud', { f: 90, d: .2, gain: .3 }); stamp.cue(11.66);
    cue(S4 + .05, 'whoosh', { d: .35, gain: .25 }); cue(14.12, 'click', { gain: .25 }); cue(15.2, 'click', { gain: .25 }); stamp.cue(16.1);
    cue(S5, 'thud', { f: 40, d: .6, gain: .6 }); cue(17.92, 'thud', { f: 70, d: .25, gain: .35 }); cue(19.34, 'thud', { f: 80, d: .2, gain: .3 }); cue(20.34, 'click', { gain: .3 }); stamp.cue(20.72);
    STEPS.forEach(([, at]) => cue(at, 'thud', { f: 110, d: .14, gain: .3 })); cue(24.98, 'click', { gain: .3 });
    cue(27.04, 'thud', { f: 60, d: .35, gain: .45 });
    slash.cue(END_MOS - .35); endCard.cue(END_IN);
  },
};
// scale font size down until txt fits maxW
function fit(txt, size, fam, maxW) { font(400, size, fam); const w = g.measureText(txt).width; return w > maxW ? size * maxW / w : size; }

// Hook: on screen from frame 0 (it's the thumbnail). Black slab on the chest, tape name card.
function sceneHook(T) {
  th(FULL, BZ + T * .01);
  const s = lerp(1.1, 1, expo(T / .25)); g.save(); g.translate(540, 1120); g.scale(s, s); g.translate(-540, -1120);
  g.globalAlpha = .9; slab(50, 880, 960, 440, '#0A0A0A', -.12); g.globalAlpha = 1;
  font(400, fit("DON'T WORK", 210, COND, 860), COND); g.fillStyle = WHITE; g.fillText("DON'T WORK", 100, 1080);
  font(400, 210, COND); g.fillStyle = BLUE; g.fillText('WITH ME', 100, 1290); g.restore();
  if (T > 1.34) { const q = back((T - 1.34) / .3); g.save(); g.translate(96, 1338); g.rotate(-.03); g.scale(q, q); font(400, 46, COND); const w = g.measureText('IF THIS SOUNDS LIKE YOU…').width + 50;
    tape(0, 0, w, 70, TAPE, 0, 9); g.fillStyle = INK; g.letterSpacing = '2px'; g.fillText('IF THIS SOUNDS LIKE YOU…', 25, 53); g.letterSpacing = '0px'; g.restore(); }
  lowerThird(T, .6, 2.7, 'Jackson Farrier', 'Head Coach · Committed', 1520);
}

// 30-day shred on a digital scale: weight drops, then rebounds straight after Christmas.
function sceneShred(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = expo((T - 3.45) / .35); if (p <= 0) return;
  const x = 70, y = 1150 + (1 - p) * 140, w = 940, h = 420;
  g.globalAlpha = .94 * clamp(p * 1.5); slab(x, y, w, h, '#0E0E10', -.06); g.globalAlpha = 1;
  font(400, 64, COND); g.fillStyle = WHITE; g.fillText('30-DAY SHRED', x + 50, y + 92);
  font(400, 30, COND); g.fillStyle = GREY; g.letterSpacing = '5px'; g.fillText('BODY WEIGHT · KG', x + 52, y + 140); g.letterSpacing = '0px';
  const dr = inOut(clamp((T - 3.84) / .76)), rb = expo(clamp((T - 4.6) / 1.0)), kg = rb > 0 ? lerp(88, 95.5, rb) : lerp(96, 88, dr);
  led(kg.toFixed(1), x + w - 60, y + 46, 150, rb > 0 ? BLUE : WHITE, { align: 'right' });
  // daily bars along the bottom: 30 days down, then the Christmas spike
  for (let d = 0; d < 34; d++) { const u = d < 30 ? d / 29 : 1, show = d < 30 ? clamp(dr * 30 - d) : clamp(rb * 4 - (d - 30)); if (show <= 0) continue;
    const v = d < 30 ? lerp(96, 88, u) : lerp(88, 95.5, (d - 29) / 4), bh = (v - 84) * 8; g.fillStyle = d < 30 ? '#3A3A40' : BLUE; g.fillRect(x + 50 + d * 25, y + h - 36 - bh * show, 15, bh * show); }
  if (T > 5.66) { g.save(); g.globalAlpha = expo((T - 5.66) / .25); g.translate(x + 50, y + 262); g.rotate(-.04); font(400, 62, MARK); g.fillStyle = WHITE; g.fillText('after Christmas…', 0, 0); g.restore(); }
  stamp(T, 6.92, 'NOT YOUR GUY', 1610);
}

// PDF on a chalkboard: written up, downloaded, never opened.
const CHALK_BG = '#1E2421';
function chalkboard() { g.fillStyle = CHALK_BG; g.fillRect(0, 0, W, H); const r = rng(77); g.lineCap = 'round';
  for (let k = 0; k < 40; k++) { g.strokeStyle = `rgba(255,255,255,${.015 + r() * .03})`; g.lineWidth = 30 + r() * 90; g.beginPath(); const x = r() * W, y = r() * H; g.moveTo(x, y); g.quadraticCurveTo(x + 200 * (r() - .5), y + 100 * (r() - .5), x + 400 * (r() - .5), y + 150 * (r() - .5)); g.stroke(); }
  g.fillStyle = '#5B4632'; g.fillRect(0, 0, W, 34); g.fillRect(0, H - 34, W, 34); }
function scenePDF(T) {
  chalkboard();
  chalkWrite('If you want a', 70, 330, T - S3, { size: 70, dur: .25 });
  chalkWrite('PDF to download', 70, 480, T - 8.42, { size: fit('PDF to download', 100, CHALK, 900), dur: .55 });
  chalkWrite('& forget it.', 70, 610, T - 9.6, { size: 100, dur: .45, col: '#FF6A5C' });
  // chalk-outlined file, drawn on as soon as the scene starts
  const p = clamp((T - S3 - .05) / .45), cx = 540, cy = 980; if (p > 0) { g.save(); const kn = back(clamp((T - 11.0) / .4)); g.translate(cx, cy + kn * 60); g.rotate(-.04 + kn * .32); g.globalAlpha = 1 - kn * .55; g.strokeStyle = '#F1F1EC'; g.lineWidth = 9; g.lineJoin = 'round'; g.setLineDash([1400 * p, 3000]);
    g.beginPath(); g.moveTo(-150, -200); g.lineTo(90, -200); g.lineTo(150, -140); g.lineTo(150, 200); g.lineTo(-150, 200); g.closePath(); g.stroke(); g.setLineDash([]);
    if (p > .7) { font(400, 80, CHALK); g.fillStyle = '#FF6A5C'; g.textAlign = 'center'; g.globalAlpha = (p - .7) / .3; g.fillText('PDF', 0, 40); g.textAlign = 'left'; g.globalAlpha = 1; }
    g.restore(); }
  const dl = clamp((T - 9.22) / .7); if (T > 9.22) { g.strokeStyle = '#F1F1EC'; g.lineWidth = 6; g.strokeRect(240, 1260, 600, 44); g.fillStyle = 'rgba(241,241,236,.85)'; g.fillRect(250, 1270, 580 * dl, 24);
    chalkWrite(dl < 1 ? 'downloading…' : 'opened: 0 times', 240, 1390, T - 9.3, { size: 54, dur: .3, col: dl < 1 ? '#F1F1EC' : '#FF6A5C' }); }
  stamp(T, 11.66, 'ALSO NOT YOUR GUY', 1600);
  facePin(870, 190, 200, back((T - S3) / .3));
}

// Weekly check-in on a clipboard: the answer vs the marker-pen truth.
function sceneCheckin(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = expo((T - S4 - .05) / .4); if (p <= 0) return;
  const ex = expoIn((T - 15.85) / .25); if (ex < 1) { const x = 90, y = 1160 + (1 - p) * 140 + ex * 900, w = 900, h = 450;
  g.save(); g.globalAlpha = clamp(p * 1.5); g.translate(540, y + h / 2); g.rotate(-.02 * (1 - p) + .012); g.translate(-540, -(y + h / 2));
  g.fillStyle = '#8A6A45'; g.beginPath(); g.roundRect(x, y, w, h, 18); g.fill();   // clipboard
  g.fillStyle = '#F7F5EF'; g.fillRect(x + 26, y + 40, w - 52, h - 62);
  g.strokeStyle = '#CFE0F0'; g.lineWidth = 2; for (let k = 0; k < 5; k++) { g.beginPath(); g.moveTo(x + 26, y + 150 + k * 66); g.lineTo(x + w - 26, y + 150 + k * 66); g.stroke(); }
  g.fillStyle = '#9DA0A8'; g.beginPath(); g.roundRect(x + w / 2 - 110, y - 18, 220, 62, 10); g.fill();   // clip
  font(400, 56, COND); g.fillStyle = INK; g.fillText('WEEKLY CHECK-IN', x + 56, y + 120);
  [['Followed the plan?', 'YES, 100%', 13.48, '3/7', 14.12], ['Hit protein?', 'EVERY DAY', 14.74, 'twice', 15.2]].forEach(([q, a, at, truth, ht], i) => { const r = expo((T - at) / .3); if (r <= 0) return; const ry = y + 210 + i * 130;
    g.globalAlpha = r * clamp(p * 1.5); font(600, 38, BODY); g.fillStyle = '#5A5D66'; g.fillText(q, x + 56, ry); font(400, 46, COND); g.fillStyle = INK; g.fillText(a, x + 520, ry);
    const s = clamp((T - ht) / .2); if (s > 0) { const aw = g.measureText(a).width; g.strokeStyle = BLUE; g.lineWidth = 7; g.lineCap = 'round'; g.beginPath(); g.moveTo(x + 512, ry - 16); g.lineTo(x + 512 + (aw + 16) * s, ry - 22); g.stroke();
      if (s >= 1) { g.save(); g.translate(x + 520, ry + 54); g.rotate(-.04); font(400, 40, MARK); g.fillStyle = BLUE; g.fillText('really: ' + truth, 0, 0); g.restore(); } }
    g.globalAlpha = clamp(p * 1.5); });
  g.restore(); }
  stamp(T, 16.1, 'NO DEAL.', 1360);
}

// BUT: slams on black. Business bar is loaded; the body bar gets loaded to match.
function sceneBut(T) {
  chalkboard(); g.fillStyle = 'rgba(8,8,8,.82)'; g.fillRect(0, 0, W, H);
  const s = lerp(1.25, 1, expo((T - S5) / .2)); g.save(); g.translate(70, 400); g.scale(s, s); font(400, 330, COND); g.fillStyle = BLUE; g.fillText('BUT', 0, 0); g.restore();
  rise('IF YOU’RE A BUSINESS OWNER…', 72, 510, T - 17.26, { size: 62, w: 400, col: WHITE, dur: .4 });
  const FULLP = [300, 260, 220], bz = expo((T - 17.92) / .5), bd = expo((T - 20.34) / .4);
  if (T > 17.92) { rise('YOUR BUSINESS', 72, 680, T - 17.92, { size: 64, w: 400, col: WHITE, dur: .35 }); barbell(540, 880, 900, FULLP, bz); }
  if (T > 19.34) { rise('YOUR BODY', 72, 1140, T - 19.34, { size: 64, w: 400, col: WHITE, dur: .35 }); barbell(540, 1340, 900, T < 20.34 ? [120] : FULLP, T < 20.34 ? expo((T - 19.44) / .4) : bd); }
  stamp(T, 20.72, 'SAME STANDARD.', 1580, -.04, '');
  facePin(870, 230, 210, back((T - S5 - .3) / .4), -.05);
}

// The deal: three reps tick off under the chin, then "I'll handle the rest" in marker on tape.
const STEPS = [['SHOW UP', 21.22], ['FOLLOW THE PLAN', 22.28], ['TELL THE TRUTH, WEEKLY', 23.34]];
function sceneDeal(T) {
  th(FULL, zoomAt(T)); captions(T);
  STEPS.forEach(([lab, at], i) => { const q = expo((T - at) / .3); if (q <= 0) return; const y = 1130 + i * 132, x = 70 - (1 - q) * 260; if (q < 1) g.globalAlpha = q;
    g.save(); g.translate(x, y); g.rotate([-.015, .01, -.008][i]); tape(0, 0, 940, 112, TAPE, 0, 30 + i);
    font(400, 70, MARK); g.fillStyle = BLUE; g.fillText(`${i + 1}.`, 34, 84);
    font(400, fit(lab, 54, MARK, 640), MARK); g.fillStyle = INK; g.fillText(lab, 130, 80); g.restore();
    if (T > at + .3) { const c = clamp((T - at - .3) / .15); g.strokeStyle = BLUE; g.lineWidth = 12; g.lineCap = 'round'; g.beginPath(); g.moveTo(x + 860, y + 58); g.lineTo(x + 860 + 16 * c, y + 58 + 18 * c); if (c >= 1) g.lineTo(x + 916, y + 30); g.stroke(); } g.globalAlpha = 1; });
  const r = back((T - 24.98) / .3); if (r > 0) { g.save(); g.translate(130, 1530); g.rotate(-.04); g.scale(r, r); font(400, 72, MARK); const w = g.measureText("I'll handle the rest.").width + 70;
    tape(0, 0, w, 110, TAPE, 0, 21); g.fillStyle = BLUE; g.fillText("I'll handle the rest.", 35, 82); g.restore(); }
}

// CTA: red slab, free video in my bio, arrow bouncing. Kept well above Instagram's bottom UI.
function sceneCTA(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = back((T - 27.04) / .35); if (p <= 0) return; g.save(); const br = 1 + .015 * Math.sin((T - 27) * 5); g.translate(540, 1300); g.scale(p * br, p * br); g.rotate(-.03);
  slab(-430, -170, 860, 330, BLUE, -.12); font(400, 140, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('FREE VIDEO', 10, -10);
  g.globalAlpha = expo((T - 28.06) / .25); font(400, 60, COND); g.letterSpacing = '6px'; g.fillText('IN MY BIO', -30, 90); g.letterSpacing = '0px'; const b = Math.sin((T - 27.5) * 7) * 10;
  g.strokeStyle = WHITE; g.lineWidth = 12; g.lineCap = 'round'; g.beginPath(); g.moveTo(190, 40 + b); g.lineTo(190, 100 + b); g.moveTo(164, 76 + b); g.lineTo(190, 104 + b); g.lineTo(216, 76 + b); g.stroke(); g.globalAlpha = 1;
  if (T > 27.5) { tape(-470, -200, 150, 50, TAPE, -.5, 41); tape(330, 120, 150, 50, TAPE, -.5, 42); }
  g.textAlign = 'left'; g.restore();
}
