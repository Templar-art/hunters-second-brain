import { useState } from 'react';
import { Cancel01Icon, Download04Icon, PlusSignIcon } from '@hugeicons/core-free-icons';
import { toast } from 'sonner';
import { Icon, Tip, Track } from '../../background-studio/components/ui';
import { downloadBlob } from '../../background-studio/utils/download';
import PreviewSwitch from '../../../components/common/Preview/PreviewSwitch';
import { SOUNDS_BY_ID } from '../sounds/catalog';
import { FRAME_RATES, deliveryWav, kitName, sfxName } from './deliver';
import { zipFiles } from './zip';

const describe = tune =>
  Object.entries(tune)
    .filter(([, value]) => typeof value === 'number')
    .map(([key, value]) => `${key}=${Number(value.toFixed(3))}`)
    .join(' ');

export async function exportKit(project, kit) {
  const files = [];
  const rows = ['file,sound,category,seconds,tune'];
  for (const [index, item] of kit.entries()) {
    const sound = SOUNDS_BY_ID[item.id];
    if (!sound) continue;
    const { blob, buffer } = await deliveryWav(sound, item.tune, { normalized: project.normalize });
    const name = sfxName(project.name, sound, index);
    files.push({ name, data: blob });
    rows.push([name, sound.name, sound.category, buffer.duration.toFixed(3), describe(item.tune)].join(','));
  }
  files.push({ name: 'sfx-list.csv', data: rows.join('\n') + '\n' });
  const zip = await zipFiles(files);
  downloadBlob(zip, kitName(project.name));
  return files.length - 1;
}

export default function ProjectSection({ sound, project, onProject, kit, onAdd, onRemove }) {
  const [busy, setBusy] = useState(false);

  const run = async () => {
    setBusy(true);
    try {
      const count = await exportKit(project, kit);
      toast.success(`${count} WAVs zipped`);
    } catch (problem) {
      toast.error(problem?.message || 'Kit export failed');
    } finally {
      setBusy(false);
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
        <PreviewSwitch
          title="Normalize −1 dBFS"
          isChecked={project.normalize}
          onChange={value => onProject({ normalize: value })}
        />
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
          {kit.map((item, index) => {
            const target = SOUNDS_BY_ID[item.id];
            if (!target) return null;
            return (
              <li key={item.key}>
                <span className="tx-kit-name" title={sfxName(project.name, target, index)}>
                  {String(index + 1).padStart(2, '0')} {target.name}
                  {Object.keys(item.tune).length ? <em> · tuned</em> : null}
                </span>
                <span className="tx-kit-meta">{target.category}</span>
                <button
                  type="button"
                  className="lab-icon-button"
                  aria-label={`Remove ${target.name}`}
                  onClick={() => onRemove(item.key)}
                >
                  <Icon icon={Cancel01Icon} size={13} />
                </button>
              </li>
            );
          })}
        </ol>
      ) : (
        <p className="snd-fx-empty">Build a kit for this edit: tune a sound, press K, repeat. Exports as one zip.</p>
      )}
      <button type="button" className="bs-export bs-wide-button tx-kit-export" onClick={run} disabled={busy || !kit.length}>
        {busy ? <span className="bs-spinner" /> : <Icon icon={Download04Icon} />}
        <span>{busy ? 'Rendering' : 'Export kit (.zip)'}</span>
      </button>
      <p className="tx-note">Every export is 48 kHz · 24-bit · stereo WAV, named for the project.</p>
    </section>
  );
}
