// Menu drawer: native <dialog> handles focus trapping and Escape.
(() => {
  const dlg = document.querySelector('[data-vx-menu]');
  const open = document.querySelector('[data-vx-menu-open]');
  if (!dlg || !open) return;
  open.addEventListener('click', () => { dlg.showModal(); open.setAttribute('aria-expanded', 'true'); });
  dlg.querySelector('[data-vx-menu-close]').addEventListener('click', () => dlg.close());
  dlg.addEventListener('close', () => { open.setAttribute('aria-expanded', 'false'); open.focus(); });
  dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
})();

// Product page: pick colour and size, show that colour's photo first, real stock left, sold-out sizes.
(() => {
  const root = document.querySelector('[data-vx-pdp]');
  if (!root) return;
  const data = JSON.parse(root.querySelector('[data-vx-json]').textContent);
  const ci = data.options.findIndex((o) => /colo/i.test(o.name));
  const si = data.options.findIndex((o) => /size/i.test(o.name));
  const fmt = (c) => '$' + (c / 100).toFixed(2);
  const $ = (s) => root.querySelector(s);
  const pick = (name) => (root.querySelector(`input[name="${name}"]:checked`) || {}).value;
  const figs = [...root.querySelectorAll('[data-vx-gallery] figure')];

  function update(fromColour) {
    const colour = ci > -1 ? pick('vx-colour') : null;
    let size = si > -1 ? pick('vx-size') : null;
    // grey out sizes that are gone in this colour
    root.querySelectorAll('[data-vx-size]').forEach((lab) => {
      const v = data.variants.find((x) => (ci < 0 || x.options[ci] === colour) && x.options[si] === lab.dataset.vxSize);
      lab.classList.toggle('is-out', !v || !v.available);
    });
    // when the colour changes, jump to the first size still in stock
    if (fromColour && si > -1) {
      const cur = data.variants.find((x) => x.options[ci] === colour && x.options[si] === size);
      if (!cur || !cur.available) {
        const first = data.variants.find((x) => x.options[ci] === colour && x.available);
        if (first) { size = first.options[si]; root.querySelector(`input[name="vx-size"][value="${CSS.escape(size)}"]`).checked = true; }
      }
    }
    const v = data.variants.find((x) => (ci < 0 || x.options[ci] === colour) && (si < 0 || x.options[si] === size));
    const buy = $('[data-vx-buy]'), stock = $('[data-vx-stock]');
    if (ci > -1) { $('[data-vx-colour-name]').textContent = colour; $('[data-vx-colour-title]').textContent = ' - ' + colour; }
    if (!v) { buy.disabled = true; buy.textContent = 'Unavailable'; stock.textContent = ''; return; }
    $('[data-vx-id]').value = v.id;
    $('[data-vx-price]').textContent = fmt(v.price);
    buy.disabled = !v.available;
    buy.textContent = v.available ? 'Add to bag' : 'Sold out';
    stock.classList.toggle('is-low', v.available && v.left !== null && v.left <= 3);
    stock.textContent = !v.available ? `Sold out in ${size}. Try another colour.` : (v.left !== null && v.left <= 3 ? `Only ${v.left} left in ${size}` : 'In stock');
    // only the chosen colour's photos (model shot + flat-lays); fall back to everything if none are tagged
    if (ci > -1 && figs.length) {
      const mine = figs.filter((f) => f.dataset.colour === colour);
      figs.forEach((f) => { f.hidden = mine.length > 0 && !mine.includes(f); });
    }
    // colour's photo first
    if (v.image && figs.length) {
      const base = (u) => (u || '').split('?')[0].replace(/_\d+x\d*(?=\.)/, '');
      const hit = figs.find((f) => base(f.dataset.src) === base(v.image));
      if (hit && hit !== hit.parentNode.firstElementChild) { hit.parentNode.prepend(hit); hit.parentNode.scrollLeft = 0; }
    }
    const url = new URL(location.href); url.searchParams.set('variant', v.id); history.replaceState(null, '', url);
  }
  root.querySelectorAll('input[name="vx-colour"]').forEach((i) => i.addEventListener('change', () => update(true)));
  root.querySelectorAll('input[name="vx-size"]').forEach((i) => i.addEventListener('change', () => update(false)));
  update(false);
})();

// Product page urgency line: real counts only.
(() => {
  const root = document.querySelector('[data-vx-pdp]');
  if (!root) return;
  const el = root.querySelector('[data-vx-urgent]');
  const data = JSON.parse(root.querySelector('[data-vx-json]').textContent);
  const ci = data.options.findIndex((o) => /colo/i.test(o.name));
  const show = () => {
    const colour = ci > -1 ? (root.querySelector('input[name="vx-colour"]:checked') || {}).value : null;
    const vs = data.variants.filter((v) => ci < 0 || v.options[ci] === colour);
    const left = vs.reduce((n, v) => n + (v.left > 0 ? v.left : 0), 0);
    const gone = vs.filter((v) => !v.available).length;
    let msg = '';
    if (left > 0 && left <= 8) msg = `Selling fast: only ${left} left in ${colour || 'stock'}`;
    else if (gone > 0 && left > 0) msg = `${gone} ${gone === 1 ? 'size has' : 'sizes have'} already sold out in ${colour || 'this style'}`;
    el.textContent = msg; el.hidden = !msg;
  };
  root.querySelectorAll('input[name="vx-colour"]').forEach((i) => i.addEventListener('change', show));
  show();
})();

// Email pop-up: once per visitor after a delay, halfway down the page, or on exit intent.
(() => {
  const dlg = document.querySelector('[data-vx-popup]');
  if (!dlg || typeof dlg.showModal !== 'function') return;
  const KEY = 'vx-popup-seen';
  const days = Number(dlg.dataset.days || 7);
  const store = {
    get() { try { return Number(localStorage.getItem(KEY) || 0); } catch (e) { return 0; } },
    set() { try { localStorage.setItem(KEY, String(Date.now())); } catch (e) { /* private mode */ } },
  };
  const open = () => { if (!dlg.open && !document.querySelector('dialog[open]')) { dlg.showModal(); store.set(); } };
  dlg.querySelectorAll('[data-vx-popup-close]').forEach((b) => b.addEventListener('click', () => dlg.close()));
  dlg.addEventListener('click', (e) => { if (e.target === dlg) dlg.close(); });
  if (dlg.querySelector('[data-vx-popup-state]') || /customer_posted=true|[?&]popup/.test(location.search)) { open(); return; }
  if (Date.now() - store.get() < days * 864e5) return;
  let armed = true;
  const fire = () => { if (!armed) return; armed = false; window.removeEventListener('scroll', onScroll); open(); };
  const onScroll = () => { if (window.scrollY > document.documentElement.scrollHeight * 0.4) fire(); };
  window.addEventListener('scroll', onScroll, { passive: true });
  setTimeout(fire, Number(dlg.dataset.delay || 6) * 1000);
  document.addEventListener('mouseout', (e) => { if (!e.relatedTarget && e.clientY <= 0) fire(); });
})();
