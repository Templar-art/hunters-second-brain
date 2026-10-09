// node render.cjs stills t1,t2,... | node render.cjs video
// Needs playwright on NODE_PATH; uses system Chrome.
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path');
const DIR = __dirname, FPS = 30, DUR = 22.5;
(async () => {
  const b = await chromium.launch({ channel: 'chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.join(DIR, 'graphics.html')); await p.evaluate(() => window.ready);
  if (process.argv[2] === 'stills') {
    for (const t of process.argv[3].split(',')) { await p.evaluate(t => window.seek(+t), t);
      await p.screenshot({ path: path.join(process.argv[4], `g_${t}.png`), omitBackground: true }); }
  } else {
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
      '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', path.join(DIR, 'build/graphics.mov')], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = 0; f < DUR * FPS; f++) { await p.evaluate(t => window.seek(t), f / FPS);
      ff.stdin.write(await p.screenshot({ type: 'png', omitBackground: true })); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
