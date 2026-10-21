"""Composite scene.py EXRs over the plate.

  blender -b --factory-startup -P comp.py -- <exr dir or file> <out dir> [--exposure 0] [--look "AgX - Punchy"] [--shadow 1.0 (power on the catcher: >1 deepens)]

The plate is display-referred sRGB; the car is scene-linear. So the car goes through Blender's own AgX view
(OCIO), the plate is linearised, multiplied by the Shadow Catcher pass (shadows and headlight spill), and
re-encoded; the car is then laid over it in display space with its alpha.
"""
import glob
import os
import sys

import bpy
import numpy as np
import OpenImageIO as oiio
import PyOpenColorIO as ocio

argv = sys.argv[sys.argv.index("--") + 1:]
src, out = argv[0], argv[1]
opt = {argv[i][2:]: argv[i + 1] for i in range(2, len(argv) - 1) if argv[i].startswith("--")}
EXPO = float(opt.get("exposure", 0)); SHPOW = float(opt.get("shadow", 1.0)); LOOK = opt.get("look", "AgX - Punchy")
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(out, exist_ok=True)

cfg = ocio.Config.CreateFromFile(os.path.join(bpy.utils.resource_path("LOCAL"), "datafiles", "colormanagement", "config.ocio"))
vt = ocio.DisplayViewTransform(src="Linear Rec.709", display="sRGB", view="AgX")
lk = ocio.LookTransform(src="Linear Rec.709", dst="Linear Rec.709", looks=LOOK)
grp = ocio.GroupTransform([ocio.ExposureContrastTransform(exposure=EXPO), lk, vt])
cpu = cfg.getProcessor(grp).getDefaultCPUProcessor()


def agx(rgb):
    x = np.ascontiguousarray(rgb.astype(np.float32))
    cpu.applyRGB(x)
    return np.clip(x, 0, 1)


def to_lin(s):
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)


def to_srgb(l):
    l = np.clip(l, 0, None)
    return np.clip(np.where(l <= 0.0031308, l * 12.92, 1.055 * np.power(l, 1 / 2.4) - 0.055), 0, 1)


plate_buf = oiio.ImageBuf(os.path.join(HERE, "plate.png"))
plate_cache = {}


def plate(w, h):
    if (w, h) not in plate_cache:
        r = oiio.ImageBufAlgo.resize(plate_buf, roi=oiio.ROI(0, w, 0, h, 0, 1, 0, 3))
        plate_cache[(w, h)] = to_lin(r.get_pixels(oiio.FLOAT)[..., :3])
    return plate_cache[(w, h)]


def parts(path):
    """Blender 5.x writes each pass as its own EXR part (subimage): read them all."""
    out, i = {}, 0
    while True:
        b = oiio.ImageBuf(path, i, 0)
        if b.has_error or b.nchannels == 0:
            break
        px = b.get_pixels(oiio.FLOAT)
        for c, n in enumerate(b.spec().channelnames):
            out[n] = px[..., c]
        i += 1
        if i > 32:
            break
    return out


def chans(allc, prefix):
    return {n.split(".")[-1]: v for n, v in allc.items() if n.startswith(prefix)}


files = sorted(glob.glob(os.path.join(src, "*.exr"))) if os.path.isdir(src) else [src]
for f in files:
    allc = parts(f)
    names = list(allc)
    comb = chans(allc, "ViewLayer.Combined.")
    sh = chans(allc, "ViewLayer.Shadow Catcher.")
    h, w = comb["R"].shape
    a = comb["A"]
    rgb = np.dstack([comb["R"], comb["G"], comb["B"]])
    un = rgb / np.maximum(a, 1e-4)[..., None]
    car = agx(un)
    S = np.clip(np.dstack([sh["R"], sh["G"], sh["B"]]), 0, None) ** SHPOW if sh else np.ones_like(rgb)
    bg = to_srgb(plate(w, h) * S)
    o = car * a[..., None] + bg * (1 - a[..., None])
    ob = oiio.ImageBuf(oiio.ImageSpec(w, h, 3, oiio.UINT8))
    ob.set_pixels(oiio.ROI(0, w, 0, h, 0, 1, 0, 3), (o * 255 + 0.5).astype(np.uint8))
    name = os.path.splitext(os.path.basename(f))[0]
    ob.write(os.path.join(out, name + ".png"))
print("COMP_OK", len(files), "frames;", "channels seen:", [n for n in names if "Shadow" in n][:3])
