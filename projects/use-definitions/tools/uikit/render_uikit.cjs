// Render the USE UI sound kit (pops, clicks, keys, chime) from the local Sound Lab engine.
// Needs Sound Lab running on :8160. Usage: NODE_PATH=tools/node_modules node tools/uikit/render_uikit.cjs <outdir>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
// cue type -> Sound Lab sound ids (each rendered as 4 takes with the engine's own pitch/tone jitter)
const KIT = {
  pop:   ['bead', 'dew', 'pebble', 'boop', 'dot'],
  click: ['nib', 'notch', 'tab', 'tink'],
  key:   ['keycap', 'chiclet', 'thock'],
  chime: ['chime', 'ping'],
};
(async () => {
  const b = await chromium.launch({ channel: 'chrome' }); const p = await b.newPage();
  await p.goto('http://localhost:8160/', { waitUntil: 'networkidle' });
  const res = await p.evaluate(async (KIT) => {
    const { renderTuned } = await import('/src/tools/sound-lab/tenx/render.js');
    const { SOUNDS_BY_ID } = await import('/src/tools/sound-lab/sounds/catalog.js');
    const wav = (buf) => {               // 24-bit stereo PCM
      const ch = buf.numberOfChannels, n = buf.length, sr = buf.sampleRate, bps = 3;
      const ab = new ArrayBuffer(44 + n * ch * bps), v = new DataView(ab); let o = 0;
      const s = (t) => { for (const c of t) v.setUint8(o++, c.charCodeAt(0)); };
      s('RIFF'); v.setUint32(o, 36 + n * ch * bps, true); o += 4; s('WAVEfmt ');
      v.setUint32(o, 16, true); o += 4; v.setUint16(o, 1, true); o += 2; v.setUint16(o, ch, true); o += 2;
      v.setUint32(o, sr, true); o += 4; v.setUint32(o, sr * ch * bps, true); o += 4; v.setUint16(o, ch * bps, true); o += 2;
      v.setUint16(o, 24, true); o += 2; s('data'); v.setUint32(o, n * ch * bps, true); o += 4;
      const d = [...Array(ch)].map((_, c) => buf.getChannelData(c));
      for (let i = 0; i < n; i++) for (let c = 0; c < ch; c++) {
        let x = Math.max(-1, Math.min(1, d[c][i])) * 8388607 | 0; v.setUint8(o++, x & 255); v.setUint8(o++, (x >> 8) & 255); v.setUint8(o++, (x >> 16) & 255);
      }
      let bin = ''; const u = new Uint8Array(ab); for (let i = 0; i < u.length; i += 32768) bin += String.fromCharCode(...u.subarray(i, i + 32768));
      return btoa(bin);
    };
    const res = [];
    for (const [type, ids] of Object.entries(KIT)) for (const id of ids) {
      const snd = SOUNDS_BY_ID[id]; if (!snd) { res.push({ type, id, err: 'missing' }); continue; }
      for (let take = 0; take < 4; take++) {
        const buf = await renderTuned(snd, { trim: { tail: true, fadeOut: 8 } }, { rate: 48000, variant: take });
        res.push({ type, id, take, dur: buf.length / buf.sampleRate, b64: wav(buf) });
      }
    }
    return res;
  }, KIT);
  for (const r of res) {
    if (r.err) { console.log('MISSING', r.id); continue; }
    fs.writeFileSync(path.join(out, `${r.type}_${r.id}_${r.take + 1}.wav`), Buffer.from(r.b64, 'base64'));
  }
  console.log('rendered', res.filter(r => !r.err).length, 'files');
  await b.close();
})();
