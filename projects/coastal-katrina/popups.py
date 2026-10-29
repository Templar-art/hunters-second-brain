"""Flythrough reel pop-ups (9:16, 1080x1920, 23.976 fps, ProRes 4444 on alpha) for 34 Albany Ave.

Look: deliberately not the cinematic reel's centred cards. A thin white stem (the C° pin's stem, turned into a tag)
grows down at the left margin and a short sentence-case line rises out of a mask beside it, holds, then lifts away.
Helvetica Neue Medium like her film captions, a soft shadow for legibility, everything inside the safe area
(left 80 px margin, sits at 62% height: clear of the IG caption/UI zone at the bottom and the top bar).

Cues are on the reel timeline (song 'Get Down' VO cut, 37.85 s, VO starting 1.0 s in), each snapped to a beat of
the song and starting on or just after the VO word it echoes. One pop-up on screen at a time.

--cut flythrough36 uses the cues for Hunter's own 36.04 s cut (Flythrough.mp4, 29 Oct): VO from 0.0, his C° pin
baked in over the coast aerial 23.3-25.5 and the end card from 32.5, so no cue goes near either.

Usage: python3 popups.py [--cut planned|flythrough36] [--preview BG.mp4 MIX.wav]
  -> out/popups-9x16[-<cut>]/NN-<slug>.mov (one per cue), ALL-popups-<len>s.mov (all cues on one track)
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
import make_cards as mc  # noqa: E402

W, H, FPS = 1080, 1920, 24000 / 1001
LENGTH = 37.85
OUT = mc.OUT / "popups-9x16"
X0, Y0 = 80, int(H * 0.62)          # stem top-left
STEM_W, STEM_H, GAP = 4, 78, 26
SIZE = 54

# (in, out, text): in = first frame of the stem; text is fully up ~0.6 s later
CUES = [
    (2.95, 5.55, "34 Albany Avenue, Currumbin"),      # VO "...heart of Currumbin Hill" 3.2
    (8.89, 10.95, "Minutes to the beach"),            # the chorus drop; VO "just minutes from the beach" 8.4-10.3
    (11.12, 13.15, "Four bedrooms · Three levels"),  # VO "Spread across three levels" 10.7-12.2 (four bedroom said at 4.8)
    (13.35, 15.20, "Private master retreat"),         # VO 13.5-14.6
    (17.80, 20.40, "Pool and cabana"),                # downbeat right after "Outside," 17.54
    (23.74, 26.40, "Beaches, creeks and cafes"),      # VO "Currumbin's beaches, creeks and cafes close by" 23.4-26.7
]
# Hunter's cut, word times from Whisper on its audio: each cue starts on the word it echoes, inside one shot where it can
CUES_36 = [
    (3.40, 5.60, "34 Albany Avenue, Currumbin"),      # after the wordmark (out by 3.2); house aerial -> frangipani
    (7.26, 9.30, "Minutes to the beach"),             # "just minutes from the beach" 7.26, over the man fishing
    (10.18, 12.20, "Four bedrooms · Three levels"),  # "Spread across three levels" 10.18
    (12.84, 14.70, "Private master retreat"),         # "private master retreat" 12.84
    (16.82, 19.40, "Pool and cabana"),                # "Outside," 16.82; pool from the 16.27 cut
    (25.60, 27.80, "Beaches, creeks and cafes"),      # boat -> Beach House cafe, after the pin shot ends 25.53
]
CUTS = {"planned": (CUES, LENGTH, "popups-9x16"), "flythrough36": (CUES_36, 36.04, "popups-9x16-flythrough36")}
FONT = mc.font(mc.MEDIUM, SIZE)
RIGHT_SAFE = 170                    # IG reel like/comment/share column sits on the right edge at this height
for _, _, txt in CUES + CUES_36:
    right = X0 + STEM_W + GAP + ImageDraw.Draw(Image.new("L", (1, 1))).textlength(txt, font=FONT)
    assert right <= W - RIGHT_SAFE, f"pop-up runs into the IG button column: {txt!r} ends at {right:.0f}px"


def ease(t):
    t = min(max(t, 0.0), 1.0)
    return 1 - (1 - t) ** 3


def draw(text, t, dur):
    """One frame of a pop-up at local time t (s) of a dur-long cue."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out = ease((t - (dur - 0.4)) / 0.4)                      # exit: fade + lift
    stem = ease(t / 0.35) * (1 - out)
    txt = ease((t - 0.15) / 0.5)
    lift = -14 * out
    d = ImageDraw.Draw(img)
    if stem > 0:
        d.rectangle([X0, Y0 + lift, X0 + STEM_W - 1, Y0 + lift + STEM_H * ease(t / 0.35)], fill=(255, 255, 255, round(255 * (1 - out))))
    if txt > 0:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(layer)
        top, bottom = FONT.getbbox("H")[1], FONT.getbbox("H")[3]
        ty = Y0 + STEM_H / 2 - (top + bottom) / 2 + 22 * (1 - txt) + lift   # rises 22 px into place
        dl.text((X0 + STEM_W + GAP, ty), text, font=FONT, fill=(255, 255, 255, 255))
        # mask: text is revealed from a line at the stem's bottom edge upward (rises out of nothing)
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).rectangle([0, 0, W, Y0 + STEM_H + 6 + lift], fill=round(255 * min(1, txt * 1.4) * (1 - out)))
        layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", (W, H), 0), mask))
        img.alpha_composite(layer)
    # soft shadow under everything for bright skies / white walls
    a = img.getchannel("A")
    if a.getbbox():
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sh.putalpha(a.filter(ImageFilter.GaussianBlur(6)).point(lambda v: round(v * 0.45)))
        base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        base.alpha_composite(sh, (2, 3))
        base.alpha_composite(img)
        img = base
    return img


def encode(frames, n, path):
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
                          "-r", "24000/1001", "-i", "-", "-c:v", "prores_ks", "-profile:v", "4444",
                          "-pix_fmt", "yuva444p10le", "-vendor", "apl0", str(path)], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frames(i / FPS).tobytes())
    p.stdin.close(); p.wait()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", nargs=2, metavar=("BG_VIDEO", "MIX_WAV"))
    ap.add_argument("--cut", default="planned", choices=list(CUTS))
    a = ap.parse_args()
    global CUES, LENGTH, OUT
    CUES, LENGTH, sub = CUTS[a.cut]
    OUT = mc.OUT / sub
    OUT.mkdir(parents=True, exist_ok=True)
    blank = np.zeros((H, W, 4), np.uint8)
    for k, (t0, t1, text) in enumerate(CUES, 1):
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        dur = t1 - t0
        encode(lambda t: np.asarray(draw(text, t, dur)), round(dur * FPS), OUT / f"{k:02d}-{slug}-at-{t0:.2f}s.mov")
        draw(text, 1.2, dur).save(OUT / f"{k:02d}-{slug}.png")

    def whole(t):
        for t0, t1, text in CUES:
            if t0 <= t < t1:
                return np.asarray(draw(text, t - t0, t1 - t0))
        return blank
    allp = OUT / f"ALL-popups-{LENGTH:.2f}s.mov"
    encode(whole, round(LENGTH * FPS), allp)
    if a.preview:
        bg, mix = a.preview
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", bg, "-i", str(allp), "-i", mix,
                        "-filter_complex", f"[0]scale={W}:{H},setsar=1[b];[b][1]overlay=format=auto,format=yuv420p[v]",
                        "-map", "[v]", "-map", "2:a", "-t", f"{LENGTH}", "-c:v", "libx264", "-crf", "16", "-c:a", "aac",
                        "-b:a", "256k", str(OUT / f"PREVIEW-popups-{a.cut}.mp4")], check=True)
    print("written to", OUT)


if __name__ == "__main__":
    main()
