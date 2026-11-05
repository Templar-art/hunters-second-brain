// Find Your Stride x Find Your Feet run reel (Ashley Cooper Construction). Times = cut-timeline seconds (words.json).
// Scenes: 42.2 title behind heads → MATES kinetic type → race-bib takeover → heartbeat + charity pill → WHY on B-roll
//         → Tommy lower third + bubbles → practical-tools checklist panel → ALL IN behind heads → training/fundraising bars
//         → coin + schools/workplaces → CTA panel + confetti.
const CAPY = 1480;                                   /* captions sit low, clear of faces and the graphics band */
const BIB_IN = 6.75, BIB_OUT = 10.3, TOOLS_IN = 24.1, TOOLS_OUT = 30.45, CTA_IN = 44.55;

/* ---------- custom parts ---------- */
function namePill(T, a, b, name, cx, cy) {
  const p = back((T - a) / .45), q = expoIn((T - b) / .25); if (p <= 0 || q >= 1) return;
  g.save(); g.translate(cx, cy); g.scale(p * (1 - q), p * (1 - q)); g.rotate(-.04);
  font(800, 54, COND); g.letterSpacing = '2px'; const tw = g.measureText(name).width + 64;
  g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 24; g.shadowOffsetY = 8;
  g.fillStyle = WHITE; g.beginPath(); g.roundRect(-tw / 2, -42, tw, 84, 42); g.fill(); g.shadowColor = 'transparent';
  g.fillStyle = BLUE; g.beginPath(); g.arc(-tw / 2 + 30, 0, 9, 0, 7); g.fill();
  g.fillStyle = INK; g.textAlign = 'center'; g.fillText(name, 12, 19); g.textAlign = 'left'; g.letterSpacing = '0px'; g.restore();
}
function speedLines(T, a, b, y0, seed = 4) {          /* running streaks that whip across, our motif instead of shards */
  if (T < a || T > b) return; const r = rng(seed), t = T - a;
  for (let i = 0; i < 9; i++) { const y = y0 + (r() - .5) * 300, len = 200 + r() * 420, sp = 2600 + r() * 1800, d = r() * .5;
    const x = -len + (t - d) * sp; if (x > W || t < d) continue;
    const gr = g.createLinearGradient(x, 0, x + len, 0); gr.addColorStop(0, 'rgba(255,107,44,0)'); gr.addColorStop(1, i % 3 ? CYAN : BLUE);
    g.fillStyle = gr; g.fillRect(x, y, len, 6 + r() * 8); }
}
function heartbeat(T, a, y, dur = .9) {                 /* ECG line draws across the chest band, then fades */
  const p = clamp((T - a) / dur), q = clamp((T - a - dur - .2) / .3); if (p <= 0 || q >= 1) return;
  const pts = []; for (let x = 0; x <= W; x += 6) { const k = (x - 540) / 60; let dy = 0;
    if (Math.abs(k) < 3.2) dy = k > -1 && k < 0 ? -150 * (1 + k) : k >= 0 && k < 1 ? 150 * (1 - k) - 60 * Math.max(0, k - .5) * 2 : Math.sin(k * 3) * 14;
    pts.push([x, y + dy]); }
  const n = Math.floor(pts.length * p);
  g.save(); g.globalAlpha = 1 - q; g.lineWidth = 9; g.lineJoin = g.lineCap = 'round'; g.strokeStyle = BLUE; g.shadowColor = BLUE; g.shadowBlur = 24;
  g.beginPath(); pts.slice(0, n).forEach(([x, yy], i) => i ? g.lineTo(x, yy) : g.moveTo(x, yy)); g.stroke();
  if (n > 0 && p < 1) { const [hx, hy] = pts[n - 1]; g.fillStyle = WHITE; g.beginPath(); g.arc(hx, hy, 12, 0, 7); g.fill(); }
  g.restore();
}
function tagPill(T, a, b, txt, cx, cy, { size = 64, label = '', fill = BLUE, col = WHITE, rot = -.05 } = {}) {
  const p = back((T - a) / .45), q = expoIn((T - b) / .25); if (p <= 0 || q >= 1) return;
  g.save(); g.translate(cx, cy); g.scale(p * (1 - q), p * (1 - q)); g.rotate(rot);
  font(800, size, COND); g.letterSpacing = '1px'; const tw = g.measureText(txt).width + 70, h = size * 1.45;
  g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 30; g.shadowOffsetY = 10; g.fillStyle = fill;
  g.beginPath(); g.roundRect(-tw / 2, -h / 2, tw, h, 16); g.fill(); g.shadowColor = 'transparent';
  g.fillStyle = col; g.textAlign = 'center'; g.fillText(txt, 0, size * .36);
  if (label) { font(700, 38, BODY); g.letterSpacing = '5px'; g.fillStyle = WHITE; g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 12; g.fillText(label, 0, -h / 2 - 22); g.shadowColor = 'transparent'; }
  g.textAlign = 'left'; g.letterSpacing = '0px'; g.restore();
}
/* Race bib takeover: dark stage, a tilted paper bib drops in, pins, band, number, date stamp, route line. */
function sceneBib(T) {
  const t = T - BIB_IN, wy = whip(T, BIB_OUT - .2, .2);
  if (wy < 0) th(FULL);
  g.save(); g.translate(0, wy);
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  speedLines(T, BIB_IN, BIB_IN + 1.2, 330, 11); speedLines(T, BIB_IN + .1, BIB_IN + 1.3, 1640, 12);
  const p = back(t / .6), bx = 540, by = 920 - (1 - clamp(p)) * 900, bw = 820, bh = 900;
  g.save(); g.translate(bx, by); g.rotate(-.06 + Math.sin(t * 1.3) * .012); g.scale(lerp(.8, 1, clamp(p)), lerp(.8, 1, clamp(p)));
  g.shadowColor = 'rgba(0,0,0,.5)'; g.shadowBlur = 60; g.shadowOffsetY = 24; g.fillStyle = LIGHT;
  g.beginPath(); g.roundRect(-bw / 2, -bh / 2, bw, bh, 22); g.fill(); g.shadowColor = 'transparent';
  [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([sx, sy]) => { g.fillStyle = '#C9C2B8'; g.beginPath(); g.arc(sx * (bw / 2 - 44), sy * (bh / 2 - 44), 14, 0, 7); g.fill();
    g.strokeStyle = '#8A847C'; g.lineWidth = 4; g.beginPath(); g.arc(sx * (bw / 2 - 44), sy * (bh / 2 - 44), 14, 0, 7); g.stroke(); });
  const band = expo((T - 7.0) / .45);                                   /* "Queenstown Marathon" spoken 7.0 */
  g.save(); g.beginPath(); g.rect(-bw / 2, -bh / 2 + 90, bw * band, 150); g.clip(); g.fillStyle = BLUE; g.fillRect(-bw / 2, -bh / 2 + 90, bw, 150);
  font(800, 84, COND); g.letterSpacing = '3px'; g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('QUEENSTOWN', 0, -bh / 2 + 160);
  font(600, 34, BODY); g.letterSpacing = '12px'; g.fillText('MARATHON', 0, -bh / 2 + 212); g.restore();
  /* bib number rolls up to 42.2 */
  const roll = clamp((t - .35) / 1.1), v = (42.2 * (1 - Math.pow(1 - roll, 3))).toFixed(1);
  g.textAlign = 'center'; g.letterSpacing = '0px'; font(800, 300, COND); g.fillStyle = INK; if (roll > 0) g.fillText(v, 0, 150);
  font(600, 36, BODY); g.letterSpacing = '10px'; g.fillStyle = GREY; if (roll > 0) g.fillText('KILOMETRES', 0, 215);
  /* route line along the bottom: mountains */
  const rp = clamp((t - .5) / 1.6), R = [[-330, 340], [-230, 280], [-170, 320], [-60, 240], [30, 310], [120, 260], [210, 330], [330, 290]];
  g.strokeStyle = INK; g.lineWidth = 7; g.lineJoin = g.lineCap = 'round'; g.setLineDash([2, 16]);
  g.beginPath(); R.forEach(([x, y], i) => { if (i / (R.length - 1) <= rp + 1e-6) i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.stroke(); g.setLineDash([]);
  if (rp >= 1) { g.fillStyle = BLUE; g.beginPath(); g.arc(330, 290, 16, 0, 7); g.fill(); }
  g.restore(); g.textAlign = 'left'; g.letterSpacing = '0px';
  /* date stamp slams on at "14th" (8.31) */
  const s = T - 8.31; if (s > 0) { const k = 1 + 1.6 * (1 - expo(s / .28)); g.save(); g.translate(800, 1440); g.rotate(.16); g.scale(k, k); g.globalAlpha = clamp(s * 6);
    g.strokeStyle = BLUE; g.lineWidth = 8; g.beginPath(); g.roundRect(-190, -95, 380, 190, 18); g.stroke();
    font(800, 104, COND); g.fillStyle = BLUE; g.textAlign = 'center'; g.fillText('14 NOV', 0, 22); font(600, 28, BODY); g.letterSpacing = '8px'; g.fillText('RACE DAY', 0, 70); g.restore(); g.textAlign = 'left'; g.letterSpacing = '0px'; }
  typeOn('RAISING FUNDS + AWARENESS', 80, 1700, T - 9.6, { size: 46, col: CYAN, track: 6, w: 500, fam: BODY, cps: 40 });
  g.restore();
}
/* Light panel checklist (practical tools). Rows tick on their spoken words. */
const TOOLS = [['Look after your mental health', 25.3], ['Manage tough days', 27.3], ['Notice when a mate is struggling', 28.35]];
const toolsTop = T => lerp(H + 40, 1060, expo((T - TOOLS_IN) / .6)) + (H - 1020) * expoIn((T - TOOLS_OUT + .35) / .35);
function sceneTools(T) {
  th(FULL); const top = toolsTop(T); panel(top);
  typeOn('PRACTICAL TOOLS', 80, top + 100, T - TOOLS_IN - .3, { size: 44, col: BLUE, track: 8, w: 600, fam: BODY, cps: 30 });
  TOOLS.forEach(([txt, at], i) => { const y = top + 210 + i * 120, p = expo((T - at) / .45); if (p <= 0) return;
    const bxx = 80 + (1 - p) * -200; g.save(); g.globalAlpha = clamp(p * 2);
    g.fillStyle = BLUE; g.beginPath(); g.roundRect(bxx, y - 52, 64, 64, 14); g.fill();
    const k = clamp((T - at - .15) / .25); g.strokeStyle = WHITE; g.lineWidth = 9; g.lineCap = 'round'; g.beginPath();
    g.moveTo(bxx + 16, y - 20); if (k > 0) g.lineTo(bxx + 16 + 12 * Math.min(1, k * 2), y - 20 + 12 * Math.min(1, k * 2)); if (k > .5) g.lineTo(bxx + 28 + 22 * (k - .5) * 2, y - 8 - 30 * (k - .5) * 2); g.stroke();
    g.restore(); font(800, 58, COND); const fit = Math.min(58, 58 * 820 / g.measureText(txt.toUpperCase()).width);
    rise(txt.toUpperCase(), 170, y, T - at, { size: fit, col: INK, dur: .45 }); });
}
/* Training vs fundraising bars on a dark glass card (no numbers: nothing invented). */
function bars(T, a, b) {
  const p = expo((T - a) / .5), q = expoIn((T - b) / .3); if (p <= 0 || q >= 1) return;
  const x = 70, y = 1080 + (1 - p) * 120 + q * 300, w = 940, h = 310;
  g.save(); g.globalAlpha = clamp(p * 2) * (1 - q); g.fillStyle = 'rgba(20,22,28,.82)'; g.beginPath(); g.roundRect(x, y, w, h, 26); g.fill();
  [['TRAINING THE BODY', 35.6, 37.1], ['RAISING THE MONEY', 38.15, 40.4]].forEach(([lab, s, e], i) => { const yy = y + 100 + i * 125;
    typeOn(lab, x + 44, yy, T - s + .2, { size: 42, col: WHITE, track: 6, w: 600, fam: BODY, cps: 40 });
    g.fillStyle = 'rgba(255,255,255,.14)'; g.beginPath(); g.roundRect(x + 44, yy + 22, w - 88, 26, 13); g.fill();
    const f = expo((T - s) / (e - s)); if (f > 0) { const gr = g.createLinearGradient(x + 44, 0, x + w - 44, 0); gr.addColorStop(0, BLUE); gr.addColorStop(1, CYAN);
      g.fillStyle = gr; g.beginPath(); g.roundRect(x + 44, yy + 22, Math.max(26, (w - 88) * f), 26, 13); g.fill();
      /* tiny runner chevron riding the bar tip */
      const tx = x + 44 + Math.max(26, (w - 88) * f); g.fillStyle = WHITE; g.beginPath(); g.moveTo(tx - 4, yy + 14); g.lineTo(tx + 18, yy + 35); g.lineTo(tx - 4, yy + 56); g.closePath(); g.fill(); } });
  g.restore();
}
/* Coin flips in on "Every dollar", spins, schools/workplaces pills fly out. */
function coin(T, a, b) {
  const p = back((T - a) / .5), q = expoIn((T - b) / .25); if (p <= 0 || q >= 1) return;
  const st = clamp((T - a) / .7), spin = st < 1 ? Math.cos(st * Math.PI * 4) : 1, sx = Math.max(.25, Math.abs(spin)) * p * (1 - q), y = 1080 - (1 - clamp(p)) * 300;
  g.save(); g.translate(540, y); g.scale(sx, p * (1 - q));
  g.shadowColor = 'rgba(0,0,0,.4)'; g.shadowBlur = 40; g.shadowOffsetY = 14; g.fillStyle = CYAN; g.beginPath(); g.arc(0, 0, 130, 0, 7); g.fill(); g.shadowColor = 'transparent';
  g.fillStyle = BLUE; g.beginPath(); g.arc(0, 0, 104, 0, 7); g.fill(); font(800, 170, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('$', 0, 60); g.textAlign = 'left'; g.restore();
}
/* CTA panel: arrow, then three lines tick on as they're said, confetti on "Cheers". */
const CTA = [['SPONSOR US', 45.7], ['SHARE THIS VIDEO', 46.5], ["WE'LL RUN THE 42.2", 47.45]];
function sceneCTA(T) {
  th(FULL); const top = lerp(H + 40, 1000, expo((T - CTA_IN) / .6)); panel(top);
  const t = T - CTA_IN; font(800, 44, COND);
  typeOn('LINK BELOW', 80, top + 100, t - .1, { size: 46, col: BLUE, track: 8, w: 600, fam: BODY, cps: 30 });
  const ay = top + 66 + Math.sin(t * 7) * 10; if (t > .4) { g.fillStyle = BLUE; g.beginPath(); g.moveTo(980, ay + 30); g.lineTo(940, ay - 14); g.lineTo(1020, ay - 14); g.closePath(); g.fill(); g.fillRect(970, ay - 60, 20, 50); }
  CTA.forEach(([txt, at], i) => { const y = top + 230 + i * 130; rise(txt, 80, y, T - at, { size: 104, col: i === 2 ? BLUE : INK, dur: .45 });
    const u = expo((T - at - .2) / .5); if (u > 0 && i < 2) { font(800, 104, COND); g.fillStyle = BLUE; g.fillRect(80, y + 18, g.measureText(txt).width * u, 8); } });
  confetti(T, 49.75);
}
function confetti(T, a) {
  const t = T - a; if (t <= 0) return; const r = rng(5);
  for (let i = 0; i < 70; i++) { const ang = -Math.PI / 2 + (r() - .5) * 2.2, sp = 900 + r() * 1300, x = 540 + Math.cos(ang) * sp * t, y = 1000 + Math.sin(ang) * sp * t + 1600 * t * t;
    g.save(); g.translate(x, y); g.rotate(r() * 6 + t * (6 + r() * 8)); g.fillStyle = [BLUE, CYAN, WHITE, '#C2410C'][i % 4]; g.fillRect(-12, -6, 24, 12 * Math.abs(Math.cos(t * 10 + i))); g.restore(); }
}

window.EP = {
  dur: 50.22,
  voEnd: 50.22,
  faceBox: { x: 150, y: 560, w: 720, h: 330 },
  cuts: [3.04, 6.63, BIB_IN, 8.34, 9.68, BIB_OUT, 11.97, 13.9, 16.4, 18.96, 24.02, 31.29, 34.94, 37.99, 41.16, 44.42],
  captions: [[0, 3.04, CAPY], [BIB_OUT, 11.85, CAPY], [17.85, TOOLS_IN, CAPY], [TOOLS_OUT, CTA_IN, CAPY]],

  frame(T) {
    if (T < 3.04) {                                                  /* 42.2 rolls up behind both heads */
      th(FULL); const roll = clamp((T - .1) / 1.4), v = (42.2 * (1 - Math.pow(1 - roll, 3))).toFixed(1);
      rise(v, 540, 760, T - .1, { size: 420, w: 800, col: WHITE, dur: .5, align: 'center', exitAt: 2.75, T });
      typeOn('KM  ·  QUEENSTOWN', 540 - 210, 300, T - .5, { size: 44, col: WHITE, track: 5, w: 600, fam: BODY, cps: 40 });
      cutout(); speedLines(T, .05, 1.2, 420, 2);
      namePill(T, .2, 2.85, 'EVERETT', 280, 1080); namePill(T, 1.12, 2.85, 'ALEX', 790, 1080);
      captions(T);
    } else if (T < BIB_IN) {                                         /* bridge B-roll: MATES kinetic type */
      th(FULL); g.fillStyle = 'rgba(0,0,0,.25)'; g.fillRect(0, 0, W, H);
      rise('A BUNCH OF', 540, 760, T - 3.5, { size: 96, align: 'center', exitAt: 6.45, T });
      letterDrop('MATES', 540 - 300, 1060, T - 3.95, { size: 300, exitAt: 6.45, T });
      rise('WHO RUN TOGETHER', 540, 1200, T - 4.35, { size: 96, col: CYAN, align: 'center', exitAt: 6.45, T });
      speedLines(T, 4.4, 5.6, 1350, 7);
    } else if (T < BIB_OUT) sceneBib(T);
    else if (T < 13.9) { th(FULL); heartbeat(T, 10.95, 1020, .8); tagPill(T, 11.9, 13.75, 'FIND YOUR FEET', 540, 1330, { size: 84, label: 'THE CHARITY' }); captions(T); }
    else if (T < 16.4) {                                             /* silent trees B-roll: WHY */
      th(FULL); letterPop('WHY', 540 - 230, 1000, T - 14.1, { size: 360 });
      rise('IT MATTERS', 540, 1150, T - 14.75, { size: 110, col: CYAN, align: 'center', exitAt: 16.1, T });
    }
    else if (T < TOOLS_IN) {                                         /* ocean → Tommy */
      th(FULL);
      tagPill(T, 17.95, 21.4, 'TOMMY HERSCHEL', 540, 1190, { size: 76, label: 'RUNS THE WORKSHOPS', fill: WHITE, col: INK, rot: .03 });
      captions(T);
    }
    else if (T < TOOLS_OUT) sceneTools(T);
    else if (T < 34.94) { th(FULL); if (T > 32.95) { rise('ALL IN', 540, 800, T - 32.95, { size: 400, col: CYAN, align: 'center', dur: .45 }); cutout(); } captions(T); }
    else if (T < 41.16) { th(FULL); bars(T, 35.15, 41.0); captions(T); }
    else if (T < CTA_IN) { th(FULL); coin(T, 41.3, 44.3); tagPill(T, 42.75, 44.3, 'SCHOOLS', 300, 1290, { size: 60 }); tagPill(T, 43.45, 44.3, 'WORKPLACES', 760, 1290, { size: 60, rot: .05 }); captions(T); }
    else sceneCTA(T);
  },
};
