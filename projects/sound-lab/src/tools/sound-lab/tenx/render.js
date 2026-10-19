// 10x render layer: wraps the stock engine with trims, multi-layer stacks, takes and loudness.
import { renderSound } from '../../../sounds/ts/react-bits-sound';
import { SOUNDS_BY_ID } from '../sounds/catalog';
import { loudness } from './loudness';

export { loudness };

const copyBuffer = (source, from = 0, to = source.length) => {
  const length = Math.max(1, to - from);
  const out = new AudioBuffer({ length, numberOfChannels: source.numberOfChannels, sampleRate: source.sampleRate });
  for (let channel = 0; channel < source.numberOfChannels; channel += 1) {
    out.getChannelData(channel).set(source.getChannelData(channel).subarray(from, from + length));
  }
  return out;
};

// Last sample above -60 dB of the peak, plus 20 ms of air.
const audibleEnd = buffer => {
  let peak = 0;
  for (let channel = 0; channel < buffer.numberOfChannels; channel += 1) {
    const data = buffer.getChannelData(channel);
    for (let i = 0; i < data.length; i += 1) peak = Math.max(peak, Math.abs(data[i]));
  }
  const floor = peak * 0.001;
  let end = 0;
  for (let channel = 0; channel < buffer.numberOfChannels; channel += 1) {
    const data = buffer.getChannelData(channel);
    for (let i = data.length - 1; i > end; i -= 1) {
      if (Math.abs(data[i]) > floor) {
        end = i;
        break;
      }
    }
  }
  return Math.min(buffer.length, end + Math.round(buffer.sampleRate * 0.02));
};

// The "Trim" effect: cut the silent tail, reverse, then fade. Runs after the engine, so it applies to everything.
export function finish(buffer, tune = {}) {
  const trim = tune.trim;
  if (!trim) return buffer;
  let out = trim.tail ? copyBuffer(buffer, 0, audibleEnd(buffer)) : copyBuffer(buffer);
  const rate = out.sampleRate;
  for (let channel = 0; channel < out.numberOfChannels; channel += 1) {
    const data = out.getChannelData(channel);
    if (trim.reverse) data.reverse();
    const fadeIn = Math.min(data.length, Math.round(((trim.fadeIn || 0) / 1000) * rate));
    const fadeOut = Math.min(data.length, Math.round(((trim.fadeOut || 0) / 1000) * rate));
    for (let i = 0; i < fadeIn; i += 1) data[i] *= Math.sin((i / fadeIn) * (Math.PI / 2));
    for (let i = 0; i < fadeOut; i += 1) data[data.length - 1 - i] *= Math.sin((i / fadeOut) * (Math.PI / 2));
  }
  return out;
}

export async function renderTuned(sound, tune = {}, { rate = 48000, variant = 0 } = {}) {
  const buffer = await renderSound(sound.recipe, tune, { sampleRate: rate, channels: 2, variant });
  return finish(buffer, tune);
}

// A take is the same sound nudged in pitch and tone, so repeated hits don't sound machine-gunned.
const jitter = (tune, take) => {
  if (!take) return tune;
  let seed = take * 9301 + 49297;
  const next = () => {
    seed = (seed * 9301 + 49297) % 233280;
    return seed / 233280 - 0.5;
  };
  return {
    ...tune,
    pitch: (tune.pitch || 0) + next() * 1.2,
    tone: Math.max(-1, Math.min(1, (tune.tone || 0) + next() * 0.16)),
    length: Math.max(0.5, Math.min(2, (tune.length || 1) * (1 + next() * 0.08)))
  };
};

export const layersOf = item => item.layers || [{ id: item.id, tune: item.tune || {}, offset: 0, gain: 0 }];

export const itemName = item =>
  item.name || layersOf(item)
    .map(layer => SOUNDS_BY_ID[layer.id]?.name)
    .filter(Boolean)
    .join(' + ');

export const itemCategory = item => (item.layers ? 'stack' : SOUNDS_BY_ID[item.id]?.category || 'sfx');

export const itemSlug = item =>
  item.layers ? slugify(item.name || layersOf(item).map(layer => layer.id).join('-')) : item.id;

const slugify = value =>
  String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');

// Any item (one sound or a stack of layers with offsets and gains) to one stereo buffer.
export async function renderItem(item, { rate = 48000, take = 0 } = {}) {
  const layers = layersOf(item);
  const rendered = [];
  for (const layer of layers) {
    const sound = SOUNDS_BY_ID[layer.id];
    if (!sound) continue;
    rendered.push({ layer, buffer: await renderTuned(sound, jitter(layer.tune || {}, take), { rate, variant: take }) });
  }
  if (!rendered.length) throw new Error('Nothing to render');
  if (!item.layers) return rendered[0].buffer;
  const lead = Math.min(0, ...rendered.map(({ layer }) => layer.offset || 0));
  const length = Math.max(
    ...rendered.map(({ layer, buffer }) => Math.round(((layer.offset || 0) - lead) * rate) + buffer.length)
  );
  const mix = new AudioBuffer({ length, numberOfChannels: 2, sampleRate: rate });
  rendered.forEach(({ layer, buffer }) => {
    const start = Math.round(((layer.offset || 0) - lead) * rate);
    const gain = Math.pow(10, (layer.gain || 0) / 20);
    for (let channel = 0; channel < 2; channel += 1) {
      const from = buffer.getChannelData(Math.min(channel, buffer.numberOfChannels - 1));
      const to = mix.getChannelData(channel);
      for (let i = 0; i < from.length; i += 1) to[start + i] += from[i] * gain;
    }
  });
  return finish(mix, item.tune || {});
}

const peakDb = buffer => {
  let peak = 0;
  for (let channel = 0; channel < buffer.numberOfChannels; channel += 1) {
    const data = buffer.getChannelData(channel);
    for (let i = 0; i < data.length; i += 1) peak = Math.max(peak, Math.abs(data[i]));
  }
  return 20 * Math.log10(Math.max(peak, 1e-9));
};

export const LEVELS = [
  { value: 'off', label: 'Off' },
  { value: 'peak', label: 'Peak −1' },
  { value: 'lufs', label: 'LUFS' }
];

export const LUFS_TARGETS = [-14, -18, -23];

// Level-match in place. LUFS mode never pushes the peak past -1 dBFS; it lands quieter than target instead.
export function level(buffer, { mode = 'peak', target = -18, ceiling = -1 } = {}) {
  if (mode === 'off') return { buffer, gain: 0 };
  const peak = peakDb(buffer);
  if (peak < -120) return { buffer, gain: 0 };
  let gain = ceiling - peak;
  if (mode === 'lufs') {
    const measured = loudness(buffer);
    if (Number.isFinite(measured)) gain = Math.min(target - measured, ceiling - peak);
  }
  const scale = Math.pow(10, gain / 20);
  for (let channel = 0; channel < buffer.numberOfChannels; channel += 1) {
    const data = buffer.getChannelData(channel);
    for (let i = 0; i < data.length; i += 1) data[i] *= scale;
  }
  return { buffer, gain };
}
