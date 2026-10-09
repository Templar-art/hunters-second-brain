// node render3.cjs stills <t,t,..> <outdir>  |  node render3.cjs video <out.mov>
const { chromium } = require('playwright'); const { spawn } = require('child_process'); const path = require('path');
const DIR = __dirname, FPS = 30, DUR = 23.0;
(async () => {
  const b = await chromium.launch({ channel: 'chrome', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('console', m => m.type() === 'error' && console.error('PAGE', m.text()));
  await p.goto('file://' + path.join(DIR, 'v3.html')); await p.evaluate(() => window.ready);
  const shot = () => p.locator('canvas').screenshot({ type: 'png' });
  if (process.argv[2] === 'stills') {
    for (const t of process.argv[3].split(',')) { await p.evaluate(t => window.seek(+t), t);
      require('fs').writeFileSync(path.join(process.argv[4], `s_${t}.png`), await shot()); }
  } else {
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
      '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p', process.argv[3]], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let f = 0; f < DUR * FPS; f++) { await p.evaluate(t => window.seek(t), f / FPS); ff.stdin.write(await shot()); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
