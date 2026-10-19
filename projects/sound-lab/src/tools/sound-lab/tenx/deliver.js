// 10x additions: delivery-spec rendering, file naming and timecode helpers for video editors.
import { renderSound } from '../../../sounds/ts/react-bits-sound';
import { encodeWav } from '../export/wav';

export const DELIVERY = { rate: 48000, depth: 24 };

export const FRAME_RATES = [
  { value: 23.976, label: '23.976' },
  { value: 24, label: '24' },
  { value: 25, label: '25' },
  { value: 29.97, label: '29.97' },
  { value: 30, label: '30' },
  { value: 50, label: '50' },
  { value: 60, label: '60' }
];

const slug = value =>
  String(value || '')
    .trim()
    .replace(/[^A-Za-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');

// PROJECT_category_sound[_01].wav — sorts by project, then by SFX family, in any bin or finder window.
export function sfxName(project, sound, index = null, extension = 'wav') {
  const parts = [slug(project), slug(sound.category), slug(sound.id)].filter(Boolean);
  if (index !== null) parts.push(String(index + 1).padStart(2, '0'));
  return `${parts.join('_')}.${extension}`;
}

export const kitName = project => `${slug(project) || 'sound-lab'}_sfx-kit.zip`;

export function peakOf(buffer) {
  let peak = 0;
  let at = 0;
  for (let channel = 0; channel < buffer.numberOfChannels; channel += 1) {
    const data = buffer.getChannelData(channel);
    for (let i = 0; i < data.length; i += 1) {
      const value = Math.abs(data[i]);
      if (value > peak) {
        peak = value;
        at = i;
      }
    }
  }
  return { peak, time: at / buffer.sampleRate };
}

// Scales in place so the loudest sample sits at `ceiling` dBFS (default -1, broadcast-safe headroom).
export function normalize(buffer, ceiling = -1) {
  const { peak } = peakOf(buffer);
  if (peak < 1e-6) return buffer;
  const gain = Math.pow(10, ceiling / 20) / peak;
  for (let channel = 0; channel < buffer.numberOfChannels; channel += 1) {
    const data = buffer.getChannelData(channel);
    for (let i = 0; i < data.length; i += 1) data[i] *= gain;
  }
  return buffer;
}

export async function renderDelivery(sound, tune = {}, { rate = DELIVERY.rate, normalized = true } = {}) {
  const buffer = await renderSound(sound.recipe, tune, { sampleRate: rate, channels: 2 });
  return normalized ? normalize(buffer) : buffer;
}

export async function deliveryWav(sound, tune, options = {}) {
  const buffer = await renderDelivery(sound, tune, options);
  return { blob: encodeWav(buffer, { bitDepth: options.depth || DELIVERY.depth, channels: 2 }), buffer };
}

const nominal = fps => Math.round(fps);
const dropFrame = fps => Math.abs(fps - 29.97) < 0.01;

// SMPTE timecode. 29.97 uses drop-frame (;) like Premiere/Resolve; 23.976 is non-drop at 24 nominal.
export function timecode(seconds, fps = 25) {
  const base = nominal(fps);
  let frames = Math.max(0, Math.floor(seconds * fps + 1e-6));
  if (dropFrame(fps)) {
    const perTen = 17982;
    const perMinute = 1798;
    const tens = Math.floor(frames / perTen);
    const rest = frames % perTen;
    frames += 18 * tens + (rest > 2 ? 2 * Math.floor((rest - 2) / perMinute) : 0);
  }
  const ff = frames % base;
  const total = Math.floor(frames / base);
  const pad = value => String(value).padStart(2, '0');
  return `${pad(Math.floor(total / 3600))}:${pad(Math.floor(total / 60) % 60)}:${pad(total % 60)}${dropFrame(fps) ? ';' : ':'}${pad(ff)}`;
}
