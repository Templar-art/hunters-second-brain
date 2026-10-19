import { useEffect, useRef, useState } from 'react';
import { Cancel01Icon, Download04Icon, PlusSignIcon, Video01Icon } from '@hugeicons/core-free-icons';
import { toast } from 'sonner';
import { Icon, Tip, Track } from '../../background-studio/components/ui';
import { downloadBlob } from '../../background-studio/utils/download';
import { encodeWav } from '../export/wav';
import { DELIVERY, levelOf, peakOf, projectSlug, timecode } from './deliver';
import { itemName, level, renderItem } from './render';
import { buildFcpxml, rateOf } from './fcpxml';
import { detectCuts } from './cuts';
import { saveFiles } from './save';
import { stackItem } from './StackSection';
import { zipFiles } from './zip';

const ALIGN = [
  { value: 'start', label: 'Start' },
  { value: 'peak', label: 'Peak' }
];

const itemOf = cue => cue.item || { id: cue.id, tune: cue.tune || {} };
const startOf = cue => cue.time - (cue.align === 'peak' ? cue.peak : 0);
const uid = () => `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;

const renderCue = async (cue, project) => level(await renderItem(itemOf(cue)), levelOf(project)).buffer;

// One WAV the length of the video with every cue in place. Drop it at the head of the edit and it lines up.
async function renderStem(cues, duration, project) {
  const rate = DELIVERY.rate;
  const frames = Math.max(1, Math.ceil(duration * rate));
  const stem = new AudioBuffer({ length: frames, numberOfChannels: 2, sampleRate: rate });
  for (const cue of cues) {
    const buffer = await renderCue(cue, project);
    const start = Math.round(startOf(cue) * rate);
    for (let channel = 0; channel < 2; channel += 1) {
      const from = buffer.getChannelData(Math.min(channel, buffer.numberOfChannels - 1));
      const to = stem.getChannelData(channel);
      for (let i = Math.max(0, -start); i < from.length && start + i < frames; i += 1) to[start + i] += from[i];
    }
  }
  if (peakOf(stem).peak > Math.pow(10, -1 / 20)) level(stem, { mode: 'peak', ceiling: -1 });
  return encodeWav(stem, { bitDepth: DELIVERY.depth, channels: 2 });
}

// Each cue as its own WAV, padded so it can sit on a whole frame and still land sample-accurate.
async function renderFcp(cues, element, project) {
  const rate = rateOf(project.fps);
  const fps = rate.den / rate.num;
  const folder = `${projectSlug(project)}_sfx-cues`;
  const files = [];
  const clips = [];
  for (const [index, cue] of cues.entries()) {
    const buffer = await renderCue(cue, project);
    const start = startOf(cue);
    const frame = Math.max(0, Math.floor(start * fps + 1e-6));
    const shift = Math.round((start - frame / fps) * DELIVERY.rate);
    const length = Math.max(1, buffer.length + shift);
    const placed = new AudioBuffer({ length, numberOfChannels: 2, sampleRate: DELIVERY.rate });
    for (let channel = 0; channel < 2; channel += 1) {
      const from = buffer.getChannelData(Math.min(channel, buffer.numberOfChannels - 1));
      const to = placed.getChannelData(channel);
      for (let i = Math.max(0, -shift); i < from.length; i += 1) to[i + shift] = from[i];
    }
    const name = `${String(index + 1).padStart(2, '0')} ${itemName(itemOf(cue))}`;
    const file = `${projectSlug(project)}_cue${String(index + 1).padStart(2, '0')}_${timecode(cue.time, project.fps).replace(/[:;]/g, '-')}.wav`;
    files.push({ name: file, data: encodeWav(placed, { bitDepth: DELIVERY.depth, channels: 2 }) });
    clips.push({ name, file, frame, frames: Math.max(1, Math.floor((length / DELIVERY.rate) * fps)) });
  }
  // The gap spans the clip, or the last SFX tail if that runs longer.
  const totalFrames = Math.max(Math.ceil(element.duration * fps), ...clips.map(clip => clip.frame + clip.frames));
  const xml = buildFcpxml({
    project,
    folder,
    clips,
    totalFrames,
    width: element.videoWidth || 1920,
    height: element.videoHeight || 1080
  });
  files.push({ name: `${folder}.fcpxml`, data: xml });
  return { folder, files };
}

export default function PictureSync({ sound, tune, stack, project, folder, cues, onCues, player, onClose }) {
  const videoRef = useRef(null);
  const [video, setVideo] = useState(null);
  const [now, setNow] = useState(0);
  const [align, setAlign] = useState('start');
  const [busy, setBusy] = useState(null);
  const [cuts, setCuts] = useState(null);
  const cache = useRef(new Map());
  const cuesRef = useRef(cues);
  cuesRef.current = cues;
  const projectRef = useRef(project);
  projectRef.current = project;

  useEffect(() => () => video && URL.revokeObjectURL(video.url), [video]);

  const bufferFor = cue => {
    const key = `${cue.key}:${project.level}:${project.lufs}`;
    if (!cache.current.has(key)) cache.current.set(key, renderCue(cue, projectRef.current));
    return cache.current.get(key);
  };

  // Render every cue ahead of time so a trigger only has to start a buffer.
  useEffect(() => {
    cues.forEach(cue => bufferFor(cue).catch(() => null));
  });

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
          if (at > last && at <= current) bufferFor(cue).then(buffer => player.playBuffer(buffer)).catch(() => null);
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
      setNow(last);
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
    setCuts(null);
    setVideo({ url: URL.createObjectURL(file), name: file.name });
  };

  const cueAt = async (item, time, how = align) => {
    const cue = { key: uid(), item, time, align: how, peak: 0 };
    cue.peak = peakOf(await renderCue(cue, projectRef.current)).time;
    return cue;
  };

  const place = async item => {
    const element = videoRef.current;
    if (!element) return;
    const cue = await cueAt(item, element.currentTime);
    onCues([...cuesRef.current, cue].sort((a, b) => a.time - b.time));
  };

  const placeSound = () => place({ id: sound.id, tune });
  const placeStack = () => place({ ...stackItem(stack), name: itemName(stackItem(stack)) });

  const cueCuts = async () => {
    const item = { id: sound.id, tune };
    const added = [];
    const taken = cue => cuesRef.current.some(other => itemOf(other).id === item.id && Math.abs(other.time - cue) < 0.02);
    for (const time of cuts) if (!taken(time)) added.push(await cueAt(item, time, 'peak'));
    onCues([...cuesRef.current, ...added].sort((a, b) => a.time - b.time));
    toast.success(`${sound.name} cued on ${added.length} cuts, peak-aligned`);
  };

  const findCuts = async () => {
    setBusy('cuts');
    try {
      const found = await detectCuts(video.url, rateOf(project.fps).den / rateOf(project.fps).num, {
        onProgress: value => setBusy(`cuts ${Math.round(value * 100)}%`)
      });
      setCuts(found);
      toast.success(found.length ? `${found.length} cuts found` : 'No hard cuts found');
    } catch (problem) {
      toast.error(problem?.message || 'Cut detection failed');
    } finally {
      setBusy(null);
    }
  };

  const exportStem = async () => {
    const element = videoRef.current;
    if (!element || !cues.length) return;
    setBusy('stem');
    try {
      const blob = await renderStem(cues, element.duration, project);
      const name = `${projectSlug(project)}_sfx-stem_${String(project.fps).replace('.', '')}fps.wav`;
      const where = await saveFiles(folder, [{ name, data: blob }]);
      toast.success(`Stem → ${where}. Place it at the first frame of the clip.`);
    } catch (problem) {
      toast.error(problem?.message || 'Stem export failed');
    } finally {
      setBusy(null);
    }
  };

  const exportFcp = async () => {
    const element = videoRef.current;
    if (!element || !cues.length) return;
    setBusy('fcp');
    try {
      const { folder: sub, files } = await renderFcp(cues, element, project);
      const where = await saveFiles(folder, files, {
        sub,
        fallback: async () => {
          const zip = await zipFiles(files.map(file => ({ ...file, name: `${sub}/${file.name}` })));
          downloadBlob(zip, `${sub}.zip`);
          return 'Downloads (zip)';
        }
      });
      toast.success(`FCP XML → ${where}. Media must sit at ${project.mediaPath}/${sub}`);
    } catch (problem) {
      toast.error(problem?.message || 'FCP export failed');
    } finally {
      setBusy(null);
    }
  };

  // Editor transport: Space/K play-pause, L play (again = 2×), J back 1 s, ←/→ or ,/. one frame (⇧ = 1 s), M cue.
  useEffect(() => {
    const onKey = event => {
      if (event.metaKey || event.ctrlKey || event.altKey) return;
      if (event.target?.closest?.('input, textarea, [role="dialog"]')) return;
      const element = videoRef.current;
      const key = event.key.toLowerCase();
      const frame = rateOf(project.fps).num / rateOf(project.fps).den;
      const nudge = by => {
        element.pause();
        element.currentTime = Math.max(0, Math.min(element.duration, element.currentTime + by));
      };
      if (key === 'm') placeSound();
      else if (!element) return;
      else if (key === ' ' || key === 'k') {
        if (key === ' ' && event.target?.closest?.('button')) return;
        if (element.paused) {
          element.playbackRate = 1;
          element.play();
        } else element.pause();
      } else if (key === 'l') {
        element.playbackRate = element.paused ? 1 : Math.min(4, element.playbackRate * 2);
        element.play();
      } else if (key === 'j') element.currentTime = Math.max(0, element.currentTime - 1);
      else if (key === 'arrowleft' || key === ',') nudge(event.shiftKey ? -1 : -frame);
      else if (key === 'arrowright' || key === '.') nudge(event.shiftKey ? 1 : frame);
      else return;
      event.preventDefault();
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
          <button type="button" className="bs-export tx-ghost" onClick={onClose} aria-label="Back to the sound">
            <Icon icon={Cancel01Icon} />
          </button>
        </Tip>
        <span className="tx-tc">{timecode(now, project.fps)}</span>
        <Track label="Align cue" value={align} options={ALIGN} onChange={setAlign} />
        <Tip label={`Place ${sound.name} at the playhead`} hint="M">
          <button type="button" className="bs-export" onClick={placeSound} disabled={!video}>
            <Icon icon={PlusSignIcon} />
            <span>Cue {sound.name}</span>
          </button>
        </Tip>
        {stack.length > 0 && (
          <button type="button" className="bs-export tx-ghost" onClick={placeStack} disabled={!video}>
            <span>Cue stack</span>
          </button>
        )}
      </div>

      <div className="tx-picture-bar">
        <button type="button" className="bs-export tx-ghost" onClick={findCuts} disabled={!video || Boolean(busy)}>
          {busy?.startsWith('cuts') ? <span className="bs-spinner" /> : null}
          <span>{busy?.startsWith('cuts') ? busy.replace('cuts', 'Scanning') : 'Find cuts'}</span>
        </button>
        <span className="tx-spacer" />
        <Tip label="One WAV the length of the clip, every cue in place">
          <button type="button" className="bs-export tx-ghost" onClick={exportStem} disabled={!video || Boolean(busy) || !cues.length}>
            {busy === 'stem' ? <span className="bs-spinner" /> : <Icon icon={Download04Icon} />}
            <span>Stem</span>
          </button>
        </Tip>
        <Tip label="Each cue as its own WAV + a Final Cut project">
          <button type="button" className="bs-export" onClick={exportFcp} disabled={!video || Boolean(busy) || !cues.length}>
            {busy === 'fcp' ? <span className="bs-spinner" /> : <Icon icon={Download04Icon} />}
            <span>FCP XML</span>
          </button>
        </Tip>
      </div>

      {cuts && cuts.length > 0 && (
        <div className="tx-cuts">
          {cuts.map(time => (
            <button
              type="button"
              className="tx-chip"
              key={time}
              onClick={() => {
                if (videoRef.current) videoRef.current.currentTime = time;
              }}
            >
              ✂ {timecode(time, project.fps)}
            </button>
          ))}
          <button type="button" className="tx-chip tx-chip-strong" onClick={cueCuts}>
            Cue {sound.name} on all {cuts.length}
          </button>
        </div>
      )}

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
                <span>{itemName(itemOf(cue))}</span>
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
      {video && (
        <p className="tx-note tx-video-name">
          {video.name} · Space/K play · L faster · J back 1 s · ←/→ frame (⇧ 1 s) · M cue
        </p>
      )}
    </div>
  );
}
