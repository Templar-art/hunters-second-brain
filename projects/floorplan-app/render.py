"""10x skin + A4 page for a CubiCasa plan (milestone 2).

The skin only changes presentation (fill, stroke, font, visibility) and adds <defs>; every geometry
attribute stays as CubiCasa drew it, and fp.checks() proves that. CubiCasa draws in centimetres
(a 2.8 m room is ~280 units wide), so floor textures and the scale bar are true to scale; the
scale is cross-checked against the printed room sizes before the bar is drawn.
"""
import base64
import io
import math
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
TEX = HERE / "assets" / "tex"
LOGOS = HERE / "assets" / "logos"
SVG = "http://www.w3.org/2000/svg"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

INK = "#1d2126"
MUTE = "#6c737b"
WALL = "#4b5157"
LINE = "#5d646b"

# room label keyword -> floor material (first match wins; checked against the 10x label)
MATERIALS = [
    ("tile", ("bath", "ens", "wc", "pdr", "powder", "l'dry", "laundry", "toilet", "shower", "mud")),
    ("carpet", ("bed", "w.i.c", "wic", "wir", "robe", "dressing", "nursery")),
    ("concrete", ("garage", "carport", "store", "storage", "basement", "shed", "workshop", "plant")),
    ("deck", ("deck", "balcony", "alfresco", "verandah", "veranda")),
    ("pavers", ("patio", "porch", "courtyard", "terrace", "yard", "pergola")),
    ("wood", ("living", "dining", "kitchen", "family", "sitting", "lounge", "hall", "foyer", "entry",
              "office", "study", "media", "rumpus", "landing", "breakfast", "nook", "reception",
              "waiting", "p'try", "pantry", "theatre", "games", "gym", "room", "bar", "void")),
]


def local(t):
    return t.rsplit("}", 1)[-1]


# ---------- transforms ----------

def parse_tf(s):
    m = np.eye(3)
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", s or ""):
        v = [float(x) for x in re.split(r"[\s,]+", args.strip()) if x]
        if name == "matrix":
            t = np.array([[v[0], v[2], v[4]], [v[1], v[3], v[5]], [0, 0, 1]])
        elif name == "translate":
            t = np.array([[1, 0, v[0]], [0, 1, v[1] if len(v) > 1 else 0], [0, 0, 1]])
        elif name == "scale":
            sy = v[1] if len(v) > 1 else v[0]
            t = np.array([[v[0], 0, 0], [0, sy, 0], [0, 0, 1]])
        elif name == "rotate":
            a = math.radians(v[0])
            t = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
            if len(v) == 3:
                t = parse_tf(f"translate({v[1]},{v[2]})") @ t @ parse_tf(f"translate({-v[1]},{-v[2]})")
        else:
            continue
        m = m @ t
    return m


def pts(poly):
    v = [float(x) for x in re.split(r"[\s,]+", poly.get("points", "").strip()) if x]
    return np.array(v).reshape(-1, 2) if len(v) >= 6 else None


def inside(p, P):
    x, y = p
    c = False
    j = len(P) - 1
    for i in range(len(P)):
        xi, yi = P[i]
        xj, yj = P[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi:
            c = not c
        j = i
    return c


def area(P):
    x, y = P[:, 0], P[:, 1]
    return abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))) / 2


# ---------- textures (real-world cm, generated, cached) ----------

def _png(arr):
    b = io.BytesIO()
    Image.fromarray(arr).save(b, "PNG", optimize=True)
    return base64.b64encode(b.getvalue()).decode()


def _noise(h, w, blur, seed):
    r = np.random.default_rng(seed).random((h, w))
    im = Image.fromarray((r * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))
    a = np.asarray(im, dtype=float) / 255
    return (a - a.mean()) / (a.std() + 1e-9)


def _tileable_noise(h, w, blur, seed):
    """Noise that wraps at the edges, so pattern tiles show no seams."""
    big = _noise(h * 3, w * 3, blur, seed)
    return big[h:2 * h, w:2 * w]


def tex_wood(seed=3):
    """Oak boards 18 cm wide, 1.8 m long, staggered; pattern 360 x 144 cm at 3 px/cm."""
    ppc, W, H, board, length = 3, 360, 144, 18, 180
    w, h = W * ppc, H * ppc
    rng = np.random.default_rng(seed)
    base = np.array([220, 204, 186], float)
    # long thin fibres: noise squashed along the board, then stretched back out
    fib = _tileable_noise(h, w // 40, 0.6, seed)
    fib = np.asarray(Image.fromarray(((fib - fib.min()) / np.ptp(fib) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), float) / 255 - .5
    fine = _tileable_noise(h, w, .5, seed + 1)
    img = np.zeros((h, w, 3))
    for r in range(H // board):
        y0, y1 = r * board * ppc, (r + 1) * board * ppc
        start = rng.integers(0, length) * ppc
        for seg in range(W // length):
            xa = (start + seg * length * ppc) % w
            xs = (np.arange(w) - xa) % w < length * ppc
            img[y0:y1, xs] = base * (1 + rng.normal(0, .014))
            img[y0:y1, int(xa):int(xa) + 1] *= .94  # end joint
        img[y0:y1] *= (1 + .045 * fib[y0:y1, :, None] + .010 * fine[y0:y1, :, None])
        img[y0:y0 + 1] *= .94  # long seam
    return np.clip(img, 0, 255).astype(np.uint8), W, H


def tex_carpet(seed=5):
    ppc, W = 3, 100
    n = _tileable_noise(W * ppc, W * ppc, .7, seed) * .022 + _tileable_noise(W * ppc, W * ppc, 6, seed + 9) * .012
    img = np.array([226, 221, 214], float) * (1 + n[..., None])
    return np.clip(img, 0, 255).astype(np.uint8), W, W


def tex_concrete(seed=7):
    ppc, W = 2, 200
    n = _tileable_noise(W * ppc, W * ppc, .6, seed) * .016 + _tileable_noise(W * ppc, W * ppc, 14, seed + 3) * .01
    img = np.array([223, 223, 220], float) * (1 + n[..., None])
    return np.clip(img, 0, 255).astype(np.uint8), W, W


def tex_deck(seed=11):
    """Hardwood decking boards 14 cm, 6 mm gaps."""
    ppc, W, H = 3, 280, 140
    w, h = W * ppc, H * ppc
    rng = np.random.default_rng(seed)
    img = np.zeros((h, w, 3))
    grain = _tileable_noise(h // 8, w, 1.0, seed)
    grain = np.asarray(Image.fromarray(((grain - grain.min()) / np.ptp(grain) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), float) / 255 - .5
    for c in range(W // 14):
        x0, x1 = c * 14 * ppc, (c + 1) * 14 * ppc
        img[:, x0:x1] = np.array([196, 176, 152]) * (1 + rng.normal(0, .04))
        img[:, x0:x1] *= (1 + .06 * grain[:, x0:x1, None])
        img[:, x1 - 2:x1] = [150, 136, 120]
    return np.clip(img, 0, 255).astype(np.uint8), W, H


def texture(kind):
    f = TEX / f"{kind}.png"
    if not f.exists():
        arr, W, H = {"wood": tex_wood, "carpet": tex_carpet, "concrete": tex_concrete, "deck": tex_deck}[kind]()
        Image.fromarray(arr).save(f, optimize=True)
    im = Image.open(f)
    scale = {"wood": 3, "carpet": 3, "concrete": 2, "deck": 3}[kind]
    return base64.b64encode(f.read_bytes()).decode(), im.width / scale, im.height / scale


def defs_xml():
    out = []
    for kind in ("wood", "carpet", "concrete", "deck"):
        b64, W, H = texture(kind)
        out.append(f'<pattern id="fp-{kind}" patternUnits="userSpaceOnUse" width="{W:g}" height="{H:g}">'
                   f'<image href="data:image/png;base64,{b64}" width="{W:g}" height="{H:g}" preserveAspectRatio="none"/></pattern>')
    # 60 cm porcelain tiles and 40 cm pavers: vector, crisp at any size
    out.append('<pattern id="fp-tile" patternUnits="userSpaceOnUse" width="60" height="60">'
               '<rect width="60" height="60" fill="#e8ebed"/><path d="M0 0.25H60M0.25 0V60" stroke="#d2d7db" stroke-width="0.5"/></pattern>')
    out.append('<pattern id="fp-pavers" patternUnits="userSpaceOnUse" width="80" height="40">'
               '<rect width="80" height="40" fill="#e4dfd6"/><path d="M0 0.4H80M0.4 0V20M40.4 20V40M0 20.4H80" stroke="#d3ccc0" stroke-width="0.8"/></pattern>')
    out.append('<filter id="fp-shadow" x="-5%" y="-5%" width="110%" height="110%">'
               '<feDropShadow dx="0" dy="1.6" stdDeviation="1.6" flood-color="#000" flood-opacity="0.22"/></filter>')
    return out


# ---------- skin ----------

FLOOR_TITLE = re.compile(r"^(basement|ground floor|upper floor|lower floor|\d+(st|nd|rd|th) floor|(first|second|third) floor)$", re.I)
LIGHT = {"#ffffff", "#e6f5ff"}


def rgbhex(h):
    h = (h or "").lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) if re.fullmatch(r"[0-9a-fA-F]{6}", h) else None


def light(h):
    c = rgbhex(h)
    return bool(c) and sum(c) / 3 > 190


def wet(h):  # CubiCasa tints wet areas blue (#e6f5ff new style, #d6e3e4 old style)
    c = rgbhex(h)
    return bool(c) and c[2] > c[0] + 8


def is_floor_layer(g):
    """Child groups that each hold one light-filled room polygon, first inside a storey group."""
    kids = [k for k in g if local(k.tag) == "g"]
    if not kids or len(kids) != len(list(g)):
        return False
    return all(light(k.get("fill")) and any(local(c.tag) == "polygon" for c in k) for k in kids)


def plan_groups(root):
    """One group per storey: the parent of each floor layer (its first child is the floors)."""
    tagged = [g for g in root.iter() if g.get("data-fp") == "storey"]
    if tagged:  # already skinned
        return tagged
    parent = {c: p for p in root.iter() for c in p}
    out = []
    for g in root.iter():
        if (local(g.tag) == "g" and is_floor_layer(g) and parent[g] not in out and list(parent[g])[0] is g
                and sum(1 for k in parent[g] if local(k.tag) == "g") >= 3):
            out.append(parent[g])
    return out


def big_group(root):
    return plan_groups(root)[0]


def chain_tf(root, target):
    """Cumulative transform from root down to (and including) target."""
    parent = {c: p for p in root.iter() for c in p}
    path, e = [], target
    while e is not None:
        path.append(e)
        e = parent.get(e)
    m = np.eye(3)
    for e in reversed(path):
        m = m @ parse_tf(e.get("transform"))
    return m


def material_for(label):
    low = label.lower()
    for mat, keys in MATERIALS:
        if any(k in low for k in keys):
            return mat
    return None


def hide(e):
    """display:none that beats CubiCasa's inline 'display: block'."""
    st = [x for x in (e.get("style") or "").split(";") if x.strip() and x.split(":")[0].strip() != "display"]
    e.set("style", ";".join(st + ["display:none"]))


def restyle(e, **attrs):
    """Change presentation only: drop inline style colours, set attributes."""
    st = e.get("style")
    if st:
        keep = [p for p in st.split(";") if p.strip() and p.split(":")[0].strip() not in
                ("fill", "stroke", "fill-opacity", "stroke-opacity", "stroke-width", "font-family", "font-size", "font-weight")]
        e.set("style", ";".join(keep))
    for k, v in attrs.items():
        e.set(k.replace("_", "-"), v)


def skin(root):
    """Apply the 10x look in place. Returns a report dict (rooms -> material, scale check)."""
    report = {"rooms": [], "unlabelled": 0, "scale": None, "storeys": 0, "floor_titles": []}
    scale_err = []
    for big in plan_groups(root):
        _skin_storey(root, big, report, scale_err)
        big.set("data-fp", "storey")
        report["storeys"] += 1
    if scale_err:
        report["scale"] = {"rooms_checked": len(scale_err), "worst_cm": round(float(max(scale_err)), 1),
                           "ok": bool(max(scale_err) <= 10)}
    # CubiCasa's own storey titles (multi-storey exports): restyle as ours
    for t in root.iter(f"{{{SVG}}}text"):
        txt = "".join(t.itertext()).strip()
        if FLOOR_TITLE.match(txt) and "display:none" not in (t.get("style") or "").replace(" ", ""):
            restyle(t, fill=MUTE, font_family="Poppins, Montserrat, sans-serif", font_weight="500",
                    font_size="26", letter_spacing="5")
            for e in [t, *t]:
                if e.text:
                    e.text = e.text.upper()
            report["floor_titles"].append(txt)
    for r in root.iter():
        if local(r.tag) == "rect" and r.get("fill") == "#ffffff":
            restyle(r, fill="none")
    defs = ET.fromstring(f'<defs xmlns="{SVG}">' + "".join(defs_xml()) + "</defs>")
    root.insert(0, defs)
    return report


def _skin_storey(root, big, report, scale_err):
    kids = list(big)
    inv_big = np.linalg.inv(chain_tf(root, big))

    # labels: centre point (in big's frame) + text
    labels = []
    label_texts = []
    for k in kids:
        ts = [t for t in k.iter() if local(t.tag) == "text"]
        if not ts or k.get("display") == "none":
            continue
        name = "".join(ts[0].itertext()).strip()
        if not name or "display:none" in (ts[0].get("style") or "").replace(" ", "") or FLOOR_TITLE.match(name):
            continue
        tparent = {c: p for p in k.iter() for c in p}
        m = inv_big @ chain_tf(root, tparent[ts[0]])
        labels.append((name, m[:2, 2]))
        label_texts.append((m, ts))
        # hide CubiCasa's corner triangles
        for g in k.iter():
            if local(g.tag) == "g" and any(local(c.tag) == "polygon" for c in g) and g.get("fill") == "#000000":
                hide(g)
        for i, t in enumerate(ts):
            s = "".join(t.itertext()).strip()
            restyle(t, fill=INK if i == 0 else "#4d545b", font_family="Poppins, Montserrat, sans-serif",
                    font_weight="500" if i == 0 else "400", font_size="23" if i == 0 else "20.5")
            dm = re.fullmatch(r"([\d.]+)m x ([\d.]+)m", s)
            if dm:  # the label group's own box is the room's width x height in units
                inner = [g for g in k if local(g.tag) == "g"]
                box = [p for p in k.iter() if local(p.tag) == "polygon"]
                if box:
                    xs = [parse_tf(g.get("transform"))[0, 2] for g in k.iter() if local(g.tag) == "g" and g.get("fill") == "#000000"]
                    ys = [parse_tf(g.get("transform"))[1, 2] for g in k.iter() if local(g.tag) == "g" and g.get("fill") == "#000000"]
                    if xs and ys:
                        w_units, h_units = max(xs) - min(xs), max(ys) - min(ys)
                        a, b = float(dm[1]) * 100, float(dm[2]) * 100
                        scale_err.append(min(abs(w_units - a) + abs(h_units - b), abs(w_units - b) + abs(h_units - a)) / 2)

    # floors: the first child of the plan holds the room polygons
    floor_layer = kids[0]
    polys = []
    for g in floor_layer:
        for p in g.iter():
            if local(p.tag) == "polygon":
                P = pts(p)
                if P is not None:
                    polys.append((g, p, P))
    for g, p, P in polys:
        hit = [n for n, c in labels if inside(c, P)]
        mat = material_for(hit[0]) if hit else None
        if not hit:
            report["unlabelled"] += 1
            mat = "tile" if wet(g.get("fill")) else "carpet" if area(P) < 40000 else "wood"
        report["rooms"].append({"label": hit[0] if hit else None, "material": mat, "m2": round(float(area(P)) / 1e4, 1)})
        restyle(g, fill=f"url(#fp-{mat})", stroke=f"url(#fp-{mat})", stroke_width="1")

    # fit labels: shrink a room's name + size until the wider line fits inside its floor polygon
    for m, ts in label_texts:
        c = m[:2, 2]
        room = [P for _, _, P in polys if inside(c, P)]
        if not room:
            continue
        P = min(room, key=area)
        w, h = P[:, 0].max() - P[:, 0].min(), P[:, 1].max() - P[:, 1].min()
        sx = math.hypot(m[0, 0], m[1, 0]) or 1
        avail = (h if abs(m[1, 0]) > abs(m[0, 0]) else w) * 0.86 / sx
        sizes = [23, 20.5]
        need = max(len("".join(t.itertext()).strip()) * sizes[min(i, 1)] * 0.56 for i, t in enumerate(ts))
        if need > avail:
            f = max(avail / need, 0.6)
            for i, t in enumerate(ts):
                t.set("font-size", f"{sizes[min(i, 1)] * f:.1f}")
            report["fitted"] = report.get("fitted", 0) + 1

    # everything else
    for k in kids[1:]:
        if any(local(t.tag) == "text" for t in k.iter()):
            continue
        direct = [c for c in k if local(c.tag) == "polygon"]
        is_wall = k.get("fill") == "#000000" or (direct and k.get("fill") in (None, "#000000") and
                                                  any(x.get("fill") == "#000000" for x in k.iter()) and not k.get("transform"))
        if is_wall:
            restyle(k, fill=WALL, stroke=WALL, filter="url(#fp-shadow)")
            for sub in k.iter():
                if sub is k:
                    continue
                if local(sub.tag) == "g" and sub.get("fill") == "#ffffff":  # windows + door openings
                    restyle(sub, fill="#ffffff", stroke=LINE, stroke_width="0.9")
                if local(sub.tag) == "g" and sub.get("fill") == "none":
                    restyle(sub, fill="none", stroke=LINE, stroke_width="0.9")
                if local(sub.tag) == "path":
                    restyle(sub, fill="none", stroke=LINE, stroke_width="0.9")
        else:  # fixtures: crisp white with a fine line
            restyle(k, stroke=LINE, stroke_width="0.9")
            for sub in k.iter():
                if sub.get("fill") == "#ffffff":
                    restyle(sub, fill="#ffffff")
                if sub.get("stroke") == "#000000":
                    restyle(sub, stroke=LINE)



def _visible(e):
    return "display:none" not in (e.get("style") or "").replace(" ", "")


def storey_titles(root):
    """[(text element, x, y)] for CubiCasa's visible storey titles, in root user space."""
    par = {c: p for p in root.iter() for c in p}
    out = []
    for t in root.iter(f"{{{SVG}}}text"):
        if FLOOR_TITLE.match("".join(t.itertext()).strip()) and _visible(t):
            m = chain_tf(root, par[t])
            out.append((t, m[0, 2], m[1, 2]))
    return out


def plan_bbox(root, groups=None, titles=None):
    """Bounding box of the given storeys' floors and walls (+ their titles), in root user space."""
    xs, ys, unit = [], [], None
    for big in groups or plan_groups(root):
        m = chain_tf(root, big)
        unit = unit or m[0, 0]
        par = {c: p for p in big.iter() for c in p}
        kids = list(big)
        for k in [kids[0]] + [k for k in kids[1:] if k.get("fill") == WALL]:
            for e in k.iter():
                if local(e.tag) != "polygon":
                    continue
                P = pts(e)
                if P is None:
                    continue
                em, q, chain = m, e, []
                while q is not big:
                    chain.append(q)
                    q = par[q]
                for c in reversed(chain):
                    em = em @ parse_tf(c.get("transform"))
                Hh = np.c_[P, np.ones(len(P))] @ em.T
                xs += list(Hh[:, 0])
                ys += list(Hh[:, 1])
    for _, tx, ty in (titles if titles is not None else storey_titles(root)):
        ys.append(ty + 8)
    return min(xs), min(ys), max(xs), max(ys), unit


STOREY_ORDER = ["BASEMENT", "LOWER FLOOR", "GROUND FLOOR", "FIRST FLOOR", "UPPER FLOOR", "SECOND FLOOR"]


def storey_pieces(root):
    """One (svg, bbox, title) per storey, each a full copy with the other storeys hidden, so storeys can
    be laid out side by side at one scale. Single-storey plans come back as one piece."""
    groups = plan_groups(root)
    titles = storey_titles(root)
    if len(groups) < 2:
        return [(root, plan_bbox(root), None)]
    info = []
    for gi, g in enumerate(groups):
        x0, y0, x1, y1, _ = plan_bbox(root, [g], [])
        own = [t for t in titles if x0 - 20 <= t[1] <= x1 + 20 and y1 - 5 <= t[2] <= y1 + 60]
        own = sorted(own, key=lambda t: t[2])[:1]
        info.append((gi, own))
    pieces = []
    src = ET.tostring(root, encoding="unicode")
    for gi, own in info:
        cp = ET.fromstring(src)
        cgroups = plan_groups(cp)
        ctitles = storey_titles(cp)
        keep_t = {round(t[2], 2) for t in own}
        for j, g in enumerate(cgroups):
            if j != gi:
                hide(g)
        mine = []
        for t, tx, ty in ctitles:
            if round(ty, 2) in keep_t:
                mine.append((t, tx, ty))
            else:
                hide(t)
        name = "".join(mine[0][0].itertext()).strip().upper() if mine else ""
        pieces.append((cp, plan_bbox(cp, [cgroups[gi]], mine), name))
    pieces.sort(key=lambda p: STOREY_ORDER.index(p[2]) if p[2] in STOREY_ORDER else 99)
    return pieces


# ---------- A4 page ----------

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


ICONS = {  # simple line icons, 48 x 32 box
    "bed": '<path d="M4 26V8M4 18h40v8M44 26V16a4 4 0 0 0-4-4H20v6M8 14h8a2 2 0 0 1 2 2v2H8z" fill="none" stroke="{c}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>',
    "bath": '<path d="M4 16h40v4a8 8 0 0 1-8 8H12a8 8 0 0 1-8-8zM10 16V7a3 3 0 0 1 6 0M13 28l-2 3M35 28l2 3" fill="none" stroke="{c}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>',
    "car": '<path d="M5 22v-5l4-7a3 3 0 0 1 2.6-1.6h24.8A3 3 0 0 1 39 10l4 7v5a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2zM5 17h38M10 24v3M38 24v3" fill="none" stroke="{c}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/><circle cx="12" cy="20" r="1.6" fill="{c}"/><circle cx="36" cy="20" r="1.6" fill="{c}"/>',
}

DISCLAIMER = ("ARTIST'S IMPRESSION ONLY. While every attempt has been made to ensure the accuracy of this floor plan's "
              "areas and measurements of doors, windows, rooms and all other items, are approximate and no responsibility "
              "is taken for any error, omission, or mis-statement. This plan is for illustrative purposes only and should "
              "only be used as such by any prospective purchaser.")


def img_data(path):
    p = Path(path)
    mime = "image/svg+xml" if p.suffix == ".svg" else "image/png" if p.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def wrap(text, width_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur]


def area_strip(job):
    a = job["areas"]
    internal = (a["gla"] or 0) + sum(v for k, v in a["excluded"].items() if a["assign"].get(k) == "internal")
    external = sum(v for k, v in a["excluded"].items() if a["assign"].get(k) == "external")
    fmt = lambda v: f"{v:,.0f}"
    parts = [f"Internal: {fmt(internal)}m²"]
    if external:
        parts.append(f"External: {fmt(external)}m²")
    parts.append(f"Total: {fmt(internal + external)}m²")
    if job.get("land_area"):
        parts.append(f"Land area: {fmt(float(job['land_area']))}m²")
    return "   |   ".join(parts)


def page(job, styled_svg_text, client=None):
    """Compose the A4 landscape page (2970 x 2100 units = 0.1 mm)."""
    root = ET.fromstring(styled_svg_text)
    vb = [float(v) for v in root.get("viewBox").split()]
    pieces = storey_pieces(root)
    unit = pieces[0][1][4]

    W, H, M = 2970, 2100, 90
    frame = (M, 235, W - M, 1785)
    site = job.get("site_plan")
    area_box = (frame[0] + 70, frame[1] + 80, (2000 if site else frame[2] - 70), frame[3] - 190)
    bw, bh = area_box[2] - area_box[0], area_box[3] - area_box[1]
    # one scale for every storey: storeys side by side in one row, or wrapped onto two rows, whichever
    # lets the plan print biggest; within a row the bottoms (titles) line up
    gap = 140
    ws = [b[2] - b[0] for _, b, _ in pieces]
    hs = [b[3] - b[1] for _, b, _ in pieces]
    n = len(pieces)
    best = None
    for cut in range(1, n + 1):
        rows = [r for r in (list(range(cut)), list(range(cut, n))) if r]
        widest = max(sum(ws[i] for i in r) for r in rows)
        tall = sum(max(hs[i] for i in r) for r in rows)
        gw = max(gap * (len(r) - 1) for r in rows)
        sc = min((bw - gw) / widest, (bh - gap * (len(rows) - 1)) / tall)
        if best is None or sc > best[0]:
            best = (sc, rows)
    s, rows = best
    cm = s * unit  # page units per centimetre of real world
    placed = []
    block_h = sum(max(hs[i] for i in r) for r in rows) * s + gap * (len(rows) - 1)
    ry = area_box[1] + (bh - block_h) / 2
    for r in rows:
        row_h = max(hs[i] for i in r) * s
        row_w = sum(ws[i] for i in r) * s + gap * (len(r) - 1)
        cx, base = area_box[0] + (bw - row_w) / 2, ry + row_h
        for i in r:
            pr, b, _ = pieces[i]
            px, py = cx - b[0] * s, base - b[3] * s
            pr.set("x", f"{vb[0]}")  # place at its own viewBox origin, so inner coords == outer coords
            pr.set("y", f"{vb[1]}")
            pr.set("width", f"{vb[2]}")
            pr.set("height", f"{vb[3]}")
            pr.attrib.pop("id", None)
            placed.append((px, py, ET.tostring(pr, encoding="unicode")))
            cx += ws[i] * s + gap
        ry += row_h + gap
    x0, y0, x1, y1 = pieces[0][1][:4]
    px, py = placed[0][0], placed[0][1]

    addr = job.get("address") or "Address"
    if "," in addr:
        street, suburb = addr.rsplit(",", 1)
        addr_svg = f'{esc(street.strip())}, <tspan font-weight="500">{esc(suburb.strip().upper())}</tspan>'
    else:
        addr_svg = esc(addr)
    c = job.get("counts", {})
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
             f'font-family="Poppins, Montserrat, sans-serif">')
    o.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    o.append(f'<text x="{M}" y="170" font-size="60" font-weight="300" fill="{INK}" letter-spacing="0.4">{addr_svg}</text>')

    # bed / bath / car + north, right aligned
    x = W - M
    north = job.get("north")
    if north is not None:
        x -= 70
        o.append(f'<g transform="translate({x + 35} 148) rotate({float(north):g})">'
                 f'<circle r="34" fill="none" stroke="{INK}" stroke-width="2.4"/>'
                 f'<path d="M0 -26 L11 12 L0 5 L-11 12 Z" fill="{INK}"/>'
                 f'<text y="30" font-size="15" font-weight="600" text-anchor="middle" fill="{INK}" transform="translate(0 -62)">N</text></g>')
        x -= 70
    for key, icon in (("cars", "car"), ("baths", "bath"), ("beds", "bed")):
        v = c.get(key)
        if v in (None, ""):
            continue
        x -= 56
        o.append(f'<g transform="translate({x - 8} 118) scale(1.3)">{ICONS[icon].format(c=INK)}</g>')
        val = f"{v:g}" if isinstance(v, (int, float)) else esc(v)
        o.append(f'<text x="{x - 18}" y="168" font-size="54" font-weight="300" text-anchor="end" fill="{INK}">{val}</text>')
        x -= 18 + 32 * len(val) + 60

    o.append(f'<rect x="{frame[0]}" y="{frame[1]}" width="{frame[2] - frame[0]}" height="{frame[3] - frame[1]}" '
             f'fill="none" stroke="#c7cdd2" stroke-width="2.4"/>')

    # the plan itself
    for qx, qy, svg_text in placed:
        o.append(f'<g transform="translate({qx:.2f} {qy:.2f}) scale({s:.6f})">{svg_text}</g>')

    # floor title + scale bar, under the plan
    ty = py + y1 * s + 70
    if not (job.get("skin") or {}).get("floor_titles"):
        o.append(f'<text x="{px + x0 * s:.1f}" y="{ty:.1f}" font-size="30" font-weight="500" letter-spacing="5" fill="{MUTE}">'
                 f'{esc((job.get("floor_title") or "GROUND FLOOR").upper())}</text>')
    if (job.get("scale") or {}).get("ok"):
        n = 5
        sx = frame[2] - 70 - n * 100 * cm
        o.append(f'<g transform="translate({sx:.1f} {frame[3] - 60:.1f})" fill="{MUTE}" font-size="18">')
        for i in range(n):
            o.append(f'<rect x="{i * 100 * cm:.1f}" y="0" width="{100 * cm:.1f}" height="7" fill="{INK if i % 2 == 0 else "#ffffff"}" stroke="{INK}" stroke-width="1.2"/>')
        for i in (0, n):
            o.append(f'<text x="{i * 100 * cm:.1f}" y="-10" text-anchor="middle">{i}{"m" if i == n else ""}</text>')
        o.append("</g>")

    # site plan (supplied image only; never generated)
    if site:
        sx0, sy0, sx1, sy1 = 2080, frame[1] + 80, frame[2] - 70, frame[3] - 420
        o.append(f'<image href="{img_data(site)}" x="{sx0}" y="{sy0}" width="{sx1 - sx0}" height="{sy1 - sy0}" preserveAspectRatio="xMidYMid meet"/>')
        o.append(f'<text x="{sx0}" y="{sy1 + 60}" font-size="30" font-weight="500" letter-spacing="5" fill="{MUTE}">SITE PLAN</text>')
        for i, item in enumerate(job.get("legend") or []):
            o.append(f'<text x="{sx0}" y="{sy1 + 130 + i * 46}" font-size="30" font-weight="300" fill="{INK}">'
                     f'<tspan font-weight="500">{i + 1}.</tspan>  {esc(item)}</text>')

    # area strip
    o.append(f'<text x="{W - M}" y="{frame[3] + 70}" font-size="38" font-weight="300" text-anchor="end" fill="{INK}">{esc(area_strip(job))}</text>')

    # footer: client block, disclaimer, 10x
    fy = 1915
    if client and client.get("logo"):
        o.append(f'<image href="{img_data(HERE / client["logo"])}" x="{M}" y="{fy - 20}" width="420" height="150" preserveAspectRatio="xMinYMid meet"/>')
    lx = M + 470
    for ag in (client or {}).get("agents_show", []):
        o.append(f'<text x="{lx}" y="{fy + 50}" font-size="40" font-weight="400" fill="{INK}">{esc(ag["name"])}</text>'
                 f'<text x="{lx}" y="{fy + 100}" font-size="40" font-weight="300" fill="{INK}">{esc(ag["phone"])}</text>')
        lx += 430
    for i, ln in enumerate(wrap(DISCLAIMER, 118)):
        o.append(f'<text x="1350" y="{fy + 18 + i * 27}" font-size="19" font-weight="300" fill="{MUTE}">{esc(ln)}</text>')
    o.append(f'<image href="{img_data(LOGOS / "10x-dark.svg")}" x="{W - M - 300}" y="{fy - 25}" width="300" height="142" preserveAspectRatio="xMaxYMid meet"/>')
    o.append("</svg>")
    return "\n".join(o)


def _chrome(cmd, out, timeout=90):
    """Headless Chrome sometimes lingers after writing; wait for the file to settle, then stop it."""
    import time
    out.unlink(missing_ok=True)
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    t0, last = time.time(), -1
    try:
        while time.time() - t0 < timeout:
            if p.poll() is not None and out.exists():
                return
            if out.exists():
                size = out.stat().st_size
                if size == last and size > 0:
                    return
                last = size
            time.sleep(0.7)
        raise RuntimeError(f"Chrome did not write {out.name}")
    finally:
        if p.poll() is None:
            p.terminate()
            try:
                p.wait(5)
            except subprocess.TimeoutExpired:
                p.kill()


def export(page_svg, out_base):
    """SVG -> PDF (A4, vector) and PNG (300 dpi) through headless Chrome."""
    out_base = Path(out_base)
    out_base.with_suffix(".svg").write_text(page_svg)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        pdf_html = td / "pdf.html"
        pdf_html.write_text('<!doctype html><meta charset="utf-8"><style>@page{size:297mm 210mm;margin:0}'
                            'html,body{margin:0}svg{width:297mm;height:210mm;display:block}</style>' + page_svg)
        png_html = td / "png.html"
        png_html.write_text('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;background:#fff}'
                            'svg{width:3508px;height:2480px;display:block}</style>' + page_svg)
        common = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
                  "--no-first-run", "--disable-extensions", f"--user-data-dir={td / 'prof'}"]
        _chrome(common + ["--no-pdf-header-footer", f"--print-to-pdf={out_base.with_suffix('.pdf')}", pdf_html.as_uri()],
                out_base.with_suffix(".pdf"))
        _chrome(common + ["--window-size=3508,2480", f"--screenshot={out_base.with_suffix('.png')}", png_html.as_uri()],
                out_base.with_suffix(".png"))
    return [out_base.with_suffix(x) for x in (".svg", ".pdf", ".png")]
