#!/usr/bin/env /usr/bin/python3
"""
Assemble a flat, drag-and-drop folder of the final posts in POSTING ORDER.
Singles -> NN_slug.png ; carousels -> NN_slug_1.png .. _M.png (grouped + ordered).
Re-runnable: wipes and rebuilds READY-TO-POST/.
"""
import os, glob, shutil

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "out")
DEST = os.path.join(HERE, "READY-TO-POST")

# (posting order slug, source post number, is_carousel)
PLAN = [
    ("welcome",              1,  False),
    ("portfolio-fits-life",  10, False),
    ("who-this-is-for",      2,  True),
    ("start-with-outcome",   13, False),
    ("why-qld",              3,  False),
    ("good-questions",       11, False),
    ("strategy-tip-01",      8,  False),
    ("brand-stamp",          15, False),
    ("common-mistakes",      4,  True),
    ("time-in-market",       22, False),
    ("growth-vs-cashflow",   18, False),
    ("different-suburbs",    12, False),
    ("strategy-chat",        6,  False),
    ("clarity",              14, False),
    ("strategy-balances",    9,  False),
    ("know-your-numbers",    21, False),
    ("strategy-tip-02",      16, False),
    ("case-study",           5,  True),
    ("buy-well",             23, False),
    ("what-is-equity",       19, False),
    ("right-team",           7,  False),
    ("rentvesting",          20, False),
    ("strategy-tip-03",      17, False),
]

def build():
    if os.path.isdir(DEST):
        shutil.rmtree(DEST)
    os.makedirs(DEST)
    for i, (slug, post, carousel) in enumerate(PLAN, start=1):
        src_dir = os.path.join(OUT, f"post-{post:02d}")
        if carousel:
            slides = sorted(glob.glob(os.path.join(src_dir, f"post-{post:02d}-*.png")))
            for s, path in enumerate(slides, start=1):
                dst = os.path.join(DEST, f"{i:02d}_{slug}_{s}.png")
                shutil.copy2(path, dst)
            print(f"{i:02d} {slug:22} carousel ({len(slides)} slides)")
        else:
            src = os.path.join(src_dir, f"post-{post:02d}.png")
            shutil.copy2(src, os.path.join(DEST, f"{i:02d}_{slug}.png"))
            print(f"{i:02d} {slug:22} single")
    n = len(glob.glob(os.path.join(DEST, "*.png")))
    print(f"\n{len(PLAN)} posts, {n} image files -> {os.path.relpath(DEST, HERE)}/")

if __name__ == "__main__":
    build()
