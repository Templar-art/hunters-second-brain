"""Reel (9:16) graphics for 4-6 Buckingham Way: one K badge pin (no outline: Hunter 2026-11-02, "for the
pin didnt need the outline") on
reel shot r17 (coast wide, house bottom-centre). Outline corners measured off his delivered still
(reel/cadastre/web06_outline.json), SIFT-registered to r17 f1 (web06_to_r17.json), then carried
through the shot by frame-to-frame KLT homographies on the lot/street area. Writes r17/render/gfx/.

Usage: python3 -I scripts/reel_graphics.py <job_dir>
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

W, H = 1080, 1920
ST = {**drone_pin.DEFAULT_STYLE,
      **json.loads((root / "projects/drone-pin/clients/kollosche.json").read_text())["style"]}
SIDE = round(ST["badge"] * W)              # same pixel size as the 16:9 badge
BADGE = drone_pin.badge(SIDE, drone_pin.k_glyph(), ST)
PIN_LINE = max(2, round(ST["pin_line"] * SIDE))
LW, SS = max(2, round(1920 * 0.0033)), 2
DRAW_START, DRAW = 2, 16                  # outline draw-on (0-based frames)
PIN_START = 2                             # pin grows right after the cut
LINE_LEN = 300
SHOW_OUTLINE = False                      # outline cut by Hunter; pin tip still comes from the Web-06 registration


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def smooth(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def track(fs):
    grey = [cv2.cvtColor(cv2.imread(str(f)), cv2.COLOR_BGR2GRAY) for f in fs]
    mask = np.zeros_like(grey[0])
    mask[1380:1900, 60:1020] = 255
    lk = dict(winSize=(31, 31), maxLevel=4, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 40, 0.01))
    Hs = [np.eye(3)]
    for k in range(1, len(fs)):
        p = cv2.goodFeaturesToTrack(grey[k - 1], 1500, 0.005, 6, mask=mask)
        q, st, _ = cv2.calcOpticalFlowPyrLK(grey[k - 1], grey[k], p, None, **lk)
        b, st2, _ = cv2.calcOpticalFlowPyrLK(grey[k], grey[k - 1], q, None, **lk)
        ok = (st.ravel() == 1) & (st2.ravel() == 1) & (np.linalg.norm(b - p, axis=2).ravel() < 0.5)
        Hk, inl = cv2.findHomography(p[ok], q[ok], cv2.RANSAC, 1.5)
        err = np.linalg.norm(cv2.perspectiveTransform(p[ok].reshape(1, -1, 2), Hk)[0] - q[ok].reshape(-1, 2), axis=1)
        if k % 8 == 0:
            print("r17 f%02d  pts %4d  inliers %4d  median %.2f px" % (k + 1, ok.sum(), inl.sum(), np.median(err[inl.ravel() == 1])))
        Hs.append(Hk @ Hs[-1])
        Hs[-1] /= Hs[-1][2, 2]
    return Hs


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


def main():
    fs = sorted((job / "reel/r17/frames").glob("f_*.png"))
    reg = json.loads((job / "reel/cadastre/web06_to_r17.json").read_text())
    LOT, TIP = np.float32(reg["poly_r17f1"]), np.float32(reg["pin_r17f1"])
    # start the draw at the top-edge midpoint under the pin, like the stills read: TR, BR, BL, TL, back
    Hs = track(fs)
    out = job / "reel/r17/render/gfx"
    out.mkdir(parents=True, exist_ok=True)
    for k in range(len(fs)):
        poly = cv2.perspectiveTransform(LOT[None], Hs[k])[0]
        tx, ty = cv2.perspectiveTransform(TIP[None, None], Hs[k])[0, 0]
        canvas = np.zeros((H * SS, W * SS), np.uint8)
        frac = smooth((k - DRAW_START) / DRAW)
        if SHOW_OUTLINE and frac > 0:
            path = partial(poly, frac) * SS
            cv2.polylines(canvas, [np.round(path * 16).astype(np.int32)], frac >= 1, 255, LW * SS, cv2.LINE_AA, shift=4)
            for x, y in path:
                cv2.circle(canvas, (int(round(x * 16)), int(round(y * 16))), LW * SS // 2 * 16, 255, -1, cv2.LINE_AA, shift=4)
        a = cv2.resize(canvas, (W, H), interpolation=cv2.INTER_AREA)
        im = Image.new("RGBA", (W, H), (255, 255, 255, 0))
        im.putalpha(Image.fromarray(a))
        grow, ka = ease((k - PIN_START) / 14), ease((k - PIN_START - 10) / 10)
        if grow > 0:
            top = ty - LINE_LEN * grow
            big = np.zeros((H * 4, PIN_LINE * 4 + 8), np.uint8)
            big[int(top * 4):int(ty * 4), 4:4 + PIN_LINE * 4] = 255
            x0 = int(np.floor(tx - PIN_LINE / 2)) - 1
            sm = cv2.resize(big, (PIN_LINE + 2, H), interpolation=cv2.INTER_AREA)
            strip = Image.new("RGBA", (PIN_LINE + 2, H), (255, 255, 255, 0))
            strip.putalpha(Image.fromarray(sm))
            im.alpha_composite(strip, (x0, 0))
        if ka > 0:
            kk = BADGE.copy()
            kk.putalpha(Image.fromarray((np.array(kk.getchannel("A")) * ka).astype(np.uint8)))
            kx, ky = tx - SIDE / 2, ty - LINE_LEN - SIDE
            fx, fy = kx - np.floor(kx), ky - np.floor(ky)
            kk = kk.transform(kk.size, Image.AFFINE, (1, 0, -fx, 0, 1, -fy), resample=Image.BILINEAR)
            im.alpha_composite(kk, (int(np.floor(kx)), int(np.floor(ky))))
        im.save(out / f"g_{k + 1:04d}.png")
    print("wrote", len(fs), "frames ->", out)


if __name__ == "__main__":
    main()
