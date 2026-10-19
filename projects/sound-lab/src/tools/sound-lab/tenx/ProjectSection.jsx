import { useState } from 'react';
import { Cancel01Icon, Download04Icon, PlusSignIcon } from '@hugeicons/core-free-icons';
import { toast } from 'sonner';
import { Icon, Tip, Track } from '../../background-studio/components/ui';
import { downloadBlob } from '../../background-studio/utils/download';
import { FRAME_RATES, deliveryWav, kitName, projectSlug, sfxName } from './deliver';
import { LEVELS, LUFS_TARGETS, itemCategory, itemName, loudness } from './render';
import { canPickFolder, forgetFolder, pickFolder, saveFiles } from './save';
import { zipFiles } from './zip';

const TAKES = [1, 3, 5].map(value => ({ value, label: value === 1 ? '1' : `${value}` }));

const describe = item =>
  (item.layers || [item])
    .map(layer => {
      const tune = Object.entries(layer.tune || {})
        .filter(([, value]) => typeof value === 'number')
        .map(([key, value]) => `${key}=${Number(value.toFixed(3))}`)
        .join(' ');
      return `${layer.id}${layer.offset ? `@${layer.offset}s` : ''}${layer.gain ? `(${layer.gain}dB)` : ''}${tune ? ` ${tune}` : ''}`;
    })
    .join(' + ');

// Every kit item × takes → WAVs + sfx-list.csv. Into the chosen folder, or one zip in Downloads.
export async function exportKit(project, kit, folder) {
  const files = [];
  const rows = ['file,name,category,seconds,lufs,recipe'];
  const takes = project.takes || 1;
  for (const [index, item] of kit.entries()) {
    for (let take = 0; take < takes; take += 1) {
      const { blob, buffer } = await deliveryWav(item, project, { take });
      const name = sfxName(project.name, item, index, 'wav', takes > 1 ? take : 0);
      files.push({ name, data: blob });
      const lufs = loudness(buffer);
      rows.push(
        [name, `"${itemName(item)}"`, itemCategory(item), buffer.duration.toFixed(3), lufs.toFixed(1), `"${describe(item)}"`].join(
          ','
        )
      );
    }
  }
  files.push({ name: 'sfx-list.csv', data: rows.join('\n') + '\n' });
  const where = await saveFiles(folder, files, {
    sub: `${projectSlug(project)}_sfx-kit`,
    fallback: async () => {
      downloadBlob(await zipFiles(files), kitName(project.name));
      return 'Downloads (zip)';
    }
  });
  return { count: files.length - 1, where };
}

export default function ProjectSection({ sound, project, onProject, folder, onFolder, kit, onAdd, onRemove }) {
  const [busy, setBusy] = useState(false);

  const run = async () => {
    setBusy(true);
    try {
      const { count, where } = await exportKit(project, kit, folder);
      toast.success(`${count} WAVs → ${where}`);
    } catch (problem) {
      toast.error(problem?.message || 'Kit export failed');
    } finally {
      setBusy(false);
    }
  };

  const choose = async () => {
    try {
      onFolder(await pickFolder());
    } catch (problem) {
      if (problem?.name !== 'AbortError') toast.error(problem?.message || 'Could not open that folder');
    }
  };

  return (
    <section className="customize-frame lab-section tx-project">
      <div className="customize-heading">
        <h2>Project</h2>
      </div>
      <div className="preview-options lab-options">
        <label className="tx-field">
          <span>Name</span>
          <input
            value={project.name}
            placeholder="e.g. CC-EP04"
            spellCheck={false}
            autoComplete="off"
            onChange={event => onProject({ name: event.target.value })}
          />
        </label>
        <p className="tx-filename" title="Export filename">
          {sfxName(project.name, sound)}
        </p>
        <div className="scrubber">
          <div className="scrubber-track bs-choice">
            <span className="bs-choice-label">Level</span>
            <Track label="Level" value={project.level} options={LEVELS} onChange={value => onProject({ level: value })} />
          </div>
        </div>
        {project.level === 'lufs' && (
          <div className="scrubber">
            <div className="scrubber-track bs-choice">
              <span className="bs-choice-label">Target</span>
              <Track
                label="LUFS target"
                value={project.lufs}
                options={LUFS_TARGETS.map(value => ({ value, label: `${value}` }))}
                onChange={value => onProject({ lufs: value })}
              />
            </div>
          </div>
        )}
        <div className="scrubber">
          <div className="scrubber-track bs-choice">
            <span className="bs-choice-label">FPS</span>
            <Track
              label="Frame rate"
              value={project.fps}
              options={FRAME_RATES.filter(rate => [23.976, 25, 29.97, 50].includes(rate.value))}
              onChange={value => onProject({ fps: value })}
            />
          </div>
        </div>
        <div className="tx-field tx-folder">
          <span>Save to</span>
          <strong title={folder ? 'Chosen folder' : 'Browser downloads'}>{folder ? folder.name : 'Downloads'}</strong>
          {folder ? (
            <button
              type="button"
              className="lab-icon-button"
              aria-label="Use Downloads again"
              onClick={() => forgetFolder().then(() => onFolder(null))}
            >
              <Icon icon={Cancel01Icon} size={13} />
            </button>
          ) : (
            canPickFolder() && (
              <button type="button" className="tx-chip" onClick={choose}>
                Choose…
              </button>
            )
          )}
        </div>
        <label className="tx-field" title="Where the cue WAVs will sit on disk, for the Final Cut XML">
          <span>FCP path</span>
          <input
            value={project.mediaPath}
            spellCheck={false}
            autoComplete="off"
            onChange={event => onProject({ mediaPath: event.target.value })}
          />
        </label>
      </div>

      <div className="customize-heading tx-kit-heading">
        <h2>Kit · {kit.length}</h2>
        <div className="customize-heading-actions">
          <Tip label="Add this sound, as tuned" hint="K">
            <button type="button" className="customize-heading-action lab-add" onClick={onAdd}>
              <Icon icon={PlusSignIcon} size={14} />
              <span>Add</span>
            </button>
          </Tip>
        </div>
      </div>
      {kit.length ? (
        <ol className="tx-kit">
          {kit.map((item, index) => (
            <li key={item.key}>
              <span className="tx-kit-name" title={sfxName(project.name, item, index)}>
                {String(index + 1).padStart(2, '0')} {itemName(item)}
                {!item.layers && Object.keys(item.tune || {}).length ? <em> · tuned</em> : null}
              </span>
              <span className="tx-kit-meta">{itemCategory(item)}</span>
              <button
                type="button"
                className="lab-icon-button"
                aria-label={`Remove ${itemName(item)}`}
                onClick={() => onRemove(item.key)}
              >
                <Icon icon={Cancel01Icon} size={13} />
              </button>
            </li>
          ))}
        </ol>
      ) : (
        <p className="snd-fx-empty">Build a kit for this edit: tune a sound, press K, repeat. Stacks and presets go in too.</p>
      )}
      <div className="scrubber tx-takes">
        <div className="scrubber-track bs-choice">
          <span className="bs-choice-label">Takes each</span>
          <Track label="Takes" value={project.takes || 1} options={TAKES} onChange={value => onProject({ takes: value })} />
        </div>
      </div>
      <button type="button" className="bs-export bs-wide-button tx-kit-export" onClick={run} disabled={busy || !kit.length}>
        {busy ? <span className="bs-spinner" /> : <Icon icon={Download04Icon} />}
        <span>{busy ? 'Rendering' : folder ? `Export kit → ${folder.name}` : 'Export kit (.zip)'}</span>
      </button>
      <p className="tx-note">
        48 kHz · 24-bit · stereo WAV, named for the project. Extra takes vary pitch and tone slightly so repeats don’t
        sound identical.
      </p>
    </section>
  );
}
