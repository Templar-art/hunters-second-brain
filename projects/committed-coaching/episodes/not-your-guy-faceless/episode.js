// Committed Coaching: "Don't work with me if…" FACELESS cut: same VO, music and SFX; graphics fill the frame.
// Take starts: 0, 2.84, 7.44, 12.4, 16.86, 21.22, 25.86 (jump cuts punch in; alternate takes zoom).
const S2 = 2.84, S3 = 7.44, S4 = 12.4, S5 = 16.86, S6 = 21.22, S7 = 25.86, END_MOS = 31.25, END_IN = END_MOS + .4;
window.EP = {
  dur: 34.8, voEnd: 31.4,
  cuts: [S2, S3, S4, S5, S6, S7, END_IN],
  captions: [[S2, S3, 520, null, 150], [S4, S5, 520, null, 150], [S6, S7, 520, null, 150], [S7, END_MOS, 520, null, 150]],   // big kinetic captions carry the voice
  frame(T) {
    if (T < S2) sceneHook(T);
    else if (T < S3) sceneShred(T);
    else if (T < S4) scenePDF(T);
    else if (T < S5) sceneCheckin(T);
    else if (T < S6) sceneBut(T);
    else if (T < S7) sceneDeal(T);
    else if (T < END_IN) sceneCTA(T);
    else endCard(T, END_IN, this.dur);
    if (T >= S7 && T < END_IN) gymClock(T, expo((T - S7) / .3));
    slash(T, END_MOS - .35);
  },
  cues() {
    cue(0, 'boom', { gain: .5 }); cue(1.34, 'click', { gain: .3 }); lowerThird.cue(.6);
    cue(3.45, 'whoosh', { d: .35, gain: .3 }); cue(4.6, 'click', { gain: .3 }); cue(5.66, 'click', { gain: .2 }); stamp.cue(6.68);
    cue(S3, 'hit', { gain: .4 }); cue(11.0, 'thud', { f: 90, d: .2, gain: .22 }); stamp.cue(11.66);
    cue(S4 + .2, 'whoosh', { d: .35, gain: .3 }); cue(14.12, 'click', { gain: .25 }); cue(15.2, 'click', { gain: .25 }); stamp.cue(16.1);
    cue(S5 - .02, 'riser', { gain: .22 }); cue(S5, 'boom', { gain: .6 }); cue(17.95, 'thud', { f: 70, d: .25, gain: .3 }); cue(19.4, 'thud', { f: 80, d: .2, gain: .25 }); cue(20.34, 'click', { gain: .3 }); stamp.cue(20.72);
    STEPS.forEach(([, at]) => cue(at, 'thud', { f: 110, d: .14, gain: .22 })); cue(24.98, 'click', { gain: .3 });
    cue(27.04, 'hit', { gain: .4 });
    slash.cue(END_MOS - .35); endCard.cue(END_IN);
  },
};
// scale font size down until txt fits maxW
function fit(txt, size, fam, maxW) { font(400, size, fam); const w = g.measureText(txt).width; return w > maxW ? size * maxW / w : size; }


// dark gym backdrop: chalk-dusted black with one red slash that moves per scene
function gymBg(T, k) { chalkboard(); g.fillStyle = 'rgba(8,8,8,.74)'; g.fillRect(0, 0, W, H);
  const r = rng(200 + k); for (let i = 0; i < 260; i++) { const x = r() * W, y = (r() * H - T * (8 + r() * 14)) % H; g.fillStyle = `rgba(255,255,255,${.04 + r() * .1})`; g.fillRect(x, y < 0 ? y + H : y, 2 + r() * 3, 2 + r() * 3); }   // drifting chalk dust
  const v = g.createRadialGradient(W / 2, H * .45, H * .2, W / 2, H * .45, H * .75); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.55)'); g.fillStyle = v; g.fillRect(0, 0, W, H); }

// Hook: the thumbnail. Full-frame type from frame 0.
function sceneHook(T) {
  gymBg(T, 0); { g.save(); led(`00:0${Math.floor(Math.max(0, T))}`, 540, 360, 210, BLUE, { align: 'center', ghost: false }); g.restore(); }
  const s = lerp(1.1, 1, expo(T / .25)); g.save(); g.translate(540, 1000); g.scale(s, s); g.translate(-540, -1000);
  font(400, fit("DON'T WORK", 280, COND, 860), COND); g.fillStyle = WHITE; g.fillText("DON'T WORK", 90, 960);
  font(400, fit('WITH ME', 300, COND, 860), COND); g.fillStyle = BLUE; g.fillText('WITH ME', 90, 1240); g.restore();
  if (T > 1.34) { const q = back((T - 1.34) / .3); g.save(); g.translate(96, 1310); g.rotate(-.03); g.scale(q, q); font(400, 60, COND); const w = g.measureText('IF THIS SOUNDS LIKE YOU…').width + 60;
    tape(0, 0, w, 90, TAPE, 0, 9); g.fillStyle = INK; g.letterSpacing = '2px'; g.fillText('IF THIS SOUNDS LIKE YOU…', 30, 68); g.letterSpacing = '0px'; g.restore(); }
  lowerThird(T, .6, 2.7, 'Jackson Farrier', 'Head Coach · Committed', 1500);
}

// 30-day shred: a big digital scale fills the frame.
function sceneShred(T) {
  gymBg(T, 1); captions(T);
  const p = expo((T - 3.45) / .35), out = expoIn((T - 6.45) / .2); if (p <= 0) return;
  if (out < 1) { const x = 60, y = 760 + (1 - p) * 140 + out * 1300, w = 960, h = 780;   // card drops away before the stamp lands, so the stamp never covers the digits
  g.globalAlpha = clamp(p * 1.5); slab(x, y, w, h, '#16161A', -.05);
  font(400, 84, COND); g.fillStyle = WHITE; g.fillText('30-DAY SHRED', x + 60, y + 120);
  font(400, 36, COND); g.fillStyle = GREY; g.letterSpacing = '6px'; g.fillText('BODY WEIGHT · KG', x + 62, y + 176); g.letterSpacing = '0px';
  const dr = inOut(clamp((T - 3.84) / .76)), rb = expo(clamp((T - 4.6) / 1.0)), kg = rb > 0 ? lerp(88, 95.5, rb) : lerp(96, 88, dr);
  if (rb > 0 && rb < .6) { g.strokeStyle = `rgba(224,32,32,${1 - rb / .6})`; g.lineWidth = 14; g.strokeRect(x + 10, y + 10, w - 20, h - 20); }
  led(kg.toFixed(1), x + w / 2, y + 240, 300, rb > 0 ? BLUE : WHITE, { align: 'center' });
  for (let d = 0; d < 34; d++) { const u = d < 30 ? d / 29 : 1, show = d < 30 ? clamp(dr * 30 - d) : clamp(rb * 4 - (d - 30)); if (show <= 0) continue;
    const v = d < 30 ? lerp(96, 88, u) : lerp(88, 95.5, (d - 29) / 4), bh = (v - 84) * 9; g.fillStyle = d < 30 ? '#3A3A40' : BLUE; g.fillRect(x + 60 + d * 25, y + h - 50 - bh * show, 15, bh * show); }
  g.globalAlpha = 1;
  if (T > 5.66) { g.save(); g.globalAlpha = expo((T - 5.66) / .25); g.translate(x + 60, y + 640); g.rotate(-.04); font(400, 72, MARK); g.fillStyle = WHITE; g.fillText('after Christmas…', 0, 0); g.restore(); } }
  g.save(); g.translate(540, 1150); g.scale(1.6, 1.6); g.translate(-540, -1150); stamp(T, 6.68, 'NOT YOUR GUY', 1150, -.1); g.restore();
}
// PDF on a chalkboard: written up, downloaded, never opened.
const CHALK_BG = '#1E2421';
function chalkboard() { g.fillStyle = CHALK_BG; g.fillRect(0, 0, W, H); const r = rng(77); g.lineCap = 'round';
  for (let k = 0; k < 40; k++) { g.strokeStyle = `rgba(255,255,255,${.015 + r() * .03})`; g.lineWidth = 30 + r() * 90; g.beginPath(); const x = r() * W, y = r() * H; g.moveTo(x, y); g.quadraticCurveTo(x + 200 * (r() - .5), y + 100 * (r() - .5), x + 400 * (r() - .5), y + 150 * (r() - .5)); g.stroke(); }
  g.fillStyle = '#5B4632'; g.fillRect(0, 0, W, 34); g.fillRect(0, H - 34, W, 34); }
function scenePDF(T) {
  chalkboard();
  chalkWrite('If you want a', 70, 330, T - S3, { size: 70, dur: .12 });
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
}


// Weekly check-in: the clipboard is the whole shot.
function sceneCheckin(T) {
  gymBg(T, 2); captions(T);
  const p = expo((T - S4) / .22); if (p <= 0) return;
  const ex = expoIn((T - 15.85) / .25); if (ex < 1) { const x = 70, y = 760 + (1 - p) * 80 + ex * 1300, w = 940, h = 820;
  g.save(); g.globalAlpha = clamp(p * 1.5); g.translate(540, y + h / 2); g.rotate(.012); g.translate(-540, -(y + h / 2));
  g.fillStyle = '#8A6A45'; g.beginPath(); g.roundRect(x, y, w, h, 20); g.fill();
  g.fillStyle = '#F7F5EF'; g.fillRect(x + 28, y + 44, w - 56, h - 70);
  g.strokeStyle = '#CFE0F0'; g.lineWidth = 2; for (let k = 0; k < 7; k++) { g.beginPath(); g.moveTo(x + 28, y + 190 + k * 70); g.lineTo(x + w - 28, y + 190 + k * 70); g.stroke(); }
  g.fillStyle = '#9DA0A8'; g.beginPath(); g.roundRect(x + w / 2 - 120, y - 20, 240, 70, 10); g.fill();
  font(400, 76, COND); g.fillStyle = INK; g.fillText('WEEKLY CHECK-IN', x + 60, y + 150);
  [['Followed the plan?', 'YES, 100%', 13.48, '3/7', 14.12], ['Hit protein?', 'EVERY DAY', 14.74, 'twice', 15.2]].forEach(([q, a, at, truth, ht], i) => { const r = expo((T - at) / .3); if (r <= 0) return; const ry = y + 320 + i * 230;
    g.globalAlpha = r * clamp(p * 1.5); font(600, 46, BODY); g.fillStyle = '#5A5D66'; g.fillText(q, x + 60, ry); font(400, 60, COND); g.fillStyle = INK; g.fillText(a, x + 560, ry);
    const s = clamp((T - ht) / .2); if (s > 0) { const aw = g.measureText(a).width; g.strokeStyle = BLUE; g.lineWidth = 8; g.lineCap = 'round'; g.beginPath(); g.moveTo(x + 550, ry - 20); g.lineTo(x + 550 + (aw + 20) * s, ry - 28); g.stroke();
      if (s >= 1) { g.save(); g.translate(x + 560, ry + 72); g.rotate(-.04); font(400, 54, MARK); g.fillStyle = BLUE; g.fillText('really: ' + truth, 0, 0); g.restore(); } }
    g.globalAlpha = clamp(p * 1.5); });
  g.restore(); }
  g.save(); g.translate(540, 1050); g.scale(2.3, 2.3); g.translate(-540, -1050); stamp(T, 16.1, 'NO DEAL.', 1050, -.1); g.restore();
}
// BUT: slams on black. Business bar is loaded; the body bar gets loaded to match.
function sceneBut(T) {
  chalkboard(); g.fillStyle = 'rgba(8,8,8,.82)'; g.fillRect(0, 0, W, H);
  const s = lerp(1.25, 1, expo((T - S5) / .2)); g.save(); g.translate(70, 400); g.scale(s, s); font(400, 330, COND); g.fillStyle = BLUE; g.fillText('BUT', 0, 0); g.restore();
  rise('IF YOU’RE A BUSINESS OWNER…', 72, 510, T - 17.26, { size: 62, w: 400, col: WHITE, dur: .4 });
  const FULLP = [300, 260, 220], bz = expo((T - 17.92) / .5), bd = expo((T - 20.34) / .4);
  if (T > 17.92) { rise('YOUR BUSINESS', 72, 680, T - 17.92, { size: 64, w: 400, col: WHITE, dur: .35 }); barbell(540, 880, 900, FULLP, bz); }
  if (T > 19.34) { rise('YOUR BODY', 72, 1140, T - 19.34, { size: 64, w: 400, col: WHITE, dur: .35 }); barbell(540, 1340, 900, T < 20.34 ? [120] : FULLP, T < 20.34 ? expo((T - 19.44) / .4) : bd); }
  g.save(); g.translate(540, 1560); g.scale(1.45, 1.45); g.translate(-540, -1560); stamp(T, 20.72, 'SAME STANDARD.', 1560, -.06, ''); g.restore();
}

// The deal: three big tape rows, then "I'll handle the rest".
const STEPS = [['SHOW UP', 21.22], ['FOLLOW THE PLAN', 22.28], ['TELL THE TRUTH, WEEKLY', 23.34]];
function sceneDeal(T) {
  gymBg(T, 3); captions(T);
  STEPS.forEach(([lab, at], i) => { const q = expo((T - at) / .3); if (q <= 0) return; const y = 760 + i * 230, x = 60 - (1 - q) * 260; if (q < 1) g.globalAlpha = q;
    g.save(); g.translate(x, y); g.rotate([-.015, .01, -.008][i]); tape(0, 0, 960, 190, TAPE, 0, 30 + i);
    font(400, 120, MARK); g.fillStyle = BLUE; g.fillText(`${i + 1}.`, 36, 140);
    font(400, fit(lab, 88, MARK, 640), MARK); g.fillStyle = INK; g.fillText(lab, 170, 128); g.restore();
    if (T > at + .3) { const c = clamp((T - at - .3) / .15); g.strokeStyle = BLUE; g.lineWidth = 14; g.lineCap = 'round'; g.beginPath(); g.moveTo(x + 850, y + 100); g.lineTo(x + 850 + 24 * c, y + 100 + 26 * c); if (c >= 1) g.lineTo(x + 930, y + 54); g.stroke(); } g.globalAlpha = 1; });
  const r = back((T - 24.98) / .3); if (r > 0) { g.save(); g.translate(540, 1530); g.rotate(-.04); g.scale(r, r); font(400, 100, MARK); const w = g.measureText("I'll handle the rest.").width + 80;
    tape(-w / 2, -80, w, 150, BLUE, 0, 21); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText("I'll handle the rest.", 0, 32); g.textAlign = 'left'; g.restore(); }
}

// CTA: big red slab + bouncing arrow, handle underneath.
function sceneCTA(T) {
  gymBg(T, 4); captions(T);
  { const u = back((T - 26.3) / .3); if (u > 0 && T < 27.04) { g.save(); g.translate(540, 960); g.rotate(-.07); g.scale(u * 1.05, u * 1.05); tape(-400, -80, 800, 150, TAPE, 0, 51); font(400, 96, MARK); g.fillStyle = INK; g.textAlign = 'center'; g.fillText('sound like you?', 0, 30); g.textAlign = 'left'; g.restore(); } }
  const p = back((T - 27.04) / .35); if (p <= 0) return; const br = 1 + .015 * Math.sin((T - 27) * 5);
  g.save(); g.translate(515, 1060); g.scale(p * br * .98, p * br * .98); g.rotate(-.03);
  slab(-460, -220, 920, 440, BLUE, -.12); font(400, 190, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('FREE VIDEO', 14, 10);
  g.globalAlpha = expo((T - 28.06) / .25); font(400, 84, COND); g.letterSpacing = '8px'; g.fillText('IN MY BIO', -40, 140); g.letterSpacing = '0px';
  const b = Math.sin((T - 27.5) * 7) * 12; g.strokeStyle = WHITE; g.lineWidth = 14; g.lineCap = 'round'; g.beginPath(); g.moveTo(250, 80 + b); g.lineTo(250, 150 + b); g.moveTo(218, 120 + b); g.lineTo(250, 154 + b); g.lineTo(282, 120 + b); g.stroke();
  g.globalAlpha = 1; if (T > 27.5) { tape(-470, -250, 150, 52, TAPE, -.5, 41); tape(330, 170, 150, 52, TAPE, -.5, 42); } g.textAlign = 'left'; g.restore();
  if (T > 28.58) { const q = back((T - 28.58) / .3); g.save(); g.translate(540, 1500); g.scale(q * 1.2, q * 1.2); font(400, 72, COND); const w = g.measureText('@JACKSONFARRIER').width + 80; slab(-w / 2, -58, w, 104, '#0A0A0A', -.18);
    g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('@JACKSONFARRIER', 0, 25); g.textAlign = 'left'; g.restore(); }
}
