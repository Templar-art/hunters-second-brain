"""Full-length (1522-frame, 63.48 s) ProRes 4444 alpha overlays for Hunter's
FCP timeline, all starting at 00:00 over Main.mp4, plus a preview comp.

Layers: opener (KOLLOSCHE wordmark + address super), lot outline, K pin
(view wide), Taylor Kleinberg outro. Timeline frame numbers are Main.mp4 frames.

Usage: ~/.venvs/typeset/bin/python -I scripts/assemble.py <job_dir> <Main.mp4> <deliver_dir>
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


def opener(f):
    if f < 72:
        return with_alpha(wordmark, 1 - ss((f - 62) / 10))   # frame 1, no fade-in; fade out by 3 s
    if f < 144:
        return with_alpha(addr, min(ss((f - 72) / 10), 1 - ss((f - 134) / 10)))
    return None


# --- outro ----------------------------------------------------------------------
outro_png = Image.open(job / "cards/kollosche-outro-taylor-16x9.png").convert("RGBA").resize((W, H), Image.LANCZOS)
OUTRO = 1463   # 61.0 s; overlay + details fade in together


def outro(f):
    return with_alpha(outro_png, ss((f - OUTRO + 1) / 15)) if f >= OUTRO else None


LAYERS = {
    "01 Opener - KOLLOSCHE wordmark + address": opener,
    "02 Lot outline (top-down 31.2s)": seq("topdown/render/gfx", "g", 748),
    "03 K badge pin (34.2s)": seq("view/render/gfx", "g", 820),
    # Birds cut 2026-11-02: Hunter rejected the plate-vfx gulls on this job ("birds are shit").
    "04 Outro - Taylor Kleinberg 0447 466 177": outro,
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

# preview: everything over the edit, original audio
ins, chain, last = [], [], "0:v"
for i, name in enumerate(LAYERS, 1):
    ins += ["-i", str(dst / f"{name}.mov")]
    chain.append(f"[{last}][{i}:v]overlay=format=auto[v{i}]")
    last = f"v{i}"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, *ins, "-filter_complex", ";".join(chain),
                "-map", f"[{last}]", "-map", "0:a", "-c:a", "copy", "-c:v", "libx264", "-crf", "14",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst / "Main - Kollosche overlays PREVIEW.mp4")], check=True)
print("preview done")
