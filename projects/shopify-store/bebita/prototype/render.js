// Local renderer: real Bebita theme sections + real product data -> static HTML pages for checking.
// node render.js  (writes ../site/{index,product,collection,cart-*}.html)
const fs = require('fs'), path = require('path');
const { Liquid, Tag, Hash } = require('liquidjs');
const VAULT = '/Users/10xhunter/Documents/Hunters Second Brain/projects/shopify-store/bebita';
const THEME = VAULT + '/theme', OUT = path.join(__dirname, '../site');
const raw = JSON.parse(fs.readFileSync(path.join(__dirname, '../products.json')));
const num = (gid) => Number(String(gid).split('/').pop());
const cents = (s) => Math.round(parseFloat(s) * 100);
const img = (url, alt) => url ? ({ src: url, alt: alt || '', width: 1200, height: 1500, toString() { return url; } }) : null;

const products = raw.map((p) => {
  const media = p.media.nodes.filter((m) => m.image).map((m) => ({ id: num(m.id), media_type: 'image', alt: m.alt, src: m.image.url, preview_image: img(m.image.url, m.alt), ...img(m.image.url, m.alt) }));
  const variants = p.variants.nodes.map((v) => {
    const opts = p.options.map((o) => (v.selectedOptions.find((s) => s.name === o.name) || {}).value);
    const vi = v.media.nodes[0] && v.media.nodes[0].image ? img(v.media.nodes[0].image.url) : null;
    return { id: num(v.id), title: v.title, price: cents(v.price), compare_at_price: v.compareAtPrice ? cents(v.compareAtPrice) : null,
      available: v.availableForSale, inventory_quantity: v.inventoryQuantity, inventory_management: 'shopify', inventory_policy: 'deny',
      options: opts, option1: opts[0], option2: opts[1], featured_image: vi, image: vi, featured_media: vi };
  });
  const first = variants.find((v) => v.available) || variants[0];
  const prices = variants.map((v) => v.price);
  return { id: num(p.id), handle: p.handle, title: p.title, url: '/products/' + p.handle, tags: p.tags, description: p.descriptionHtml,
    options: p.options.map((o) => o.name), available: variants.some((v) => v.available),
    options_with_values: p.options.map((o, i) => ({ name: o.name, position: i + 1, values: o.values, selected_value: first.options[i] })),
    variants, media, images: media, featured_image: media[0] ? img(media[0].src, media[0].alt) : null,
    price: Math.min(...prices), price_min: Math.min(...prices), price_max: Math.max(...prices), price_varies: new Set(prices).size > 1,
    selected_or_first_available_variant: first, first_available_variant: first, has_only_default_variant: false, metafields: {} };
});
const byTag = (t) => products.filter((p) => p.tags.includes(t));
const coll = (handle, title) => ({ handle, title, url: '/collections/' + handle, products: byTag(handle === 'tops' ? 'top' : handle === 'bottoms' ? 'bottom' : handle), description: '', get products_count() { return this.products.length; }, toString() { return handle; } });
const collections = { active: coll('active', 'Active'), swim: coll('swim', 'Swim'), tops: coll('tops', 'Tops'), bottoms: coll('bottoms', 'Bottoms') };
const linklists = { 'main-menu': { links: ['Active', 'Swim', 'Tops', 'Bottoms', 'About', 'FAQ', 'Contact'].map((t) => ({ title: t, url: '/' + t.toLowerCase() })) } };

const engine = new Liquid({ root: [THEME + '/sections', THEME + '/snippets'], extname: '.liquid', jsTruthy: false, ownPropertyOnly: false });
let lastSchema = null;
engine.registerTag('schema', class extends Tag { constructor(t, r, l) { super(t, r, l); this.body = ''; const s = l.parser.parseStream(r); while (r.length) { const x = r.shift(); if (x.name === 'endschema') break; this.body += x.getText(); } } render() { lastSchema = JSON.parse(this.body); return ''; } });
engine.registerTag('form', class extends Tag {
  constructor(t, r, l) { super(t, r, l); this.args = t.args; this.tpls = []; const s = l.parser.parseStream(r).on('tag:endform', () => s.stop()).on('template', (x) => this.tpls.push(x)).on('end', () => { throw new Error('form unclosed'); }); s.start(); }
  * render(ctx, emitter) {
    const type = this.args.split(',')[0].trim().replace(/['"]/g, '');
    const attrs = [...this.args.matchAll(/([\w-]+):\s*'([^']*)'/g)].map(([, k, v]) => ` ${k}="${v}"`).join('');
    const action = type === 'product' ? '/cart/add' : '/contact#contact_form';
    emitter.write(`<form method="post" action="${action}" ${attrs} accept-charset="UTF-8">`);
    ctx.push({ form: { posted_successfully: !!ctx.environments.__posted, errors: null } });
    yield this.liquid.renderer.renderTemplates(this.tpls, ctx, emitter); ctx.pop(); emitter.write('</form>');
  }
});
engine.registerTag('paginate', class extends Tag {
  constructor(t, r, l) { super(t, r, l); this.tpls = []; const s = l.parser.parseStream(r).on('tag:endpaginate', () => s.stop()).on('template', (x) => this.tpls.push(x)); s.start(); }
  * render(ctx, emitter) { ctx.push({ paginate: { pages: 1, current_page: 1, previous: null, next: null, parts: [] } }); yield this.liquid.renderer.renderTemplates(this.tpls, ctx, emitter); ctx.pop(); }
});
const money = (c) => '$' + (Number(c || 0) / 100).toFixed(2);
engine.registerFilter('money', money);
engine.registerFilter('image_url', (v, ...a) => { const u = v && (v.src || v.url || v); const kw = a.find((x) => Array.isArray(x) && x[0] === 'width'); const w = kw ? kw[1] : 800; return typeof u === 'string' ? u + (u.includes('?') ? '&' : '?') + 'width=' + (w || 800) : ''; });
engine.registerFilter('image_tag', (u, ...a) => { const o = {}; for (let i = 0; i < a.length; i++) if (Array.isArray(a[i])) o[a[i][0]] = a[i][1]; return `<img src="${u}" alt="${(o.alt || '').replace(/"/g, '&quot;')}" loading="${o.loading || 'lazy'}" width="1200" height="1500">`; });
engine.registerFilter('asset_url', (f) => 'file://' + THEME.replace(/ /g, '%20') + '/assets/' + f);
engine.registerFilter('stylesheet_tag', (u) => `<link rel="stylesheet" href="${u}">`);
engine.registerFilter('pluralize', (n, a, b) => (n == 1 ? a : b));
engine.registerFilter('json', (v) => JSON.stringify(v === undefined ? null : v));

function settingsFor(file, given) {
  engine.parseAndRenderSync(fs.readFileSync(`${THEME}/sections/${file}.liquid`, 'utf8').match(/{%-?\s*schema\s*-?%}[\s\S]*?{%-?\s*endschema\s*-?%}/)[0], {});
  const s = {};
  for (const d of (lastSchema.settings || [])) if ('default' in d) s[d.id] = d.default;
  Object.assign(s, given || {});
  for (const d of (lastSchema.settings || [])) {
    if (d.type === 'collection' && typeof s[d.id] === 'string') s[d.id] = collections[s[d.id]];
    if (d.type === 'image_picker' && typeof s[d.id] === 'string') { const f = s[d.id].replace('shopify://shop_images/', ''); s[d.id] = img('file://' + (VAULT + '/web/' + f).replace(/ /g, '%20')); }
    if (d.type === 'link_list' && typeof s[d.id] === 'string') s[d.id] = linklists[s[d.id]] || linklists['main-menu'];
  }
  return s;
}
function renderGroup(jsonFile, scope) {
  const j = JSON.parse(fs.readFileSync(jsonFile, 'utf8').replace(/^\s*\/\*[\s\S]*?\*\//, ''));
  return j.order.map((id) => { const sec = j.sections[id]; if (!sec.type.startsWith('bb-')) return `<!-- skipped ${sec.type} -->`;
    const blocks = Object.entries(sec.blocks || {}).map(([bid, b]) => ({ id: bid, type: b.type, settings: b.settings || {}, shopify_attributes: '' }));
    const order = sec.block_order ? sec.block_order.map((b) => blocks.find((x) => x.id === b)) : blocks;
    const section = { id, settings: settingsFor(sec.type, sec.settings), blocks: order };
    for (const b of order) for (const [k, v] of Object.entries(b.settings)) if (typeof v === 'string' && v.startsWith('shopify://shop_images/')) b.settings[k] = img('file://' + (VAULT + '/web/' + v.slice(22)).replace(/ /g, '%20'));
    return `<div class="shopify-section" id="shopify-section-${id}">` + engine.renderFileSync(sec.type, { ...scope, section }) + '</div>'; }).join('\n');
}
const BK = VAULT + '/theme-backup';
function page(name, tplName, tplJson, extra, posted) {
  const scope = { shop: { name: 'Bebita Collective', money_format: '${{amount}}' }, routes: { root_url: '/', cart_url: '/cart', cart_add_url: '/cart/add', cart_change_url: '/cart/change', all_products_collection_url: '/collections/all', collections_url: '/collections' },
    template: { name: tplName }, collections, linklists, cart: { item_count: 0, items: [], total_price: 0 }, settings: {}, __posted: posted, ...extra };
  engine.options.globals = scope;
  const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${name}</title><style>body{margin:0;background:#f6d7dd}</style></head><body>
${renderGroup(BK + '/header-group.v2.json', scope)}<main>${renderGroup(tplJson, scope)}</main>${renderGroup(BK + '/footer-group.v2.json', scope)}</body></html>`;
  fs.writeFileSync(path.join(OUT, name + '.html'), html);
}
function cartOf(list) {
  const items = list.map(([h, colour, size, q = 1]) => { const p = products.find((x) => x.handle === h); const v = p.variants.find((x) => x.options[0] === colour && x.options[1] === size);
    return { product: p, variant: v, image: v.featured_image || p.featured_image, url: p.url + '?variant=' + v.id, quantity: q, key: String(v.id), title: p.title,
      options_with_values: p.options.map((n, i) => ({ name: n, value: v.options[i] })), final_line_price: v.price * q, original_line_price: v.price * q, url_to_remove: '/cart/change?id=' + v.id + '&quantity=0' }; });
  return { items, item_count: items.reduce((a, b) => a + b.quantity, 0), total_price: items.reduce((a, b) => a + b.final_line_price, 0) };
}
fs.mkdirSync(OUT, { recursive: true });
page('index', 'index', BK + '/index.v2.json');
page('product', 'product', BK + '/product.v2.json', { product: products.find((p) => p.handle === 'seamless-sports-bra') });
page('product-swim', 'product', BK + '/product.v2.json', { product: products.find((p) => p.handle === 'triangle-bikini-top') });
page('collection', 'collection', BK + '/collection.v2.json', { collection: collections.active });
page('cart-top', 'cart', BK + '/cart.v2.json', { cart: cartOf([['seamless-sports-bra', 'Red', 'M']]) });
page('cart-set', 'cart', BK + '/cart.v2.json', { cart: cartOf([['seamless-sports-bra', 'Red', 'M'], ['seamless-scrunch-shorts', 'Red', 'S']]) });
page('cart-empty', 'cart', BK + '/cart.v2.json', {});
page('popup-done', 'index', BK + '/index.v2.json', {}, true);
console.log('rendered', fs.readdirSync(OUT));
