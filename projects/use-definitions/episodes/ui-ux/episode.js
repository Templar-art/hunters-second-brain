// UI / UX: user interface / user experience (06 Oct clip, 32.2s).
const ORBIT_IN = 2.9, PHONE_IN = 6.7, FEEL_IN = 12.25, FLOW_IN = 18.7, DRAG_IN = 27.3, END_MOS = 31.7, END_IN = END_MOS + .4;
window.EP = {
  dur: 35.2, voEnd: 31.8,
  punchIns: [[4.9, 6.7]],
  captions: [[ORBIT_IN, PHONE_IN, 1240], [FLOW_IN, DRAG_IN, 1760], [DRAG_IN, END_MOS, 1010]],
  cuts: [ORBIT_IN, PHONE_IN, FLOW_IN, DRAG_IN, END_IN],
  frame(T) {
    if (T < ORBIT_IN) titleCard(T, 'UI/UX', 2.6);
    else if (T < PHONE_IN) sceneOrbit(T);
    else if (T < FLOW_IN) scenePhone(T);
    else if (T < DRAG_IN) sceneFlow(T);
    else if (T < END_IN) sceneDrag(T);
    else endCard(T, END_IN, this.dur);
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('UI/UX', 2.6); lowerThird.cue(3.0);
    CHIPS.forEach((c, i) => cue(4.22 + i * .12, 'pop', { f: 700 + i * 80, d: .05, gain: .14 }));
    iris.cue(PHONE_IN - .5); cue(7.0, 'whoosh', { d: .4, gain: .3 }); cue(8.08, 'riser', { d: .4, gain: .12 }); cue(8.3, 'chime', { f: 988, gain: .12 });
    [9.6, 10.0, 10.46].forEach((t, i) => cue(t, 'pop', { f: 900 + i * 150, gain: .18 }));
    cue(FEEL_IN, 'whoosh', { d: .4, gain: .25 }); cue(15.16, 'click', { gain: .4 }); cue(16.12, 'pop', { f: 1200, gain: .2 }); cue(16.72, 'click', { f: 1800, gain: .4 }); cue(17.94, 'pop', { f: 900, gain: .25 }); burst.cue(17.94);
    cue(FLOW_IN - .1, 'whoosh', { d: .5, gain: .4 }); SCREENS.forEach(([, at]) => { cue(at - .15, 'whoosh', { d: .25, bright: .5, gain: .2 }); cue(at, 'click', { gain: .3 }); });
    cue(DRAG_IN, 'whoosh', { d: .3, gain: .3 }); behindHead.cue(27.48, null);
    DIALOGS.forEach(([, at]) => cue(at, 'thud', { f: 110, d: .15, gain: .22 }));
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};

// ---- phone mockup helper: rounded device, notch, screen callback (clipped) ----
function phone(cx, cy, w, h, screen, tilt = 0) {
  g.save(); g.translate(cx, cy); g.rotate(tilt);
  g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 60; g.shadowOffsetY = 26; g.fillStyle = '#0B0F14';
  g.beginPath(); g.roundRect(-w / 2, -h / 2, w, h, w * .14); g.fill(); g.shadowColor = 'transparent';
  const b = w * .035, sx = -w / 2 + b, sy = -h / 2 + b, sw = w - b * 2, sh = h - b * 2;
  g.save(); g.beginPath(); g.roundRect(sx, sy, sw, sh, w * .11); g.clip(); screen(sx, sy, sw, sh); g.restore();
  g.fillStyle = '#0B0F14'; g.beginPath(); g.roundRect(-w * .16, sy + 14, w * .32, 34, 17); g.fill();
  g.restore();
}
function fingertip(x, y, press) {          // press 0..1 → shrinks + ripple
  g.save(); g.globalAlpha = .9; g.fillStyle = 'rgba(255,255,255,.85)'; g.strokeStyle = 'rgba(0,28,46,.3)'; g.lineWidth = 3;
  const r = 34 * (1 - press * .25); g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); g.stroke();
  if (press > 0) { g.strokeStyle = `rgba(18,221,235,${1 - press})`; g.lineWidth = 6; g.beginPath(); g.arc(x, y, 34 + press * 70, 0, 7); g.stroke(); }
  g.restore();
}

// Disciplines orbit the head.
const CHIPS = ['Visual design', 'Layout', 'Typography', 'Motion', 'Accessibility', 'Research', 'Interaction'];
function sceneOrbit(T) {
  th(FULL, zoomAt(T)); lowerThird(T, 3.0, 4.2);
  CHIPS.forEach((c, i) => { const p = back((T - 3.85 - i * .1) / .4); if (p <= 0) return;
    const f = faceScreen(zoomAt(T)), fc = f.x + f.w / 2, a = i / CHIPS.length * 6.283 + (T - 4) * .5;
    // orbit ring sized to clear the tracked face: chips pass beside / below it, never across it
    const x = fc + Math.cos(a) * (f.w / 2 + 230), y = f.y + f.h * .55 + Math.sin(a) * (f.h / 2 + 120), front = Math.sin(a) > 0;
    font(700, 42, COND); const w = g.measureText(c).width + 48;
    g.save(); g.translate(x, y); g.scale(p, p);
    g.fillStyle = i % 2 ? WHITE : CYAN; g.shadowColor = 'rgba(0,0,0,.25)'; g.shadowBlur = 20; g.beginPath(); g.roundRect(-w / 2, -32, w, 64, 32); g.fill();
    g.shadowColor = 'transparent'; g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText(c, 0, 14); g.textAlign = 'left'; g.restore(); });
  captions(T); iris(T, PHONE_IN - .5, 540, 900, scenePhone);
}

// Phone: wireframe → styled (UI) → steps → feels good (UX taps / toggle / like).
function phoneScreen(T) {
  return (x, y, w, h) => {
    const styled = expo((T - 8.08) / .6);
    g.fillStyle = lerpCol('#E9EBEE', '#F7FAFC', styled); g.fillRect(x, y, w, h);
    // hero card
    g.fillStyle = lerpCol('#D3D7DC', BLUE, styled); g.beginPath(); g.roundRect(x + 30, y + 110, w - 60, 260, 26); g.fill();
    if (styled > .3) { g.globalAlpha = styled; font(800, 64, COND); g.fillStyle = WHITE; g.fillText('Welcome', x + 60, y + 230); font(500, 26, BODY); g.fillText('Everything in one place.', x + 60, y + 280); g.globalAlpha = 1; }
    // list rows
    for (let i = 0; i < 3; i++) { const ry = y + 410 + i * 120; g.fillStyle = WHITE; g.beginPath(); g.roundRect(x + 30, ry, w - 60, 96, 20); g.fill();
      g.fillStyle = lerpCol('#D3D7DC', [CYAN, '#7FD6FF', '#C3A6FF'][i], styled); g.beginPath(); g.arc(x + 85, ry + 48, 26, 0, 7); g.fill();
      g.fillStyle = '#D9DDE1'; g.beginPath(); g.roundRect(x + 130, ry + 30, w * .45, 16, 8); g.fill(); g.beginPath(); g.roundRect(x + 130, ry + 58, w * .3, 12, 6); g.fill();
      // numbered steps on "clear to follow"
      const sp = back((T - [9.6, 10.0, 10.46][i]) / .35); if (sp > 0) { g.save(); g.translate(x + w - 80, ry + 48); g.scale(sp, sp); g.fillStyle = NAVY; g.beginPath(); g.arc(0, 0, 24, 0, 7); g.fill();
        font(800, 30, COND); g.fillStyle = CYAN; g.textAlign = 'center'; g.fillText(String(i + 1), 0, 11); g.textAlign = 'left'; g.restore(); } }
    // toggle (responsive)
    const on = expo((T - 16.72) / .25), ty = y + h - 330;
    g.fillStyle = lerpCol('#C9CDD2', CYAN, on); g.beginPath(); g.roundRect(x + w - 170, ty, 120, 64, 32); g.fill();
    g.fillStyle = WHITE; g.beginPath(); g.arc(x + w - 138 + on * 56, ty + 32, 26, 0, 7); g.fill();
    font(600, 30, BODY); g.fillStyle = INK; g.fillText('Notifications', x + 40, ty + 42);
    // primary button (quick tap)
    const press = T > 15.16 && T < 15.6 ? Math.sin((T - 15.16) / .44 * Math.PI) : 0, by = y + h - 210;
    g.save(); g.translate(x + w / 2, by + 50); g.scale(1 - press * .06, 1 - press * .06);
    g.fillStyle = lerpCol('#B9BEC4', NAVY, styled); g.beginPath(); g.roundRect(-(w - 60) / 2, -50, w - 60, 100, 50); g.fill();
    font(700, 40, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(T > 15.4 ? 'Done ✓' : 'Continue', 0, 14); g.textAlign = 'left'; g.restore();
    // heart (feel good)
    const hp = back((T - 17.94) / .4); if (hp > 0) { g.save(); g.translate(x + w - 90, y + 160); g.scale(hp, hp); g.fillStyle = '#FF5A7A';
      g.beginPath(); g.moveTo(0, 18); g.bezierCurveTo(-40, -10, -20, -40, 0, -20); g.bezierCurveTo(20, -40, 40, -10, 0, 18); g.fill(); g.restore(); }
  };
}
function lerpCol(a, b, p) { const pa = [1, 3, 5].map(i => parseInt(a.slice(i, i + 2), 16)), pb = [1, 3, 5].map(i => parseInt(b.slice(i, i + 2), 16));
  return `rgb(${pa.map((v, i) => Math.round(lerp(v, pb[i], clamp(p)))).join(',')})`; }
function scenePhone(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  const p = expo((T - 6.2) / .6), feel = inOut((T - FEEL_IN) / .7);
  const cx = lerp(540, 580, feel), cy = lerp(1080, 1130, feel) + (1 - p) * 900, s = lerp(1, 1.04, feel);
  typeOn(T < FEEL_IN ? 'User interface' : 'User experience', 60, 250, T - (T < FEEL_IN ? 6.3 : FEEL_IN + .1), { size: 30, col: BLUE, track: 6, upper: true, cps: 30 });
  if (T < FEEL_IN) { rise('Looks good.', 54, 430, T - 7.48, { size: 150, w: 800, col: INK, dur: .45, exitAt: FEEL_IN - .1, T }); }
  else { rise('Feels good.', 54, 430, T - 17.72, { size: 150, w: 800, col: INK, dur: .45 }); rise('Quick. Responsive.', 54, 430, T - 13.0, { size: 110, w: 800, col: BLUE, dur: .4, exitAt: 17.6, T }); }
  phone(cx, cy, 560 * s, 1120 * s, phoneScreen(T), lerp(0, -.04, feel));
  // fingertip choreography during the "feel" beat
  if (T > 14.6 && T < 18.6) { const tx = T < 16.4 ? cx + 200 * s : cx + 150 * s, ty = T < 16.4 ? cy + 400 * s : cy + 270 * s;   // tap beside the label, never on it
    const pr = T > 15.16 && T < 15.6 ? (T - 15.16) / .44 : T > 16.72 && T < 17.1 ? (T - 16.72) / .38 : 0; fingertip(tx, ty, pr); }
  burst(T, 17.94, cx + 180, cy - 380, 18, 3);
  faceCircle(900, 1720, 120, back((T - 7.2) / .6));
}

// Half layout: speaker left, phone right swiping through the first-time flow.
const SCREENS = [['Sign up', 21.64], ['Sign in', 22.68], ['Add a friend', 23.88], ['Search', 25.88]];
function sceneFlow(T) {
  g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  const p = inOut((T - FLOW_IN) / .6), colW = lerp(W, 520, p);
  g.save(); g.beginPath(); g.rect(0, 0, colW, H); g.clip(); th({ x: 0, y: 0, w: colW, h: H }, lerp(BZ, 1.0, p), .3); g.restore();
  g.fillStyle = CYAN; g.fillRect(colW - 4, 0, 4, H);
  typeOn('First time in the app', 560, 260, T - 19.0, { size: 22, col: CYAN, track: 4, upper: true, cps: 40 });
  let idx = -1; SCREENS.forEach(([, at], i) => { if (T >= at) idx = i; });
  phone(800, 980, 440, 880, (x, y, w, h) => {
    g.fillStyle = '#F7FAFC'; g.fillRect(x, y, w, h);
    SCREENS.forEach(([lab, at], i) => { const sx = x + w * (i - idx) - (idx >= 0 && T - SCREENS[idx][1] < .35 ? (1 - expo((T - SCREENS[idx][1]) / .35)) * -w : 0);
      if (Math.abs(sx - x) > w * 1.2) return;
      font(800, 60, COND); g.fillStyle = INK; g.fillText(lab, sx + 30, y + 190);
      for (let k = 0; k < (i === 3 ? 1 : 2); k++) { g.fillStyle = WHITE; g.strokeStyle = '#D9DDE1'; g.lineWidth = 2; g.beginPath(); g.roundRect(sx + 30, y + 250 + k * 100, w - 60, 76, 16); g.fill(); g.stroke(); }
      if (i === 2) { for (let k = 0; k < 3; k++) { g.fillStyle = [CYAN, '#7FD6FF', '#C3A6FF'][k]; g.beginPath(); g.arc(sx + 70, y + 520 + k * 90, 28, 0, 7); g.fill();
        g.fillStyle = '#D9DDE1'; g.beginPath(); g.roundRect(sx + 120, y + 508 + k * 90, 180, 22, 11); g.fill(); } }
      g.fillStyle = BLUE; g.beginPath(); g.roundRect(sx + 30, y + h - 190, w - 60, 90, 45); g.fill();
      font(700, 38, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(lab, sx + w / 2, y + h - 132); g.textAlign = 'left'; });
    if (idx < 0) { font(700, 44, COND); g.fillStyle = GREY; g.textAlign = 'center'; g.fillText('Where do I go?', x + w / 2, y + h / 2); g.textAlign = 'left'; }
  });
  if (idx >= 0) { const t = T - SCREENS[idx][1], pr = t < .3 ? t / .3 : 0; fingertip(960, 980 + 310, pr); }
  // progress dots
  SCREENS.forEach((_, i) => { g.fillStyle = i <= idx ? CYAN : '#2B4A62'; g.beginPath(); g.arc(740 + i * 40, 1490, 10, 0, 7); g.fill(); });
  captions(T);
}

// "An absolute drag": DRAG behind the head, then bad-software dialogs pile up.
const DIALOGS = [['Please wait…', 29.15], ['Error 0x80004005', 29.78], ['Are you sure?', 30.1], ['Session expired', 30.32], ['Loading…', 30.66]];
function sceneDrag(T) {
  th(FULL, zoomAt(T));
  if (T >= 27.48 && T < 29.5) { const f = faceScreen(zoomAt(T)); font(800, 100, COND); const w100 = g.measureText('DRAG').width;
    const sz = clamp((f.x - 100) / w100 * 100, 110, 250);   // fits fully left of the face with a 60px gap
    rise('DRAG', 30, 560, T - 27.48, { size: sz, w: 800, dur: .4 }); cutout(zoomAt(T)); }
  DIALOGS.forEach(([msg, at], i) => { const p = back((T - at) / .3); if (p <= 0) return; const r = rng(i + 4);
    const x = i % 2 ? 560 : 60, y = 1090 + Math.floor(i / 2) * 210;
    g.save(); g.translate(x + 230, y + 90); g.scale(p, p); g.translate(-(x + 230), -(y + 90));
    card(x, y, 460, 180, '#ECECEC', 6, .35); g.fillStyle = '#C8C8C8'; g.fillRect(x, y, 460, 40);
    font(500, 20, MONO); g.fillStyle = '#555'; g.fillText('Legacy App', x + 16, y + 27); g.fillText('✕', x + 430, y + 27);
    font(600, 32, BODY); g.fillStyle = '#222'; g.fillText(msg, x + 30, y + 105);
    g.strokeStyle = '#999'; g.lineWidth = 2; g.strokeRect(x + 330, y + 128, 100, 36); font(500, 20, MONO); g.fillStyle = '#222'; g.fillText('OK', x + 365, y + 153);
    g.restore(); });
  if (T > 30.66) { g.save(); g.translate(790, 1720); g.rotate(T * 6); g.strokeStyle = WHITE; g.lineWidth = 12; g.lineCap = 'round';
    g.beginPath(); g.arc(0, 0, 60, 0, 4.5); g.stroke(); g.restore(); }
  captions(T);
}
