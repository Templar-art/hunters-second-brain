"""Plate analysis (cuts, sky colour, grain) and the compositor.

The compositor never touches a plate pixel the CG doesn't cover: out = plate*(1-a) + cg*a,
with plate-matched grain added only inside the CG alpha. verify() proves it.
"""
import cv2
import numpy as np


def find_cuts(paths, factor=8.0):
    """Indices i where frame i starts a new shot (mean abs diff >> median)."""
    prev, diffs = None, []
    for p in paths:
        g = cv2.resize(cv2.imread(p, 0), (480, 270)).astype(np.float32)
        diffs.append(0.0 if prev is None else float(np.abs(g - prev).mean()))
        prev = g
    med = float(np.median(diffs[1:])) if len(diffs) > 2 else 0.0
    return [i for i, d in enumerate(diffs) if i > 0 and d > max(factor * med, 12.0)], diffs


def usable_range(n, cuts):
    """Longest run of frames (1-based inclusive) without a cut."""
    bounds = [0] + cuts + [n]
    best = max(zip(bounds[:-1], bounds[1:]), key=lambda ab: ab[1] - ab[0])
    return best[0] + 1, best[1]


def sky_colour(img_bgr):
    """Median of the brightest 20% of the top 10% of rows, linearised. Returns RGB 0-1 linear."""
    h = img_bgr.shape[0]
    top = img_bgr[: max(4, h // 10)].reshape(-1, 3).astype(np.float32) / 255
    lum = top @ np.array([0.0722, 0.7152, 0.2126])
    sel = top[lum >= np.quantile(lum, 0.8)]
    srgb = np.median(sel, 0)[::-1]
    lin = np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)
    return [float(x) for x in lin]


def warmth(img_bgr):
    """Mean R/B ratio of mid-tones: >1 warm plate, <1 cool."""
    f = img_bgr.reshape(-1, 3).astype(np.float32)
    lum = f.mean(1)
    m = (lum > 60) & (lum < 200)
    return float(f[m, 2].mean() / max(1.0, f[m, 0].mean()))


def grain_sigma(paths):
    """Temporal-free grain estimate: high-pass std in the flattest 10% of 16px blocks, per channel (0-255)."""
    sig = []
    for p in paths[: min(6, len(paths))]:
        im = cv2.imread(p).astype(np.float32)
        hp = im - cv2.GaussianBlur(im, (0, 0), 1.2)
        g = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
        grad = cv2.blur(np.abs(cv2.Sobel(g, cv2.CV_32F, 1, 0)) + np.abs(cv2.Sobel(g, cv2.CV_32F, 0, 1)), (16, 16))
        m = grad <= np.quantile(grad, 0.10)
        sig.append([float(hp[..., c][m].std()) for c in range(3)])
    return np.median(np.array(sig), 0).tolist()  # BGR


def analyse(paths):
    first = cv2.imread(paths[0])
    return {"sky_linear_rgb": sky_colour(first), "warmth_rb": warmth(first), "grain_bgr": grain_sigma(paths)}


def composite(plate_path, cg_path, out_path, grain_bgr=None, soften=0.5, seed=0):
    plate = cv2.imread(plate_path).astype(np.float32)
    if cg_path is None:
        cv2.imwrite(out_path, plate.astype(np.uint8))
        return
    cg = cv2.imread(cg_path, cv2.IMREAD_UNCHANGED).astype(np.float32)
    if cg.shape[:2] != plate.shape[:2]:  # draft tier renders at reduced size
        cg = cv2.resize(cg, (plate.shape[1], plate.shape[0]), interpolation=cv2.INTER_LINEAR)
    if soften > 0:
        cg = cv2.GaussianBlur(cg, (0, 0), soften)
    a = cg[..., 3:4] / 255.0
    rgb = cg[..., :3]
    col = rgb  # Blender writes PNG with straight (unpremultiplied) alpha
    if grain_bgr is not None:
        rng = np.random.default_rng(seed)
        n = rng.standard_normal(col.shape[:2] + (1,)).astype(np.float32)  # luma-correlated grain
        col = col + n * np.array(grain_bgr, np.float32) * 0.9
    out = plate * (1 - a) + col * a
    out = np.where(a > 0, out, plate)  # bit-exact plate outside the CG
    cv2.imwrite(out_path, np.clip(out + 0.5, 0, 255).astype(np.uint8))


def verify(plate_paths, cg_paths, comp_paths, pad=7):
    """Max abs change outside the (dilated) CG alpha. Must be 0."""
    worst = 0
    k = np.ones((pad, pad), np.uint8)
    for p, c, o in zip(plate_paths, cg_paths, comp_paths):
        plate, comp = cv2.imread(p).astype(int), cv2.imread(o).astype(int)
        if c is None:
            worst = max(worst, int(np.abs(plate - comp).max()))
            continue
        a = cv2.imread(c, cv2.IMREAD_UNCHANGED)[..., 3]
        if a.shape != plate.shape[:2]:
            a = cv2.resize(a, (plate.shape[1], plate.shape[0]), interpolation=cv2.INTER_LINEAR)
        m = cv2.dilate((a > 0).astype(np.uint8), k) == 0
        worst = max(worst, int(np.abs(plate - comp)[m].max()))
    return worst
