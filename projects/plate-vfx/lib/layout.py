"""Auto-route birds through a shot.

Random search over flight params, scored by simulating each bird through the fitted
camera: time spent inside the safe area (16:9 full frame or the 9:16 centre crop),
entering from an edge (no popping in mid-frame), readable on-screen size, and spacing
from the birds already placed. Lessons baked in: diagonal fly-aways banked toward camera
(side-on crossers read as crosses), one close hero, the rest stepping back in depth.
"""
import math
import random
import numpy as np
import flight

SAFE = {"16:9": 1.0, "9:16": 9 / 16 * 9 / 16, "4:5": (4 / 5) * (9 / 16), "1:1": 9 / 16}


def safe_rect(w, h, aspect):
    frac = SAFE.get(aspect, 1.0)
    sw = w * frac
    return ((w - sw) / 2, 0, (w + sw) / 2, h)


def track_bird(b, cam, f_px, fps, w, h):
    n = len(cam["frames"])
    keys = flight.simulate(b, cam["frames"][0], f_px, fps, n)
    pts = []
    for k in keys:
        if abs(k["frame"] - round(k["frame"])) > 1e-6:
            continue
        i = int(round(k["frame"])) - 1
        pts.append(flight.project(k["pos"], cam["frames"][i], f_px, w, h))
    return pts


def score(b, pts, rect, f_px, placed, min_px):
    x0, y0, x1, y1 = rect
    n = len(pts)
    vis, sizes, pen = 0, [], 0.0
    for i, p in enumerate(pts):
        if p is None:
            continue
        x, y, z = p
        span_px = b["span"] * f_px / z
        sizes.append(span_px)
        m = span_px / 2
        if x0 + m < x < x1 - m and y0 + m < y < y1 - m:
            vis += 1
        for q in placed:
            if q[i] is None:
                continue
            d = math.hypot(x - q[i][0], y - q[i][1])
            if d < 1.4 * (span_px / 2 + b["span"] * f_px / q[i][2] / 2):
                pen += 1.0 / n
    if not sizes:
        return -9, {}
    first = pts[0]
    # must not pop in: at frame 1 either off-frame or already near an edge
    pop = 0.0
    if first is not None:
        fx, fy, _ = first
        edge = min(fx - x0, x1 - fx, fy - y0, y1 - fy)
        if edge > 0.18 * (x1 - x0):
            pop = 0.6
    small = max(0.0, (min_px - min(sizes)) / min_px) * 0.3
    s = vis / n - pen * 2 - pop - small
    return s, dict(visible=vis / n, min_px=min(sizes), max_px=max(sizes), overlap=pen)


def auto(cam, count=4, aspect="16:9", seed=1, direction=1, min_px=16, tries=2500, log=print):
    w, h = cam["width"], cam["height"]
    fps = cam["fps"][0] / cam["fps"][1]
    f_px = cam["lens_mm"] / 36 * w
    rect = safe_rect(w, h, aspect)
    rng = random.Random(seed)
    # depth bands: one hero, then stepping back
    bands = [(6.0, 9.0), (10.0, 14.0), (15.0, 20.0), (21.0, 30.0), (30.0, 42.0), (12.0, 26.0)]
    placed_pts, birds = [], []
    for i in range(count):
        lo, hi = bands[min(i, len(bands) - 1)]
        best = None
        for _ in range(tries):
            depth = math.exp(rng.uniform(math.log(lo), math.log(hi)))
            heading = rng.uniform(32, 55)
            bank = rng.uniform(8, 14)
            if direction < 0:
                heading, bank = 180 - heading, -bank
            b = dict(tag="hero" if i == 0 else f"b{i + 1}", depth=round(depth, 2),
                     sx=round(rng.uniform(-1.3, 0.4) * w / 2 * direction), sy=round(rng.uniform(-1.15, 0.2) * h / 2),
                     speed=round(rng.uniform(9.0, 11.0), 2), hz=round(rng.uniform(2.7, 3.3), 2),
                     phase=round(rng.random(), 2), heading=round(heading, 1), bank=round(bank, 1),
                     span=round(rng.uniform(0.9, 1.0), 2), glides=[])
            if rng.random() < 0.6:
                t_shot = (len(cam["frames"]) - 1) / fps
                a = rng.uniform(-0.2, t_shot * 0.8)
                b["glides"] = [[round(a, 2), round(a + rng.uniform(0.3, 0.8), 2)]] if a > 0.05 else [[0.0, round(rng.uniform(0.3, 0.6), 2)]]
            pts = track_bird(b, cam, f_px, fps, w, h)
            s, info = score(b, pts, rect, f_px, placed_pts, min_px)
            if best is None or s > best[0]:
                best = (s, b, pts, info)
        s, b, pts, info = best
        b["score"] = {k: round(v, 3) for k, v in info.items()}
        birds.append(b)
        placed_pts.append(pts)
        log(f"  {b['tag']}: depth {b['depth']}m, visible {info['visible']:.0%} of shot in {aspect} safe area, "
            f"{info['min_px']:.0f}-{info['max_px']:.0f}px span")
    return {"aspect": aspect, "seed": seed, "safe_rect": rect, "birds": birds}


def preview(layout, cam, plate_img, out_path):
    """Draw each bird's screen path + safe area over the first plate frame."""
    import cv2
    w, h = cam["width"], cam["height"]
    fps = cam["fps"][0] / cam["fps"][1]
    f_px = cam["lens_mm"] / 36 * w
    img = cv2.imread(plate_img)
    x0, y0, x1, y1 = [int(v) for v in layout["safe_rect"]]
    cv2.rectangle(img, (x0, y0), (x1 - 1, y1 - 1), (255, 255, 255), 2)
    cols = [(60, 60, 255), (60, 200, 255), (80, 255, 80), (255, 160, 60), (255, 80, 200), (200, 200, 200)]
    for j, b in enumerate(layout["birds"]):
        pts = [p for p in track_bird(b, cam, f_px, fps, w, h) if p is not None]
        for a, c in zip(pts[:-1], pts[1:]):
            cv2.line(img, (int(a[0]), int(a[1])), (int(c[0]), int(c[1])), cols[j % len(cols)], 3)
        if pts:
            cv2.circle(img, (int(pts[0][0]), int(pts[0][1])), 9, cols[j % len(cols)], -1)
            cv2.putText(img, b["tag"], (int(pts[-1][0]) + 8, int(pts[-1][1])), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cols[j % len(cols)], 2)
    cv2.imwrite(out_path, img)
