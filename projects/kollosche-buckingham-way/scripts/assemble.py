"""Full-length (1522-frame, 63.48 s) ProRes 4444 alpha overlays for Hunter's
FCP timeline, all starting at 00:00 over Main.mp4, plus a preview comp.

Layers: opener wordmark, address super (separate, hard cut), lot outline, K pin
(view wide), sky gulls, Taylor Kleinberg + Thibault Parolini outro. Timeline frame numbers are Main.mp4 frames.

Usage: ~/.venvs/typeset/bin/python -I scripts/assemble.py <job_dir> <Main.mp4> <deliver_dir> [sfx_mix.mp4]
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import uharfbuzz as hb
from PIL import Image, ImageDraw, ImageFont

job, src, dst = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3])
root = job.parents[1]
W, H, N, FPS = 1920, 1080, 1522, "24000/1001"
FONT = str(Path.home() / "Library/Fonts/SöhneBreit-Kräftig.otf")


def ss(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def with_alpha(im, k):
    if k >= 1:
        return im
    im = im.copy()
    im.putalpha(Image.fromarray((np.array(im.getchannel("A")) * k).astype(np.uint8)))
    return im


def seq(folder, prefix, start, offset=0):
    """frame -> image for a PNG sequence placed at timeline frame `start`."""
    files = sorted((job / folder).glob(prefix + "_*.png"))[offset:]
    return {start + i: f for i, f in enumerate(files)}


# --- opener -------------------------------------------------------------------
wordmark = Image.open(root / "raw/kollosche/brand-logos/Kollosche-3840-x-2160.png").convert("RGBA").resize((W, H), Image.LANCZOS)
hbf = hb.Font(hb.Face(hb.Blob.from_file_path(FONT)))


def address(lines):
    """Measured from Kollosche's 4K example: cap 47 px, ~8% tracking, 78 px pitch, centred block."""
    S = 3840
    probe = ImageFont.truetype(FONT, 1000)
    hb_ = probe.getbbox("H")
    size = round(47 / ((hb_[3] - hb_[1]) / 1000))
    font = ImageFont.truetype(FONT, size)
    ink = font.getbbox("H")
    track = 0.08 * size
    im = Image.new("L", (S, 2160), 0)
    d = ImageDraw.Draw(im)
    top0 = 1080 - (78 * (len(lines) - 1) + 47) / 2
    for i, text in enumerate(lines):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(hbf, buf, {"kern": True})
        adv = [g.x_advance / hbf.face.upem * size for g in buf.glyph_positions]
        x = S / 2 - (sum(adv) + track * (len(text) - 1)) / 2
        for c, w in zip(text, adv):
            d.text((x, top0 + i * 78 - ink[1]), c, font=font, fill=255)
            x += w + track
    out = Image.new("RGBA", (S, 2160), (255, 255, 255, 0))
    out.putalpha(im)
    return out.resize((W, H), Image.LANCZOS)


addr = address(["4-6 BUCKINGHAM WAY", "ELANORA"])


# Hunter 2026-11-02: wordmark -> address is a hard cut, no transition, and each is its own layer.
def opener_wordmark(f):
    return wordmark if f < 72 else None                      # frame 1 to 3 s, hard cut out


def opener_address(f):
    return addr if 72 <= f < 144 else None                   # hard cut in on the wordmark's last frame + 1


# --- outro ----------------------------------------------------------------------
outro_png = Image.open(job / "cards/kollosche-outro-taylor_thibault-16x9.png").convert("RGBA").resize((W, H), Image.LANCZOS)
OUTRO = 1463   # 61.0 s; overlay + details fade in together


def outro(f):
    return with_alpha(outro_png, ss((f - OUTRO + 1) / 15)) if f >= OUTRO else None


LAYERS = {
    "01a Opener - KOLLOSCHE wordmark (0-3s)": opener_wordmark,
    "01b Opener - address 4-6 Buckingham Way (3-6s)": opener_address,
    "02 Lot outline (top-down 31.2s)": seq("topdown/render/gfx", "g", 748),
    "03 K badge pin (34.2s)": seq("view/render/gfx", "g", 820),
    # v1 gulls rejected ("birds are shit": grey specks over canopy); v2 keeps them in the sky (--sky-y).
    "03b Birds - gulls in the sky (34.2s + 60.6s)": {**seq("view/render/birds_png", "b", 820), **seq("pullout_wide/render/birds_png", "b", 1453)},
    "04 Outro - Taylor Kleinberg + Thibault Parolini": outro,
}


def frame(layer, f):
    if callable(layer):
        return layer(f)
    p = layer.get(f)
    return Image.open(p).convert("RGBA") if p else None


dst.mkdir(parents=True, exist_ok=True)
blank = np.zeros((H, W, 4), np.uint8).tobytes()
for name, layer in LAYERS.items():
    out = dst / f"{name}.mov"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                           "-r", FPS, "-i", "-", "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
                           "-vendor", "apl0", str(out)], stdin=subprocess.PIPE)
    for f in range(N):
        im = frame(layer, f)
        ff.stdin.write(blank if im is None else im.tobytes())
    ff.stdin.close()
    ff.wait()
    print("wrote", out.name)

# preview: everything over the edit (source scaled to the overlay size: Main.mp4 is now a 4K export),
# audio from the SFX mix when given, else the edit's own
audio = sys.argv[4] if len(sys.argv) > 4 else None
ins, chain, last = [], [f"[0:v]scale={W}:{H}:flags=lanczos[v0]"], "v0"
for i, name in enumerate(LAYERS, 1):
    ins += ["-i", str(dst / f"{name}.mov")]
    chain.append(f"[{last}][{i}:v]overlay=format=auto[v{i}]")
    last = f"v{i}"
amap = ["-map", f"{len(LAYERS) + 1}:a"] if audio else ["-map", "0:a"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, *ins, *(["-i", audio] if audio else []),
                "-filter_complex", ";".join(chain), "-map", f"[{last}]", *amap, "-c:a", "aac", "-b:a", "256k",
                "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-shortest",
                str(dst / "Main - Kollosche overlays + SFX PREVIEW.mp4")], check=True)
print("preview done")
