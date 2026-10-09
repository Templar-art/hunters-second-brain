// Webhooks: a reverse API (14 Oct clip, 29.4s).
const REV_IN = 1.6, POLL_IN = 4.1, FIRE_IN = 8.4, EX_IN = 15.6, PING_IN = 23.95, END_MOS = 29.3, END_IN = END_MOS + .4;
window.EP = {
  dur: 32.7, voEnd: 29.4,
  punchIns: [[2.9, 4.1]],
  cuts: [REV_IN, POLL_IN, FIRE_IN, EX_IN, PING_IN, END_IN],
  captions: [[REV_IN, POLL_IN, 1040], [PING_IN, END_MOS, T => lerp(H + 40, PANEL_Y, expo((T - PING_IN) / .6)) - 60]],
  frame(T) {
    if (T < REV_IN) titleCard(T, 'WEBHOOKS', 1.35);
    else if (T < POLL_IN) sceneReverse(T);
    else if (T < FIRE_IN) scenePoll(T);
    else if (T < EX_IN) sceneFire(T);
    else if (T < PING_IN) sceneExample(T);
    else if (T < END_IN) scenePing(T);
    else endCard(T, END_IN, this.dur);
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('WEBHOOKS', 1.35); cue(1.62, 'whoosh', { d: .4, bright: .5, gain: .3 }); cue(2.1, 'click', { gain: .3 });
    whip.cue(POLL_IN - .15); [5.6, 6.6, 7.56].forEach(t => cue(t, 'pop', { f: 900, gain: .18 }));
    cue(FIRE_IN, 'whoosh', { d: .35, gain: .3 }); cue(9.02, 'thud', { f: 60, d: .4, gain: .45 }); cue(12.4, 'whoosh', { d: .45, bright: .6, gain: .45 }); cue(14.6, 'chime', { f: 1175, gain: .1 });
    iris.cue(EX_IN - .45); cue(16.6, 'typing', { n: 12, cps: 26 }); cue(17.94, 'click', { gain: .35 }); cue(18.2, 'chime', { f: 988, gain: .1 }); cue(21.6, 'typing', { n: 20, cps: 40 });
    cue(PING_IN - .1, 'whoosh', { d: .5, gain: .4 }); cue(24.88, 'pop', { f: 1200, gain: .25 }); cue(26.0, 'chime', { f: 1318, gain: .12 });
    mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};
function pillW(txt, x, y, p, bg = CYAN, fg = NAVY, size = 28) { if (p <= 0) return; g.save(); g.translate(x, y); g.scale(p, p); font(500, size, MONO); g.letterSpacing = '2px';
  const w = g.measureText(txt).width + 40; g.fillStyle = bg; g.beginPath(); g.roundRect(-w / 2, -size, w, size * 2, size); g.fill(); g.fillStyle = fg; g.textAlign = 'center'; g.fillText(txt, 0, size * .35); g.textAlign = 'left'; g.letterSpacing = '0px'; g.restore(); }

// "A reverse API": the API → card spins around to ← API.
function sceneReverse(T) {
  th(FULL, zoomAt(T)); captions(T);
  const p = back((T - REV_IN) / .4); if (p <= 0) return; const flip = inOut((T - 2.1) / .5);
  g.save(); g.translate(540, 1400); g.scale(p, p); g.rotate(flip * Math.PI); card(-330, -120, 660, 240, NAVY, 30, .35);
  g.rotate(flip > .5 ? Math.PI : 0); font(800, 120, COND); g.fillStyle = flip > .5 ? CYAN : WHITE; g.textAlign = 'center'; g.fillText(flip > .5 ? '← API' : 'API →', 0, 42); g.textAlign = 'left'; g.restore();
  const rt = back((T - 3.28) / .35); if (rt > 0) { g.save(); g.translate(800, 1290); g.scale(rt, rt); g.rotate(.08); g.fillStyle = CYAN; g.beginPath(); g.roundRect(-90, -40, 180, 80, 20); g.fill();
    font(800, 56, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('REST', 0, 20); g.textAlign = 'left'; g.restore(); }
}

// The old way: polling. You keep asking, the server keeps saying "nothing yet".
function scenePoll(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('Normally: you have to ask', 60, 250, T - POLL_IN - .1, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  [['You', 220], ['API', 860]].forEach(([lab, x], i) => { const q = back((T - POLL_IN - .1 - i * .1) / .4); if (q <= 0) return; g.save(); g.translate(x, 520); g.scale(q, q);
    g.fillStyle = i ? BLUE : WHITE; g.strokeStyle = BLUE; g.lineWidth = 4; g.beginPath(); g.roundRect(-110, -80, 220, 160, 26); g.fill(); g.stroke();
    font(800, 70, COND); g.fillStyle = i ? WHITE : INK; g.textAlign = 'center'; g.fillText(lab, 0, 24); g.textAlign = 'left'; g.restore(); });
  const asks = [[5.6, 'Any new data?', 'Nothing yet.'], [6.6, 'Any new data?', 'Nothing yet.'], [7.56, 'Any new data?', 'Here you go.']];
  asks.forEach(([at, q, a], i) => { const y = 760 + i * 250, pq = back((T - at) / .3), pa = back((T - at - .35) / .3);
    if (pq > 0) { g.save(); g.translate(220, y); g.scale(pq, pq); g.fillStyle = BLUE; g.beginPath(); g.roundRect(-20, -40, 420, 80, 30); g.fill(); font(600, 34, BODY); g.fillStyle = WHITE; g.fillText(q, 10, 12); g.restore(); }
    if (pa > 0) { g.save(); g.translate(860, y + 100); g.scale(pa, pa); g.fillStyle = i === 2 ? CYAN : WHITE; g.strokeStyle = '#C9CDD2'; g.lineWidth = 2; g.beginPath(); g.roundRect(-380, -40, 400, 80, 30); g.fill(); g.stroke();
      font(600, 34, BODY); g.fillStyle = INK; g.textAlign = 'right'; g.fillText(a, -10, 12); g.textAlign = 'left'; g.restore(); } });
  faceCircle(910, 1720, 110, back((T - POLL_IN - .2) / .6));
}

// Webhook: an event happens in the system and it fires data to your API automatically.
function sceneFire(T) {
  const wy = whip(T, EX_IN + 10); g.fillStyle = NAVY; g.fillRect(0, 0, W, H);
  typeOn('With a webhook', 70, 250, T - FIRE_IN - .1, { size: 30, col: CYAN, track: 6, upper: true, cps: 32 });
  const sp = back((T - 8.42) / .4); if (sp > 0) { g.save(); g.translate(540, 560); g.scale(sp, sp); card(-260, -150, 520, 300, '#0E3148', 26, .3);
    font(800, 80, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('Software system', 0, 20); g.textAlign = 'left'; g.restore(); }
  const bolt = back((T - 9.02) / .35); if (bolt > 0) { g.save(); g.translate(760, 430); g.scale(bolt, bolt); g.fillStyle = '#FFD580';
    g.beginPath(); g.moveTo(10, -60); g.lineTo(-30, 10); g.lineTo(0, 10); g.lineTo(-15, 60); g.lineTo(35, -15); g.lineTo(5, -15); g.closePath(); g.fill(); g.restore();
    if (T > 9.2) pillW('SOMETHING HAPPENED', 540, 790, back((T - 9.3) / .35), '#FFD580', NAVY, 24); }
  const yp = back((T - 13.7) / .45); if (yp > 0) { g.save(); g.translate(540, 1420); g.scale(yp, yp); card(-260, -130, 520, 260, BLUE, 26, .3);
    font(800, 80, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('Your API', 0, 26); g.textAlign = 'left'; g.restore(); }
  // the fire: packet shoots down on "fired off"
  if (T > 12.4) { const k = expo((T - 12.4) / .6), y = lerp(720, 1290, k); g.strokeStyle = CYAN; g.lineWidth = 6; g.setLineDash([14, 12]); g.lineDashOffset = -T * 60;
    g.beginPath(); g.moveTo(540, 720); g.lineTo(540, y); g.stroke(); g.setLineDash([]);
    g.save(); g.shadowColor = CYAN; g.shadowBlur = 30; g.fillStyle = CYAN; g.beginPath(); g.roundRect(480, y - 30, 120, 60, 30); g.fill(); font(500, 22, MONO); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('DATA', 540, y + 8); g.textAlign = 'left'; g.restore(); }
  rise('Automatic.', 70, 1700, T - 11.32, { size: 140, w: 800, col: WHITE, dur: .45 });
  faceCircle(900, 1700, 100, back((T - FIRE_IN - .3) / .6));
}

// Example: a mailing-list signup, then "send me a message to this URL".
function sceneExample(T) {
  g.fillStyle = LIGHT; g.fillRect(0, 0, W, H);
  typeOn('For example', 60, 230, T - EX_IN - .1, { size: 28, col: BLUE, track: 5, upper: true, cps: 36 });
  const fp = back((T - 15.9) / .45); if (fp > 0) { g.save(); g.translate(540, 560); g.scale(fp, fp); card(-440, -230, 880, 460, WHITE, 30, .12);
    font(800, 64, COND); g.fillStyle = INK; g.fillText('Join the mailing list', -380, -130);
    g.fillStyle = '#F3F3F3'; g.strokeStyle = '#C9CDD2'; g.lineWidth = 2; g.beginPath(); g.roundRect(-380, -60, 760, 90, 16); g.fill(); g.stroke();
    typeOn('jo@example.com', -350, 0, T - 16.6, { size: 34, col: INK, track: 0, cps: 26, caret: T < 17.9 });
    const press = T > 17.94 && T < 18.3 ? .06 : 0; g.save(); g.translate(0, 140); g.scale(1 - press, 1 - press);
    g.fillStyle = T > 18.1 ? '#28C941' : BLUE; g.beginPath(); g.roundRect(-380, -50, 760, 100, 50); g.fill(); font(700, 44, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText(T > 18.1 ? 'Subscribed ✓' : 'Subscribe', 0, 15); g.textAlign = 'left'; g.restore();
    g.restore(); }
  const sp = back((T - 19.9) / .45); if (sp > 0) { g.save(); g.translate(540, 1180); g.scale(sp, sp); card(-440, -200, 880, 400, NAVY, 30, .3);
    font(500, 24, MONO); g.letterSpacing = '4px'; g.fillStyle = GREY; g.fillText('WEBHOOK', -380, -120); g.letterSpacing = '0px';
    font(700, 44, COND); g.fillStyle = WHITE; g.fillText('When: someone subscribes', -380, -40);
    font(700, 44, COND); g.fillText('Send to:', -380, 50); g.fillStyle = '#0B2233'; g.beginPath(); g.roundRect(-380, 80, 760, 80, 14); g.fill();
    typeOn('yourapp.com/hooks/subscriber', -360, 135, T - 22.3, { size: 30, col: CYAN, track: 0, cps: 40, caret: true }); g.restore(); }
  faceCircle(910, 1740, 110, back((T - EX_IN - .3) / .6));
}

// "Pings a message to that URL straight away": toast lands in a panel under the head.
function scenePing(T) {
  th(FULL, zoomAt(T)); const top = lerp(H + 40, PANEL_Y, expo((T - PING_IN) / .6)); panel(top); captions(T); const oy = top - PANEL_Y;
  const tp = back((T - PING_IN - .15) / .4); if (tp > 0) { g.save(); g.translate(540, 1480 + oy); g.scale(tp, tp); card(-450, -110, 900, 220, WHITE, 26, .15);
    g.fillStyle = CYAN; g.beginPath(); g.arc(-360, 0, 50, 0, 7); g.fill(); font(800, 50, COND); g.fillStyle = NAVY; g.textAlign = 'center'; g.fillText('⚡', -360, 18); g.textAlign = 'left';
    font(700, 46, COND); g.fillStyle = INK; g.fillText('New subscriber received', -280, -14); font(500, 24, MONO); g.fillStyle = GREY; g.fillText('POST /hooks/subscriber · just now', -280, 34); g.restore(); }
  pillW('STRAIGHT AWAY', 540, 1700 + oy, back((T - 26.0) / .35));
}
