"""Composite scene_track.py EXRs over a Sony S-Log3 / S-Gamut3.Cine plate.

  blender -b --factory-startup -P comp_log.py -- <shot dir> [--gain 1.0] [--shadow 1.0] [--only N]
Plate: <shot>/plate16/p_####.png (16-bit full-range RGB from ffmpeg, i.e. legal-range codes expanded).
Pipeline: decode S-Log3 -> linear S-Gamut3.Cine -> linear Rec.709; multiply by the Shadow Catcher; lay the
scene-linear car over with its alpha; then
  log/    re-encode to S-Log3/S-Gamut3.Cine (16-bit PNG): grade it with the rest of the shoot
  rec709/ quick preview through Blender's AgX (Punchy) view
The decode/encode is an exact round trip, so the plate is untouched outside the car and its shadow.
"""
import glob, os, sys
import bpy
import numpy as np
import OpenImageIO as oiio
import PyOpenColorIO as ocio

a = sys.argv[sys.argv.index("--") + 1:]; SHOT = os.path.abspath(a[0])
opt = {a[i][2:]: a[i + 1] for i in range(1, len(a) - 1) if a[i].startswith("--")}
GAIN = float(opt.get("gain", 1.0)); SHP = float(opt.get("shadow", 1.0))
SG3C_TO_709 = np.array([[1.6269474, -0.5401385, -0.0868088],
                        [-0.1785155, 1.4179409, -0.2394254],
                        [-0.0444361, -0.1959199, 1.2403560]])
TO_SG3C = np.linalg.inv(SG3C_TO_709)


def slog3_decode(rgb):          # rgb: full-range 0..1 from legal-range video
    c = (64 + rgb * 876) / 1023
    return np.where(c >= 171.2102946929 / 1023, (10 ** ((c * 1023 - 420) / 261.5)) * 0.19 - 0.01,
                    (c * 1023 - 95) * 0.01125 / (171.2102946929 - 95))


def slog3_encode(x):
    c = np.where(x >= 0.01125, (420 + np.log10((x + 0.01) / 0.19) * 261.5) / 1023,
                 (x * (171.2102946929 - 95) / 0.01125 + 95) / 1023)
    return np.clip((c * 1023 - 64) / 876, 0, 1)


cfg = ocio.Config.CreateFromFile(os.path.join(bpy.utils.resource_path("LOCAL"), "datafiles", "colormanagement", "config.ocio"))
cpu = cfg.getProcessor(ocio.GroupTransform([ocio.LookTransform(src="Linear Rec.709", dst="Linear Rec.709", looks="AgX - Punchy"),
                                            ocio.DisplayViewTransform(src="Linear Rec.709", display="sRGB", view="AgX")])).getDefaultCPUProcessor()


def agx(x):
    y = np.ascontiguousarray(x.astype(np.float32)); cpu.applyRGB(y); return np.clip(y, 0, 1)


def parts(path):
    out, i = {}, 0
    while i < 32:
        b = oiio.ImageBuf(path, i, 0)
        if b.has_error or b.nchannels == 0:
            break
        px = b.get_pixels(oiio.FLOAT)
        for k, n in enumerate(b.spec().channelnames):
            out[n] = px[..., k]
        i += 1
    return out


def write(path, img, bits16):
    h, w = img.shape[:2]
    fmt = oiio.UINT16 if bits16 else oiio.UINT8; mx = 65535 if bits16 else 255
    b = oiio.ImageBuf(oiio.ImageSpec(w, h, 3, fmt))
    b.set_pixels(oiio.ROI(0, w, 0, h, 0, 1, 0, 3), (np.clip(img, 0, 1) * mx + 0.5).astype(np.uint16 if bits16 else np.uint8))
    b.write(path)


exrs = sorted(glob.glob(os.path.join(SHOT, "exr", "*.exr")))
if "only" in opt:
    exrs = [e for e in exrs if os.path.basename(e).endswith("%04d.exr" % int(opt["only"]))]
for d in ("log", "rec709"):
    os.makedirs(os.path.join(SHOT, d), exist_ok=True)
for e in exrs:
    f = int(os.path.basename(e).split("_")[-1].split(".")[0])
    pl = oiio.ImageBuf(os.path.join(SHOT, "plate16", "p_%04d.png" % f)).get_pixels(oiio.FLOAT)[..., :3]
    lin709 = slog3_decode(pl) @ SG3C_TO_709.T
    ch = parts(e)
    A = ch["ViewLayer.Combined.A"]; car = np.dstack([ch["ViewLayer.Combined." + c] for c in "RGB"]) * GAIN
    S = np.clip(np.dstack([ch["ViewLayer.Shadow Catcher." + c] for c in "RGB"]), 0, None) ** SHP \
        if "ViewLayer.Shadow Catcher.R" in ch else 1.0
    comp = lin709 * S * (1 - A[..., None]) + car          # car is premultiplied
    name = os.path.basename(e).replace(".exr", ".png")
    write(os.path.join(SHOT, "log", name), slog3_encode(comp @ TO_SG3C.T), True)
    write(os.path.join(SHOT, "rec709", name), agx(comp), False)
print("COMP_LOG_OK", len(exrs))
