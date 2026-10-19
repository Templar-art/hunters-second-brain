// Scene-cut detection in the browser: sample the clip every 0.1 s on a tiny canvas, compare luma histograms,
// then refine each hit to the exact frame with a short binary search. Nothing leaves the machine.
const W = 64;
const H = 36;
const BINS = 32;

const seek = (video, time) =>
  new Promise(resolve => {
    const done = () => {
      video.removeEventListener('seeked', done);
      resolve();
    };
    video.addEventListener('seeked', done);
    video.currentTime = time;
  });

export async function detectCuts(url, fps, { onProgress = () => {}, step = 0.1, alive = () => true } = {}) {
  const video = document.createElement('video');
  video.muted = true;
  video.preload = 'auto';
  video.src = url;
  await new Promise((resolve, reject) => {
    video.onloadedmetadata = resolve;
    video.onerror = () => reject(new Error('Could not read the clip'));
  });
  const canvas = document.createElement('canvas');
  canvas.width = W;
  canvas.height = H;
  const context = canvas.getContext('2d', { willReadFrequently: true });

  const histogram = async time => {
    await seek(video, time);
    context.drawImage(video, 0, 0, W, H);
    const { data } = context.getImageData(0, 0, W, H);
    const bins = new Float32Array(BINS);
    for (let i = 0; i < data.length; i += 4) {
      const luma = 0.2126 * data[i] + 0.7152 * data[i + 1] + 0.0722 * data[i + 2];
      bins[Math.min(BINS - 1, Math.floor((luma / 256) * BINS))] += 1;
    }
    return bins.map(value => value / (W * H));
  };
  const distance = (a, b) => a.reduce((sum, value, index) => sum + Math.abs(value - b[index]), 0) / 2;

  const duration = video.duration;
  const times = [];
  for (let t = 0; t < duration - 0.02; t += step) times.push(t);
  const scores = [];
  let previous = await histogram(0);
  for (let i = 1; i < times.length && alive(); i += 1) {
    const next = await histogram(times[i]);
    scores.push({ from: times[i - 1], to: times[i], score: distance(previous, next), a: previous, b: next });
    previous = next;
    onProgress(i / times.length);
  }

  // A cut is a spike well above its neighbourhood, not just a busy shot.
  const hits = scores.filter((entry, index) => {
    const around = scores.slice(Math.max(0, index - 5), index + 6).filter(other => other !== entry);
    const sorted = around.map(other => other.score).sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)] || 0;
    return entry.score > 0.3 && entry.score > median * 3 + 0.08;
  });

  const frame = 1 / fps;
  const cuts = [];
  for (const hit of hits) {
    if (!alive()) break;
    let low = hit.from;
    let high = hit.to;
    while (high - low > frame * 1.01) {
      const middle = Math.round((low + high) / 2 / frame) * frame;
      if (middle <= low || middle >= high) break;
      const sample = await histogram(middle);
      if (distance(hit.a, sample) < distance(sample, hit.b)) low = middle;
      else high = middle;
    }
    cuts.push(Math.round(high / frame) * frame);
  }
  video.removeAttribute('src');
  video.load();
  return cuts;
}
