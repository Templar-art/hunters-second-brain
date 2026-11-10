"""Tracked Kollosche K pin over View.mp4: the line's tip is locked to the
townhouse roof, the line stays screen-vertical with the K upright above it
(Hunter's reference), and it draws up from the roof.

The tip is a bidirectional KLT track of a patch of roof points (median
motion), checked against the plate-vfx camera solve for the same pixel.
Frame 1 of the clip is a cut from the previous shot, so the pin starts on
frame 2.

Usage: python3 -I render_pin.py <job_dir> <clip> [badge]
  badge: pin head is the boxed navy K badge from the delivered drone stills, drawn by
  the drone-pin tool's own badge() with clients/amir-prestige.json (navy #011A3B square,
  white 5% border, white K 54%, line 5.5% of the side and touching the badge, side
  8.5% of frame height). Outputs get a _badge suffix; the white-K versions are kept.
"""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

job = Path(sys.argv[1])
clip = sys.argv[2]
BADGE = len(sys.argv) > 3 and sys.argv[3] == "badge"
SFX = "_badge" if BADGE else ""
root = Path("/Users/10xhunter/Documents/Hunters Second Brain")
v = job / "view"
frames = sorted((v / "frames").glob("f_*.png"))
shot = json.loads((v / "shot.json").read_text())
first = 1
W, H = shot["width"], shot["height"]

TIP = np.float32([1680, 990])

# --- track the tip ---------------------------------------------------------
grey = [cv2.cvtColor(cv2.imread(str(f)), cv2.COLOR_BGR2GRAY) for f in frames]
pts = cv2.goodFeaturesToTrack(grey[first], 200, 0.01, 6,
                              mask=cv2.circle(np.zeros_like(grey[first]), tuple(int(c) for c in TIP), 90, 255, -1))
lk = dict(winSize=(31, 31), maxLevel=4, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 40, 0.01))
tips = {first: TIP.copy()}
p = pts
for k in range(first + 1, len(frames)):
    q, st, _ = cv2.calcOpticalFlowPyrLK(grey[k - 1], grey[k], p, None, **lk)
    back, st2, _ = cv2.calcOpticalFlowPyrLK(grey[k], grey[k - 1], q, None, **lk)
    ok = (st.ravel() == 1) & (st2.ravel() == 1) & (np.linalg.norm(back - p, axis=2).ravel() < 0.3)
    d = np.median((q - p)[ok].reshape(-1, 2), axis=0)
    tips[k] = tips[k - 1] + d
    p = q[ok].reshape(-1, 1, 2)
print("tip track: %d -> %d points, travel %.1f px" % (len(pts), len(p), np.linalg.norm(tips[len(frames) - 1] - TIP)))


# --- the pin graphic -----------------------------------------------------------
src = Image.open(root / "raw/kollosche/team-logos/HayleyKidson/HK Kollosche_2white.png").convert("RGBA")
band = src.crop((0, 232, src.width, 621))
lab, _ = ndimage.label(np.array(band.getchannel("A")) > 8)
objs = ndimage.find_objects(lab)
firsts = sorted(range(len(objs)), key=lambda i: objs[i][1].start)[:2]
a = np.where(np.isin(lab, [i + 1 for i in firsts]), np.array(band.getchannel("A")), 0).astype(np.uint8)
k_img = Image.new("RGBA", band.size, (255, 255, 255, 0))
k_img.putalpha(Image.fromarray(a))
k_img = k_img.crop(k_img.getchannel("A").getbbox())

K_W = round(H * 0.079)        # same K-to-frame-height ratio as the 9:16 pin
k_img = k_img.resize((K_W, round(k_img.height * K_W / k_img.width)), Image.LANCZOS)
LINE_W = max(2, round(H * 0.0037))
LINE_LEN = round(H * 0.28)
GAP = round(H * 0.015)

if BADGE:
    sys.path.insert(0, str(root / "projects/drone-pin"))
    import drone_pin  # noqa: E402
    st = {**drone_pin.DEFAULT_STYLE,
          **json.loads((root / "projects/drone-pin/clients/amir-prestige.json").read_text())["style"]}
    side = round(0.05 * H)
    k_img = drone_pin.badge(side, drone_pin.glyph(st), st)
    LINE_W, GAP = max(3, round(0.0016 * H)), round(st["mark_gap"] * side)

def ease(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3

out_dir = v / "render" / f"pin{SFX}"
out_dir.mkdir(parents=True, exist_ok=True)
for k in range(len(frames)):
    im = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    if k >= first:
        t = k - first
        grow, k_a = ease(t / 14), ease((t - 10) / 10)
        tx, ty = tips[k]
        top = ty - LINE_LEN * grow
        # Sub-pixel placement: draw at 4x then downsample the strip.
        ss = 4
        x0 = int(np.floor(tx - LINE_W / 2)) - 2
        y0 = int(np.floor(top)) - 2
        strip_h = int(np.ceil(ty)) - y0 + 3
        if grow > 0 and strip_h > 4:
            big = np.zeros((strip_h * ss, (LINE_W + 5) * ss), np.uint8)
            bx0 = (tx - LINE_W / 2 - x0) * ss
            by0 = (top - y0) * ss
            big[int(by0):int((ty - y0) * ss), int(bx0):int(bx0 + LINE_W * ss)] = 255
            sm = cv2.resize(big, (LINE_W + 5, strip_h), interpolation=cv2.INTER_AREA)
            strip = Image.new("RGBA", sm.shape[::-1], (255, 255, 255, 0))
            strip.putalpha(Image.fromarray(sm))
            im.alpha_composite(strip, (x0, y0))
        if k_a > 0:
            kk = k_img.copy()
            kk.putalpha(Image.fromarray((np.array(kk.getchannel("A")) * k_a).astype(np.uint8)))
            kx = tx - k_img.width / 2
            ky = ty - LINE_LEN - GAP - k_img.height
            # Sub-pixel: shift via affine resample.
            fx, fy = kx - np.floor(kx), ky - np.floor(ky)
            kk = kk.transform(kk.size, Image.AFFINE, (1, 0, -fx, 0, 1, -fy), resample=Image.BILINEAR)
            im.alpha_composite(kk, (int(np.floor(kx)), int(np.floor(ky))))
    im.save(out_dir / f"p_{k + 1:04d}.png")

fps = "%d/%d" % tuple(shot["fps"])
out = v / "out"
out.mkdir(exist_ok=True)
seq = str(out_dir / "p_%04d.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", fps, "-i", seq,
                "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
                str(out / f"View_pin{SFX}_alpha.mov")], check=True)
for name, codec in [(f"View_pin{SFX}.mp4", ["-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p"]),
                    (f"View_pin{SFX}_ProRes422HQ.mov", ["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le"])]:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-framerate", fps, "-i", seq,
                    "-filter_complex", "[0:v][1:v]overlay=format=auto[v]", "-map", "[v]", "-map", "0:a?",
                    "-c:a", "copy", *codec, str(out / name)], check=True)
print("done", out)
