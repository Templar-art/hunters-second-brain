import { useState } from 'react';
import { Cancel01Icon, PlayIcon, PlusSignIcon } from '@hugeicons/core-free-icons';
import { toast } from 'sonner';
import { Icon, Tip } from '../../background-studio/components/ui';
import PreviewSlider from '../../../components/common/Preview/PreviewSlider';
import { SOUNDS_BY_ID } from '../sounds/catalog';
import { levelOf } from './deliver';
import { itemName, level, renderItem } from './render';

const signed = (value, unit) => `${value > 0 ? '+' : ''}${value}${unit}`;

export const stackItem = stack => ({
  layers: stack.map(({ id, tune, offset, gain }) => ({ id, tune, offset, gain }))
});

// Layer sounds into one designed hit: e.g. whoosh into impact with a sub underneath.
export default function StackSection({ stack, onStack, project, player, onAdd, onKit, onSave }) {
  const [busy, setBusy] = useState(false);
  const update = (key, patch) => onStack(stack.map(layer => (layer.key === key ? { ...layer, ...patch } : layer)));

  const audition = async () => {
    setBusy(true);
    try {
      const buffer = level(await renderItem(stackItem(stack)), levelOf(project)).buffer;
      await player.playBuffer(buffer, { exclusive: true });
    } catch (problem) {
      toast.error(problem?.message || 'Could not render the stack');
    } finally {
      setBusy(false);
    }
  };

  const named = () => ({ ...stackItem(stack), name: itemName(stackItem(stack)) });

  return (
    <section className="customize-frame lab-section tx-stack">
      <div className="customize-heading">
        <h2>Stack · {stack.length}</h2>
        <div className="customize-heading-actions">
          <Tip label="Layer this sound, as tuned" hint="S">
            <button type="button" className="customize-heading-action lab-add" onClick={onAdd}>
              <Icon icon={PlusSignIcon} size={14} />
              <span>Layer</span>
            </button>
          </Tip>
        </div>
      </div>
      {stack.length ? (
        <>
          {stack.map(layer => (
            <div className="snd-fx tx-layer" key={layer.key}>
              <div className="snd-fx-head">
                <h3>
                  {SOUNDS_BY_ID[layer.id]?.name}
                  {Object.keys(layer.tune || {}).length ? <em> · tuned</em> : null}
                </h3>
                <button
                  type="button"
                  className="customize-heading-action lab-heading-icon"
                  aria-label="Remove layer"
                  onClick={() => onStack(stack.filter(item => item.key !== layer.key))}
                >
                  <Icon icon={Cancel01Icon} size={14} />
                </button>
              </div>
              <div className="preview-options lab-options">
                <PreviewSlider
                  title="Offset"
                  min={-2}
                  max={12}
                  step={0.01}
                  value={layer.offset}
                  displayValue={value => signed(Number(value.toFixed(2)), ' s')}
                  onChange={value => update(layer.key, { offset: value })}
                />
                <PreviewSlider
                  title="Gain"
                  min={-24}
                  max={6}
                  step={0.5}
                  value={layer.gain}
                  displayValue={value => signed(value, ' dB')}
                  onChange={value => update(layer.key, { gain: value })}
                />
              </div>
            </div>
          ))}
          <div className="tx-row">
            <button type="button" className="bs-export tx-ghost" onClick={audition} disabled={busy}>
              {busy ? <span className="bs-spinner" /> : <Icon icon={PlayIcon} />}
              <span>Play</span>
            </button>
            <button type="button" className="bs-export tx-ghost" onClick={() => onKit(named())}>
              <span>To kit</span>
            </button>
            <button type="button" className="bs-export tx-ghost" onClick={() => onSave(named())}>
              <span>Save</span>
            </button>
            <button type="button" className="bs-export tx-ghost" onClick={() => onStack([])}>
              <span>Clear</span>
            </button>
          </div>
        </>
      ) : (
        <p className="snd-fx-empty">
          Press S to layer the current sound. Stack a whoosh, an impact and a sub, then nudge offsets so they hit
          together.
        </p>
      )}
    </section>
  );
}
