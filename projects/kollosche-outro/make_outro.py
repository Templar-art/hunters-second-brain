"""Kollosche agent outro: the 50% navy overlay, agent names and numbers in
Söhne Breit Kräftig, and the copyright small print, all fading in together
(Kollosche video guidelines: no logo or K on the outro).

The layout is measured from Kollosche's own Taylor x Thibault end cards in
raw/kollosche/end-cards/: cap height, tracking, line pitch, the two blank
lines between agents, block centring, and the small print (copied pixel for
pixel from the card). Needs ~/.venvs/typeset (uharfbuzz + Pillow) for kerning. `--check` re-renders Taylor and Thibault and diffs the
result against the card.

Usage:
  ~/.venvs/typeset/bin/python -I make_outro.py <repo_root> <out_dir> "NAME|0400 000 000" ["NAME|NUMBER" ...]
  ~/.venvs/typeset/bin/python -I make_outro.py <repo_root> <out_dir> --check
"""
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import uharfbuzz as hb

root, out = Path(sys.argv[1]), Path(sys.argv[2])
args = sys.argv[3:]
check = args == ["--check"]
agents = ([("TAYLOR KLEINBERG", "0446 466 177"), ("THIBAULT PAROLINI", "0401 023 142")] if check
          else [tuple(s.upper() for s in a.split("|")) for a in args])
out.mkdir(parents=True, exist_ok=True)
FONT = os.path.expanduser("~/Library/Fonts/SöhneBreit-Kräftig.otf")
CARDS = {  # aspect: (reference card, delivery size)
    "16x9": ("Taylour & Thibault Main End Card.png", (3840, 2160)),
    "9x16": ("Taylor x Thibault Reel End Card.png", (1080, 1920)),
}
HB_FONT = hb.Font(hb.Face(hb.Blob.from_file_path(FONT)))
FPS, FADE, HOLD = 25, 15, 4 * 25


def text_rows(card):
    """Bands of white text in the card: list of (top, bottom, x0, x1)."""
    a = np.array(card)
    white = (a[:, :, 0] > 200) & (a[:, :, 3] > 200)
    ys = np.where(white.any(1))[0]
    runs, s, p = [], ys[0], ys[0]
    for y in ys[1:]:
        if y - p > 4:
            runs.append((s, p))
            s = y
        p = y
    runs.append((s, p))
    res = []
    for t, b in runs:
        xs = np.where(white[t:b + 1].any(0))[0]
        res.append((t, b, xs.min(), xs.max()))
    return res


def advances(text, size):
    """Kerned advances (px) from HarfBuzz; the cards are kerned with no tracking."""
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(HB_FONT, buf, {"kern": True})
    return [g.x_advance / HB_FONT.face.upem * size for g in buf.glyph_positions]


def draw_line(canvas, text, font, track, cap_top, cx):
    """Draw centred, kerned caps so the cap top lands on cap_top."""
    adv = advances(text, font.size)
    total = sum(adv) + track * (len(text) - 1)
    ink = font.getbbox("H")
    x = cx - total / 2
    layer = Image.new("L", canvas.size, 0)
    d = ImageDraw.Draw(layer)
    for c, w in zip(text, adv):
        d.text((x, cap_top - ink[1]), c, font=font, fill=255)
        x += w + track
    canvas.paste(Image.new("RGBA", canvas.size, (255, 255, 255, 255)), (0, 0), layer)

for aspect, (card_name, size) in CARDS.items():
    card = Image.open(root / "raw/kollosche/end-cards" / card_name).convert("RGBA")
    CW, CH = card.size
    rows = text_rows(card)
    # Big text = the first four bands; the rest is the small print.
    big, small = rows[:4], rows[4:]
    cap = np.mean([b - t + 1 for t, b, _, _ in big])
    pitch = big[1][0] - big[0][0]
    agent_step = big[2][0] - big[0][0]

    probe = ImageFont.truetype(FONT, 1000)
    hbox = probe.getbbox("H")
    em = cap / ((hbox[3] - hbox[1]) / 1000)
    font = ImageFont.truetype(FONT, int(round(em)))
    track = 0.0  # measured: the card's word widths match kerned Kräftig with no tracking

    # Card overlay colour and the small print, kept exactly as Kollosche set them.
    overlay = card.getpixel((5, 5))
    # The reel card carries no small print; the landscape card does.
    sp_top = small[0][0] - 20 if small else None
    small_print = card.crop((0, sp_top, CW, CH)) if small else None

    # Layout for N agents, centred on the same middle as the card's block.
    card_mid = (big[0][0] + big[-1][1]) / 2
    n = len(agents)
    block_h = (n - 1) * agent_step + pitch + cap
    top0 = card_mid - block_h / 2
    frame = Image.new("RGBA", (CW, CH), overlay)
    if small_print:
        frame.paste(small_print, (0, sp_top))  # replace, not composite: it carries the overlay too
    for i, (name, phone) in enumerate(agents):
        y = top0 + i * agent_step
        draw_line(frame, name, font, track, y, CW / 2)
        draw_line(frame, phone, font, track, y + pitch, CW / 2)

    if check:
        a = np.array(frame).astype(int)
        b = np.array(card).astype(int)
        diff = np.abs(a[:, :, 3] - b[:, :, 3])
        print(f"{aspect}: em {em:.1f}px tracking {track:.2f}px  alpha diff mean {diff.mean():.2f}, "
              f"pixels off >64: {(diff > 64).mean() * 100:.3f}%")

    final = frame.resize(size, Image.LANCZOS)
    tag = "check" if check else "_".join(a[0].split()[0].lower() for a in agents)
    png = out / f"kollosche-outro-{tag}-{aspect}.png"
    final.save(png)
    if check:
        continue
    # Fade everything in together over FADE frames, then hold.
    seq = out / f"_seq_{aspect}"
    seq.mkdir(exist_ok=True)
    alpha = np.array(final.getchannel("A")).astype(np.float32)
    for f in range(FADE + HOLD):
        t = min(1.0, (f + 1) / FADE)
        t = t * t * (3 - 2 * t)
        fr = final.copy()
        fr.putalpha(Image.fromarray((alpha * t).astype(np.uint8)))
        fr.save(seq / f"{f:04d}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(seq / "%04d.png"),
                    "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
                    str(png.with_suffix(".mov"))], check=True)
    for p in seq.iterdir():
        p.unlink()
    seq.rmdir()
    print("wrote", png.name, png.with_suffix(".mov").name)
