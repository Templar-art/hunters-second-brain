"""Tracked Coastal pins on a plate-vfx job (camera.json from `plate_vfx.py prep`).

Two looks for Hunter to pick from, both locked to one ground point through the solved camera:
  c    - Coastal C° pin (same art + timing as projects/coastal-katrina/animate.py: white stem draws up,
         C° mark fades/settles on top)
  card - Coastal C° mark over a white address line + sub line on the same stem

Usage: python3 coastal_pin.py <job> --at X Y [--look c|card] [--start 0.3] [--scale 1.4]
Outputs <job>/out/pin_<look>.mp4 (comp, original audio) + pin_<look>_alpha.mov (ProRes 4444 overlay)
and <job>/pilot_pin_<look>.png.
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(VAULT, "projects", "plate-vfx", "lib"))
import ground  # noqa: E402

MARK = os.path.join(VAULT, "projects", "drone-pin", "logos", "coastal-c-white.png")
FONT = os.path.expanduser("~/Library/Fonts/Poppins-SemiBold.ttf")
FONT_REG = os.path.expanduser("~/Library/Fonts/Poppins-Regular.ttf")


def ease(t):
    t = min(1.0, max(0.0, t))
    return 1 - (1 - t) ** 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job")
    ap.add_argument("--at", nargs=2, type=float, required=True, help="frame-1 pixel of the ground point")
    ap.add_argument("--look", default="c", choices=["c", "card"])
    ap.add_argument("--start", type=float, default=0.3, help="seconds before the stem starts drawing")
    ap.add_argument("--label", default="34 Albany Avenue")
    ap.add_argument("--sub", default="Currumbin")
    ap.add_argument("--scale", type=float, default=1.0, help="pin size multiplier (9:16 reels read small at 1.0; 1.4 on phone)")
    a = ap.parse_args()
    job = os.path.abspath(a.job)
    cam = json.load(open(os.path.join(job, "camera.json")))
    shot = json.load(open(os.path.join(job, "shot.json")))
    w, h = cam["width"], cam["height"]
    fps = shot["fps"][0] / shot["fps"][1]
    track = ground.track([a.at], cam)

    # Sizes from the Katrina pin (4K, Lita Ct stills scale): C° ~194 px wide, stem ~757 px
    k = w / 1400 * a.scale
    mark = Image.open(MARK).convert("RGBA")
    mw = round(68 * k)
    mark = mark.resize((mw, round(mark.height * mw / mark.width)), Image.LANCZOS)
    stem_len, stem_w, gap = round(200 * k), max(2, round(2.5 * k)), round(10 * k)
    if a.look == "card":
        f1, f2 = ImageFont.truetype(FONT, round(30 * k)), ImageFont.truetype(FONT_REG, round(20 * k))

    lay = os.path.join(job, "render", f"pin_{a.look}")
    os.makedirs(lay, exist_ok=True)
    for i, p in enumerate(track):
        t = i / fps - a.start
        s, m = ease(t / 0.7), ease((t - 0.5) / 0.6)
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        gx, gy = float(p[0][0]), float(p[0][1])
        if s > 0:
            top = gy - stem_len * s
            d.rectangle([gx - stem_w / 2, top, gx + stem_w / 2, gy], fill=(255, 255, 255, 255))
            r = 2.2 * stem_w
            d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(255, 255, 255, round(255 * s)))
        if m > 0:
            sc = 0.92 + 0.08 * m
            mm = mark.resize((max(1, round(mark.width * sc)), max(1, round(mark.height * sc))), Image.LANCZOS)
            mm.putalpha(mm.getchannel("A").point(lambda v: round(v * m)))
            y = gy - stem_len - gap
            if a.look == "card":
                lay_txt = Image.new("RGBA", (w, h), (0, 0, 0, 0))
                dt = ImageDraw.Draw(lay_txt)
                b1, b2 = dt.textbbox((0, 0), a.label, font=f1), dt.textbbox((0, 0), a.sub, font=f2)
                y2 = y - (b2[3] - b2[1])
                y1 = y2 - round(8 * k) - (b1[3] - b1[1])
                dt.text((gx - (b2[2] - b2[0]) / 2 - b2[0], y2 - b2[1]), a.sub, font=f2, fill=(255, 255, 255, 230))
                dt.text((gx - (b1[2] - b1[0]) / 2 - b1[0], y1 - b1[1]), a.label, font=f1, fill=(255, 255, 255, 255))
                lay_txt.putalpha(lay_txt.getchannel("A").point(lambda v: round(v * m)))
                img.alpha_composite(lay_txt)
                y = y1 - round(14 * k)
            img.alpha_composite(mm, (round(gx - mm.width / 2), round(y - mm.height)))
        img.save(os.path.join(lay, f"b_{i + 1:04d}.png"))

    out = os.path.join(job, "out")
    os.makedirs(out, exist_ok=True)
    rate = f"{shot['fps'][0]}/{shot['fps'][1]}"
    seq = os.path.join(lay, "b_%04d.png")
    run = lambda *c: subprocess.run(["ffmpeg", "-v", "error", "-y", *c], check=True)
    run("-framerate", rate, "-i", seq, "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
        os.path.join(out, f"pin_{a.look}_alpha.mov"))
    # Soft drop shadow so the white reads over bright roofs, then comp over the plate
    run("-i", shot["clip"], "-framerate", rate, "-i", seq, "-filter_complex",
        "[1]split[g][s];[s]colorchannelmixer=rr=0:gg=0:bb=0:aa=0.35,gblur=sigma=6[sh];"
        "[0][sh]overlay=3:3[b];[b][g]overlay=0:0:format=auto,format=yuv420p",
        "-map", "0:a?", "-c:v", "libx264", "-crf", "12", "-c:a", "copy", os.path.join(out, f"pin_{a.look}.mp4"))
    pick = min(len(track), round((a.start + 1.6) * fps))
    run("-ss", f"{pick / fps:.3f}", "-i", os.path.join(out, f"pin_{a.look}.mp4"), "-frames:v", "1",
        os.path.join(job, f"pilot_pin_{a.look}.png"))
    print(f"pin {a.look}: {len(track)} frames -> {out}")


if __name__ == "__main__":
    main()
