// CRUD episode. Times are VO word timestamps from words.json (see tools/transcribe.py).
// Scene order: title → lower third → mosaic → def card → whip → stands-for → REST → endpoint panel
//              → full light slide (actions) → whip → 200 OK → shatter/mosaic → end card.
const STANDS = [['C', 'reate', 6.40], ['R', 'ead', 6.60], ['U', 'pdate', 7.12], ['D', 'elete', 7.68]];
const ACT = [['POST', 'Creates', 15.38], ['GET', 'Reads', 16.62], ['PUT', 'Updates', 17.58], ['DELETE', 'Deletes', 18.38]];
const JSON_OUT = '{ "id": 102, "deleted": true }';
const ENDPOINT_IN = 10.45, ACTIONS_IN = 14.95;
const panelTop = T => lerp(H + 40, PANEL_Y, expo((T - ENDPOINT_IN) / .6));

window.EP = {
  dur: 23.6,
  voEnd: 19.8,                                        // source audio is trimmed + faded here
  dropWords: [[19.8, 99]],                            // whisper hallucinated a repeat at the tail
  punchIns: [[3.6, 5.0], [12.3, 14.95]],
  // v7: hard scene cuts (scene switches in frame() + punch-in edges) so motion blur never straddles them
  cuts: [2.3, 3.6, 5.0, 6.25, 8.12, 10.45, 12.3, 14.95, 19.33, 20.4],
  // deliberate transitions the QC continuity check should ignore (mosaics, whips, card flips, panel moves)
  qcAllow: [[0, 0.6], [2.1, 2.6], [4.5, 5.4], [5.9, 6.5], [7.9, 8.4], [10.3, 11.1], [14.7, 15.4], [15.3, 15.7], [16.5, 16.8], [17.5, 17.8], [18.3, 18.6], [18.9, 19.6], [19.9, 20.8]],
  captions: [[2.2, 5.0, 1200], [8.0, 10.45, 1240], [ENDPOINT_IN, ACTIONS_IN, T => panelTop(T) - 80], [19.0, 20.05, 1380]],

  frame(T) {
    if (T < 2.3) titleCard(T, 'CRUD', 2.0, 'Definitions', [985, 800]);   // v7: shards moved off the ear/eye line to the shoulder
    else if (T < 5.0) { th(FULL, zoomAt(T)); captions(T); lowerThird(T, 2.35, 4.7); }
    else if (T < 6.25) defCard(T, 5.0, 6.05, 'CRUD', 'see · are · you · dee', T => standsFor(T, 6.05, 8.12, 'CRUD', STANDS));
    else if (T < 8.12) standsFor(T, 6.05, 8.12, 'CRUD', STANDS);
    else if (T < ENDPOINT_IN) { th(FULL, BZ * 1.14); behindHead(T, 9.88, 10.45, 'REST', 'API'); captions(T); }
    else if (T < ACTIONS_IN) sceneEndpoint(T);
    else if (T < 19.33) sceneActions(T);
    else if (T < 20.4) sceneOK(T);
    else endCard(T, 20.4, this.dur, 'Definitions', true);           // v7: alive end card (no dead 2s hold)
    mosaic(T, 4.62, 3);
    mosaic(T, 20.0, 9);
  },

  cues() {
    titleCard.cue('CRUD'); lowerThird.cue(2.35);
    mosaic.cue(4.62); defCard.cue(5.0, 6.05, 'see · are · you · dee');
    standsFor.cue(6.05, 8.12, 'CRUD', STANDS); cue(8.0, 'thud', { f: 70, d: .25, gain: .25 });
    behindHead.cue(9.88, 'API');
    cue(10.35, 'whoosh', { d: .55, gain: .45 });                          // panel rises
    cue(10.76, 'pop', { f: 700, d: .07, gain: .18 }); cue(10.9, 'pop', { f: 780, d: .07, gain: .18 });
    cue(11.3, 'pop', { f: 520, d: .07, gain: .15 }); cue(11.5, 'typing', { n: 8, cps: 28 });
    cue(13.84, 'thud', { f: 80, d: .25, gain: .3 }); cue(14.0, 'typing', { n: 10, cps: 28 });
    terminal.cue(13.3, 'curl -X POST \\', '    api.example.com/users');
    cue(14.85, 'whoosh', { d: .6, gain: .5 });                            // panel takes over
    cue(15.15, 'pop', { f: 600, d: .08, gain: .2 }); cue(15.3, 'typing', { n: 12, cps: 30 });
    ACT.forEach(([, , at], i) => { cue(at - .05, 'whoosh', { d: .25, bright: .35, gain: .25 }); cue(at, 'pop', { f: 500 + i * 120, d: .07, gain: .25 }); });
    cue(15.5, 'pop', { f: 900, d: .05, gain: .15 }); cue(17.9, 'pop', { f: 1100, d: .05, gain: .15 });
    cue(18.45, 'whoosh', { d: .3, bright: .5, gain: .15 }); cue(18.9, 'whoosh', { d: .3, gain: .2 });
    whip.cue(19.1); okCard.cue(19.15, 19.95, JSON_OUT);
    mosaic.cue(20.0); endCard.cue(20.4);
  },
};

// Endpoint panel: You → endpoint box → Database; terminal card types the request.
function sceneEndpoint(T) {
  th(FULL, zoomAt(T));
  const top = panelTop(T);
  terminal(T, 13.3, ACTIONS_IN, 'curl -X POST \\', '    api.example.com/users');
  captions(T);
  panel(top);
  const cy = 1500 + top - PANEL_Y;
  g.save(); g.translate(540, cy); g.scale(1.1, 1.1); g.translate(-540, -cy);
  const pu = expo((T - 10.76) / .5), pd = expo((T - 10.9) / .5);
  g.strokeStyle = INK; g.lineWidth = 3;
  const L1 = expo((T - 11.2) / .5), L2 = expo((T - 11.35) / .5);
  g.beginPath(); g.moveTo(222, cy); g.lineTo(lerp(222, 370, L1), cy); g.stroke();
  g.beginPath(); g.moveTo(710, cy); g.lineTo(lerp(710, 858, L2), cy); g.stroke();
  if (L2 > .95) { g.fillStyle = CYAN; g.strokeStyle = INK; g.lineWidth = 3; g.beginPath(); g.arc(828, cy, 12, 0, 7); g.fill(); g.stroke(); }
  iconUser(160, cy, 62, pu); iconDB(920, cy, 62, pd);
  font(700, 40, COND); g.fillStyle = INK; g.textAlign = 'center';
  g.globalAlpha = pu; g.fillText('You', 160, cy + 120); g.globalAlpha = pd; g.fillText('Database', 920, cy + 120);
  g.globalAlpha = 1; g.textAlign = 'left';
  const fill = expo((T - 13.84) / .4), bw = 340, bh = 140, bx = 540 - bw / 2, by = cy - bh / 2;
  if (T > 11.3) {
    g.save(); g.translate(540, cy); const s = lerp(.85, 1, back((T - 11.3) / .5)); g.scale(s, s); g.translate(-540, -cy);
    g.setLineDash([12, 10]); g.strokeStyle = '#AEB4BA'; g.lineWidth = 3; g.beginPath(); g.roundRect(bx, by, bw, bh, 18); g.stroke(); g.setLineDash([]);
    if (fill < .02) { font(800, 80, COND); g.fillStyle = '#C2C7CC'; g.textAlign = 'center'; g.fillText('?', 540, cy + 28); g.textAlign = 'left'; }
    if (fill > 0) { g.save(); g.shadowColor = 'rgba(0,155,232,.45)'; g.shadowBlur = 30; g.shadowOffsetY = 10; g.fillStyle = BLUE;
      g.beginPath(); g.roundRect(540 - bw / 2 * fill, by, bw * fill, bh, 18); g.fill(); g.restore();
      typeOn('/api/users', 540 - 125, cy + 16, T - 14.0, { size: 46, col: WHITE, w: 500, track: 0, cps: 28 }); }
    g.restore();
  }
  typeOn('Endpoint', 540 - 80, by - 34, T - 11.5, { size: 28, col: BLUE, track: 6, upper: true, cps: 28 });
  g.restore();
}

// Full light slide: method pills, giant verb, users table that acts out each verb, face circle.
const ROWS0 = [[101, 'Sam Bruhn', 'Founder', 'active'], [102, 'Alex Kim', 'Developer', 'active']];
function sceneActions(T) {
  const top = lerp(PANEL_Y, 0, inOut((T - ACTIONS_IN) / .55)), wy = whip(T, 19.1, .22);
  if (wy < 0) sceneOK(T);
  g.save(); g.translate(0, wy);
  th(FULL, zoomAt(T - .01)); panel(top);
  if (top > 4) { g.restore(); return; }
  let a = -1; ACT.forEach(([, , at], i) => { if (T >= at - .05) a = i; });
  faceCircle(880, 250, 150, back((T - 15.15) / .6));
  let px = 60; const xs = [];
  ACT.forEach(([m], i) => { const pp = expo((T - 15.1 - i * .06) / .4); g.save(); g.globalAlpha = pp; g.translate(0, (1 - pp) * 20);
    xs.push(px); px += pill(m, px, 330) + 14; g.restore(); });
  if (a >= 0) { font(500, 28, MONO); g.letterSpacing = '2px';
    const prev = Math.max(0, a - 1), k = a === 0 ? expo((T - ACT[0][2] + .05) / .3) : expo((T - ACT[a][2] + .05) / .25);
    const wOf = i => g.measureText(ACT[i][0]).width + 36;
    const hx = lerp(xs[prev], xs[a], a === 0 ? 1 : k), hw = lerp(wOf(prev), wOf(a), a === 0 ? 1 : k);
    g.globalAlpha = a === 0 ? k : 1; g.fillStyle = CYAN; g.beginPath(); g.roundRect(hx, 330, hw, 52, 26); g.fill();
    g.fillStyle = NAVY; g.fillText(ACT[a][0], xs[a] + 18, 365); g.globalAlpha = 1; g.letterSpacing = '0px'; }
  ACT.forEach(([, word, at], i) => { const next = ACT[i + 1] ? ACT[i + 1][2] - .05 : 99;
    if (T >= at - .05 && T < next + .2) rise(word, 54, 640, T - at - (i ? .08 : -.05), { size: 250, w: 800, col: INK, dur: .45, exitAt: next, T }); });
  const pt = expo((T - 15.25) / .6), cx = 50, cyy = 790 + (1 - pt) * 80, cw = 980;
  g.save(); g.globalAlpha = pt;
  typeOn('Users', cx + 10, cyy - 26, T - 15.3, { size: 28, col: BLUE, track: 6, upper: true, cps: 24 });
  const nRows = 2 + (T >= 15.38 ? 1 : 0) - (T >= 18.9 ? expo((T - 18.9) / .4) : 0);
  typeOn(`${Math.round(2 + (T >= 15.38 ? 1 : 0) - (T >= 18.9 ? 1 : 0))} rows`, cx + 140, cyy - 26, T - 15.3, { size: 28, col: GREY, track: 4, upper: true, cps: 40 });
  const RH = 96, ch = 100 + RH * nRows + 30;
  g.shadowColor = 'rgba(0,0,0,.10)'; g.shadowBlur = 40; g.shadowOffsetY = 14; g.fillStyle = WHITE;
  g.beginPath(); g.roundRect(cx, cyy, cw, ch, 20); g.fill(); g.restore();
  g.save(); g.globalAlpha = pt;
  const C = [cx + 40, cx + 170, cx + 500, cx + 790];
  font(500, 24, MONO); g.letterSpacing = '3px'; g.fillStyle = GREY;
  ['ID', 'NAME', 'ROLE', 'STATUS'].forEach((h, i) => g.fillText(h, C[i], cyy + 62)); g.letterSpacing = '0px';
  g.fillStyle = '#E5E7EA'; g.fillRect(cx + 30, cyy + 90, cw - 60, 2);
  const rows = [...ROWS0.map(r => [...r]), [103, 'Jo Lee', 'Designer', 'new']];
  if (T >= 17.9) rows[2][3] = 'active';
  let y = cyy + 100;
  rows.forEach((r, i) => {
    if (i === 2 && T < 15.38) return;
    const isNew = i === 2, del = i === 1 && T >= 18.38;
    let hgt = RH, alpha = 1, slide = 0;
    if (isNew) { const pn = expo((T - 15.5) / .5); alpha = pn; slide = (1 - pn) * -40; }
    if (i === 1 && T >= 18.9) { const pc2 = expo((T - 18.9) / .4); hgt = RH * (1 - pc2); alpha = 1 - pc2; }
    g.save(); g.beginPath(); g.rect(cx, y, cw, hgt); g.clip(); g.globalAlpha = pt * alpha;
    const hl = (isNew && win(T, 15.5, 16.5)) ? 1 - clamp((T - 16.2) / .3) : (i === 0 && win(T, 16.62, 17.5)) ? expo((T - 16.62) / .25) * (1 - clamp((T - 17.3) / .2)) : (isNew && win(T, 17.58, 18.3)) ? expo((T - 17.58) / .25) * (1 - clamp((T - 18.1) / .2)) : 0;
    if (hl > 0) { g.globalAlpha = pt * alpha * hl; g.fillStyle = 'rgba(18,221,235,.28)'; g.fillRect(cx + 16, y + 10 + slide, cw - 32, RH - 20); g.globalAlpha = pt * alpha; }
    const by = y + 62 + slide;
    font(500, 32, MONO); g.fillStyle = INK; g.fillText(String(r[0]), C[0], by);
    font(600, 42, COND); g.fillText(r[1], C[1], by + 2); g.fillStyle = '#555A60'; g.fillText(r[2], C[2], by + 2);
    const st = r[3], newOn = st === 'new'; font(500, 24, MONO);
    const sw = g.measureText(st).width + 30; g.lineWidth = 2.5;
    const flip = isNew && T >= 17.9 ? back((T - 17.9) / .4) : 1;
    g.save(); g.translate(C[3] + sw / 2, by - 10); g.scale(1, flip); g.translate(-(C[3] + sw / 2), -(by - 10));
    g.strokeStyle = newOn ? CYAN : BLUE; g.fillStyle = newOn ? CYAN : WHITE;
    g.beginPath(); g.roundRect(C[3], by - 30, sw, 42, 21); g.fill(); g.stroke();
    g.fillStyle = newOn ? NAVY : BLUE; g.fillText(st, C[3] + 15, by - 1); g.restore();
    if (del) { const ps = expo((T - 18.45) / .4); g.fillStyle = INK; g.fillRect(C[0] - 6, by - 14, (cw - 80) * ps, 3); }
    g.fillStyle = '#EEF0F2'; g.fillRect(cx + 30, y + hgt - 1, cw - 60, 1.5);
    g.restore(); y += hgt;
  });
  g.restore();
  g.restore();
}

function sceneOK(T) {
  th(FULL, BZ);
  if (T < 20.05) captions(T);
  okCard(T, 19.15, 19.95, JSON_OUT);
}
