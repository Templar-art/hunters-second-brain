#!/usr/bin/env python3
"""
2026 HIA Gold Coast & Northern Rivers Housing Awards — animated title card.

Renders a transparent-alpha title sequence: the HIA logo assembles from its
layers, then the type builds in on a stagger.

Logo source: raw/assets/hia/hia-logo.svg
If that file is missing a clearly-marked placeholder shield is drawn instead,
so layout and timing can be approved before the real artwork lands.

    python3 build.py            # 25 and 30 fps ProRes 4444 + preview gif
"""

import math
import os
import re
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.abspath(os.path.join(HERE, "..", ".."))
SVG = os.path.join(VAULT, "raw", "assets", "hia", "hia-logo.svg")
OUT = os.path.join(HERE, "out")

W, H = 1920, 1080
SS = 2                      # supersample factor; subpixel-clean transforms
DUR = 4.0

GREEN = (0, 88, 61)
YELLOW = (255, 213, 32)
WHITE = (255, 255, 255)

FONTS = os.path.expanduser("~/Library/Fonts")
F_SEMI = os.path.join(FONTS, "Poppins-SemiBold.ttf")
F_MED = os.path.join(FONTS, "Poppins-Medium.ttf")
F_BOLD = os.path.join(FONTS, "Poppins-Bold.ttf")

LINES = [
    ("2026", F_SEMI, 46, 0.34, YELLOW),
    ("HIA GOLD COAST & NORTHERN RIVERS", F_MED, 40, 0.20, WHITE),
    ("HOUSING AWARDS", F_BOLD, 92, 0.06, WHITE),
]


# ---------------------------------------------------------------- easing ----

def spring(t, z=0.50, w=26.0):
    """Damped spring, 0 -> 1, one soft overshoot (~5%)."""
    if t <= 0:
        return 0.0
    wd = w * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w * t) * (math.cos(wd * t) + (z * w / wd) * math.sin(wd * t))


def ease_out(t, d, p=3):
    return 1 - (1 - min(max(t / d, 0.0), 1.0)) ** p


# ---------------------------------------------------------------- layers ----

def render_svg_layer(svg_text, viewbox, colour, path, width):
    import cairosvg
    groups = re.findall(r'<g[^>]*fill="%s".*?</g>' % colour, svg_text, re.S)
    if not groups:
        return None
    tmp = os.path.join(OUT, "_layer.svg")
    with open(tmp, "w") as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">{groups[0]}</svg>')
    cairosvg.svg2png(url=tmp, write_to=path, output_width=width)
    return np.asarray(Image.open(path).convert("RGBA"))


def build_layers(res=2400):
    """Return dict of RGBA arrays: shield, hand, slats, letters, roof."""
    if not os.path.exists(SVG):
        return placeholder_layers(res), True

    from scipy import ndimage
    svg = open(SVG).read()
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    shield = render_svg_layer(svg, vb, "#00583D", os.path.join(OUT, "lay-shield.png"), res)
    white = render_svg_layer(svg, vb, "#FFFFFF", os.path.join(OUT, "lay-white.png"), res)
    roof = render_svg_layer(svg, vb, "#FFD520", os.path.join(OUT, "lay-roof.png"), res)

    h, w = white.shape[:2]
    lab, n = ndimage.label(white[..., 3] > 128)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    hand_id = int(np.argmax(sizes)) + 1
    slices = ndimage.find_objects(lab)

    letters = np.zeros((h, w), bool)
    slats = np.zeros((h, w), bool)
    for i, sl in enumerate(slices, 1):
        if i == hand_id:
            continue
        # the HIA lettering lives in the top third of the shield
        (letters if sl[0].stop < h * 0.32 else slats)[lab == i] = True

    def cut(mask):
        o = np.zeros((h, w, 4), "uint8")
        o[..., :3] = WHITE
        o[..., 3] = np.where(mask, white[..., 3], 0)
        return o

    return {
        "shield": shield,
        "hand": cut(lab == hand_id),
        "slats": cut(slats),
        "letters": cut(letters),
        "roof": roof,
    }, False


def placeholder_layers(res):
    """Marked stand-in so layout/timing can be judged without the artwork."""
    h = int(res * 476 / 420)
    def blank():
        return np.zeros((h, res, 4), "uint8")

    shield = Image.new("RGBA", (res, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(shield)
    d.rounded_rectangle([res * 0.04, h * 0.03, res * 0.96, h * 0.97],
                        radius=int(res * 0.18), fill=GREEN + (255,))
    f = ImageFont.truetype(F_BOLD, int(res * 0.13))
    d.text((res / 2, h * 0.42), "LOGO", font=f, fill=WHITE + (255,), anchor="mm")
    f2 = ImageFont.truetype(F_MED, int(res * 0.055))
    d.text((res / 2, h * 0.56), "placeholder", font=f2, fill=YELLOW + (255,), anchor="mm")

    return {"shield": np.asarray(shield), "hand": blank(),
            "slats": blank(), "letters": blank(), "roof": blank()}


# ------------------------------------------------------------------ type ----

def tracked_text(text, font_path, px, tracking_em, colour):
    """Render letterspaced text to a tight RGBA image (tracking in em)."""
    font = ImageFont.truetype(font_path, px)
    gap = px * tracking_em
    widths = [font.getlength(c) for c in text]
    total = sum(widths) + gap * (len(text) - 1)
    asc, desc = font.getmetrics()
    img = Image.new("RGBA", (int(total) + 4, asc + desc + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 2.0
    for c, adv in zip(text, widths):
        d.text((x, 2), c, font=font, fill=colour + (255,))
        x += adv + gap
    return img.crop(img.getbbox())      # tight to the ink, so stacking is predictable


# --------------------------------------------------------------- compose ----

def place(canvas, layer_img, cx, cy, scale, opacity, dy=0.0):
    """Composite layer_img centred at (cx, cy) with subpixel scale/offset."""
    if opacity <= 0.001 or scale <= 0.001:
        return
    sw, sh = layer_img.size
    dw, dh = sw * scale, sh * scale
    # inverse affine: canvas -> source, so nothing snaps to whole pixels
    m = (1 / scale, 0, (-(cx - dw / 2)) / scale,
         0, 1 / scale, (-(cy + dy - dh / 2)) / scale)
    warped = layer_img.transform(canvas.size, Image.AFFINE, m, resample=Image.BICUBIC)
    if opacity < 1:
        a = np.asarray(warped).astype(float).copy()
        a[..., 3] *= opacity
        warped = Image.fromarray(a.clip(0, 255).astype("uint8"), "RGBA")
    canvas.alpha_composite(warped)


def frame(t, layers, type_imgs, rule_w, lay):
    c = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))

    logo_h = lay["logo_h"]
    lx, ly = W * SS / 2, lay["logo_cy"]
    src_h = layers["shield"].height
    fit = logo_h / src_h

    # shield — the pop
    s = 0.65 + 0.35 * spring(t)
    place(c, layers["shield"], lx, ly, fit * s, ease_out(t, 0.15))

    # hand rises from below, clipped to the shield silhouette
    th = t - 0.18
    if th > 0:
        rise = (1 - ease_out(th, 0.45)) * logo_h * 0.22
        place(c, layers["hand"], lx, ly, fit * s, ease_out(th, 0.25), dy=rise)
        place(c, layers["slats"], lx, ly, fit * s, ease_out(th - 0.04, 0.25), dy=rise * 0.6)

    # lettering fades up
    place(c, layers["letters"], lx, ly, fit * s, ease_out(t - 0.26, 0.30))

    # roof settles on
    tr = t - 0.32
    if tr > 0:
        rs = 0.88 + 0.12 * spring(tr, z=0.55, w=24.0)
        place(c, layers["roof"], lx, ly, fit * s * rs, ease_out(tr, 0.22),
              dy=-(1 - ease_out(tr, 0.4)) * logo_h * 0.05)

    # rule wipes from centre
    tw = t - 0.55
    if tw > 0:
        frac = ease_out(tw, 0.5)
        half = rule_w * frac / 2
        y = lay["rule_y"]
        d = ImageDraw.Draw(c)
        d.rectangle([W * SS / 2 - half, y, W * SS / 2 + half, y + 2 * SS],
                    fill=YELLOW + (int(255 * min(frac * 2, 1)),))

    # type stagger
    for img, start, y in type_imgs:
        tt = t - start
        if tt <= 0:
            continue
        o = ease_out(tt, 0.35)
        place(c, img, W * SS / 2, y, 1.0, o, dy=(1 - o) * 22 * SS)

    # exit
    if t > 3.6:
        k = ease_out(t - 3.6, 0.4)
        a = np.asarray(c).astype(float).copy()
        a[..., 3] *= (1 - k)
        c = Image.fromarray(a.clip(0, 255).astype("uint8"), "RGBA")

    return c.resize((W, H), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    layers, placeholder = build_layers()
    if placeholder:
        print("!! raw/assets/hia/hia-logo.svg not found — PLACEHOLDER shield in use")
    layers = {k: Image.fromarray(v, "RGBA") for k, v in layers.items()}

    # --- layout: one centred stack, logo / rule / three type lines ----------
    starts = [0.65, 0.78, 0.90]
    imgs = [tracked_text(text, fp, px * SS, tr, col) for text, fp, px, tr, col in LINES]

    logo_h = H * SS * 0.30
    gap_logo_rule = H * SS * 0.058
    gap_rule_type = H * SS * 0.042
    leading = [H * SS * 0.030, H * SS * 0.034]      # between line 1-2 and 2-3

    type_h = sum(i.height for i in imgs) + sum(leading)
    total = logo_h + gap_logo_rule + gap_rule_type + type_h
    top = (H * SS - total) / 2

    lay = {"logo_h": logo_h, "logo_cy": top + logo_h / 2,
           "rule_y": top + logo_h + gap_logo_rule}

    type_imgs = []
    y = lay["rule_y"] + gap_rule_type
    for k, (img, st) in enumerate(zip(imgs, starts)):
        type_imgs.append((img, st, y + img.height / 2))
        y += img.height + (leading[k] if k < len(leading) else 0)

    rule_w = max(i.width for i in imgs) * 1.02

    for fps in (25, 30):
        d = os.path.join(OUT, f"fr{fps}")
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        n = int(fps * DUR)
        for i in range(n):
            frame(i / fps, layers, type_imgs, rule_w, lay).save(f"{d}/f{i:04d}.png")
        mov = os.path.join(OUT, f"hia-awards-title-1080p{fps}.mov")
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-framerate", str(fps), "-i", f"{d}/f%04d.png",
                        "-c:v", "prores_ks", "-profile:v", "4444",
                        "-pix_fmt", "yuva444p10le", "-alpha_bits", "16",
                        "-vendor", "apl0", mov], check=True)
        print("wrote", os.path.basename(mov), n, "frames")

    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", f"{OUT}/fr25/f%04d.png", "-filter_complex",
                    "[0:v]scale=640:-1,fps=25,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    os.path.join(OUT, "preview.gif")], check=True)
    print("wrote preview.gif")


if __name__ == "__main__":
    sys.exit(main())
