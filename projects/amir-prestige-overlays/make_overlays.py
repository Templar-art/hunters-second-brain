"""Amir Prestige video overlays, matched to their own listing films (44 Via Roma, Nov 2026), as
ProRes 4444 alpha MOVs for FCP (25 fps) in 16:9 4K and 9:16 1080x1920, plus a PNG of each.

  00  logo opener      white "amir prestige" wordmark centred over footage, soft shadow, no box;
                       eases in, hard cut out (Kollosche lesson: logo to address is a hard cut)
  01  address super    one centred line, street Montserrat Regular caps + suburb Bold caps, no box
  01n property name    e.g. "Bella Vista": large Playfair Display Italic with a hairline swash under it
                       (a nod to the cut through their wordmark), small tracked Montserrat line below;
                       letters settle from wide tracking as it fades in
  02  agent names      left and right, Playfair Display title case over Montserrat mobile numbers
  03  end card         solid black, small white "amir prestige" wordmark centred (opaque)
  04  grey mat         their framed-montage border, #D6D6D6 with a transparent window

Fonts: Montserrat + Playfair Display (OFL, fonts/). Their site font is Garet (not licensed here);
Montserrat matches the supers in their films. Wordmark: raw/amir-prestige (1000 px web PNG).

Usage:
  ~/.venvs/typeset/bin/python -I make_overlays.py <out_dir> [--address "44 VIA ROMA|ISLE OF CAPRI"]
      [--name "Bella Vista" [--name-sub "ISLE OF CAPRI"]] [--agent "Omar Amir-Mian|0428 553 883"] ...
      [--preview frame.jpg]
"""
import argparse
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
VAULT = HERE.parent.parent
FPS = 25
SIZES = {"16x9": (3840, 2160), "9x16": (1080, 1920)}
MONT = str(HERE / "fonts" / "Montserrat[wght].ttf")
PLAY = str(HERE / "fonts" / "PlayfairDisplay[wght].ttf")
PLAY_I = str(HERE / "fonts" / "PlayfairDisplay-Italic[wght].ttf")
MAT = (0xD6, 0xD6, 0xD6)
WORDMARK = Image.open(VAULT / "raw/amir-prestige/amir-prestige-wordmark-white.png").convert("RGBA")
WORDMARK = WORDMARK.crop(WORDMARK.getchannel("A").getbbox())


def font(path, size, weight):
    f = ImageFont.truetype(path, round(size))
    f.set_variation_by_axes([{"Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700}[weight]])
    return f


def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def run(draw, x, y_cap_top, s, f, track_em, fill=(255, 255, 255, 255)):
    """Draw s from x with its cap top on y; returns the advance."""
    top = f.getbbox("H")[1]
    tr = track_em * f.size
    for c in s:
        draw.text((x, y_cap_top - top), c, font=f, fill=fill)
        x += f.getlength(c) + tr
    return x


def width(s, f, track_em):
    return sum(f.getlength(c) for c in s) + track_em * f.size * (len(s) - 1)


def cap(f):
    b = f.getbbox("H")
    return b[3] - b[1]


def shadowed(im, W, k=0.45):
    """Soft diffuse shadow, no box: holds white type on bright walls and sky, as in their films."""
    a = im.getchannel("A").filter(ImageFilter.GaussianBlur(W * 0.003))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(a.point(lambda v: round(v * k)))
    sh.alpha_composite(im)
    return sh


def opener(W, H):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ww = W * (0.30 if W > H else 0.62)
    lg = WORDMARK.resize((round(ww), round(ww * WORDMARK.height / WORDMARK.width)), Image.LANCZOS)
    im.alpha_composite(lg, ((W - lg.width) // 2, (H - lg.height) // 2))
    return shadowed(im, W)


def address(W, H, street, suburb):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    port = H > W
    c = H * (0.021 if not port else 0.0135)          # cap height, measured off their 1280x676 frame
    fr, fb = font(MONT, c / 0.70, "Regular"), font(MONT, c / 0.70, "Bold")
    a, b = f"{street}, ", suburb
    tr = 0.03
    total = width(a, fr, tr) + fr.size * tr + width(b, fb, tr)
    if port and total > W * 0.86:                    # 9:16: street over suburb
        y = H / 2 - c * 1.4
        run(d, (W - width(street, fr, tr)) / 2, y, street, fr, tr)
        run(d, (W - width(b, fb, tr)) / 2, y + c * 2.0, b, fb, tr)
    else:
        x = run(d, (W - total) / 2, H / 2 - c / 2, a, fr, tr)
        run(d, x, H / 2 - c / 2, b, fb, tr)
    return shadowed(im, W)


def name_title(W, H, name, sub, t):
    """t in 0..1 = settle progress: tracking eases from wide to set, swash draws left to right."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    port = H > W
    c = H * (0.075 if not port else 0.042)
    f = font(PLAY_I, c / 0.71, "Regular")
    tr = 0.10 - 0.08 * ease(t)
    wn = width(name, f, tr)
    y = H / 2 - c * (0.75 if sub else 0.5)
    run(d, (W - wn) / 2, y, name, f, tr)
    # Hairline swash under the name: a shallow arc that draws on, echoing the cut through their wordmark.
    set_w = width(name, f, 0.02)
    x0, x1 = W / 2 - set_w * 0.46, W / 2 + set_w * 0.46
    yb = y + c * 1.28
    lw = max(2, round(c * 0.028))
    n = 200
    xs = np.linspace(x0, x0 + (x1 - x0) * ease(min(1, t * 1.15)), n)
    u = (xs - x0) / (x1 - x0)
    ys = yb - np.sin(u * np.pi) * c * 0.10 + (u - 0.5) * c * 0.10
    ss = 4
    big = Image.new("L", (W * ss // 4, H * ss // 4), 0)   # same size; supersample only the stroke ends
    bd = ImageDraw.Draw(big)
    pts = [(float(a), float(b)) for a, b in zip(xs, ys)]
    if len(pts) > 1 and xs[-1] - xs[0] > 1:
        bd.line(pts, fill=255, width=lw, joint="curve")
        # taper both ends so it reads as a pen stroke, not a rule
        fade = np.clip(np.minimum(u, 1 - u) / 0.18, 0, 1) if t >= 1 else np.clip(u / 0.18, 0, 1)
        stroke = Image.new("RGBA", (W, H), (255, 255, 255, 0))
        alpha = np.array(big, np.float32)
        col = np.interp(np.arange(W), xs, fade, left=0, right=0)
        stroke.putalpha(Image.fromarray((alpha * col[None, :]).astype(np.uint8)))
        im.alpha_composite(stroke)
    if sub:
        fs = font(MONT, c * 0.20 / 0.70, "Medium")
        ts = 0.42
        run(d, (W - width(sub, fs, ts)) / 2, yb + c * 0.55, sub, fs, ts, fill=(255, 255, 255, 235))
    return shadowed(im, W, 0.40)


def agents_card(W, H, agents):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    port = H > W
    c = H * (0.030 if not port else 0.019)
    fn = font(PLAY, c / 0.71, "Regular")
    fp = font(MONT, c * 0.46 / 0.70, "Regular")
    if port or len(agents) == 1:
        xs = [W / 2] if len(agents) == 1 else [W / 2] * len(agents)
        ys = [H * 0.5 - (len(agents) - 1) * c * 1.6 + i * c * 3.2 for i in range(len(agents))]
    else:   # their layout: names at the outer thirds of the hero shot, a touch above centre
        xs = [W * 0.27, W * 0.73][:len(agents)] if len(agents) == 2 else list(np.linspace(W * 0.2, W * 0.8, len(agents)))
        ys = [H * 0.47] * len(agents)
    for (nm, ph), x, y in zip(agents, xs, ys):
        run(d, x - width(nm, fn, 0) / 2, y, nm, fn, 0)
        if ph:
            run(d, x - width(ph, fp, 0.06) / 2, y + c * 1.45, ph, fp, 0.06)
    return shadowed(im, W)


def end_card(W, H):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    ww = W * (0.10 if W > H else 0.30)   # their end card: a small wordmark, lots of black
    lg = WORDMARK.resize((round(ww), round(ww * WORDMARK.height / WORDMARK.width)), Image.LANCZOS)
    im.alpha_composite(lg, ((W - lg.width) // 2, (H - lg.height) // 2))
    return im


def mat(W, H):
    """Grey border with a clear window; measured off their framed montage (sides 3.6 %, top/bottom 7.4 %)."""
    im = Image.new("RGBA", (W, H), MAT + (255,))
    sx, sy = (0.036, 0.074) if W > H else (0.06, 0.06)
    win = Image.new("RGBA", (W - 2 * round(W * sx), H - 2 * round(H * sy)), (0, 0, 0, 0))
    im.paste(win, (round(W * sx), round(H * sy)))
    return im


def faded(img, a):
    if a >= 1:
        return img
    out = img.copy()
    out.putalpha(Image.fromarray((np.array(img.getchannel("A")).astype(np.float32) * a).astype(np.uint8)))
    return out


def write_mov(frames_fn, n, path):
    seq = path.parent / f"_seq_{path.stem}"
    seq.mkdir(exist_ok=True)
    last, last_img = None, None
    for f in range(n):
        img = frames_fn(f)
        img.save(seq / f"{f:04d}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(seq / "%04d.png"),
                    "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", str(path)], check=True)
    for p in seq.iterdir():
        p.unlink()
    seq.rmdir()


def inout(f, n, fin=10, fout=10):
    return ease(min((f + 1) / fin, (n - f) / fout))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--address", help='"STREET|SUBURB"')
    ap.add_argument("--name", help='property name, e.g. "Bella Vista"')
    ap.add_argument("--name-sub", help="small line under the name (e.g. the suburb)")
    ap.add_argument("--agent", action="append", default=[], help='"Name|mobile"')
    ap.add_argument("--preview", help="a video frame to comp the stills over")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    agents = [tuple((s.split("|") + [""])[:2]) for s in a.agent]
    for asp, (W, H) in SIZES.items():
        op = opener(W, H)
        write_mov(lambda f: faded(op, ease((f + 1) / 12)), 3 * FPS, out / f"00 Amir logo opener {asp}.mov")
        op.save(out / f"00 Amir logo opener {asp}.png")
        parts = [op]
        if a.address:
            st, sb = (a.address.upper().split("|") + [""])[:2]
            ad = address(W, H, st, sb)
            n = 3 * FPS
            write_mov(lambda f: faded(ad, inout(f, n)), n, out / f"01 Amir address {asp}.mov")
            ad.save(out / f"01 Amir address {asp}.png")
            parts.append(ad)
        if a.name:
            sub = (a.name_sub or "").upper()
            n, settle = 4 * FPS, round(1.6 * FPS)
            final = name_title(W, H, a.name, sub, 1)
            slug = a.name.replace("/", "-")
            write_mov(lambda f: faded(name_title(W, H, a.name, sub, (f + 1) / settle) if f < settle else final,
                                      inout(f, n, 14, 12)), n, out / f"01n Amir name {slug} {asp}.mov")
            final.save(out / f"01n Amir name {slug} {asp}.png")
            parts.append(final)
        if agents:
            ag = agents_card(W, H, agents)
            n = 3 * FPS
            write_mov(lambda f: faded(ag, inout(f, n)), n, out / f"02 Amir agents {asp}.mov")
            ag.save(out / f"02 Amir agents {asp}.png")
            parts.append(ag)
        ec = end_card(W, H)
        write_mov(lambda f: ec, 3 * FPS, out / f"03 Amir end card {asp}.mov")
        ec.save(out / f"03 Amir end card {asp}.png")
        mt = mat(W, H)
        write_mov(lambda f: mt, 5 * FPS, out / f"04 Amir grey mat {asp}.mov")
        mt.save(out / f"04 Amir grey mat {asp}.png")
        parts += [ec, mt]
        if a.preview:
            bg = Image.open(a.preview).convert("RGBA")
            sc = max(W / bg.width, H / bg.height)
            bg = bg.resize((round(bg.width * sc), round(bg.height * sc)), Image.LANCZOS)
            bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
            tiles = []
            for p in parts:
                t = bg.copy()
                t.alpha_composite(p)
                t.thumbnail((1280, 1280))
                tiles.append(t.convert("RGB"))
            cols = 3 if W > H else len(tiles)
            rows = (len(tiles) + cols - 1) // cols
            tw, th = tiles[0].size
            sheet = Image.new("RGB", (cols * tw + 20 * (cols - 1), rows * th + 20 * (rows - 1)), "black")
            for i, t in enumerate(tiles):
                sheet.paste(t, ((i % cols) * (tw + 20), (i // cols) * (th + 20)))
            sheet.save(out / f"_preview {asp}.jpg", quality=90)
        print("wrote", asp)


main()
