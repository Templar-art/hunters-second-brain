// Render an episode's picture track. Usage:
//   node render.cjs <ep_dir> video            → <ep_dir>/build/picture.mp4 (+ build/cues.json, build/render.json)
//   node render.cjs <ep_dir> stills 1.0,5.2   → <ep_dir>/build/qa/s_<t>.png
const { chromium } = require('playwright'); const { spawn } = require('child_process');
const path = require('path'), fs = require('fs');
const ROOT = __dirname, EP = path.resolve(process.argv[2]), MODE = process.argv[3] || 'video', FPS = 24000 / 1001;
(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('PAGE ERROR', e.message));
  const rel = path.relative(path.join(ROOT, 'engine'), EP);
  await p.goto('file://' + path.join(ROOT, 'engine/page.html') + '?ep=' + encodeURIComponent(rel) + (process.env.SUB ? '&sub=' + process.env.SUB : '') + (process.env.SHUTTER ? '&shutter=' + process.env.SHUTTER : ''));
  const { dur } = await p.evaluate(() => window.ready);
  const voEnd = await p.evaluate(() => EP.voEnd || 0);
  fs.mkdirSync(path.join(EP, 'build/qa'), { recursive: true });
  fs.writeFileSync(path.join(EP, 'build/cues.json'), JSON.stringify(await p.evaluate(() => window.cues())));
  fs.writeFileSync(path.join(EP, 'build/render.json'), JSON.stringify({ dur, voEnd }));
  const shot = () => p.locator('canvas').screenshot({ type: 'png' });
  if (MODE === 'textcheck') {                          // every 0.1s: text covered by later drawing, or running off-screen (≥0.3s runs)
    const runs = {};
    for (let t = 0; t < dur; t += .1) { const iss = await p.evaluate(t => window.textAudit(t), t);
      for (const i of iss) { const k = i.kind + '|' + i.txt; (runs[k] = runs[k] || []).push(+t.toFixed(1)); } }
    const out = [];
    for (const [k, ts] of Object.entries(runs)) { let a = ts[0], prev = ts[0];
      for (const t of ts.slice(1).concat([1e9])) { if (t - prev > .15) { if (prev - a >= .45) { const [kind, txt] = k.split('|'); out.push({ kind, txt, from: a, to: prev }); } a = t; } prev = t; } }
    out.sort((x, y) => x.from - y.from);
    fs.writeFileSync(path.join(EP, 'build/textcheck.json'), JSON.stringify(out, null, 1));
    console.log(out.length ? `TEXT ISSUES: ${out.length}\n` + out.map(o => `  ${o.from}–${o.to}s ${o.kind}: "${o.txt}"`).join('\n') : 'TEXT CLEAR');
  } else if (MODE === 'facecheck') {
    // Sample every 0.1s. A violation = face covered >4% for ≥0.3s. Full-slide takeovers (face AND torso hidden) are
    // filtered in the engine; sub-0.3s whips are transitions.
    const samples = []; for (let t = 0; t < dur; t += .1) samples.push([+t.toFixed(1), await p.evaluate(t => window.faceAudit(t), t)]);
    const runs = []; let cur = null;
    for (const [t, c] of samples) { const bad = c > .04;
      if (bad) { if (!cur) cur = { a: t, b: t, max: 0 }; cur.b = t; cur.max = Math.max(cur.max, c); } else if (cur) { runs.push(cur); cur = null; } }
    if (cur) runs.push(cur);
    const v = runs.filter(r => r.b - r.a >= .3).map(r => ({ from: r.a, to: r.b, maxPct: Math.round(r.max * 100) }));
    fs.writeFileSync(path.join(EP, 'build/facecheck.json'), JSON.stringify(v));
    console.log(v.length ? 'FACE COVERED: ' + v.map(r => `${r.from}–${r.to}s (max ${r.maxPct}%)`).join(' · ') : 'FACE CLEAR');
  } else if (MODE === 'stills') {
    for (const t of process.argv[4].split(',')) { await p.evaluate(t => window.seek(+t), t);
      fs.writeFileSync(path.join(EP, `build/qa/s_${t}.png`), await shot()); }
  } else {
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', '24000/1001', '-i', '-',
      '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', path.join(EP, 'build/picture.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
    const N = Math.round(dur * FPS);
    for (let f = 0; f < N; f++) { await p.evaluate(t => window.seek(t), f / FPS); ff.stdin.write(await shot());
      if (f % 150 === 0) console.log(`frame ${f}/${N}`); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
