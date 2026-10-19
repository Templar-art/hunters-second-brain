import { useRef } from 'react';
import { Cancel01Icon, PlusSignIcon } from '@hugeicons/core-free-icons';
import { toast } from 'sonner';
import { Icon, Tip } from '../../background-studio/components/ui';
import { downloadBlob } from '../../background-studio/utils/download';

// House presets: named tuned sounds and stacks, reusable across jobs. JSON export/import keeps them portable.
export default function PresetsSection({ presets, onPresets, onSave, onLoad, onKit }) {
  const fileRef = useRef(null);

  const exportJson = () =>
    downloadBlob(
      new Blob([JSON.stringify({ version: 1, presets }, null, 2)], { type: 'application/json' }),
      'sound-lab-presets.json'
    );

  const importJson = async file => {
    try {
      const parsed = JSON.parse(await file.text());
      const incoming = (parsed.presets || []).filter(preset => preset?.name && preset?.item);
      const known = new Set(presets.map(preset => preset.name));
      onPresets([...presets, ...incoming.filter(preset => !known.has(preset.name))]);
      toast.success(`${incoming.length} presets read`);
    } catch {
      toast.error('That file is not a Sound Lab presets file');
    }
  };

  return (
    <section className="customize-frame lab-section tx-presets">
      <div className="customize-heading">
        <h2>Presets · {presets.length}</h2>
        <div className="customize-heading-actions">
          <Tip label="Save this sound, as tuned">
            <button type="button" className="customize-heading-action lab-add" onClick={onSave}>
              <Icon icon={PlusSignIcon} size={14} />
              <span>Save</span>
            </button>
          </Tip>
        </div>
      </div>
      {presets.length ? (
        <ol className="tx-kit">
          {presets.map(preset => (
            <li key={preset.key}>
              <button type="button" className="tx-cue-seek tx-kit-name" onClick={() => onLoad(preset)}>
                {preset.name}
                {preset.item.layers ? <em> · stack</em> : null}
              </button>
              <button type="button" className="tx-chip" onClick={() => onKit(preset)}>
                kit
              </button>
              <button
                type="button"
                className="lab-icon-button"
                aria-label={`Delete ${preset.name}`}
                onClick={() => onPresets(presets.filter(item => item.key !== preset.key))}
              >
                <Icon icon={Cancel01Icon} size={13} />
              </button>
            </li>
          ))}
        </ol>
      ) : (
        <p className="snd-fx-empty">Save tuned sounds and stacks you like, e.g. “10x whoosh soft”, to reuse on any job.</p>
      )}
      <div className="tx-row">
        <button type="button" className="bs-export tx-ghost" onClick={exportJson} disabled={!presets.length}>
          <span>Export JSON</span>
        </button>
        <button type="button" className="bs-export tx-ghost" onClick={() => fileRef.current?.click()}>
          <span>Import</span>
        </button>
        <input
          ref={fileRef}
          type="file"
          accept="application/json,.json"
          hidden
          onChange={event => {
            if (event.target.files?.[0]) importJson(event.target.files[0]);
            event.target.value = '';
          }}
        />
      </div>
    </section>
  );
}
