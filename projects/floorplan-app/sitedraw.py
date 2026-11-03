#!/usr/bin/env python3
"""Illustrated site plan drawn by code from measured data (no AI): the house is the CubiCasa plan's own
footprint, the lot is the QLD cadastre boundary, the aerial only decides placement and lawn vs paving.

    sitedraw.py <job slug> [--turn DEG] [--dx M] [--dy M]    # nudges if auto-placement is off

Needs sitegen.py to have run first (work/site-raw.png + job.json "site").
Writes work/site-drawn.png and job.json "site_drawn" {turn_deg, offset_px, score}.

Roof planes come from the footprint itself: each roof pixel slopes toward the nearest eave, so the
plane direction is the distance-transform gradient; quantising it gives hip roof planes, and the lines
between planes are the hips and ridges. That is how a hip roof on that footprint looks; the real roof
can differ (gables, skillions), which is why the result is labelled an illustration of the footprint.
"""
import argparse
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

import render as R

HERE = Path(__file__).resolve().parent
EAVE_CM = 60
ROOFED_OVERRIDE = set()  # covered areas a person has confirmed sit under the main tiled roof
OUTDOOR = ("yard", "patio", "deck", "balcony", "porch", "terrace", "courtyard", "alfresco", "verandah", "pergola")


def plan_rooms(root):
    """Floor polygons in plan units (cm) with the room label inside each."""
    big = R.big_group(root)
    kids = list(big)
    inv = np.linalg.inv(R.chain_tf(root, big))
    labels = []
    for k in kids:
        ts = [t for t in k.iter() if R.local(t.tag) == "text"]
        if not ts:
            continue
        name = "".join(ts[0].itertext()).strip()
        par = {c: p for p in k.iter() for c in p}
        m = inv @ R.chain_tf(root, par[ts[0]])
        labels.append((name, m[:2, 2]))
    rooms = []
    for p in kids[0].iter():
        if R.local(p.tag) != "polygon":
            continue
        P = R.pts(p)
        if P is None:
            continue
        m = inv @ R.chain_tf(root, p)
        Q = (np.c_[P, np.ones(len(P))] @ m.T)[:, :2]
        hit = [n for n, c in labels if R.inside(c, Q)]
        rooms.append((hit[0] if hit else "", Q))
    return rooms


def footprint_masks(rooms, cm_per_px, roofed_covered=()):
    """(roofed, covered-outdoor) masks of the house in its own frame, plus the frame origin."""
    allp = np.vstack([q for _, q in rooms])
    lo = allp.min(0) - 60
    hi = allp.max(0) + 60
    W, H = (np.ceil((hi - lo) / cm_per_px)).astype(int) + 1
    roof = np.zeros((H, W), np.uint8)
    cov = np.zeros((H, W), np.uint8)
    for name, q in rooms:
        pts = np.round((q - lo) / cm_per_px).astype(np.int32)
        low = name.lower()
        if any(k in low for k in OUTDOOR) and id(q) not in roofed_covered:
            if "covered" in low:
                cv2.fillPoly(cov, [pts], 255)
            continue
        cv2.fillPoly(roof, [pts], 255)
    # walls sit between room polygons: close the gaps (~ 30 cm) so the roof is one solid shape
    k = max(3, int(round(30 / cm_per_px)) | 1)
    roof = cv2.morphologyEx(roof, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (k, k)))
    # a roof spans straight over small wall steps (< 1.5 m) and overhangs the walls by ~ 0.6 m of eave
    big = max(3, int(round(150 / cm_per_px)) | 1)
    roof = cv2.morphologyEx(roof, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (big, big)))
    eave = max(3, int(round(2 * EAVE_CM / cm_per_px)) | 1)
    roof = cv2.dilate(roof, cv2.getStructuringElement(cv2.MORPH_RECT, (eave, eave)))
    cov = cv2.morphologyEx(cov, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (k, k)))
    cov[roof > 0] = 0
    return roof, cov


def rotate_mask(m, deg):
    h, w = m.shape
    c = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(c, deg, 1.0)
    cos, sin = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(h * sin + w * cos) + 2, int(h * cos + w * sin) + 2
    M[0, 2] += nw / 2 - c[0]
    M[1, 2] += nh / 2 - c[1]
    return cv2.warpAffine(m, M, (nw, nh), flags=cv2.INTER_NEAREST)


def roofiness(aerial):
    """Aerial pixels that look like roof: not vegetation, not deep shadow."""
    hsv = cv2.cvtColor(aerial, cv2.COLOR_RGB2HSV).astype(np.float32)
    rgb = aerial.astype(np.float32)
    green = (rgb[..., 1] > rgb[..., 0] + 4) & (rgb[..., 1] > rgb[..., 2])
    dark = hsv[..., 2] < 70
    return (~green & ~dark).astype(np.float32)


def place(roof, cov, aerial, lot_mask, base_turn, extra_turn=None):
    """Try the four square turns against the lot axis; slide each over the aerial; best overlap wins."""
    score_map = roofiness(aerial) * 2 - 1  # roof-like +1, else -1
    score_map[lot_mask == 0] = -3  # the house must sit inside its lot
    best = None
    turns = [base_turn + extra_turn] if extra_turn is not None else [base_turn + k * 90 for k in range(4)]
    for t in turns:
        r = rotate_mask(roof, t)
        c = rotate_mask(cov, t)
        tpl = (r > 0).astype(np.float32)  # place by the indoor footprint only; outdoor areas are judged after
        if tpl.shape[0] >= score_map.shape[0] or tpl.shape[1] >= score_map.shape[1]:
            continue
        res = cv2.matchTemplate(score_map, tpl, cv2.TM_CCORR)
        _, v, _, loc = cv2.minMaxLoc(res)
        v /= tpl.sum()
        if best is None or v > best[0]:
            best = (v, t, loc, r, c)
    return best


def largest_rect(m):
    """Largest all-True axis-aligned rectangle in a bool mask (histogram method): (x0, y0, x1, y1) inclusive-exclusive."""
    h, w = m.shape
    hist = np.zeros(w, np.int32)
    best = (0, None)
    for y in range(h):
        hist = np.where(m[y], hist + 1, 0)
        st = []
        for x in range(w + 1):
            cur = hist[x] if x < w else 0
            start = x
            while st and st[-1][1] >= cur:
                sx, sh = st.pop()
                if sh * (x - sx) > best[0]:
                    best = (sh * (x - sx), (sx, y - sh + 1, x, y + 1))
                start = sx
            st.append((start, cur))
    return best[1]


def grow(m, r):
    x0, y0, x1, y1 = r
    h, w = m.shape
    moved = True
    while moved:
        moved = False
        if y0 > 0 and m[y0 - 1, x0:x1].all(): y0 -= 1; moved = True
        if y1 < h and m[y1, x0:x1].all(): y1 += 1; moved = True
        if x0 > 0 and m[y0:y1, x0 - 1].all(): x0 -= 1; moved = True
        if x1 < w and m[y0:y1, x1].all(): x1 += 1; moved = True
    return x0, y0, x1, y1


def rect_cover(mask, min_px=200):
    m = mask > 0
    left = m.copy()
    rects = []
    while left.sum() > 0.01 * m.sum():
        r = largest_rect(left)
        if r is None or (r[2] - r[0]) * (r[3] - r[1]) < min_px:
            break
        r = grow(m, r)
        rects.append(r)
        left[r[1]:r[3], r[0]:r[2]] = False
    return rects


def hip_planes(roof, turn, at, shape):
    """Plane id + shade per pixel of the page-frame roof, from hip roofs on a rectangle cover of the house frame."""
    small = cv2.resize(roof, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    rects = [(x0 * 2, y0 * 2, x1 * 2, y1 * 2) for x0, y0, x1, y1 in rect_cover(small)]
    h, w = roof.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    height = np.full((h, w), -1.0, np.float32)
    pid = np.zeros((h, w), np.int32)
    shade = np.ones((h, w), np.float32)
    # side normals in the house frame (x right, y down) -> rotate by turn for lighting on the page
    t = math.radians(-turn)
    rot = np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])
    light = np.array([-0.6, -0.8])
    side_n = [np.array(v, float) for v in ((-1, 0), (1, 0), (0, -1), (0, 1))]
    for i, (x0, y0, x1, y1) in enumerate(rects):
        d = np.stack([xx - x0, x1 - xx, yy - y0, y1 - yy])  # distance to left/right/top/bottom eave
        inside = (d.min(0) >= 0)
        hgt = np.where(inside, d.min(0), -1)
        side = d.argmin(0)
        win = hgt > height
        height[win] = hgt[win]
        pid[win] = i * 4 + side[win] + 1
        for k in range(4):
            sel = win & (side == k)
            shade[sel] = 0.93 + 0.15 * float(np.dot(rot @ side_n[k], light))
    pid[roof == 0] = 0
    # into the page frame with the same turn + offset as the masks
    P = rotate_mask(pid.astype(np.float32), turn)
    S = rotate_mask(shade, turn)
    H, W = shape
    plane = np.zeros((H, W), np.int32)
    f = np.ones((H, W), np.float32)
    x0, y0 = at
    ph, pw = P.shape
    ys, xs = slice(max(0, y0), min(H, y0 + ph)), slice(max(0, x0), min(W, x0 + pw))
    plane[ys, xs] = P[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0].astype(np.int32)
    f[ys, xs] = S[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0]
    f[f == 0] = 1
    return plane, f


# ---------- drawing ----------

def tile_texture(h, w, s):
    """Terracotta tile courses: rows every ~ 0.33 m, staggered butt joints."""
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    row = 33 / s
    course = (y % row) < max(1.0, row * 0.12)
    joint = ((x + (np.floor(y / row) % 2) * row * 0.75) % (row * 1.5)) < max(1.0, row * 0.07)
    return course | joint


def draw(aerial, lot_px, roof, cov, at, s, roof_house, turn, roof_rgb=(205, 98, 64)):
    H, W = aerial.shape[:2]
    canvas = aerial.astype(np.float32)
    # context outside the lot: soft, desaturated, lighter (the lot is the subject)
    grey = canvas.mean(2, keepdims=True)
    ctx = (canvas * 0.4 + grey * 0.6) * 0.3 + 255 * 0.7
    lot = np.zeros((H, W), np.uint8)
    cv2.fillPoly(lot, [np.round(np.array(lot_px)).astype(np.int32)], 255)
    # inside the lot: lawn where the aerial is green, pale paving elsewhere
    rgb = aerial.astype(np.float32)
    veg = ((rgb[..., 1] > rgb[..., 0] + 4) & (rgb[..., 1] > rgb[..., 2])).astype(np.uint8) * 255
    veg = cv2.morphologyEx(veg, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    veg = cv2.GaussianBlur(veg, (0, 0), 2) > 110
    noise = cv2.GaussianBlur(np.random.default_rng(3).random((H, W)).astype(np.float32), (0, 0), 6)
    noise = (noise - noise.mean()) / (noise.std() + 1e-6)
    lawn = np.stack([150 + 8 * noise, 196 + 10 * noise, 104 + 6 * noise], -1)
    pave = np.full((H, W, 3), (226, 224, 219), np.float32)
    inside = np.where(veg[..., None], lawn, pave)
    out = np.where(lot[..., None] > 0, inside, ctx)
    # house: place masks
    x0, y0 = at
    full_roof = np.zeros((H, W), np.uint8)
    full_cov = np.zeros((H, W), np.uint8)
    h, w = roof.shape
    ys, xs = slice(max(0, y0), min(H, y0 + h)), slice(max(0, x0), min(W, x0 + w))
    full_roof[ys, xs] = roof[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0]
    full_cov[ys, xs] = cov[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0]
    # soft drop shadow (sun from the top left)
    sh = cv2.GaussianBlur(np.roll(np.roll((full_roof | full_cov).astype(np.float32) / 255, 6, 0), 6, 1), (0, 0), 4)
    out *= (1 - 0.35 * sh)[..., None]
    # flat covered roofs: light grey with slats
    full_cov[lot == 0] = 0
    cv_m = full_cov > 0
    slat = (np.mgrid[0:H, 0:W][1] % max(3, int(40 / s))) < 1
    out[cv_m] = np.where(slat[cv_m][:, None], (200, 202, 205), (236, 237, 239))
    # roof planes: the house mask (axis-aligned in its own frame) is covered by maximal rectangles; the
    # roof is the union of a hip roof on each, i.e. height = max over rectangles of distance to its eaves,
    # and each pixel's plane is the winning rectangle's nearest side. Straight hips, valleys and ridges.
    plane, f = hip_planes(roof_house, turn, at, (H, W))
    rm = full_roof > 0
    base = np.array(roof_rgb, np.float32)
    tex = tile_texture(H, W, s)
    col = base[None, None, :] * f[..., None]
    col = np.where(tex[..., None], col * 0.86, col)
    out[rm] = col[rm]
    # hips/ridges: boundaries between planes, and the eaves outline
    pid = plane.copy()
    pid[~rm] = -1
    edges = (np.diff(pid, axis=0, prepend=pid[:1]) != 0) | (np.diff(pid, axis=1, prepend=pid[:, :1]) != 0)
    ridge = edges & cv2.erode(full_roof, np.ones((3, 3), np.uint8)).astype(bool)
    out[ridge] = base * 0.62
    eave = cv2.morphologyEx(full_roof | full_cov, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
    out[eave] = (60, 48, 42)
    # lot line: thin dark fence line
    img = np.clip(out, 0, 255).astype(np.uint8)
    cv2.polylines(img, [np.round(np.array(lot_px)).astype(np.int32)], True, (70, 70, 64), 2, cv2.LINE_AA)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--turn", type=float)
    ap.add_argument("--dx", type=float, default=0)
    ap.add_argument("--dy", type=float, default=0)
    a = ap.parse_args()
    job = HERE / "jobs" / a.slug
    data = json.loads((job / "job.json").read_text())
    site = data["site"]
    aerial = np.asarray(Image.open(job / "work" / "site-raw.png").convert("RGB"))
    s = site["m_per_px"] * 100  # cm per px
    lot_px = site["lot_px"]
    H, W = aerial.shape[:2]
    lot_mask = np.zeros((H, W), np.uint8)
    cv2.fillPoly(lot_mask, [np.round(np.array(lot_px)).astype(np.int32)], 255)
    rooms = plan_rooms(ET.parse(job / "work" / "plan.svg").getroot())
    roof, cov = footprint_masks(rooms, s)
    # the lot's long side is vertical in the site image; houses sit square to their lot
    P = np.array(lot_px)
    edges = np.diff(np.vstack([P, P[:1]]), axis=0)
    longest = edges[np.argmax(np.hypot(*edges.T))]
    base = math.degrees(math.atan2(longest[1], longest[0])) - 90
    v, t, loc, r, c = place(roof, cov, aerial, lot_mask, base, a.turn - base if a.turn is not None else None)
    # each covered outdoor area: under the main tiled roof, or open/flat? the aerial decides, per area
    hsv = cv2.cvtColor(aerial, cv2.COLOR_RGB2HSV)
    allp = np.vstack([q for _, q in rooms])
    lo = allp.min(0) - 60
    tiled, shares = [], {}
    for name, q in rooms:
        if not any(k in name.lower() for k in OUTDOOR):
            continue
        m = np.zeros_like(roof)
        cv2.fillPoly(m, [np.round((q - lo) / s).astype(np.int32)], 255)
        ys, xs = np.nonzero(rotate_mask(m, t))
        ys, xs = ys + loc[1], xs + loc[0]
        ok = (ys >= 0) & (ys < H) & (xs >= 0) & (xs < W)
        tile = roofiness(aerial)[ys[ok], xs[ok]]
        flat = (hsv[ys[ok], xs[ok], 1] < 40) & (hsv[ys[ok], xs[ok], 2] > 170)
        share_tile = float((tile.astype(bool) & ~flat).mean()) if ok.any() else 0.0
        shares[name + f" @{len(shares)}"] = round(share_tile, 2)
        if name in ROOFED_OVERRIDE or share_tile > 0.6:  # tile in the aerial over most of it -> under the main roof
            tiled.append(id(q))
    covered_roof = shares
    flat_share = None
    if tiled:
        roof, cov = footprint_masks(rooms, s, set(tiled))
        v, t, loc, r, c = place(roof, cov, aerial, lot_mask, base, t - base)
    at = (int(loc[0] + a.dx * 100 / s), int(loc[1] + a.dy * 100 / s))
    img = draw(aerial, lot_px, r, c, at, s, roof, t)
    Image.fromarray(img).save(job / "work" / "site-drawn.png")
    data["site_drawn"] = {"turn_deg": round(t, 1), "offset_px": list(at), "score": round(float(v), 3), "covered_roof": covered_roof, 
                          "method": "CubiCasa footprint + QLD cadastre lot, auto-placed on the aerial; roof planes drawn as hips"}
    (job / "job.json").write_text(json.dumps(data, indent=1))
    print(job / "work" / "site-drawn.png", data["site_drawn"])


if __name__ == "__main__":
    main()
