"""Review system for the 18 Maryland build: layout checks + render checks, one report.

  python3 review.py layout            -> qc/review_layout_<level>.png + review.json (furniture rules)
  python3 review.py renders <dir>     -> adds render checks for every PNG in <dir> (exposure, clipping, noise)
  python3 review.py html              -> qc/review.html (both, with thumbnails)

Layout rules (layout.json, written by interior.py):
  FACING   a piece with a target must point its front at it (<= 15 deg); seats/beds with only a direction must not
           face straight into a wall within 0.6 m.
  WALL     no footprint inside a wall (> 0.004 m2 at 2 cm raster).
  OVERLAP  no two pieces overlap, except chairs/stools tucked under their own table (<= 40 % of the chair).
  BACKED   pieces flagged wall=True (beds, TV units, desks, bedsides) have their back within 0.3 m of a wall.
  BEDSIDE  every bed has a bedside on both sides (standing rule: two bedsides always).
  DOORWAY  footprint over an opening's swing zone -> warning.
Render rules: clipped highlights > 2 % or crushed blacks > 12 % -> warning; mean luma outside 0.18-0.75 -> warning;
high-frequency noise score above threshold -> warning (more samples).
"""
import glob
import json
import math
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = 0.02                                        # raster metres per px
LAYOUT = os.path.join(HERE, "layout.json")
REPORT = os.path.join(HERE, "review.json")


def corners(p, shrink=0.0):
    (cx, cy), (fx, fy) = p["at"], p["front"]
    w, d = p["size"][0] / 2 - shrink, p["size"][1] / 2 - shrink
    sx, sy = -fy, fx                               # side axis (width); front axis (depth)
    return [(cx + sx * a + fx * b, cy + sy * a + fy * b) for a, b in ((-w, -d), (w, -d), (w, d), (-w, d))]


class Raster:
    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y1 = x0, y1; self.W = int((x1 - x0) / RES) + 1; self.H = int((y1 - y0) / RES) + 1

    def px(self, pts):
        return np.array([[(x - self.x0) / RES, (self.y1 - y) / RES] for x, y in pts], np.int32)

    def poly(self, pts):
        m = np.zeros((self.H, self.W), np.uint8); cv2.fillPoly(m, [self.px(pts)], 1); return m

    def rect(self, xa, ya, xb, yb):
        return self.poly([(xa, ya), (xb, ya), (xb, yb), (xa, yb)])


def ang(a, b):
    d = math.degrees(math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])); return abs(d)


def ray_hits_wall(R, wallmask, at, front, dist):
    for t in np.arange(0.05, dist, RES):
        x, y = at[0] + front[0] * t, at[1] + front[1] * t
        c, r = int((x - R.x0) / RES), int((R.y1 - y) / RES)
        if 0 <= r < R.H and 0 <= c < R.W and wallmask[r, c]:
            return t
    return None


def layout():
    L = json.load(open(LAYOUT)); issues = []; per_level = {}
    for level in ("ground", "upper"):
        P = [p for p in L["placed"] if p["level"] == level]
        W = [w[1:] for w in L["walls"] if w[0] == level]; O = [o[1:] for o in L["openings"] if o[0] == level]
        if not P:
            continue
        xs = [v for w in W for v in (w[0], w[2])] + [c[0] for p in P for c in corners(p)]
        ys = [v for w in W for v in (w[1], w[3])] + [c[1] for p in P for c in corners(p)]
        R = Raster(min(xs) - 2, min(ys) - 2, max(xs) + 2, max(ys) + 2)
        wm = np.zeros((R.H, R.W), np.uint8)
        for w in W:
            wm |= R.rect(*w)
        fp = {p["name"] + f"#{i}": (p, R.poly(corners(p, 0.02))) for i, p in enumerate(P)}

        def bad(p, rule, msg, sev="FAIL"):
            issues.append(dict(level=level, piece=p["name"], room=p["room"], rule=rule, severity=sev, detail=msg))

        for key, (p, m) in fp.items():
            if p["target"]:
                to = (p["target"][0] - p["at"][0], p["target"][1] - p["at"][1])
                a = ang(p["front"], to)
                if a > 15:
                    bad(p, "FACING", f"front is {a:.0f} deg off its target")
            elif p["kind"] in ("seat", "bed"):
                t = ray_hits_wall(R, wm, p["at"], p["front"], p["size"][1] / 2 + 0.6)
                if t:
                    bad(p, "FACING", f"faces a wall {t - p['size'][1] / 2:.2f} m in front")
            a = int((m & wm).sum()) * RES * RES
            if a > 0.004:
                bad(p, "WALL", f"{a:.3f} m2 inside a wall")
            if p["wall"]:
                back = (-p["front"][0], -p["front"][1])
                t = ray_hits_wall(R, wm, p["at"], back, p["size"][1] / 2 + 0.3)
                if not t:
                    bad(p, "BACKED", "back is not against a wall (> 0.3 m)")
            for o in O:
                xa, ya, xb, yb = o; horiz = (xb - xa) > (yb - ya)
                zone = (xa, ya - 0.7, xb, yb + 0.7) if horiz else (xa - 0.7, ya, xb + 0.7, yb)
                if (m & R.rect(*zone)).sum() * RES * RES > 0.05:
                    bad(p, "DOORWAY", "sits in an opening's clearance zone", "WARN"); break
        keys = list(fp)
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                (p, m), (q, n) = fp[keys[i]], fp[keys[j]]
                ov = int((m & n).sum())
                if not ov:
                    continue
                if p["z"] + p["size"][2] <= q["z"] + 0.01 or q["z"] + q["size"][2] <= p["z"] + 0.01:
                    continue                                   # stacked (TV above a cabinet), not touching
                kinds = {p["kind"], q["kind"]}
                small = min(m.sum(), n.sum())
                if kinds & {"seat", "stool"} and kinds & {"table", "fixture"} and ov / small <= 0.4:
                    continue
                if "hanging" in kinds:
                    continue
                bad(p, "OVERLAP", f"overlaps {q['name']} by {ov * RES * RES:.2f} m2")
        for p in P:
            if p["kind"] != "bed":
                continue
            sides = [q for q in P if q["kind"] == "bedside" and q["room"] == p["room"]]
            side_axis = (-p["front"][1], p["front"][0])
            s = {math.copysign(1, (q["at"][0] - p["at"][0]) * side_axis[0] + (q["at"][1] - p["at"][1]) * side_axis[1]) for q in sides}
            if s != {-1.0, 1.0}:
                bad(p, "BEDSIDE", f"bedsides on {len(s)} side(s), needs both")
        per_level[level] = draw(level, R, wm, O, P, issues)
    fails = [i for i in issues if i["severity"] == "FAIL"]
    rep = load(); rep["layout"] = dict(pieces=len(L["placed"]), fails=len(fails),
                                       warns=len(issues) - len(fails), issues=issues, images=per_level)
    json.dump(rep, open(REPORT, "w"), indent=1)
    print(f"LAYOUT {len(L['placed'])} pieces: {len(fails)} FAIL, {len(issues) - len(fails)} WARN")
    for i in issues:
        print(f"  {i['severity']:4} {i['rule']:8} {i['piece']:38} {i['detail']}")
    return len(fails)


def draw(level, R, wm, O, P, issues):
    img = np.full((R.H, R.W, 3), 255, np.uint8); img[wm > 0] = (60, 60, 60)
    for o in O:
        cv2.rectangle(img, tuple(R.px([(o[0], o[1])])[0]), tuple(R.px([(o[2], o[3])])[0]), (200, 230, 200), -1)
    badn = {i["piece"] for i in issues if i["level"] == level and i["severity"] == "FAIL"}
    warnn = {i["piece"] for i in issues if i["level"] == level}
    for p in P:
        c = (0, 0, 220) if p["name"] in badn else (0, 150, 255) if p["name"] in warnn else (180, 120, 40)
        cv2.polylines(img, [R.px(corners(p))], True, c, 2)
        a = R.px([p["at"]])[0]; b = R.px([(p["at"][0] + p["front"][0] * 0.6, p["at"][1] + p["front"][1] * 0.6)])[0]
        cv2.arrowedLine(img, tuple(a), tuple(b), c, 2, tipLength=0.35)
        if p["target"]:
            cv2.circle(img, tuple(R.px([p["target"]])[0]), 3, (0, 160, 0), -1)
    path = os.path.join(HERE, "qc", f"review_layout_{level}.png"); cv2.imwrite(path, img)
    return os.path.relpath(path, HERE)


def renders(d):
    rep = load(); out = rep.get("renders", {})
    for f in sorted(glob.glob(os.path.join(d, "*.png"))):
        im = cv2.imread(f); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
        clip = float((g > 0.985).mean()); crush = float((g < 0.02).mean()); mean = float(g.mean())
        hf = cv2.Laplacian(cv2.GaussianBlur(g, (0, 0), 0.6), cv2.CV_32F)
        flat = cv2.GaussianBlur(g, (0, 0), 4); flat_mask = np.abs(cv2.Laplacian(flat, cv2.CV_32F)) < 0.002
        noise = float(np.std(hf[flat_mask])) if flat_mask.any() else 0.0
        notes = []
        if clip > 0.02: notes.append(f"clipped {clip:.1%}")
        if crush > 0.12: notes.append(f"crushed {crush:.1%}")
        if not 0.18 <= mean <= 0.75: notes.append(f"mean luma {mean:.2f}")
        if noise > 0.02: notes.append(f"noise {noise:.3f}")
        out[os.path.relpath(f, HERE)] = dict(clip=round(clip, 4), crush=round(crush, 4), mean=round(mean, 3),
                                             noise=round(noise, 4), verdict="WARN" if notes else "PASS", notes=notes)
        print(f"  {out[os.path.relpath(f, HERE)]['verdict']:4} {os.path.basename(f):40} {', '.join(notes)}")
    rep["renders"] = out; json.dump(rep, open(REPORT, "w"), indent=1)


def load():
    return json.load(open(REPORT)) if os.path.exists(REPORT) else {}


def html():
    rep = load(); lay = rep.get("layout", {}); rows = []
    for i in lay.get("issues", []):
        rows.append(f"<tr class='{i['severity']}'><td>{i['severity']}</td><td>{i['rule']}</td><td>{i['room']}</td>"
                    f"<td>{i['piece']}</td><td>{i['detail']}</td></tr>")
    shots = "".join(f"<figure class='{v['verdict']}'><img src='{os.path.relpath(os.path.join(HERE, k), os.path.join(HERE, 'qc'))}'>"
                    f"<figcaption>{os.path.basename(k)} · {v['verdict']} {' · '.join(v['notes'])}</figcaption></figure>"
                    for k, v in rep.get("renders", {}).items())
    plans = "".join(f"<figure><img src='{os.path.basename(v)}'><figcaption>{k} plan: arrow = front, green dot = target, red = fail</figcaption></figure>"
                    for k, v in lay.get("images", {}).items())
    page = f"""<!doctype html><meta charset=utf-8><title>18 Maryland Review</title>
<style>body{{font:14px -apple-system,sans-serif;margin:24px;background:#f4f4f2;color:#222}}h1{{font-weight:600}}
table{{border-collapse:collapse;width:100%;background:#fff}}td{{padding:4px 8px;border-bottom:1px solid #ddd}}
tr.FAIL td:first-child{{color:#c00;font-weight:700}}tr.WARN td:first-child{{color:#c80}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:12px}}figure{{margin:0;background:#fff;padding:6px}}
figure img{{width:100%;display:block}}figure.WARN figcaption{{color:#c80}}figcaption{{font-size:12px;padding-top:4px}}</style>
<h1>18 Maryland · review</h1><p>Layout: {lay.get('pieces', 0)} pieces · <b>{lay.get('fails', 0)} fail</b> · {lay.get('warns', 0)} warn</p>
<table>{''.join(rows) or '<tr><td>No layout issues</td></tr>'}</table><h2>Plans</h2><div class=grid>{plans}</div>
<h2>Renders</h2><div class=grid>{shots}</div>"""
    open(os.path.join(HERE, "qc", "review.html"), "w").write(page); print("wrote qc/review.html")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "layout"
    if cmd == "layout":
        sys.exit(1 if layout() else 0)
    if cmd == "renders":
        renders(sys.argv[2])
    if cmd == "html":
        html()
