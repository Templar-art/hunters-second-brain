"""Relight prep: turn one plate frame into a lit-able 3D scene for Blender (blender/build_relight.py).

Geometry: Apple Depth Pro gives sharp relative depth but no usable metric scale from a drone. So the camera
solve's ground plane (z=0) is the truth for "where the ground is", and Depth Pro only supplies local relief:
an upper-envelope polynomial fit of log-depth finds the depth model's own ground, objects are whatever sits
in front of it, relief height = Cz * (1 - depth / ground_depth), cleaned by a low-percentile baseline.
Each pixel then becomes a vertex on its own camera ray at that height, so frame 1 reprojects exactly.

Masks (one RGB PNG, same UVs as the plate): R = water (glossy, reflects the HDRI in Cycles),
G = window emission (marks.json dusk.windows polygons; automatic detection was tried and rejected, see
`auto_windows`), B = pools (from marks.json dusk.pools).
"""
import json
import os

import cv2
import numpy as np
from scipy.ndimage import percentile_filter

import ground


def relief(depth, sky, Cz, s=4, deg=5):
    h, w = depth.shape
    ds = cv2.resize(depth, (w // s, h // s), interpolation=cv2.INTER_AREA)
    sk = cv2.resize(sky.astype(np.uint8), (w // s, h // s)) > 0
    yy, xx = np.mgrid[0:h // s, 0:w // s]
    X, Y = xx.ravel() / (w / s) - 0.5, yy.ravel() / (h / s) - 0.5
    B = np.stack([X ** i * Y ** j for i in range(deg + 1) for j in range(deg + 1 - i)], 1)
    L, m = np.log(ds).ravel(), ~sk.ravel()
    wts = np.ones(m.sum())
    for _ in range(12):  # objects are closer than the ground -> down-weight points below the surface
        sw = np.sqrt(wts)
        coef = np.linalg.lstsq(B[m] * sw[:, None], L[m] * sw, rcond=None)[0]
        r = L[m] - B[m] @ coef
        wts = np.where(r > -0.02, 1.0, np.exp(r / 0.02) * 0.05 + 1e-3)
    ratio = np.clip(ds / np.exp((B @ coef).reshape(h // s, w // s)), 0, 1.2)
    rel = Cz * (1 - ratio)
    base = cv2.GaussianBlur(percentile_filter(rel, 10, size=41), (0, 0), 6)
    rel = cv2.resize(np.clip(rel - base, 0, 40), (w, h), interpolation=cv2.INTER_LINEAR)
    return cv2.medianBlur(rel.astype(np.float32), 5)


def verts(height, M, f_px, w, h, step=2):
    """Vertex grid (h/step, w/step, 3): each pixel's ray, stopped at its relief height above z=0."""
    M = np.asarray(M)
    ys, xs = np.mgrid[0:h:step, 0:w:step].astype(np.float32)
    ys, xs = ys + step / 2 - 0.5, xs + step / 2 - 0.5
    rc = np.stack([xs, ys, np.ones_like(xs)], -1) @ ground.cam_A(f_px, w, h).T
    dw = rc @ M[:3, :3].T
    hh = cv2.resize(height, (w // step, h // step), interpolation=cv2.INTER_AREA)
    t = (hh - M[2, 3]) / dw[..., 2]
    return (M[:3, 3] + t[..., None] * dw).astype(np.float32), t > 0


def normals(V):
    dx = np.gradient(V, axis=1)
    dy = np.gradient(V, axis=0)
    n = np.cross(dy, dx)
    n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
    return n * np.sign(n[..., 2:3] + 1e-9)


def prep(job, frame=1, step=2, log=print):
    cam = json.load(open(os.path.join(job, "camera.json")))
    shot = json.load(open(os.path.join(job, "shot.json")))
    w, h = cam["width"], cam["height"]
    f_px = cam["lens_mm"] / 36 * w
    M = cam["frames"][frame - shot["range"][0]]
    rd = os.path.join(job, "relight")
    depth = np.load(os.path.join(rd, f"depth_{frame:04d}.npy"))
    rdm = lambda t: cv2.imread(os.path.join(job, "sky", f"{t}_{frame:04d}.png"), 0).astype(np.float32) / 255
    sky, water, build = rdm("prob") > 0.5, rdm("water"), rdm("build")
    height = relief(depth, sky, float(np.asarray(M)[2, 3]))
    V, ok = verts(height, M, f_px, w, h, step)
    keep = ok & (cv2.resize(sky.astype(np.uint8), (w // step, h // step), interpolation=cv2.INTER_NEAREST) == 0)
    n = normals(V)
    wall = np.clip((0.75 - n[..., 2]) / 0.45, 0, 1)  # 1 for vertical surfaces, 0 for roofs/ground
    wall = cv2.resize(wall, (w, h), interpolation=cv2.INTER_LINEAR)
    plate = cv2.imread(os.path.join(job, "frames", f"f_{frame:04d}.png"))
    lum = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    local = cv2.GaussianBlur(lum, (0, 0), 6)
    dark = np.clip((local - lum) / 0.12 + (0.45 - lum) / 0.35, 0, 1)  # glass reads darker than its wall in daylight
    auto = np.clip(build, 0, 1) * dark * wall  # kept for reference: lights shadowed walls + recesses, not glass
    mp = os.path.join(job, "marks.json")
    dm = json.load(open(mp)).get("dusk", {}) if os.path.exists(mp) else {}

    def raster(polys):
        buf = np.zeros((h, w), np.float32)
        for q in polys:
            cv2.fillPoly(buf, [np.round(np.asarray(q) * 4).astype(np.int32)], 1.0, cv2.LINE_AA, shift=2)
        return buf
    emit = cv2.GaussianBlur(raster(dm.get("windows", [])), (0, 0), 0.6)
    pools = raster(dm.get("pools", []))
    mask = np.dstack([pools, emit, np.clip(water, 0, 1)])  # BGR -> R water, G emit, B pools
    cv2.imwrite(os.path.join(rd, f"mask_{frame:04d}.png"), np.clip(mask * 255 + 0.5, 0, 255).astype(np.uint8))
    lamps = []
    if os.path.exists(mp):
        L = json.load(open(mp)).get("dusk", {}).get("lamps", [])
        if L:
            lamps = ground.to_ground(L, M, f_px, w, h).tolist()
    np.savez_compressed(os.path.join(rd, f"geo_{frame:04d}.npz"), V=V, keep=keep, step=step)
    json.dump({"camera": M, "lens_mm": cam["lens_mm"], "width": w, "height": h, "frame": frame,
               "plate": os.path.abspath(os.path.join(job, "frames", f"f_{frame:04d}.png")),
               "mask": os.path.abspath(os.path.join(rd, f"mask_{frame:04d}.png")),
               "geo": os.path.abspath(os.path.join(rd, f"geo_{frame:04d}.npz")), "lamps": lamps},
              open(os.path.join(rd, f"scene_{frame:04d}.json"), "w"), indent=1)
    log(f"relight prep: {int(keep.sum())} verts, emit px {int((emit > 0.3).sum())}, lamps {len(lamps)}")
    return height, auto
