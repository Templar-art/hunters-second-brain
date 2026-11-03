#!/usr/bin/env python3
"""Site plan from the address alone: QLD cadastre lot + QLD government aerial -> faded cut-out.

    sitegen.py <job slug> ["address"]     # address defaults to job.json's

Writes jobs/<slug>/work/site.png and records in job.json:
  site_plan  path to the image the page uses
  site       {lotplan, lot_area_m2 (cadastre, 'sourced'), rotation_deg, m_per_px, imagery}
Markers are NOT placed here: job.json "site_markers" [{"label", "x", "y"}] (0-1 of the image) are set by a
person in review. The legend lists the marker labels in order.
"""
import json
import math
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "drone-pin"))
import drone_pin  # noqa: E402  (cadastre lookup lives there)

IMAGERY = ("https://spatial-img.information.qld.gov.au/arcgis/rest/services/Basemaps/"
           "LatestStateProgram_AllUsers/ImageServer/exportImage")
R = 6378137.0


def qld_address(address):
    """QLD's address register writes units as 'U53/3 …'; accept '53/3 …' too."""
    a = re.sub(r",|\bQLD\b|\b\d{4}\b", " ", address).strip()
    return re.sub(r"^(\d+[A-Z]?)/", r"U\1/", a, flags=re.I)


def merc(lon, lat):
    return R * math.radians(lon), R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def fetch(bb, n):
    q = urllib.parse.urlencode(dict(bbox=",".join(f"{v:.3f}" for v in bb), bboxSR=3857, imageSR=3857,
                                    size=f"{n},{n}", format="png", f="image"))
    with urllib.request.urlopen(f"{IMAGERY}?{q}", timeout=90) as r:
        return Image.open(__import__("io").BytesIO(r.read())).convert("RGB")


def build(address, out_png, context=0.55, n=2000, flip=False):
    rec, ring = drone_pin.lookup(qld_address(address))
    lat0 = ring[0][1]
    P = np.array([merc(x, y) for x, y in ring])
    k = math.cos(math.radians(lat0))  # mercator metres -> ground metres
    c = P.mean(0)
    # long axis of the lot -> vertical on the page (the deliverables show lots upright)
    u, s, vt = np.linalg.svd(P - c)
    ax = vt[0]
    rot = math.degrees(math.atan2(ax[0], ax[1]))  # angle of long axis from north, degrees
    span = np.ptp(P, 0).max()
    half = span * (0.5 + context) * 1.42  # room to rotate without empty corners
    bb = (c[0] - half, c[1] - half, c[0] + half, c[1] + half)
    im = fetch(bb, n)
    px = lambda q: ((q[:, 0] - bb[0]) / (2 * half) * n, (bb[3] - q[:, 1]) / (2 * half) * n)
    X, Y = px(P)
    # (service max 2048 px high)
    # rotate image + ring about the centre so the long axis is vertical
    def turned(a):
        t = math.radians(a)
        dx, dy = X - n / 2, Y - n / 2
        return n / 2 + dx * math.cos(t) - dy * math.sin(t), n / 2 + dx * math.sin(t) + dy * math.cos(t)
    # pick the turn (and its 180 twin, via flip) that stands the lot upright; flip=True turns it 180
    cands = [((a + 90) % 180) - 90 for a in (rot, -rot)]
    rot = max(cands, key=lambda a: np.ptp(turned(a)[1]) / np.ptp(turned(a)[0]))
    if flip:
        rot += 180
    Xr, Yr = turned(rot)
    im = im.rotate(-rot, resample=Image.BICUBIC, center=(n / 2, n / 2))
    # crop to the lot plus context
    w, h = np.ptp(Xr), np.ptp(Yr)
    pad = max(w, h) * context * 0.5
    box = (int(Xr.min() - pad * 1.2), int(Yr.min() - pad * 0.45), int(Xr.max() + pad * 1.2), int(Yr.max() + pad * 0.45))
    im = im.crop(box)
    im.save(Path(out_png).with_name('site-raw.png'))  # unsoftened crop: input for an illustrated pass
    ring_px = [(x - box[0], y - box[1]) for x, y in zip(Xr, Yr)]
    # soften: a touch brighter/airier like the finals, then a feathered rounded-rect fade to white
    arr = np.asarray(im).astype(np.float32)
    arr = arr * 0.9 + 255 * 0.1
    im = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
    W, H = im.size
    mask = Image.new("L", (W, H), 0)
    f = int(min(W, H) * 0.09)
    ImageDraw.Draw(mask).rounded_rectangle((f, f, W - f, H - f), radius=f * 2, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(f * 0.8))
    out = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    out.paste(im, (0, 0), mask)
    d = ImageDraw.Draw(out)
    d.line(ring_px + [ring_px[0]], fill=(255, 255, 255, 235), width=max(3, W // 260))
    out.save(out_png)
    m_per_px = 2 * half / n * k
    return {"lotplan": rec["lotplan"], "address_register": rec["address"],
            "lot_area_m2": rec.get("lot_area"), "lot_area_source": "QLD cadastre (DCDB)",
            "rotation_deg": round(rot, 1), "m_per_px": round(m_per_px, 4),
            "imagery": "QLD Spatial Imagery Subscription Plan, latest public state program",
            "lot_px": [[round(x, 1), round(y, 1)] for x, y in ring_px], "size": [W, H]}


def main(slug, address=None):
    job = HERE / "jobs" / slug
    data = json.loads((job / "job.json").read_text())
    address = address or data.get("address")
    if not address:
        raise SystemExit("No address: pass one or set it in the job.")
    png = job / "work" / "site.png"
    data["site"] = build(address, png, flip=bool(data.get("site_flip")))
    data["site_plan"] = str(png)
    data.setdefault("site_markers", [])
    if not data.get("land_area") and data["site"]["lot_area_m2"]:
        data["land_area_suggested"] = data["site"]["lot_area_m2"]  # a person confirms; never auto-printed
    (job / "job.json").write_text(json.dumps(data, indent=1))
    print(png, {k: v for k, v in data["site"].items() if k != "lot_px"})


if __name__ == "__main__":
    main(*sys.argv[1:3])
