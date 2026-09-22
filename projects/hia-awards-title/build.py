#!/usr/bin/env python3
"""
2026 HIA Gold Coast & Northern Rivers Housing Awards — animated title card.

Three modes, same lockup and timing:

  green   deep HIA-green field, type knocked out in white. Self-contained,
          instantly HIA without needing the logo.
  punch   green field with the type cut OUT of it as real alpha holes, so
          whatever you lay underneath in FCP plays inside the letters.
  alpha   type on transparency, to comp over your own dark footage.

Layout is centred. A yellow rule draws outward from the centre to the width
of the hero line; type arrives by mask reveal from its own baseline, with a
light vertical parallax so the hold breathes.

    python3 build.py            # renders all three modes
"""

import math
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

W, H = 1920, 1080
SS = 2
DUR = 4.6                   # seconds
EXIT = 0.55                 # seconds of fade-out at the tail
FPS_SET = (50, 25)          # 50p first; 25 kept for a 25p timeline
MODES = ("green", "punch", "alpha")

HIA_GREEN = (0, 88, 61)
YELLOW = (255, 213, 32)
WHITE = (255, 255, 255)

FONTS = os.path.expanduser("~/Library/Fonts")
F_SEMI = os.path.join(FONTS, "Poppins-SemiBold.ttf")
F_MED = os.path.join(FONTS, "Poppins-Medium.ttf")
F_BOLD = os.path.join(FONTS, "Poppins-Bold.ttf")

YEAR = ("2026", F_SEMI, 32, 0.52)
HERO = ("HOUSING AWARDS", F_BOLD, 112, 0.02)
REGION = ("HIA GOLD COAST & NORTHERN RIVERS", F_MED, 37, 0.30)



# ---------------------------------------------------------------- easing ----

def ease_out(t, d, p=3):
    return 1 - (1 - min(max(t / d, 0.0), 1.0)) ** p


def ease_in_out(t, d):
    u = min(max(t / d, 0.0), 1.0)
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ type ----

def tracked_text(text, font_path, px, tracking_em):
    """Letterspaced text as a white-on-transparent stencil, cropped to ink."""
    px = int(px)
    font = ImageFont.truetype(font_path, px)
    gap = px * tracking_em
    widths = [font.getlength(c) for c in text]
    total = sum(widths) + gap * (len(text) - 1)
    asc, desc = font.getmetrics()
    img = Image.new("L", (int(total) + 4, asc + desc + 4), 0)
    d = ImageDraw.Draw(img)
    x = 2.0
    for ch, adv in zip(text, widths):
        d.text((x, 2), ch, font=font, fill=255)
        x += adv + gap
    return img.crop(img.getbbox())


def spec(s):
    text, fp, px, tr = s
    return tracked_text(text, fp, px * SS, tr)


# --------------------------------------------------------------- stencil ----

def stamp(mask, stencil, left, top, scale=1.0):
    """Add a stencil into an L-mode mask at float position/scale."""
    if scale <= 0.001:
        return
    dw = stencil.width * scale
    m = (1 / scale, 0, -left / scale, 0, 1 / scale, -top / scale)
    warped = stencil.transform(mask.size, Image.AFFINE, m, resample=Image.BICUBIC)
    mask.paste(ImageChops_lighter(mask, warped))


def ImageChops_lighter(a, b):
    from PIL import ImageChops
    return ImageChops.lighter(a, b)


def reveal_up(mask, stencil, left, baseline, t, start, dur=0.66, scale=1.0):
    """Wipe type up from its baseline; the baseline itself never moves."""
    tt = t - start
    if tt <= 0:
        return
    p = ease_out(tt, dur, p=4)
    keep = max(1, int(round(stencil.height * p)))
    strip = stencil.crop((0, stencil.height - keep, stencil.width, stencil.height))
    lift = (1 - ease_out(tt, dur * 1.2, p=3)) * 12 * SS
    stamp(mask, strip, left, baseline - strip.height * scale + lift, scale)


# ----------------------------------------------------------------- layout ----

def layout(year, hero, region):
    """Everything centres on the frame's vertical axis."""
    gap_year = H * SS * 0.058
    gap_hero = H * SS * 0.046

    total = year.height + gap_year + hero.height + gap_hero + region.height
    y = (H * SS - total) / 2

    lay = {"cx": W * SS / 2, "hero_w": hero.width, "year_w": year.width}
    lay["year_base"] = y + year.height
    lay["rule_y"] = lay["year_base"] + gap_year * 0.34
    lay["hero_base"] = lay["year_base"] + gap_year + hero.height
    lay["region_base"] = lay["hero_base"] + gap_hero + region.height
    return lay


# ------------------------------------------------------------------ frame ----

def frame(t, mode, year, hero, region, lay, bg=None):
    size = (W * SS, H * SS)
    cx = lay["cx"]

    # gentle vertical parallax so the hold breathes without a fake zoom
    drift = ease_in_out(t, DUR) * 9 * SS

    def left_of(img):
        return cx - img.width / 2

    # 1. the type stencil for this frame
    ink = Image.new("L", size, 0)
    ya = ease_out(t, 0.45)
    if ya > 0:
        tmp = Image.new("L", size, 0)
        stamp(tmp, year, left_of(year), lay["year_base"] - year.height - drift * 0.30)
        ink = tmp if ya >= 1 else tmp.point(lambda v: int(v * ya))
    reveal_up(ink, hero, left_of(hero), lay["hero_base"] - drift * 0.55,
              t, 0.22, dur=0.72)
    reveal_up(ink, region, left_of(region), lay["region_base"] - drift * 0.80,
              t, 0.44, dur=0.60)

    # 2. the field
    if mode == "alpha":
        c = Image.new("RGBA", size, (0, 0, 0, 0))
        col = Image.new("RGBA", size, WHITE + (255,))
        c.paste(col, (0, 0), ink)
    else:
        field_a = ease_out(t, 0.55, p=4)
        c = Image.new("RGBA", size, HIA_GREEN + (int(255 * field_a),))
        if mode == "green":
            col = Image.new("RGBA", size, WHITE + (255,))
            c.paste(col, (0, 0), ink)
        else:                                   # punch: type becomes holes
            a = np.asarray(c).astype(np.int16).copy()
            a[..., 3] = np.clip(a[..., 3] - np.asarray(ink).astype(np.int16), 0, 255)
            c = Image.fromarray(a.astype("uint8"), "RGBA")

    # 3. yellow furniture on top — rule off the right edge, then the roof
    d = ImageDraw.Draw(c)
    tw = t - 0.10
    if tw > 0:
        p = ease_out(tw, 1.0, p=4)
        half = lay["hero_w"] / 2 * p
        y = lay["rule_y"] - drift * 0.42
        d.rectangle([cx - half, y, cx + half, y + 2 * SS],
                    fill=YELLOW + (int(255 * min(tw / 0.2, 1.0)),))

    # 4. exit
    if t > DUR - EXIT:
        k = ease_in_out(t - (DUR - EXIT), EXIT)
        a = np.asarray(c).astype(float).copy()
        a[..., 3] *= (1 - k)
        c = Image.fromarray(a.clip(0, 255).astype("uint8"), "RGBA")

    return c.resize((W, H), Image.LANCZOS)


def encode(mode, fps, n):
    d = os.path.join(OUT, "fr_%s_%d" % (mode, fps))
    mov = os.path.join(OUT, "hia-awards-%s-1080p%d.mov" % (mode, fps))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-framerate", str(fps), "-i", "%s/f%%04d.png" % d,
                    "-c:v", "prores_ks", "-profile:v", "4444",
                    "-pix_fmt", "yuva444p10le", "-alpha_bits", "16",
                    "-vendor", "apl0", mov], check=True)
    print("wrote", os.path.basename(mov), n, "frames")


def main():
    os.makedirs(OUT, exist_ok=True)
    year, hero, region = spec(YEAR), spec(HERO), spec(REGION)
    lay = layout(year, hero, region)

    for mode in MODES:
        for fps in FPS_SET:
            d = os.path.join(OUT, "fr_%s_%d" % (mode, fps))
            shutil.rmtree(d, ignore_errors=True)
            os.makedirs(d)
            n = int(round(fps * DUR))
            for i in range(n):
                frame(i / fps, mode, year, hero, region, lay).save("%s/f%04d.png" % (d, i))
            encode(mode, fps, n)

    for mode in MODES:
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", "%s/fr_%s_25/f%%04d.png" % (OUT, mode),
                        "-filter_complex",
                        "[0:v]scale=720:-1,fps=25,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                        os.path.join(OUT, "preview-%s.gif" % mode)], check=True)
    print("wrote previews")


if __name__ == "__main__":
    sys.exit(main())
