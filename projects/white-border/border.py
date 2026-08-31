#!/usr/bin/env python3
"""White-border framing for 10x Visuals stills.

Puts a clean white mat around a photo for Instagram grid posts. Unlike the
first pass (24 Aug, SaltPM Kingscliff), the border is computed off the long
edge so the margin is optically even on every side, and the canvas can be
locked to a single aspect ratio so a mixed portrait/landscape carousel reads
as one consistent grid.

    python3 border.py IMAGE_OR_FOLDER [...] [options]

Common uses:
    # match the 24 Aug SaltPM look, but with even margins
    python3 border.py ~/Downloads/shoot --border 12 --ratio native

    # carousel-safe: every frame comes out 4:5 with the same mat
    python3 border.py ~/Downloads/shoot --border 8 --ratio 4:5
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}
RATIOS = {"1:1": 1.0, "4:5": 4 / 5, "5:4": 5 / 4, "3:4": 3 / 4, "9:16": 9 / 16}


def collect(paths):
    out = []
    for raw in paths:
        p = Path(raw).expanduser()
        if p.is_dir():
            out += sorted(f for f in p.iterdir() if f.suffix.lower() in EXTS)
        elif p.suffix.lower() in EXTS:
            out.append(p)
        else:
            print(f"skip (not an image): {p}", file=sys.stderr)
    return out


def frame(img, border_pct, ratio, bottom_weight, colour):
    """Mat `img` on a `colour` canvas.

    border_pct is a share of the photo's LONG edge, so the mat reads the same
    thickness whether the frame is portrait or landscape.
    """
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    w, h = img.size
    margin = round(max(w, h) * border_pct / 100)

    canvas_w, canvas_h = w + margin * 2, h + margin * 2
    if ratio is not None:
        # grow the short side only — the photo is never cropped
        target = ratio  # width / height
        if canvas_w / canvas_h > target:
            canvas_h = round(canvas_w / target)
        else:
            canvas_w = round(canvas_h * target)

    x = (canvas_w - w) // 2
    free_v = canvas_h - h
    # bottom_weight 1.0 = dead centre; >1 sits the photo higher, the way a
    # print is matted so the bottom margin carries a little more visual weight
    y = round(free_v / (1 + bottom_weight))

    canvas = Image.new("RGB", (canvas_w, canvas_h), colour)
    canvas.paste(img, (x, y))
    return canvas


def main():
    ap = argparse.ArgumentParser(description="Add a white mat to photos for IG.")
    ap.add_argument("inputs", nargs="+", help="image files and/or folders")
    ap.add_argument("--border", type=float, default=12.0,
                    help="mat thickness as %% of the photo's long edge (default 12, the 24 Aug SaltPM setting)")
    ap.add_argument("--ratio", default="native",
                    help="output aspect: native, 1:1, 4:5, 5:4, 3:4, 9:16 (default native)")
    ap.add_argument("--bottom-weight", type=float, default=1.0,
                    help="1.0 centres the photo; 1.15 leaves a slightly heavier bottom margin")
    ap.add_argument("--colour", default="#ffffff", help="mat colour (default pure white)")
    ap.add_argument("--out", default=None,
                    help="output folder (default: a 'bordered' folder beside the first input)")
    ap.add_argument("--suffix", default="-border", help="filename suffix (default -border)")
    ap.add_argument("--max-edge", type=int, default=2048,
                    help="cap the finished canvas's long edge, in px (default 2048; 0 keeps full res)")
    ap.add_argument("--quality", type=int, default=95, help="JPEG quality (default 95)")
    args = ap.parse_args()

    files = collect(args.inputs)
    if not files:
        sys.exit("no images found")

    if args.ratio.lower() in ("native", "none"):
        ratio = None
    elif args.ratio in RATIOS:
        ratio = RATIOS[args.ratio]
    else:
        sys.exit(f"unknown ratio {args.ratio!r} — use native or one of {', '.join(RATIOS)}")

    out_dir = Path(args.out).expanduser() if args.out else files[0].parent / "bordered"
    out_dir.mkdir(parents=True, exist_ok=True)

    for f in files:
        with Image.open(f) as img:
            framed = frame(img, args.border, ratio, args.bottom_weight, args.colour)
        if args.max_edge and max(framed.size) > args.max_edge:
            framed.thumbnail((args.max_edge, args.max_edge), Image.LANCZOS)
        dest = out_dir / f"{f.stem}{args.suffix}.jpg"
        framed.save(dest, "JPEG", quality=args.quality, subsampling=0, optimize=True)
        print(f"{f.name}  ->  {dest.name}  ({framed.width}x{framed.height})")

    print(f"\n{len(files)} file(s) written to {out_dir}")


if __name__ == "__main__":
    main()
