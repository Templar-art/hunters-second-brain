"""REAL Specialists video overlays: an opener (logo, then an optional address super on a hard cut)
and an agent end card, as ProRes 4444 alpha MOVs for FCP, 16:9 4K and 9:16 1080x1920.

Brand: orange #E45E39 (from the logo on realspecialists.com), Lato (their web font, OFL, in fonts/),
logo traced from their site PNG (rs-logo-*.svg/png). The end card is their brand tile: solid orange,
white logo, white type.

Usage:
  ~/.venvs/typeset/bin/python -I make_overlays.py <out_dir> --agent "CONNOR HEWITT|0400 000 000" \
      [--agent "NAME|NUMBER"] [--address "21 ALBANY AVENUE|CURRUMBIN"] [--preview <frame.jpg>]
"""
import argparse
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ORANGE = (0xE4, 0x5E, 0x39)
FPS = 25
SIZES = {"16x9": (3840, 2160), "9x16": (1080, 1920)}
FONT = {w: str(HERE / "fonts" / f"Lato-{w}.ttf") for w in ("Black", "Bold", "Regular", "Light")}
LOGO_W = Image.open(HERE / "rs-logo-white.png").convert("RGBA")
LOGO_W = LOGO_W.crop(LOGO_W.getchannel("A").getbbox())


def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def logo(width):
    return LOGO_W.resize((round(width), round(width * LOGO_W.height / LOGO_W.width)), Image.LANCZOS)


def text(draw, xy_center_top, s, font, track_em, fill=(255, 255, 255, 255)):
    """Centred, tracked text whose cap top lands on y."""
    x_c, y = xy_center_top
    track = track_em * font.size
    widths = [font.getlength(c) for c in s]
    total = sum(widths) + track * (len(s) - 1)
    x = x_c - total / 2
    top = font.getbbox("H")[1]
    for c, w in zip(s, widths):
        draw.text((x, y - top), c, font=font, fill=fill)
        x += w + track
    return font.getbbox("H")[3] - top   # cap height


def opener_logo(W, H):
    """White logo centred over a light scrim so it holds on bright sky."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, round(255 * 0.22)))
    lw = W * (0.34 if W > H else 0.66)
    lg = logo(lw)
    im.alpha_composite(lg, ((W - lg.width) // 2, (H - lg.height) // 2))
    return im


def opener_address(W, H, lines):
    """Address super: a short orange rule over tracked white caps (Lato Black, then Light)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, round(255 * 0.22)))
    d = ImageDraw.Draw(im)
    base = H * (0.034 if W > H else 0.022)
    f1 = ImageFont.truetype(FONT["Black"], round(base / 0.72))
    f2 = ImageFont.truetype(FONT["Regular"], round(base * 0.62 / 0.72))   # Light read too thin over footage
    rule_w, rule_h = base * 1.6, max(2, round(base * 0.09))
    y = H / 2 - base * 1.3
    d.rectangle([W / 2 - rule_w / 2, y - base * 0.9, W / 2 + rule_w / 2, y - base * 0.9 + rule_h], fill=ORANGE + (255,))
    cap = text(d, (W / 2, y), lines[0], f1, 0.12)
    if len(lines) > 1:
        text(d, (W / 2, y + cap + base * 0.75), lines[1], f2, 0.32)
    return im


def end_card(W, H, agents):
    """Their brand tile: solid orange, white logo, agents in Lato Black caps over Regular numbers."""
    im = Image.new("RGBA", (W, H), ORANGE + (255,))
    d = ImageDraw.Draw(im)
    port = H > W
    lg = logo(W * (0.30 if not port else 0.62))
    base = H * (0.030 if not port else 0.019)
    fn = ImageFont.truetype(FONT["Black"], round(base / 0.72))
    fp = ImageFont.truetype(FONT["Regular"], round(base * 0.8 / 0.72))
    gap_logo = base * 3.2
    per = base * 1.0 + base * 0.8 + base * 0.7      # name cap + gap + number cap
    between = base * 1.8
    block = lg.height + gap_logo + len(agents) * per + (len(agents) - 1) * between
    y = (H - block) / 2
    im.alpha_composite(lg, ((W - lg.width) // 2, round(y)))
    y += lg.height + gap_logo
    for name, phone in agents:
        cap = text(d, (W / 2, y), name, fn, 0.14)
        if phone:
            text(d, (W / 2, y + cap + base * 0.7), phone, fp, 0.10)
        y += per + between
    small = ImageFont.truetype(FONT["Bold"], round(base * 0.42 / 0.72))
    text(d, (W / 2, H - H * (0.06 if not port else 0.07)), "REALSPECIALISTS.COM", small, 0.30,
         fill=(255, 255, 255, 230))
    return im


def write_mov(frames_fn, n, path):
    seq = path.parent / f"_seq_{path.stem}"
    seq.mkdir(exist_ok=True)
    for f in range(n):
        frames_fn(f).save(seq / f"{f:04d}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(seq / "%04d.png"),
                    "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", str(path)], check=True)
    for p in seq.iterdir():
        p.unlink()
    seq.rmdir()


def faded(img, a):
    if a >= 1:
        return img
    out = img.copy()
    out.putalpha(Image.fromarray((np.array(img.getchannel("A")).astype(np.float32) * a).astype(np.uint8)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--agent", action="append", default=[], help='"NAME|NUMBER" (number optional)')
    ap.add_argument("--address", help='"LINE 1|LINE 2"')
    ap.add_argument("--preview", help="a video frame to comp the stills over for review")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    agents = [tuple((s.upper().split("|") + [""])[:2]) for s in a.agent] or [("", "")]
    tag = "_".join(n.split()[0].lower() for n, _ in agents if n) or "noagent"
    fade = 12
    for asp, (W, H) in SIZES.items():
        lg = opener_logo(W, H)
        # 01a logo 0-3 s: eases in, hard cut out (Kollosche lesson: logo to address is a hard cut).
        write_mov(lambda f: faded(lg, ease((f + 1) / fade)), 3 * FPS, out / f"01a REAL logo opener {asp}.mov")
        lg.save(out / f"01a REAL logo opener {asp}.png")
        if a.address:
            ad = opener_address(W, H, [s.upper() for s in a.address.split("|")])
            n = 3 * FPS
            write_mov(lambda f: faded(ad, ease((n - f) / fade)), n, out / f"01b REAL address {asp}.mov")
            ad.save(out / f"01b REAL address {asp}.png")
        ec = end_card(W, H, agents)
        write_mov(lambda f: faded(ec, ease((f + 1) / 15)), 15 + 4 * FPS, out / f"02 REAL end card {tag} {asp}.mov")
        ec.save(out / f"02 REAL end card {tag} {asp}.png")
        if a.preview:
            bg = Image.open(a.preview).convert("RGBA")
            sc = max(W / bg.width, H / bg.height)
            bg = bg.resize((round(bg.width * sc), round(bg.height * sc)), Image.LANCZOS)
            bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
            parts = [lg] + ([ad] if a.address else []) + [ec]
            tiles = []
            for p in parts:
                t = bg.copy()
                t.alpha_composite(p)
                t.thumbnail((1280, 1280))
                tiles.append(t.convert("RGB"))
            sheet = Image.new("RGB", (sum(t.width for t in tiles) + 20 * (len(tiles) - 1), tiles[0].height), "black")
            x = 0
            for t in tiles:
                sheet.paste(t, (x, 0))
                x += t.width + 20
            sheet.save(out / f"_preview {asp}.jpg", quality=90)
        print("wrote", asp)


main()
