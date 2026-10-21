"""Camera-follow pass: a tripod operator panning, tilting and zooming with the car.

  python3 follow.py <comp dir> <out dir> [--w 1920 --h 1080] [--lag 0.35] [--size 0.22] [--fmax 3000]

The comp frames are the locked shot (plate + car, both from one nodal point). Rotating a camera about its own
centre needs no depth, so each output frame is an exact reprojection of the locked frame:
  output ray = K_out^-1 (u, v, 1) -> rotate by pitch then yaw -> K_src -> source pixel.
No stretching or parallax faking; the only limit is the source field of view, so the aim is clamped to keep
the output frustum inside the photo. The aim follows the car through a critically damped spring (operator
lag); zoom keeps the car near a target frame width and also eases. Camera motion blur: 3 shutter samples.
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

argv = sys.argv[1:]
src, out = argv[0], argv[1]
opt = {argv[i][2:]: argv[i + 1] for i in range(2, len(argv) - 1) if argv[i].startswith("--")}
WO, HO = int(opt.get("w", 1920)), int(opt.get("h", 1080))
LAG = float(opt.get("lag", 0.35))        # spring time constant, seconds
SIZE = float(opt.get("size", 0.22))      # target car width as a fraction of frame width
FMAX = float(opt.get("fmax", 3000))
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(out, exist_ok=True)

W2, H2, F, CX, CY, CAMH, FPS = 1600, 1066, 1102.0, 800.0, 533.0, 1.6, 25
CAR_W, CAR_Z = 1.95, 0.55
track = json.load(open(os.path.join(HERE, "track.json")))


def rays(yaw, pitch, fo, uu, vv):
    """Output pixel grid -> source pixel coords for a camera turned by yaw (right +) and pitch (up +)."""
    x, y, z = (uu - WO / 2) / fo, -(vv - HO / 2) / fo, np.ones_like(uu)
    cp, sp, cy, sy = math.cos(pitch), math.sin(pitch), math.cos(yaw), math.sin(yaw)
    y, z = y * cp + z * sp, -y * sp + z * cp
    x, z = x * cy + z * sy, -x * sy + z * cy
    return CX + F * x / z, CY - F * y / z


EDGE = np.array([(u, v) for u in (0, WO / 2, WO) for v in (0, HO / 2, HO)], float)


def fits(yaw, pitch, fo):
    us, vs = rays(yaw, pitch, fo, EDGE[:, 0], EDGE[:, 1])
    return us.min() >= 0 and us.max() <= W2 and vs.min() >= 0 and vs.max() <= H2


FMIN = F * WO / W2 * 1.02   # widest the output can go with the camera dead centre
# ---- desired aim and zoom per frame
want = []
for f, X, Y, Z in track:
    x, y, z = X, Z + CAR_Z - CAMH, Y
    d = math.sqrt(x * x + y * y + z * z)
    fo = min(FMAX, max(FMIN, SIZE * WO * d / CAR_W))
    want.append((math.atan2(x, z), math.atan2(y, math.hypot(x, z)), math.log(fo)))
want = np.array(want)

# ---- operator: critically damped spring on (yaw, pitch, log f), started at rest on the car
w0 = 2.0 / LAG; dt = 1.0 / FPS
pos, vel, aim = want[0].copy(), np.zeros(3), []
for k in range(len(want)):
    for _ in range(4):
        h = dt / 4
        acc = w0 * w0 * (want[k] - pos) - 2 * w0 * vel
        vel += acc * h; pos += vel * h
    yaw, pitch, fo = pos[0], pos[1], math.exp(pos[2])
    if not fits(yaw, pitch, fo):        # pull toward centre / zoom in just enough to stay inside the photo
        lo, hi = 0.0, 1.0
        for _ in range(20):
            t = (lo + hi) / 2
            (lo, hi) = (t, hi) if fits(yaw * t, pitch * t, fo) else (lo, t)
        yaw, pitch = yaw * lo, pitch * lo
    aim.append((yaw, pitch, fo))
aim = np.array(aim)
json.dump(aim.tolist(), open(os.path.join(HERE, "aim.json"), "w"))

uu, vv = np.meshgrid(np.arange(WO) + 0.5, np.arange(HO) + 0.5)


def sample(img, us, vs):
    us = np.clip(us - 0.5, 0, W2 - 1.001); vs = np.clip(vs - 0.5, 0, H2 - 1.001)
    x0, y0 = us.astype(int), vs.astype(int); fx, fy = (us - x0)[..., None], (vs - y0)[..., None]
    a, b = img[y0, x0], img[y0, x0 + 1]; c, d = img[y0 + 1, x0], img[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


files = sorted(f for f in os.listdir(src) if f.endswith(".png") and not f.startswith("test"))
if "frame" in opt:                      # preview one frame: --frame N uses comp/test_000N.png at aim N
    files, first = ["test_%04d.png" % int(opt["frame"])], int(opt["frame"]) - 1
else:
    first = 0
for i, name in enumerate(files, start=first):
    img = np.asarray(Image.open(os.path.join(src, name)).convert("RGB"), np.float32)
    acc = 0
    for s in (-0.25, 0.0, 0.25):        # 180-degree shutter on the camera move
        j = min(max(i + s, 0), len(aim) - 1); j0 = int(j); j1 = min(j0 + 1, len(aim) - 1); t = j - j0
        yaw, pitch, fo = (1 - t) * aim[j0] + t * aim[j1]
        acc = acc + sample(img, *rays(yaw, pitch, fo, uu, vv))
    Image.fromarray(np.clip(acc / 3 + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(out, name))
print("FOLLOW_OK", len(files), "frames; zoom range", round(aim[:, 2].min()), "-", round(aim[:, 2].max()))
