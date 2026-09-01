#!/usr/bin/env python3
"""Renders every artboard to PNG, one folder per post.

Artboards are static HTML, so they render outside the canvas runtime: inline the
images as data URIs, set the body to exactly 1080 x 1440, and screenshot headless
at 2x for 2160 x 2880 masters.

    python3 export_png.py             # every page, 2x masters
    python3 export_png.py --scale 1   # 1080 x 1440
    python3 export_png.py --page 1    # one page only
"""
import base64, json, mimetypes, os, re, shutil, subprocess, sys, tempfile

W, H = 1080, 1440
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.abspath(os.path.join("..", "exports"))
FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Poppins:wght@300;400;500;600&display=swap")

scale = 1 if "--scale" in sys.argv and sys.argv[sys.argv.index("--scale") + 1] == "1" else 2
only = int(sys.argv[sys.argv.index("--page") + 1]) if "--page" in sys.argv else None
_cache = {}


def datauri(name):
    if name not in _cache:
        mt = mimetypes.guess_type(name)[0] or "image/png"
        with open(name, "rb") as fh:
            _cache[name] = f"data:{mt};base64," + base64.b64encode(fh.read()).decode()
    return _cache[name]


def standalone(dc_path):
    src = open(dc_path).read()
    style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
    body = re.search(r"</helmet>(.*?)</x-dc>", src, re.S).group(1)
    for m in set(re.findall(r'src="([^"]+\.(?:jpg|jpeg|png))"', body)):
        body = body.replace(f'src="{m}"', f'src="{datauri(m)}"')
    return (f'<!doctype html><meta charset="utf-8">'
            f'<link rel="stylesheet" href="{FONTS}">'
            f"<style>{style}"
            f"html,body{{margin:0;padding:0;width:{W}px;height:{H}px;overflow:hidden}}"
            f"</style>{body}")


def slug(text):
    text = re.sub(r"[^\w\s-]", "", text).strip()
    return re.sub(r"[\s_]+", "-", text)


def main():
    if not os.path.exists(CHROME):
        sys.exit("Google Chrome not found — needed for headless rendering.")
    canvas = json.load(open("canvas.json"))
    pages = {p["id"]: p["name"] for p in canvas["pages"]}
    order = {pid: i for i, pid in enumerate(pages, start=1)}

    by_page = {}
    for ab in canvas["artboards"]:
        by_page.setdefault(ab.get("page", "page-1"), []).append(ab)

    if only is None and os.path.isdir(OUT):
        shutil.rmtree(OUT)
    total = 0
    tmp = tempfile.mkdtemp()
    for pid, boards in by_page.items():
        if only is not None and order[pid] != only:
            continue
        boards.sort(key=lambda a: a["x"])
        folder = os.path.join(OUT, f"{order[pid]:02d}-{slug(pages[pid])}")
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)
        for i, ab in enumerate(boards, start=1):
            dc = ab["file"]
            html = os.path.join(tmp, "frame.html")
            with open(html, "w") as fh:
                fh.write(standalone(dc))
            png = os.path.join(folder, f"{i:02d}-{dc[:-8]}.png")
            subprocess.run([
                CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                f"--force-device-scale-factor={scale}",
                f"--window-size={W},{H}",
                "--virtual-time-budget=9000",
                f"--screenshot={png}", f"file://{html}",
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            if os.path.exists(png):
                total += 1
            else:
                print("FAILED", dc)
        print(f"{os.path.basename(folder)}: {len(boards)}")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{total} PNGs at {W*scale} x {H*scale} in {OUT}")


if __name__ == "__main__":
    main()
