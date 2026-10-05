#!/usr/bin/env python3
"""Local preview of the vx storefront with the real stock, prices and photos (no Shopify needed).
Mirrors the markup of theme/sections/vx-*.liquid so the shared vx.css / vx.js can be checked in a browser.
Usage: python3 bebita/prototype/vx/build.py   -> writes bebita/prototype/vx/*.html
"""
import html, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BB = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, BB)
from stock import STOCK  # noqa: E402
from load_stock import PRICE, PHOTOS, handle, SIZE_ORDER, flats  # noqa: E402
FLAT = flats()

E = html.escape
CSS, JS = "../../theme/assets/vx.css", "../../theme/assets/vx.js"
img = lambda h, c: f"../../products/bebita-{h}-{handle(c)}.jpg"
money = lambda d: f"${d:.2f}"

products, vid = [], 1000
for name, line, role, cols in STOCK:
    h = handle(name); sizes = [s for s in SIZE_ORDER if any(s in v for v in cols.values())]
    refs = PHOTOS.get(name, {}); fb = refs.get("_") or next(iter(refs.values()), None)
    variants, images, seen = [], [], set()
    for c in cols:
        ref = refs.get(c, fb)
        if ref not in seen: seen.add(ref); images.append(img(h, c))
        for fp in FLAT.get((name, c), []): images.append('../../products/flat/' + os.path.basename(fp))
        for s in sizes:
            vid += 1; q = cols[c].get(s, 0)
            variants.append({"id": vid, "options": [c, s], "price": PRICE[name] * 100, "available": q > 0, "left": q,
                             "image": img(h, c) if ref else None})
    products.append(dict(name=name, handle=h, line=line, role=role, price=PRICE[name], colours=list(cols), sizes=sizes,
                         variants=variants, images=images, left=sum(sum(v.values()) for v in cols.values()),
                         sold=sum(1 for v in variants if not v["available"])))
by = {p["handle"]: p for p in products}

def head(title):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} – Bebita Collective</title><link rel="stylesheet" href="{CSS}"></head><body class="vx-body">
<div class="vx vx-announce"><a href="collection-all.html">Final stock: when it's gone, it's gone · Free shipping over $150</a></div>
<header class="vx vx-head">
  <div class="vx-head__left">
    <button class="vx-icon vx-hide-desk" type="button" aria-label="Menu" aria-controls="vx-menu" aria-expanded="false" data-vx-menu-open><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    <nav class="vx-head__nav" aria-label="Main"><ul role="list">{NAV}</ul></nav>
  </div>
  <a class="vx-logo" href="index.html" aria-label="Bebita home"><img class="vx-logo__img" src="../../assets/bebita-vx-logo.png" alt="Bebita"></a>
  <div class="vx-head__right">
    <a class="vx-icon" href="#" aria-label="Search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg></a>
    <a class="vx-icon" href="cart.html" aria-label="Bag, 1 item"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8h16l-1.5 12h-13z"/><path d="M8.5 8V6.5a3.5 3.5 0 0 1 7 0V8"/></svg><span class="vx-icon__count">1</span></a>
  </div>
</header>
<dialog class="vx vx-drawer" id="vx-menu" aria-label="Menu" data-vx-menu><div class="vx-drawer__top"><span class="vx-logo"><img class="vx-logo__img" src="../../assets/bebita-vx-logo.png" alt="Bebita"></span>
<button class="vx-icon" type="button" aria-label="Close menu" data-vx-menu-close><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5 5 19"/></svg></button></div>
<ul role="list">{NAV}</ul></dialog>
"""

MENU = [("Active", "collection-active.html"), ("Swim", "collection-swim.html"), ("Tops", "collection-tops.html"),
        ("Bottoms", "collection-bottoms.html"), ("Shop all", "collection-all.html")]
NAV = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in MENU)

FOOT = """<footer class="vx vx-foot"><div class="vx-foot__cols">
<div><h3>Shop</h3><ul role="list"><li><a href="collection-active.html">Active</a></li><li><a href="collection-swim.html">Swim</a></li><li><a href="collection-tops.html">Tops</a></li><li><a href="collection-bottoms.html">Bottoms</a></li></ul></div>
<div><h3>Help</h3><ul role="list"><li><a href="#">Shipping</a></li><li><a href="#">Returns &amp; exchanges</a></li><li><a href="#">Size guide</a></li><li><a href="#">Contact</a></li></ul></div>
<div><h3>About</h3><ul role="list"><li><a href="#">Our story</a></li><li><a href="#">FAQ</a></li></ul></div>
<div><h3>Follow</h3><ul role="list"><li><a href="https://www.instagram.com/bebitaactive/">Instagram · Active</a></li><li><a href="https://www.instagram.com/bebitaswim/">Instagram · Swim</a></li></ul></div>
<div class="vx-foot__news"><h3>Stay in the loop</h3><p>Subscribe for 10% off your first order, plus first word when sizes come back.</p>
<form class="vx-foot__form" onsubmit="return false"><label class="vx-sr" for="n">Email</label><input id="n" type="email" placeholder="Email address" required><button type="submit">Join</button></form></div>
</div><div class="vx-foot__base"><span>&copy; 2026 Bebita Collective</span><span>Sent from the Gold Coast</span></div></footer>"""

POP = """<dialog class="vx vx-pop" data-vx-popup data-delay="6" data-days="7" aria-labelledby="vx-pop-title"><div class="vx-pop__inner">
<figure class="vx-pop__media"><img src="../../assets/bebita-vx-popup.jpg" alt=""></figure>
<div class="vx-pop__body"><button type="button" class="vx-icon vx-pop__close" data-vx-popup-close aria-label="Close"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
<form class="vx-pop__form" onsubmit="this.hidden=true;this.nextElementSibling.hidden=false;this.nextElementSibling.querySelector('h2').focus();return false"><p class="vx-pop__kicker">Final stock</p><h2 id="vx-pop-title" class="vx-pop__title" tabindex="-1" autofocus>10% off your first order</h2>
<p class="vx-pop__text">Subscribe for 10% off your first order. Once this run is gone, it's gone, so grab your size first.</p>
<label class="vx-sr" for="vx-pop-email">Email</label><input class="vx-pop__input" id="vx-pop-email" type="email" placeholder="Email address" required>
<button class="vx-buy" type="submit">Get 10% off</button><button type="button" class="vx-pop__skip" data-vx-popup-close>No thanks, I'll pay full price</button>
<p class="vx-pop__fine">One use per customer. Unsubscribe any time.</p></form><div hidden><h2 class="vx-pop__title" tabindex="-1">You're in. Here's 10% off.</h2><p class="vx-pop__text">Use this code at checkout on your first order.</p><p class="vx-pop__code">BEBITA10</p><a class="vx-buy vx-pop__btn" href="collection-all.html">Shop now</a></div></div></div></dialog>"""

def page(title, body):
    return head(title).replace("{NAV}", NAV) + body + FOOT + POP + f'<script src="{JS}"></script></body></html>'

def card(p):
    alt = f'<img class="vx-card__alt" src="{p["images"][1]}" alt="" loading="lazy">' if len(p["images"]) > 1 else ""
    if p["left"] == 0: badge = '<span class="vx-badge vx-badge--sold">Sold out</span>'
    elif p["left"] <= 3: badge = f'<span class="vx-badge vx-badge--low">Only {p["left"]} left</span>'
    elif p["left"] <= 8: badge = '<span class="vx-badge vx-badge--low">Selling fast</span>'
    else: badge = ""
    sub = f'{len(p["colours"])} colours' if len(p["colours"]) > 1 else p["colours"][0]
    return f"""<a class="vx-card" href="product-{p['handle']}.html"><div class="vx-card__media"><img src="{p['images'][0]}" alt="{E(p['name'])}" loading="lazy">{alt}{badge}</div>
<div class="vx-card__meta"><h3 class="vx-card__title">{E(p['name'])}</h3><span class="vx-card__price">{money(p['price'])}</span><span class="vx-card__sub">{E(sub)}</span></div></a>"""

grid = lambda ps: '<ul class="vx-grid" role="list">' + "".join(f"<li>{card(p)}</li>" for p in ps) + "</ul>"
active = [p for p in products if p["line"] == "active"]; swim = [p for p in products if p["line"] == "swim"]
best = sorted(products, key=lambda p: -p["left"])

def tile(src, label, href): return f'<a class="vx-tile" href="{href}"><img src="../../assets/{src}" alt="" loading="lazy"><span>{label}</span></a>'

index = f"""<div class="vx vx-heroes vx-heroes--split">
<a class="vx-hero" href="collection-active.html"><img src="../../assets/bebita-vx-hero.jpg" alt="Shop Active"><div class="vx-hero__text"><h2 class="vx-hero__title">Shop Active</h2><p class="vx-hero__sub">The original run. Final stock.</p></div></a>
<a class="vx-hero" href="collection-swim.html"><img src="../../assets/bebita-vx-hero-swim.jpg" alt="Shop Swim"><div class="vx-hero__text"><h2 class="vx-hero__title">Shop Swim</h2><p class="vx-hero__sub">Bikinis, one pieces, sarongs</p></div></a></div>
<section class="vx"><div class="vx-sechead"><h2>Active</h2><a href="collection-active.html">View all</a></div>{grid(sorted(active, key=lambda p: -p['left'])[:8])}</section>
<div class="vx vx-tiles">{tile('bebita-vx-tile-tops.jpg','Shop tops','collection-tops.html')}{tile('bebita-vx-tile-bottoms.jpg','Shop bottoms','collection-bottoms.html')}</div>
<section class="vx"><div class="vx-sechead"><h2>Swim</h2><a href="collection-swim.html">View all</a></div>{grid(sorted(swim, key=lambda p: -p['left'])[:4])}</section>
<div class="vx vx-tiles">{tile('bebita-vx-tile-active.jpg','Shop active','collection-active.html')}{tile('bebita-vx-tile-swim.jpg','Shop swim','collection-swim.html')}</div>"""
open(os.path.join(HERE, "index.html"), "w").write(page("Home", index))

COLS = {"all": ("Shop all", products), "active": ("Active", active), "swim": ("Swim", swim),
        "tops": ("Tops", [p for p in products if p["role"] in ("top", "set")]), "bottoms": ("Bottoms", [p for p in products if p["role"] == "bottom"])}
chips = lambda cur: '<nav class="vx-chips" aria-label="Collections">' + "".join(
    f'<a href="collection-{k}.html"{" aria-current=\"page\"" if k == cur else ""}>{t}</a>' for k, (t, _) in COLS.items()) + "</nav>"
for k, (t, ps) in COLS.items():
    body = f'<section class="vx"><div class="vx-colhead"><h1>{t}</h1><p>{len(ps)} styles</p></div>{chips(k)}{grid(ps)}</section>'
    open(os.path.join(HERE, f"collection-{k}.html"), "w").write(page(t, body))

for p in products:
    first = next((v for v in p["variants"] if v["available"]), p["variants"][0])
    data = {"options": [{"name": "Colour", "values": p["colours"]}, {"name": "Size", "values": p["sizes"]}], "variants": p["variants"]}
    figs = "".join(f'<figure data-src="{u}"><img src="{u}" alt="{E(p["name"])}"></figure>' for u in p["images"])
    sw = ""
    for c in p["colours"]:
        avail = any(v["available"] for v in p["variants"] if v["options"][0] == c)
        u = next(v["image"] for v in p["variants"] if v["options"][0] == c)
        sw += f'<label class="vx-swatch{"" if avail else " is-out"}" title="{E(c)}{"" if avail else " (sold out)"}"><img src="{u}" alt=""><input type="radio" name="vx-colour" value="{E(c)}" {"checked" if c == first["options"][0] else ""} aria-label="{E(c)}{"" if avail else ", sold out"}"></label>'
    sz = "".join(f'<label class="vx-size" data-vx-size="{E(s)}"><input type="radio" name="vx-size" value="{E(s)}" {"checked" if s == first["options"][1] else ""}><span>{E(s)}</span></label>' for s in p["sizes"])
    rel = [q for q in best if q["line"] == p["line"] and q["handle"] != p["handle"] and q["role"] != p["role"]][:4]
    body = f"""<section class="vx vx-pdp" data-vx-pdp><script type="application/json" data-vx-json>{json.dumps(data)}</script>
<div class="vx-pdp__gallery" data-vx-gallery>{figs}</div>
<div class="vx-pdp__info"><div class="vx-pdp__row"><h1 class="vx-pdp__title">{E(p['name'])}<span data-vx-colour-title></span></h1><span class="vx-pdp__price" data-vx-price>{money(p['price'])}</span></div>
<form data-vx-form onsubmit="location.href='cart.html';return false"><input type="hidden" name="id" value="{first['id']}" data-vx-id>
<fieldset style="border:0;margin:0;padding:0"><legend class="vx-pdp__label">Colour: <span data-vx-colour-name></span></legend><div class="vx-swatches">{sw}</div></fieldset>
<fieldset style="border:0;margin:0;padding:0"><legend class="vx-pdp__label">Size</legend><div class="vx-sizes">{sz}</div></fieldset>
<p class="vx-stock" data-vx-stock aria-live="polite"></p><p class="vx-urgent" data-vx-urgent hidden></p>
<button class="vx-buy" type="submit" data-vx-buy>Add to bag</button></form>
<p class="vx-note">Free shipping over $150. Sent from the Gold Coast in 1–2 business days.</p>
<div class="vx-acc"><details open><summary>Details &amp; fit</summary><div class="vx-acc__body"><p>From the original Bebita {p['line'].title()} run. Once these are gone, they're gone.</p></div></details>
<details><summary>Size guide</summary><div class="vx-acc__body"><p>XS 6 · S 8 · M 10 · L 12 · XL 14 (AU sizes).</p></div></details>
<details><summary>Delivery &amp; returns</summary><div class="vx-acc__body"><p>$9.95 standard, free over $150, $14.95 express. Australia only.</p></div></details></div></div></section>
<section class="vx"><div class="vx-sechead"><h2>Complete the set</h2></div>{grid(rel)}</section>"""
    open(os.path.join(HERE, f"product-{p['handle']}.html"), "w").write(page(p["name"], body))

# cart preview: one pair of shorts in the bag, $105 short of free shipping
item = by["muse-scrunch-shorts"]; addons = [by[h] for h in ("sarong", "triangle-bikini-top", "ruched-swim-skirt", "signature-halter")]
adds = "".join(f"""<li class="vx-addon"><a class="vx-addon__img" href="product-{a['handle']}.html"><img src="{a['images'][0]}" alt="{E(a['name'])}"></a>
<p><span>{E(a['name'])}</span><span>{money(a['price'])}</span></p><form onsubmit="return false"><select aria-label="Option for {E(a['name'])}">{''.join(f'<option>{E(v["options"][0])} / {E(v["options"][1])}</option>' for v in a['variants'] if v['available'])}</select>
<button class="vx-buy" type="submit">Add</button></form></li>""" for a in addons)
cart = f"""<section class="vx vx-cart"><h1>Your bag</h1><ul class="vx-cart__lines" role="list"><li class="vx-line">
<a class="vx-line__img" href="product-muse-scrunch-shorts.html"><img src="{item['images'][0]}" alt="Muse Scrunch Shorts"></a>
<div><p class="vx-line__title"><a href="product-muse-scrunch-shorts.html">Muse Scrunch Shorts</a></p><p class="vx-line__opts">Red / M</p>
<div class="vx-qty"><a href="#" aria-label="One less">&minus;</a><span>1</span><a href="#" aria-label="One more">+</a></div><a class="vx-line__remove" href="#">Remove</a></div><span>$45.00</span></li></ul>
<div class="vx-addons"><h2>Add $105.00 for free shipping</h2><p>Easy add-ons to get you there.</p><ul role="list">{adds}</ul></div><aside class="vx-cart__sum"><p class="vx-cart__ship">$105.00 away from free shipping</p><div class="vx-bar" aria-hidden="true"><i style="width:30%"></i></div>
<p><span>Subtotal</span><span>$45.00</span></p><p class="vx-cart__ship">Shipping calculated at checkout</p><button class="vx-buy" type="button">Checkout</button></aside>
</section>"""
open(os.path.join(HERE, "cart.html"), "w").write(page("Bag", cart))
print("wrote", len(products), "product pages + index, collections, cart")
