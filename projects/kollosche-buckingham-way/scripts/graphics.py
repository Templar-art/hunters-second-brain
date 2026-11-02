"""Kollosche graphics for 4-6 Buckingham Way: tracked white lot outline on the
top-down, K badge pins on the View wide and the final pull-out. Writes RGBA
PNG sequences per shot into <shot>/render/gfx/ (frame-for-frame with the
shot's frames/). Assembled into full-length timeline overlays by assemble.py.

Tracking (plate-vfx solver fails on the top-down and pull-out: speed-ramp whips):
- topdown: chained SIFT homographies from the sharp last frame back to the
  first frame the outline draws (same method as kollosche-drone-graphics).
- view / pullout: bidirectional KLT on a roof patch, median motion.
Pin head = drone-pin's badge() + clients/kollosche.json, identical to the stills.

Usage: python3 -I scripts/graphics.py <job_dir>
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

job = Path(sys.argv[1]).resolve()
root = job.parents[1]
sys.path.insert(0, str(root / "projects/drone-pin"))
import drone_pin  # noqa: E402

W, H = 1920, 1080
ST = {**drone_pin.DEFAULT_STYLE,
      **json.loads((root / "projects/drone-pin/clients/kollosche.json").read_text())["style"]}
SIDE = round(ST["badge"] * H)
BADGE = drone_pin.badge(SIDE, drone_pin.k_glyph(), ST)
PIN_LINE = max(2, round(ST["pin_line"] * SIDE))


def frames(shot):
    return sorted((job / shot / "frames").glob("f_*.png"))


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def smooth(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def save(shot, k, rgba):
    d = job / shot / "render" / "gfx"
    d.mkdir(parents=True, exist_ok=True)
    rgba.save(d / f"g_{k + 1:04d}.png")


# --- top-down: lot outline ----------------------------------------------------
def topdown():
    fs = frames("topdown")
    n = len(fs)
    START, DRAW = 37, 14          # 0-based: draw-on once the whip has slowed
    # Hunter's own lot outline from his delivered top-down still (Drone Graphics/Web-02), carried to the
    # last frame by a SIFT homography (cadastre/lot_from_hunter_still.json; matches QLD lot 130RP206900).
    LOT = np.float32(json.loads((job / "cadastre/lot_from_hunter_still.json").read_text())["lot_f72"])
    sift = cv2.SIFT_create(nfeatures=6000)
    S = 0.5

    def feats(p):
        g = cv2.cvtColor(cv2.imread(str(p)), cv2.COLOR_BGR2GRAY)
        return sift.detectAndCompute(cv2.resize(g, None, fx=S, fy=S, interpolation=cv2.INTER_AREA), None)

    bf = cv2.BFMatcher()
    Hs = {n - 1: np.eye(3)}
    kb, db = feats(fs[-1])
    for k in range(n - 2, START - 1, -1):
        ka, da = feats(fs[k])
        good = [m for m, m2 in bf.knnMatch(db, da, k=2) if m.distance < 0.75 * m2.distance]
        src = np.float32([kb[m.queryIdx].pt for m in good]) / S
        dst = np.float32([ka[m.trainIdx].pt for m in good]) / S
        Hk, inl = cv2.findHomography(src, dst, cv2.RANSAC, 3.0)
        err = np.linalg.norm(cv2.perspectiveTransform(src[None], Hk)[0] - dst, axis=1)[inl.ravel() == 1]
        print("topdown f%02d  inliers %4d  median %.2f px" % (k + 1, inl.sum(), np.median(err)))
        Hs[k] = Hk @ Hs[k + 1]
        Hs[k] /= Hs[k][2, 2]
        kb, db = ka, da
    LW, SS = max(2, round(W * 0.0033)), 2   # outline_w from the Kollosche style

    def partial(poly, frac):
        pts = np.vstack([poly, poly[:1]])
        seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
        target, out = seg.sum() * frac, [pts[0]]
        for a, b, L in zip(pts[:-1], pts[1:], seg):
            if target >= L:
                out.append(b)
                target -= L
            else:
                out.append(a + (b - a) * target / L)
                break
        return np.array(out)

    for k in range(n):
        canvas = np.zeros((H * SS, W * SS), np.uint8)
        frac = smooth((k - START) / DRAW)
        if k >= START and frac > 0:
            poly = cv2.perspectiveTransform(LOT[None], Hs[k])[0]
            path = partial(poly, frac) * SS
            cv2.polylines(canvas, [np.round(path * 16).astype(np.int32)], frac >= 1, 255, LW * SS, cv2.LINE_AA, shift=4)
            for x, y in path:
                cv2.circle(canvas, (int(round(x * 16)), int(round(y * 16))), LW * SS // 2 * 16, 255, -1, cv2.LINE_AA, shift=4)
        a = cv2.resize(canvas, (W, H), interpolation=cv2.INTER_AREA)
        im = Image.new("RGBA", (W, H), (255, 255, 255, 0))
        im.putalpha(Image.fromarray(a))
        save("topdown", k, im)


# --- pins -------------------------------------------------------------------------
def klt(fs, tip, last):
    grey = [cv2.cvtColor(cv2.imread(str(f)), cv2.COLOR_BGR2GRAY) for f in fs[:last + 1]]
    mask = cv2.circle(np.zeros_like(grey[0]), tuple(int(c) for c in tip), 45, 255, -1)
    p = cv2.goodFeaturesToTrack(grey[0], 200, 0.01, 4, mask=mask)
    lk = dict(winSize=(31, 31), maxLevel=4, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 40, 0.01))
    tips = [np.float32(tip)]
    for k in range(1, last + 1):
        q, st, _ = cv2.calcOpticalFlowPyrLK(grey[k - 1], grey[k], p, None, **lk)
        b, st2, _ = cv2.calcOpticalFlowPyrLK(grey[k], grey[k - 1], q, None, **lk)
        ok = (st.ravel() == 1) & (st2.ravel() == 1) & (np.linalg.norm(b - p, axis=2).ravel() < 0.5)
        tips.append(tips[-1] + np.median((q - p)[ok].reshape(-1, 2), axis=0))
        p = q[ok].reshape(-1, 1, 2)
    print("klt: %d points survive, travel %.1f px" % (len(p), np.linalg.norm(tips[-1] - tips[0])))
    return tips


def pin(shot, tip, line_len, last, fade_out=None):
    """fade_out: (start, frames) 0-based; pin hidden after last."""
    fs = frames(shot)
    tips = klt(fs, tip, last)
    for k in range(len(fs)):
        im = Image.new("RGBA", (W, H), (255, 255, 255, 0))
        if k <= last:
            grow, ka = ease(k / 14), ease((k - 10) / 10)
            vis = 1.0 if fade_out is None else 1 - smooth((k - fade_out[0]) / fade_out[1])
            tx, ty = tips[k]
            top = ty - line_len * grow
            ss = 4
            x0, y0 = int(np.floor(tx - PIN_LINE / 2)) - 2, int(np.floor(top)) - 2
            sh = int(np.ceil(ty)) - y0 + 3
            if grow > 0 and sh > 4 and vis > 0:
                big = np.zeros((sh * ss, (PIN_LINE + 5) * ss), np.uint8)
                bx = (tx - PIN_LINE / 2 - x0) * ss
                big[int((top - y0) * ss):int((ty - y0) * ss), int(bx):int(bx + PIN_LINE * ss)] = 255
                sm = cv2.resize(big, (PIN_LINE + 5, sh), interpolation=cv2.INTER_AREA)
                strip = Image.new("RGBA", sm.shape[::-1], (255, 255, 255, 0))
                strip.putalpha(Image.fromarray((sm * vis).astype(np.uint8)))
                im.alpha_composite(strip, (x0, y0))
            if ka * vis > 0:
                kk = BADGE.copy()
                kk.putalpha(Image.fromarray((np.array(kk.getchannel("A")) * ka * vis).astype(np.uint8)))
                kx, ky = tx - SIDE / 2, ty - line_len - SIDE
                fx, fy = kx - np.floor(kx), ky - np.floor(ky)
                kk = kk.transform(kk.size, Image.AFFINE, (1, 0, -fx, 0, 1, -fy), resample=Image.BILINEAR)
                im.alpha_composite(kk, (int(np.floor(kx)), int(np.floor(ky))))
        save(shot, k, im)


if __name__ == "__main__":
    which = sys.argv[2:] or ["topdown", "view", "pullout"]
    if "topdown" in which:
        topdown()
    if "view" in which:
        pin("view", (1062, 925), round(H * 0.36), len(frames("view")) - 1)
    # The pull-out pin was cut by Hunter (2026-11-02): "the end pin is unnecessary".
