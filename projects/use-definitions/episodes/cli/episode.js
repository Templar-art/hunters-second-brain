// CLI: command line interface (03 Oct clip, 29.4s).
const CRT_IN = 4.0, TOOLS_IN = 10.9, YOU_IN = 16.8, TERM_IN = 22.0, END_MOS = 29.3, END_IN = END_MOS + .4;
window.EP = {
  dur: 32.9, voEnd: 29.5,
  punchIns: [[2.9, 4.0], [19.5, 22.0]],
  cuts: [2.25, CRT_IN, TOOLS_IN, YOU_IN, TERM_IN, END_IN],
  captions: [[2.2, CRT_IN, 1200], [TOOLS_IN, YOU_IN, 1170], [YOU_IN, TERM_IN, 1240], [TERM_IN, END_MOS, 1040]],
  frame(T) {
    if (T < 2.25) titleCard(T, 'CLI', 1.95);
    else if (T < CRT_IN) { th(FULL, zoomAt(T)); captions(T); lowerThird(T, 2.3, 3.8); iris(T, CRT_IN - .5, 540, 760, sceneCRT); }
    else if (T < TOOLS_IN) sceneCRT(T);
    else if (T < YOU_IN) sceneTools(T);
    else if (T < TERM_IN) { th(FULL, zoomAt(T)); if (T >= 18.42) { letterPop('YOU.', 40, 560, T - 18.42, { size: 330, stagger: .07 }); cutout(zoomAt(T)); } captions(T); }
    else if (T < END_IN) sceneTerminal(T);
    else endCard(T, END_IN, this.dur);
    mosaic(T, END_MOS, 9);
  },
  cues() {
    titleCard.cue('CLI', 1.95); lowerThird.cue(2.3); iris.cue(CRT_IN - .5);
    cue(4.5, 'pop', { f: 700, gain: .2 }); cue(5.0, 'click', { gain: .3 }); cue(5.68, 'pop', { f: 900, gain: .2 });
    cue(7.4, 'thud', { f: 50, d: .4, gain: .45 }); cue(7.4, 'ticks', { n: 10, gap: .03, gain: .35 });
    cue(8.0, 'typing', { n: 60, cps: 45, gain: .22 }); cue(9.6, 'pop', { f: 1100, gain: .15 }); cue(10.1, 'typing', { n: 7, cps: 14 });
    cue(TOOLS_IN - .1, 'whoosh', { d: .4, gain: .4 }); cardStack.cue(TOOLS);
    letterPop.cue(18.42, 4); burst.cue(18.8);
    cue(TERM_IN - .1, 'whoosh', { d: .5, gain: .45 });
    CMDS.forEach(([c, , at]) => { cue(at, 'typing', { n: c.length, cps: 30 }); cue(at + c.length / 30 + .2, 'click', { f: 1600, gain: .3 }); });
    cue(28.4, 'chime', { f: 1175, gain: .1 }); mosaic.cue(END_MOS); endCard.cue(END_IN);
  },
};

// Full-screen terminal world: a pretty GUI window first, which glitches down into raw text + a prompt line.
function sceneCRT(T) {
  g.fillStyle = '#020B12'; g.fillRect(0, 0, W, H);
  const pretty = T < 7.4;
  if (pretty) {                                        // "nice pretty interfaces"
    const p = back((T - 4.15) / .5), x = 90, y = 360, w = 900, h = 900;
    g.save(); g.translate(540, y + h / 2); g.scale(p, p); g.translate(-540, -(y + h / 2));
    card(x, y, w, h, LIGHT, 30, .4);
    g.fillStyle = WHITE; g.beginPath(); g.roundRect(x, y, w, 90, [30, 30, 0, 0]); g.fill();
    ['#FF6159', '#FFBD2E', '#28C941'].forEach((c, i) => { g.fillStyle = c; g.beginPath(); g.arc(x + 50 + i * 36, y + 45, 11, 0, 7); g.fill(); });
    rise('Nice, pretty', x + 60, y + 260, T - 4.3, { size: 110, w: 800, col: INK, dur: .45 });
    rise('interfaces.', x + 60, y + 380, T - 5.68, { size: 110, w: 800, col: BLUE, dur: .45 });
    [0, 1, 2].forEach(i => { const pp = back((T - 5.0 - i * .12) / .4); if (pp <= 0) return; const bx = x + 60 + i * 270;
      g.save(); g.translate(bx + 120, y + 560); g.scale(pp, pp); card(-120, -80, 240, 160, WHITE, 22, .1);
      g.fillStyle = i === 1 ? CYAN : '#D9DDE1'; g.beginPath(); g.roundRect(-80, -40, 160, 26, 13); g.fill();
      g.fillStyle = '#E5E7EA'; g.beginPath(); g.roundRect(-80, 6, 110, 18, 9); g.fill(); g.restore(); });
    const bp = back((T - 6.2) / .4); if (bp > 0) { g.save(); g.translate(540, y + 770); g.scale(bp, bp);
      g.fillStyle = BLUE; g.beginPath(); g.roundRect(-200, -50, 400, 100, 50); g.fill();
      font(700, 50, COND); g.fillStyle = WHITE; g.textAlign = 'center'; g.fillText('Get started', 0, 17); g.textAlign = 'left'; g.restore(); }
    g.restore();
    return;
  }
  // "just a bunch of text on the screen" (glitch in, scanlines, typed lines)
  glitch(T, 1 - clamp((T - 7.4) / .35), () => {
    g.fillStyle = '#020B12'; g.fillRect(0, 0, W, H);
    // scanlines + vignette
    g.fillStyle = 'rgba(0,0,0,.25)'; for (let y = 0; y < H; y += 6) g.fillRect(0, y, W, 2);
    const v = g.createRadialGradient(540, 960, 400, 540, 960, 1200); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.6)');
    g.fillStyle = v; g.fillRect(0, 0, W, H);
    const lines = ['USE-OS v1.0  (c) 1986', 'MEM 640K OK', 'LOADING DRIVERS....... DONE', 'READY.', '', 'A:\\> dir', ' SCRIPTS   <DIR>', ' FILES     <DIR>', ' README    TXT   1,024'];
    let chars = 22 + Math.floor((T - 7.4) * 45);
    lines.forEach((l, i) => { const n = clamp(chars, 0, l.length); chars -= l.length + 2; if (n <= 0) return;
      font(500, 40, MONO); g.fillStyle = CYAN; g.globalAlpha = .9; g.fillText(l.slice(0, n), 80, 340 + i * 62); g.globalAlpha = 1; });
    // prompt line at the bottom
    if (T > 9.6) { const p = expo((T - 9.6) / .4); g.fillStyle = CYAN; g.fillRect(60, 1290, 960 * p, 3);
      typeOn('> ls -la', 80, 1370, T - 10.1, { size: 48, col: WHITE, track: 0, cps: 14, caret: true });
      typeOn('a little line at the bottom', 80, 1460, T - 9.7, { size: 26, col: GREY, track: 5, upper: true, cps: 50 }); }
  });
  faceCircle(880, 1680, 130, back((T - 8.0) / .6));
}

// "Still around in IDEs": talking head top, a stack of tools that ship a terminal.
const TOOLS = [['Claude Code', 'terminal built in', 14.08, true], ['Cursor', 'terminal built in', 14.78], ['VS Code', 'terminal built in', 15.08]];
function sceneTools(T) {
  th(FULL, BZ);
  const p = expo((T - TOOLS_IN) / .5);
  g.save(); g.globalAlpha = p; card(40, 1250 + (1 - p) * 80, 1000, 200, NAVY, 22, .35);
  typeOn('Still around in most IDEs', 80, 1318, T - 11.1, { size: 26, col: CYAN, track: 5, upper: true, cps: 40 });
  rise('Still around.', 80, 1420, T - 11.24, { size: 90, w: 800, col: WHITE, dur: .45, exitAt: 16.1, T });
  rise('Built right in.', 80, 1420, T - 16.28, { size: 90, w: 800, col: CYAN, dur: .45 });
  g.restore();
  cardStack(T, TOOLS, 60, 1480, 960, 120, 14);
  captions(T);
}

// Big live terminal over the head: each command types as he names it, then prints a result.
const CMDS = [['sed -i "s/old/new/" app.js', 'modified 1 file', 22.76], ['./run-local.sh', 'script finished in 0.4s', 25.28], ['npm run dev', 'ready on localhost:3000', 27.2]];
function sceneTerminal(T) {
  th(FULL, zoomAt(T));
  const p = expo((T - TERM_IN) / .5), x = 40, w = 1000, h = 620, y = 1080 + (1 - p) * 900;
  card(x, y, w, h, '#020B12', 24, .45);
  g.fillStyle = '#16222C'; g.beginPath(); g.roundRect(x, y, w, 70, [24, 24, 0, 0]); g.fill();
  ['#FF6159', '#FFBD2E', '#28C941'].forEach((c, i) => { g.fillStyle = c; g.beginPath(); g.arc(x + 40 + i * 30, y + 35, 9, 0, 7); g.fill(); });
  typeOn('zsh — ~/project', x + 400, y + 45, T - TERM_IN, { size: 22, col: GREY, track: 2, cps: 40 });
  CMDS.forEach(([c, out, at], i) => { const ly = y + 160 + i * 160, t = T - at; if (t <= 0) return;
    typeOn('$', x + 40, ly, t, { size: 38, col: CYAN, track: 0, cps: 99 });
    const done = c.length / 30;
    typeOn(c, x + 80, ly, t, { size: 38, col: WHITE, track: 0, cps: 30, caret: t < done + .2 });
    if (t > done + .2) { const pp = expo((t - done - .2) / .3); g.globalAlpha = pp; font(500, 30, MONO); g.fillStyle = CYAN; g.fillText('✓ ' + out, x + 80, ly + 56); g.globalAlpha = 1; } });
  captions(T);
}
