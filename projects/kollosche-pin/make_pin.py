"""Kollosche K location pin: the K from the wordmark over a thin white line
dropping to the property. Renders a transparent PNG plus an animated
ProRes 4444 (alpha) for Final Cut, 1080x1920 @ 25 fps.

Layout follows Hunter's reference (2026-10-27): the K is ~14% of frame
width, the line is ~6 px, and the line's tip marks the house.

Usage: python3 -I make_pin.py <repo_root> <out_dir> [navy]
  navy: K taken from the official navy wordmark (#011A3B) instead of the white
  team wordmark; the line stays white. Outputs get a -navy suffix.
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

root, out = Path(sys.argv[1]), Path(sys.argv[2])
NAVY = len(sys.argv) > 3 and sys.argv[3] == "navy"
SUFFIX = "-navy" if NAVY else ""
out.mkdir(parents=True, exist_ok=True)
W, H, FPS = 1080, 1920, 25

# The K glyph: the first two connected shapes (stem + arm) of the wordmark.
if NAVY:
    band = Image.open(root / "raw/kollosche/brand-logos/wordmark/Kollosche-wordmark-navy.png").convert("RGBA")
    K_RGB = (1, 26, 59)
else:
    src = Image.open(root / "raw/kollosche/team-logos/HayleyKidson/HK Kollosche_2white.png").convert("RGBA")
    band = src.crop((0, 232, src.width, 621))
    K_RGB = (255, 255, 255)
lab, _ = ndimage.label(np.array(band.getchannel("A")) > 8)
objs = ndimage.find_objects(lab)
first = sorted(range(len(objs)), key=lambda i: objs[i][1].start)[:2]
keep = np.isin(lab, [i + 1 for i in first])
alpha = np.where(keep, np.array(band.getchannel("A")), 0).astype(np.uint8)
k = Image.new("RGBA", band.size, K_RGB + (0,))
k.putalpha(Image.fromarray(alpha))
k = k.crop(k.getchannel("A").getbbox())

K_W = round(W * 0.14)
k = k.resize((K_W, round(k.height * K_W / k.width)), Image.LANCZOS)
LINE_W, GAP = 6, 28

def layout(tip_y, k_top):
    """Returns positions for a pin whose line ends at tip_y."""
    line_top = k_top + k.height + GAP
    return line_top, tip_y

def frame(k_top, tip_y, grow, k_alpha):
    """grow 0..1 = how much of the line has drawn up from the tip."""
    im = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    line_top, tip = layout(tip_y, k_top)
    length = tip - line_top
    top = tip - length * grow
    if grow > 0:
        y0 = int(np.floor(top))
        line = Image.new("RGBA", (LINE_W, tip - y0), (255, 255, 255, 255))
        # Soften the growing end by its sub-pixel coverage.
        cov = 1 - (top - y0)
        la = np.array(line.getchannel("A"))
        la[0, :] = int(255 * cov)
        line.putalpha(Image.fromarray(la))
        im.alpha_composite(line, ((W - LINE_W) // 2, y0))
    if k_alpha > 0:
        kk = k.copy()
        kk.putalpha(Image.fromarray((np.array(kk.getchannel("A")) * k_alpha).astype(np.uint8)))
        im.alpha_composite(kk, ((W - k.width) // 2, k_top))
    return im

def ease_out(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3

variants = {
    # name: (K top y, tip y). Long matches the reference; short suits closer wides.
    "long": (round(H * 0.18), round(H * 0.84)),
    "short": (round(H * 0.30), round(H * 0.62)),
}
for name, (k_top, tip_y) in variants.items():
    frame(k_top, tip_y, 1, 1).save(out / f"kollosche-pin-{name}{SUFFIX}.png")
    seq = out / f"_seq_{name}{SUFFIX}"
    seq.mkdir(exist_ok=True)
    total = FPS * 5  # 0.5 s line draw, K fades, then hold; trim in FCP
    for f in range(total):
        grow = ease_out(f / 14)
        k_a = ease_out((f - 10) / 10)
        frame(k_top, tip_y, grow, k_a).save(seq / f"{f:04d}.png")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(seq / "%04d.png"),
         "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
         "-alpha_bits", "16", str(out / f"kollosche-pin-{name}{SUFFIX}.mov")],
        check=True,
    )
    for p in seq.iterdir():
        p.unlink()
    seq.rmdir()
    print(name, "K", k.size, "K top", k_top, "tip", tip_y)
