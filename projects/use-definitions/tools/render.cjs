// Render an episode's picture track. Usage:
//   node render.cjs <ep_dir> video            → <ep_dir>/build/picture.mp4 (+ build/cues.json, build/render.json)
//   node render.cjs <ep_dir> stills 1.0,5.2   → <ep_dir>/build/qa/s_<t>.png
const { chromium } = require('playwright'); const { spawn } = require('child_process');
const path = require('path'), fs = require('fs');
const ROOT = path.join(__dirname, '..'), EP = path.resolve(process.argv[2]), MODE = process.argv[3] || 'video', FPS = 30;
(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('PAGE ERROR', e.message));
  const rel = path.relative(path.join(ROOT, 'engine'), EP);
  await p.goto('file://' + path.join(ROOT, 'engine/page.html') + '?ep=' + encodeURIComponent(rel));
  const { dur } = await p.evaluate(() => window.ready);
  const voEnd = await p.evaluate(() => EP.voEnd || 0);
  fs.mkdirSync(path.join(EP, 'build/qa'), { recursive: true });
  fs.writeFileSync(path.join(EP, 'build/cues.json'), JSON.stringify(await p.evaluate(() => window.cues())));
  fs.writeFileSync(path.join(EP, 'build/render.json'), JSON.stringify({ dur, voEnd }));
  const shot = () => p.locator('canvas').screenshot({ type: 'png' });
  if (MODE === 'stills') {
    for (const t of process.argv[4].split(',')) { await p.evaluate(t => window.seek(+t), t);
      fs.writeFileSync(path.join(EP, `build/qa/s_${t}.png`), await shot()); }
  } else {
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
      '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', path.join(EP, 'build/picture.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
    const N = Math.round(dur * FPS);
    for (let f = 0; f < N; f++) { await p.evaluate(t => window.seek(t), f / FPS); ff.stdin.write(await shot());
      if (f % 150 === 0) console.log(`frame ${f}/${N}`); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
