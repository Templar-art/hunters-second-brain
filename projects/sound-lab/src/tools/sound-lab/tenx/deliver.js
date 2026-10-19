// 10x additions: delivery-spec rendering, file naming and timecode helpers for video editors.
import { itemCategory, itemSlug, level, renderItem } from './render';
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

// PROJECT_category_sound[_01][-2].wav — sorts by project, then by SFX family, in any bin or finder window.
// Works for a catalog sound or a kit item (single sound or stack).
export function sfxName(project, item, index = null, extension = 'wav', take = 0) {
  const parts = [slug(project), slug(itemCategory(item)), slug(itemSlug(item))].filter(Boolean);
  if (index !== null) parts.push(String(index + 1).padStart(2, '0'));
  return `${parts.join('_')}${take ? `-${take + 1}` : ''}.${extension}`;
}

export const kitName = project => `${slug(project) || 'sound-lab'}_sfx-kit.zip`;
export const projectSlug = project => slug(project.name) || 'sound-lab';

// peak: the loudest sample (for headroom). time: centre of the loudest 10 ms window (for alignment) — a single
// sample in a noisy rumble wanders by tens of ms between renders, the envelope doesn't.
export function peakOf(buffer) {
  const rate = buffer.sampleRate;
  const channels = Array.from({ length: buffer.numberOfChannels }, (_, index) => buffer.getChannelData(index));
  const window = Math.max(1, Math.round(rate * 0.01));
  let peak = 0;
  let best = -1;
  let at = 0;
  for (let from = 0; from < buffer.length; from += window) {
    let energy = 0;
    const to = Math.min(buffer.length, from + window);
    for (let i = from; i < to; i += 1) {
      let mono = 0;
      channels.forEach(data => {
        peak = Math.max(peak, Math.abs(data[i]));
        mono += data[i];
      });
      energy += mono * mono;
    }
    if (energy > best) {
      best = energy;
      at = (from + to) / 2;
    }
  }
  return { peak, time: at / rate };
}

export const levelOf = project => ({ mode: project.level, target: project.lufs });

export async function renderDelivery(item, project, { take = 0, levelled = true } = {}) {
  const buffer = await renderItem(item, { rate: DELIVERY.rate, take });
  return levelled ? level(buffer, levelOf(project)).buffer : buffer;
}

export async function deliveryWav(item, project, options = {}) {
  const buffer = await renderDelivery(item, project, options);
  return { blob: encodeWav(buffer, { bitDepth: DELIVERY.depth, channels: 2 }), buffer };
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
