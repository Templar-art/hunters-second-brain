"""Katrina Walsh start + end cards for 9:16 reels (1080x1920, 23.976 fps, ProRes 4444 on alpha).

Same art as the 16:9 film cards (make_cards.py / animate.py), re-laid for vertical: text sized to the
narrow frame, everything kept above the bottom ~25% where Instagram's caption UI sits.
  start: COASTAL° wordmark fades in, holds, fades out over the opening drone (her films open this way).
  end:   name, number, COASTAL° wordmark ease in one after another and hold (no background, Hunter 29 Oct).

Usage: python3 reel_cards.py [--start-len 3.2] [--end-len 4.63] [--preview start.png end.png]
"""
import argparse
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

sys.path.insert(0, str(Path(__file__).parent))
import make_cards as mc  # noqa: E402
import animate as an  # noqa: E402

W, H, FPS = 1080, 1920, 24000 / 1001
mc.W, mc.H = an.W, an.H = W, H
an.FPS = FPS


def start_card(length, scrim=0.0):
    """COASTAL° wordmark centred over the opening drone, as her films open (Main 0:00). Fade + small rise in, out by the cut.

    scrim > 0 lays a soft feathered black band behind the wordmark at that opacity, plus a faint shadow on the letters,
    so it reads over busy drone footage (Hunter 29 Oct: logo lost over the flythrough's treetops)."""
    cy = int(H * 0.45)

    def logo_draw(d, img):
        logo = Image.open(mc.LOGO_WHITE).convert("RGBA")
        lw = int(W * 0.55)
        logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
        img.alpha_composite(logo, ((W - lw) // 2, cy - logo.height // 2))
    logo = an.layer(logo_draw)
    blank = np.zeros((H, W, 4), np.float32)
    shade = None
    if scrim > 0:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        band = np.exp(-((yy - cy) / 210) ** 2) * (0.75 + 0.25 * np.exp(-((xx - W / 2) / 700) ** 2))
        shadow = gaussian_filter(logo[..., 3], 14) * 0.6
        shade = np.zeros((H, W, 4), np.float32)
        shade[..., 3] = np.clip(band * scrim + shadow * (1 - band * scrim), 0, 1)

    def frame(t):
        f = blank.copy()
        k = an.phase(t, 0.2, 1.0)
        a = k * (1 - an.phase(t, length - 0.7, 0.6))
        if shade is not None:
            an.over(f, shade, a)
        an.over(f, logo, a, dy=(1 - k) * 10)
        return f

    name = f"coastal-wordmark-open-anim-9x16-scrim{round(scrim * 100)}.mov" if scrim > 0 else "coastal-wordmark-open-anim-9x16.mov"
    an.encode(frame, round(length * FPS), mc.OUT / name)
    return frame(length / 2)


def end_card(length):
    name = an.layer(lambda d, i: mc.centred(d, "KATRINA WALSH", mc.font(mc.LIGHT, 92), cy=H * 0.40))
    num = an.layer(lambda d, i: mc.centred(d, "0429 899 295", mc.font(mc.LIGHT, 92), cy=H * 0.40 + 115))

    def logo_draw(d, img):
        logo = Image.open(mc.LOGO_WHITE).convert("RGBA")
        lw = int(W * 0.55)
        logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
        img.alpha_composite(logo, ((W - lw) // 2, int(H * 0.64) - logo.height // 2))
    logo = an.layer(logo_draw)
    blank = np.zeros((H, W, 4), np.float32)

    def frame(t):
        f = blank.copy()
        for lyr, start in ((name, 0.3), (num, 0.6), (logo, 1.1)):
            k = an.phase(t, start, 1.0)
            an.over(f, lyr, k, dy=(1 - k) * 10)
        return f

    an.encode(frame, round(length * FPS), mc.OUT / "katrina-walsh-end-card-anim-alpha-9x16.mov")
    return frame(length)


def preview(card, bg_path, out):
    bg = Image.open(bg_path).convert("RGBA").resize((W, H))
    bg.alpha_composite(Image.fromarray((np.clip(card, 0, 1) * 255).astype(np.uint8)))
    bg.convert("RGB").save(out, quality=90)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-len", type=float, default=3.2)
    ap.add_argument("--end-len", type=float, default=4.63)
    ap.add_argument("--scrim", type=float, default=0.0, help="opacity of a soft dark band behind the start wordmark")
    ap.add_argument("--preview", nargs=2, metavar=("START_BG", "END_BG"))
    a = ap.parse_args()
    mc.OUT.mkdir(exist_ok=True)
    s, e = start_card(a.start_len, a.scrim), end_card(a.end_len)
    if a.preview:
        preview(s, a.preview[0], mc.OUT / "preview-start-9x16.jpg")
        preview(e, a.preview[1], mc.OUT / "preview-end-card-9x16.jpg")
    print("written to", mc.OUT)
