// Bebita set picker: choose a top and a bottom (style, colour, size), then add both to the bag at once.
// Products arrive as JSON rendered by sections/bb-picker.liquid; nothing here is hardcoded to a catalogue.
(() => {
  const root = document.querySelector('[data-bb-picker]');
  if (!root || !root.querySelector('.bb-picker__slots')) return;

  const products = JSON.parse(root.querySelector('[data-bb-products]').textContent || '[]');
  const colourMap = Object.fromEntries(
    (JSON.parse(root.querySelector('[data-bb-colours]').textContent || '""') || '')
      .split(/\s*(?:\n|\\n)\s*/).map((l) => l.split(':').map((s) => s.trim())).filter((p) => p.length === 2 && p[1])
      .map(([name, hex]) => [name.toLowerCase(), hex])
  );
  const moneyFormat = root.dataset.moneyFormat || '${{amount}}';
  const money = (cents) => {
    const n = (cents / 100);
    return moneyFormat
      .replace(/\{\{\s*amount_no_decimals\s*\}\}/, Math.round(n).toLocaleString('en-AU'))
      .replace(/\{\{\s*amount\s*\}\}/, n.toLocaleString('en-AU', { minimumFractionDigits: 2, maximumFractionDigits: 2 }))
      .replace(/<[^>]*>/g, '');
  };
  const optIndex = (p, re) => p.options.findIndex((o) => re.test(o.name));
  const COLOUR = /colou?r/i, SIZE = /size/i;

  const state = { line: 'active', top: {}, bottom: {} };

  // Deep link from a product page: /?top=<handle>#picker or ?bottom=<handle>
  const params = new URLSearchParams(location.search);
  for (const slot of ['top', 'bottom']) {
    const p = products.find((x) => x.handle === params.get(slot));
    if (p) { state.line = p.line; state[slot].productId = p.id; }
  }

  const el = (tag, attrs = {}, text) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (text != null) n.textContent = text;
    return n;
  };

  function chipGroup(container, items, selected, onPick, render) {
    container.replaceChildren();
    container.setAttribute('role', 'radiogroup');
    items.forEach((item, i) => {
      const b = el('button', { type: 'button', role: 'radio', 'aria-checked': String(item.value === selected), tabindex: item.value === selected || (!selected && i === 0) ? '0' : '-1' });
      render(b, item);
      if (item.disabled) b.setAttribute('aria-disabled', 'true');
      b.addEventListener('click', () => { if (!item.disabled) onPick(item.value); });
      b.addEventListener('keydown', (e) => {
        const dir = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
        if (!dir) return;
        e.preventDefault();
        const bs = [...container.querySelectorAll('[role=radio]')];
        const next = bs[(bs.indexOf(b) + dir + bs.length) % bs.length];
        next.focus(); next.click();
      });
      container.append(b);
    });
  }

  function variantFor(p, colour, size) {
    const ci = optIndex(p, COLOUR), si = optIndex(p, SIZE);
    return p.variants.find((v) => (ci < 0 || v.options[ci] === colour) && (si < 0 || v.options[si] === size));
  }

  function renderSlot(slot) {
    const box = root.querySelector(`[data-bb-slot="${slot}"]`);
    const list = products.filter((p) => p.role === slot && p.line === state.line);
    const s = state[slot];
    const empty = box.querySelector('[data-bb-empty]');
    const controls = box.querySelector('.bb-slot__controls');
    const media = box.querySelector('[data-bb-slot-media]');
    let img = media.querySelector('img');
    if (!img) { img = el('img', { width: '720', height: '900', alt: '', decoding: 'async' }); img.hidden = true; media.append(img); }
    if (!list.length) {
      empty.hidden = false; controls.hidden = true; img.hidden = true; s.variant = null; return;
    }
    empty.hidden = true; controls.hidden = false;
    let p = list.find((x) => x.id === s.productId) || list[0];
    s.productId = p.id;
    const ci = optIndex(p, COLOUR), si = optIndex(p, SIZE);
    const colours = ci >= 0 ? p.options[ci].values : [];
    const sizes = si >= 0 ? p.options[si].values : [];
    if (!colours.includes(s.colour)) s.colour = colours.find((c) => p.variants.some((v) => v.options[ci] === c && v.available)) || colours[0];
    if (!sizes.includes(s.size)) s.size = undefined;

    chipGroup(box.querySelector('[data-bb-chips="style"]'), list.map((x) => ({ value: x.id, label: x.title })), p.id,
      (id) => { s.productId = id; s.colour = undefined; renderSlot(slot); renderBar(); }, (b, it) => { b.textContent = it.label; });
    box.querySelector('[data-bb-group="style"]').hidden = list.length < 2;

    chipGroup(box.querySelector('[data-bb-chips="colour"]'), colours.map((c) => ({
      value: c, disabled: !p.variants.some((v) => v.options[ci] === c && v.available),
    })), s.colour, (c) => { s.colour = c; renderSlot(slot); renderBar(); }, (b, it) => {
      const sw = el('span', { class: 'bb-swatch', 'aria-hidden': 'true' });
      const hex = colourMap[it.value.toLowerCase()];
      if (hex) sw.style.background = hex; else sw.classList.add('bb-swatch--none');
      b.append(sw, el('span', { class: 'visually-hidden' }, it.value + (it.disabled ? ', sold out' : '')));
      b.title = it.value;
    });
    box.querySelector('[data-bb-value="colour"]').textContent = s.colour || '';
    box.querySelector('[data-bb-group="colour"]').hidden = !colours.length;

    chipGroup(box.querySelector('[data-bb-chips="size"]'), sizes.map((z) => {
      const v = variantFor(p, s.colour, z);
      return { value: z, disabled: !v || !v.available };
    }), s.size, (z) => { s.size = z; renderSlot(slot); renderBar(); }, (b, it) => {
      b.textContent = it.value;
      if (it.disabled) b.append(el('span', { class: 'visually-hidden' }, ', sold out'));
    });
    box.querySelector('[data-bb-group="size"]').hidden = !sizes.length;

    const v = sizes.length ? (s.size ? variantFor(p, s.colour, s.size) : null) : variantFor(p, s.colour, undefined);
    s.variant = v && v.available ? v : null;
    s.product = p;
    const src = (v && v.image) || (variantFor(p, s.colour, sizes[0]) || {}).image || p.image;
    if (src) { img.src = src; img.alt = `${p.title}${s.colour ? ', ' + s.colour : ''}`; img.hidden = false; }
    const stock = box.querySelector('[data-bb-stock]');
    stock.textContent = v && !v.available ? 'Sold out in this size'
      : v && v.left !== null && v.left > 0 && v.left <= 5 ? `Only ${v.left} left in ${s.size || 'this colour'}` : '';
  }

  function renderBar() {
    const t = state.top, b = state.bottom;
    const summary = root.querySelector('[data-bb-summary]');
    const total = root.querySelector('[data-bb-total]');
    const add = root.querySelector('[data-bb-add]');
    const ready = t.variant && b.variant;
    if (ready) {
      summary.textContent = `${t.product.title}, ${t.colour || ''} ${t.size || ''} + ${b.product.title}, ${b.colour || ''} ${b.size || ''}`.replace(/\s+/g, ' ');
      total.textContent = money(t.variant.price + b.variant.price);
    } else {
      const need = [!t.variant && 'a top size', !b.variant && 'a bottom size'].filter(Boolean).join(' and ');
      summary.textContent = products.length ? `Choose ${need} to finish your set.` : root.querySelector('[data-bb-summary]').dataset.prompt || summary.textContent;
      total.textContent = '';
    }
    add.disabled = !ready;
  }

  function setLine(line) {
    state.line = line;
    root.querySelectorAll('[data-bb-pick-line]').forEach((b) => b.setAttribute('aria-checked', String(b.dataset.bbPickLine === line)));
    renderSlot('top'); renderSlot('bottom'); renderBar();
  }
  root.querySelectorAll('[data-bb-pick-line]').forEach((b) => b.addEventListener('click', () => setLine(b.dataset.bbPickLine)));

  root.querySelector('[data-bb-add]').addEventListener('click', async (e) => {
    const btn = e.currentTarget, err = root.querySelector('[data-bb-error]');
    err.hidden = true; btn.disabled = true; btn.setAttribute('aria-busy', 'true');
    const label = btn.textContent; btn.textContent = 'Adding your set…';
    try {
      const r = await fetch(root.dataset.cartAdd, {
        method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ items: [{ id: state.top.variant.id, quantity: 1 }, { id: state.bottom.variant.id, quantity: 1 }] }),
      });
      if (!r.ok) {
        const j = await r.json().catch(() => ({}));
        throw new Error(j.description || 'That set could not be added. One of the sizes may have just sold out.');
      }
      location.href = root.dataset.cartUrl;
    } catch (x) {
      err.textContent = x.message || 'Something went wrong adding your set. Please try again.';
      err.hidden = false; btn.disabled = false; btn.removeAttribute('aria-busy'); btn.textContent = label;
    }
  });

  root.querySelector('[data-bb-summary]').dataset.prompt = root.querySelector('[data-bb-summary]').textContent;
  setLine(state.line);
})();

// Mirrors: switch between the Active and Swim rows.
(() => {
  document.querySelectorAll('[data-bb-lines]').forEach((sec) => {
    const tabs = [...sec.querySelectorAll('[data-bb-line]')];
    if (!tabs.length) return;
    const show = (line, focus) => {
      tabs.forEach((t) => {
        const on = t.dataset.bbLine === line;
        t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1;
        if (on && focus) t.focus();
      });
      sec.querySelectorAll('[data-bb-row]').forEach((r) => { r.hidden = r.dataset.bbRow !== line; });
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => show(t.dataset.bbLine));
      t.addEventListener('keydown', (e) => {
        const dir = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
        if (dir) { e.preventDefault(); show(tabs[(i + dir + tabs.length) % tabs.length].dataset.bbLine, true); }
      });
    });
  });
})();
