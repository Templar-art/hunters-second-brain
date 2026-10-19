// Loudness metering, kept dependency-free so it can be checked against ffmpeg ebur128 in Node.
// ITU-R BS.1770-4 K-weighting (libebur128 coefficients, any sample rate).
const kWeight = (input, rate) => {
  const biquad = (data, b0, b1, b2, a1, a2) => {
    const out = new Float32Array(data.length);
    let x1 = 0;
    let x2 = 0;
    let y1 = 0;
    let y2 = 0;
    for (let i = 0; i < data.length; i += 1) {
      const x = data[i];
      const y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2;
      out[i] = y;
      x2 = x1;
      x1 = x;
      y2 = y1;
      y1 = y;
    }
    return out;
  };
  let K = Math.tan((Math.PI * 1681.974450955533) / rate);
  const Q1 = 0.7071752369554196;
  const Vh = Math.pow(10, 3.999843853973347 / 20);
  const Vb = Math.pow(Vh, 0.4996667741545416);
  let a0 = 1 + K / Q1 + K * K;
  const shelf = biquad(
    input,
    (Vh + (Vb * K) / Q1 + K * K) / a0,
    (2 * (K * K - Vh)) / a0,
    (Vh - (Vb * K) / Q1 + K * K) / a0,
    (2 * (K * K - 1)) / a0,
    (1 - K / Q1 + K * K) / a0
  );
  K = Math.tan((Math.PI * 38.13547087602444) / rate);
  const Q2 = 0.5003270373238773;
  a0 = 1 + K / Q2 + K * K;
  return biquad(shelf, 1, -2, 1, (2 * (K * K - 1)) / a0, (1 - K / Q2 + K * K) / a0);
};

// Integrated loudness in LUFS. SFX shorter than one 400 ms block fall back to the ungated whole-file level.
export function loudness(buffer) {
  const rate = buffer.sampleRate;
  const channels = Array.from({ length: buffer.numberOfChannels }, (_, index) =>
    kWeight(buffer.getChannelData(index), rate)
  );
  const power = (from, to) => {
    let sum = 0;
    channels.forEach(data => {
      let channelSum = 0;
      for (let i = from; i < to; i += 1) channelSum += data[i] * data[i];
      sum += channelSum / Math.max(1, to - from);
    });
    return sum;
  };
  const toLufs = value => -0.691 + 10 * Math.log10(Math.max(value, 1e-12));
  const block = Math.round(rate * 0.4);
  const step = Math.round(rate * 0.1);
  if (buffer.length < block) return toLufs(power(0, buffer.length));
  const blocks = [];
  for (let from = 0; from + block <= buffer.length; from += step) blocks.push(power(from, from + block));
  const absolute = blocks.filter(value => toLufs(value) > -70);
  if (!absolute.length) return -Infinity;
  const relative = toLufs(absolute.reduce((a, b) => a + b, 0) / absolute.length) - 10;
  const gated = absolute.filter(value => toLufs(value) > relative);
  return toLufs(gated.reduce((a, b) => a + b, 0) / gated.length);
}
