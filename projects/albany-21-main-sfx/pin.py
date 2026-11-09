"""REAL Specialists pin on the wide drone shot of 21 Albany Ave Main.mp4.

Shot = Main frames 872-917 (36.37-38.29 s). Roof ridge tracked with LK + partial affine
(work/pin_track.json, 1080p coords). Orange REAL logo sits on the sky, thin white line down to
the ridge, centred under the logo. Renders a 4K ProRes 4444 alpha overlay (starts at Main frame 872)
and the RGBA frames for a 1080p preview composite.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).parent
LOGO = "/Volumes/10X SSD3/21 Albany Avenue, Currumbin/Video/REAL Overlays/03 REAL pin logo only.png"
S = 2                   # 1080 -> 4K
LOGO_W = 280            # px @1080
LINE_W = 4              # px @1080
LOGO_BOTTOM = 440       # y @1080 of the logo's bottom at the first frame (horizon ~484)
GAP = 12
FADE_START, FADE_LEN = 3, 8

tr = json.load(open(HERE / "work/pin_track.json"))
tips = np.array(tr["tip"]) * S
logo = Image.open(LOGO).convert("RGBA")
lw = LOGO_W * S
logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
lh = logo.height
out = HERE / "work/pin_frames"; out.mkdir(exist_ok=True)
dy = tips[0][1] - LOGO_BOTTOM * S   # tip-to-logo-bottom distance, held constant (pin rides with the roof)
W, H = 1920 * S, 1080 * S
for k, (x, y) in enumerate(tips):
    t = np.clip((k - FADE_START) / FADE_LEN, 0, 1); a = t * t * (3 - 2 * t)
    fr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lb = y - dy
    fr.alpha_composite(logo, (int(round(x - lw / 2)), int(round(lb - lh))))
    line = Image.new("RGBA", (LINE_W * S, int(round(y - (lb + GAP * S)))), (255, 255, 255, 255))
    fr.alpha_composite(line, (int(round(x - LINE_W * S / 2)), int(round(lb + GAP * S))))
    if a < 1:
        r, g, b, al = fr.split(); fr = Image.merge("RGBA", (r, g, b, al.point(lambda v: int(v * a))))
    fr.save(out / f"p_{k:03d}.png")
dst = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "result"
dst.mkdir(parents=True, exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "24000/1001", "-i", str(out / "p_%03d.png"),
                "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-vendor", "apl0",
                str(dst / "04 REAL pin wide drone 4K (Main 00-00-36-08).mov")], check=True)
print("frames", len(tips), "->", dst)
