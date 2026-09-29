// Bebita product page: keep price, stock, variant id, image and URL in step with the chosen options.
(() => {
  const root = document.querySelector('[data-bb-product]');
  if (!root) return;
  const p = JSON.parse(root.querySelector('[data-bb-product-json]').textContent);
  const map = Object.fromEntries((JSON.parse(root.querySelector('[data-bb-colours]').textContent || '""') || '')
    .split(/\n/).map((l) => l.split(':').map((s) => s.trim())).filter((x) => x.length === 2 && x[1]).map(([n, h]) => [n.toLowerCase(), h]));
  root.querySelectorAll('[data-bb-swatch]').forEach((s) => { const h = map[s.dataset.bbSwatch]; if (h) s.style.background = h; else s.classList.add('bb-swatch--none'); });
  const fmt = root.dataset.moneyFormat || '${{amount}}';
  const money = (c) => fmt.replace(/\{\{\s*amount\s*\}\}/, (c / 100).toLocaleString('en-AU', { minimumFractionDigits: 2 })).replace(/\{\{\s*amount_no_decimals\s*\}\}/, Math.round(c / 100)).replace(/<[^>]*>/g, '');
  const form = root.querySelector('[data-bb-form]');
  const sets = [...root.querySelectorAll('[data-bb-option]')];
  const update = () => {
    const chosen = sets.map((f) => (f.querySelector('input:checked') || {}).value);
    sets.forEach((f, i) => { f.querySelector('[data-bb-option-value]').textContent = chosen[i] || ''; });
    const v = p.variants.find((x) => x.options.every((o, i) => o === chosen[i]));
    const add = root.querySelector('[data-bb-add]'), stock = root.querySelector('[data-bb-stock]');
    // Mark sizes that are sold out in the chosen colour
    sets.forEach((f, i) => f.querySelectorAll('input').forEach((inp) => {
      const probe = chosen.slice(); probe[i] = inp.value;
      const pv = p.variants.find((x) => x.options.every((o, k) => o === probe[k]));
      inp.closest('.bb-chip').toggleAttribute('data-soldout', !pv || !pv.available);
    }));
    if (!v) { add.disabled = true; add.textContent = 'Unavailable'; stock.textContent = ''; return; }
    root.querySelector('[data-bb-variant-id]').value = v.id;
    root.querySelector('[data-bb-price]').textContent = money(v.price);
    add.disabled = !v.available; add.textContent = v.available ? 'Add to bag' : 'Sold out';
    stock.textContent = !v.available ? 'Sold out in this size' : (v.left !== null && v.left > 0 && v.left <= 5 ? `Only ${v.left} left` : '');
    const url = new URL(location.href); url.searchParams.set('variant', v.id); history.replaceState(null, '', url);
    if (v.image) { const lead = root.querySelector('.bb-product__shot--lead img'); if (lead) { lead.removeAttribute('srcset'); lead.src = v.image; } }
  };
  form.addEventListener('change', update);
  update();
})();
