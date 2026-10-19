import { useEffect, useRef, useState } from 'react';
import { Cancel01Icon, Download04Icon, PlusSignIcon, Video01Icon } from '@hugeicons/core-free-icons';
import { toast } from 'sonner';
import { Icon, Tip, Track } from '../../background-studio/components/ui';
import { downloadBlob } from '../../background-studio/utils/download';
import { SOUNDS_BY_ID } from '../sounds/catalog';
import { encodeWav } from '../export/wav';
import { DELIVERY, normalize, peakOf, renderDelivery, timecode } from './deliver';

const ALIGN = [
  { value: 'start', label: 'Start' },
  { value: 'peak', label: 'Peak' }
];

const startOf = cue => cue.time - (cue.align === 'peak' ? cue.peak : 0);

const stemName = (project, fps) =>
  `${(project.name || 'sound-lab').trim().replace(/[^A-Za-z0-9]+/g, '-')}_sfx-stem_${String(fps).replace('.', '')}fps.wav`;

// One WAV the length of the video with every cue in place. Drop it at the head of the edit and it lines up.
async function renderStem(cues, duration, project) {
  const rate = DELIVERY.rate;
  const frames = Math.max(1, Math.ceil(duration * rate));
  const stem = new AudioBuffer({ length: frames, numberOfChannels: 2, sampleRate: rate });
  for (const cue of cues) {
    const sound = SOUNDS_BY_ID[cue.id];
    if (!sound) continue;
    const buffer = await renderDelivery(sound, cue.tune, { normalized: false });
    const start = Math.round(startOf(cue) * rate);
    for (let channel = 0; channel < 2; channel += 1) {
      const from = buffer.getChannelData(Math.min(channel, buffer.numberOfChannels - 1));
      const to = stem.getChannelData(channel);
      for (let i = Math.max(0, -start); i < from.length && start + i < frames; i += 1) to[start + i] += from[i];
    }
  }
  if (peakOf(stem).peak > Math.pow(10, -1 / 20)) normalize(stem, -1);
  return encodeWav(stem, { bitDepth: DELIVERY.depth, channels: 2 });
}

export default function PictureSync({ sound, tune, project, cues, onCues, player, onClose }) {
  const videoRef = useRef(null);
  const [video, setVideo] = useState(null);
  const [now, setNow] = useState(0);
  const [align, setAlign] = useState('start');
  const [busy, setBusy] = useState(false);
  const cuesRef = useRef(cues);
  cuesRef.current = cues;

  useEffect(() => () => video && URL.revokeObjectURL(video.url), [video]);

  // Render every cue ahead of time so a trigger only has to start a buffer.
  useEffect(() => {
    cues.forEach(cue => SOUNDS_BY_ID[cue.id] && player.preload(SOUNDS_BY_ID[cue.id], cue.tune));
  }, [cues, player]);

  // Fire each cue as the playhead crosses its start, so the SFX is heard against picture.
  useEffect(() => {
    const element = videoRef.current;
    if (!element) return undefined;
    let last = element.currentTime;
    let frame = 0;
    const check = () => {
      const current = element.currentTime;
      setNow(current);
      if (!element.paused && current >= last) {
        cuesRef.current.forEach(cue => {
          const at = startOf(cue);
          if (at > last && at <= current) {
            const target = SOUNDS_BY_ID[cue.id];
            if (target) player.play(target, cue.tune, { exclusive: false }).catch(() => null);
          }
        });
      }
      last = current;
    };
    const tick = () => {
      check();
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    // A jump is a seek, not playback: skip the cues in between. timeupdate backs up rAF when the tab is throttled.
    const onSeek = () => {
      last = element.currentTime;
    };
    element.addEventListener('seeking', onSeek);
    element.addEventListener('seeked', onSeek);
    element.addEventListener('timeupdate', check);
    return () => {
      cancelAnimationFrame(frame);
      element.removeEventListener('seeking', onSeek);
      element.removeEventListener('seeked', onSeek);
      element.removeEventListener('timeupdate', check);
    };
  }, [video, player]);

  const load = file => {
    if (!file || !file.type.startsWith('video/')) return;
    setVideo({ url: URL.createObjectURL(file), name: file.name });
  };

  const place = async () => {
    const element = videoRef.current;
    if (!element) return;
    const buffer = await renderDelivery(sound, tune, { normalized: false });
    const cue = {
      key: `${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      id: sound.id,
      tune,
      time: element.currentTime,
      align,
      peak: peakOf(buffer).time
    };
    onCues([...cuesRef.current, cue].sort((a, b) => a.time - b.time));
  };

  const exportStem = async () => {
    const element = videoRef.current;
    if (!element || !cues.length) return;
    setBusy(true);
    try {
      const blob = await renderStem(cues, element.duration, project);
      downloadBlob(blob, stemName(project, project.fps));
      toast.success('Stem exported. Place it at the first frame of the clip.');
    } catch (problem) {
      toast.error(problem?.message || 'Stem export failed');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    const onKey = event => {
      if (event.key.toLowerCase() !== 'm' || event.metaKey || event.ctrlKey) return;
      if (event.target?.closest?.('input, textarea')) return;
      event.preventDefault();
      place();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  return (
    <div
      className="lab-stage tx-picture"
      onDragOver={event => event.preventDefault()}
      onDrop={event => {
        event.preventDefault();
        load(event.dataTransfer.files?.[0]);
      }}
    >
      {video ? (
        <video ref={videoRef} className="tx-video" src={video.url} controls playsInline />
      ) : (
        <label className="tx-drop">
          <Icon icon={Video01Icon} size={28} />
          <strong>Drop a clip or click to load</strong>
          <span>Stays on this Mac. Nothing uploads.</span>
          <input type="file" accept="video/*" hidden onChange={event => load(event.target.files?.[0])} />
        </label>
      )}

      <div className="tx-picture-bar">
        <Tip label="Back to the sound" hint="P">
          <button type="button" className="bs-export tx-ghost" onClick={onClose}>
            <Icon icon={Cancel01Icon} />
          </button>
        </Tip>
        <span className="tx-tc">{timecode(now, project.fps)}</span>
        <Track label="Align cue" value={align} options={ALIGN} onChange={setAlign} />
        <Tip label={`Place ${sound.name} at the playhead`} hint="M">
          <button type="button" className="bs-export" onClick={place} disabled={!video}>
            <Icon icon={PlusSignIcon} />
            <span>Cue {sound.name}</span>
          </button>
        </Tip>
        <Tip label="One WAV the length of the clip, every cue in place">
          <button type="button" className="bs-export" onClick={exportStem} disabled={!video || busy || !cues.length}>
            {busy ? <span className="bs-spinner" /> : <Icon icon={Download04Icon} />}
            <span>Stem</span>
          </button>
        </Tip>
      </div>

      {cues.length > 0 && (
        <ol className="tx-cues">
          {cues.map(cue => (
            <li key={cue.key}>
              <button
                type="button"
                className="tx-cue-seek"
                onClick={() => {
                  if (videoRef.current) videoRef.current.currentTime = cue.time;
                }}
              >
                <span className="tx-tc">{timecode(cue.time, project.fps)}</span>
                <span>{SOUNDS_BY_ID[cue.id]?.name}</span>
                <em>{cue.align === 'peak' ? `peak −${cue.peak.toFixed(2)}s` : 'start'}</em>
              </button>
              <button
                type="button"
                className="lab-icon-button"
                aria-label="Remove cue"
                onClick={() => onCues(cues.filter(item => item.key !== cue.key))}
              >
                <Icon icon={Cancel01Icon} size={13} />
              </button>
            </li>
          ))}
        </ol>
      )}
      {video && <p className="tx-note tx-video-name">{video.name}</p>}
    </div>
  );
}
