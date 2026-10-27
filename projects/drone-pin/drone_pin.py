"""Drone photo pinning: auto-places the Kollosche K pin and the lot outline on
DJI drone stills, from the drone's own position data and the Queensland
cadastre. You approve or nudge each photo in a browser, then it renders.

How it works:
  1. The address gives the lot/plan and its surveyed boundary (QLD Spatial,
     free and public). The pin tip goes on the lot's interior point at roof height.
  2. Each photo's DJI XMP gives where the drone was (GPS, height above takeoff)
     and where the gimbal pointed (yaw, pitch, roll). EXIF gives the 35 mm focal
     length. Lightroom's crop (crs:Crop*) survives export, so the original frame
     is rebuilt and the lot is projected through it onto the exported photo.
  3. Drone compass and GPS drift by a degree or two. Drag a pin tip in the
     review page and it solves that photo's yaw/pitch correction; "Apply to
     flight" carries the median correction to every photo you haven't touched.
  4. The outline is freely editable per photo (corners, move, add/delete
     points), a "behind" brush hides it where buildings stand in front, and
     location pins (label + auto distance) clicked on one photo appear on every
     photo that sees that spot.

Usage (~/.venvs/typeset python: OpenCV, SciPy, Pillow and HarfBuzz for kerned labels):
  PY=~/.venvs/typeset/bin/python
  $PY -I drone_pin.py init   <job_dir> <photos_dir> --address "47 Somerset Drive Mudgeeraba"
  $PY -I drone_pin.py review <job_dir>          # opens the review page
  $PY -I drone_pin.py render <job_dir>          # finished JPGs + transparent PNG overlays
"""
import base64
import os
import argparse
import http.server
import io
import json
import math
import re
import shutil
import subprocess
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.optimize import least_squares

Image.MAX_IMAGE_PIXELS = None  # 100 MP drone exports are ours, not a decompression bomb

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
QLD = "https://spatial-gis.information.qld.gov.au/arcgis/rest/services/PlanningCadastre/LandParcelPropertyFramework/MapServer"
DIAG35 = math.hypot(36, 24)
ROOF_H = 6.0          # default metres above ground for the pin tip (--roof-height per site)
TARGET_MAX_RANGE = 120  # m: only top-downs and close shots may set the house (a 245 m drag moved it metres off)
PREVIEW = 3200        # long edge of review previews (px); sharp enough to zoom in on
EXTS = {".jpg", ".jpeg", ".tif", ".tiff", ".png"}

# Pin and outline, matched to Kollosche's own listing stills (Hunter's refs,
# 2026-10-27): a navy square badge with a thin white border and a white K,
# sitting straight on a thin white line. Fractions of photo height unless noted.
# Proportions measured from Kollosche's own 'Kollosche Map Pin.png' (Drive, 3026 The Boulevard):
# border 5% and K 54% of the badge, pin line 5.5% of the badge width.
BADGE, BADGE_K, BADGE_BORDER, PIN_LINE = 0.085, 0.54, 0.05, 0.055   # badge side; K width and border as fractions of the badge
BADGE_FILL = (1, 26, 59)                             # Kollosche Blue #011A3B
LINE_W, LINE_LEN, TOP_MARGIN = 0.0024, 0.42, 0.05   # LINE_W: location-pin lines
BLACKOUT_FEATHER = 0.0015                            # blackout edge softness, of photo width
OUTLINE_W = 0.0033                                   # of photo width, x per-photo outline_w (0.5-3)
# Subtle drop shadow under the outline only (Hunter, 2026-10-27): soft, slightly
# below, low opacity. All in multiples of the outline width.
SHADOW_OFFSET, SHADOW_BLUR, SHADOW_OPACITY = 0.5, 0.6, 0.6
# Location pins: dot on the spot, thin line up, label (Kräftig caps) over the
# distance (Buch). Fractions of photo height; tracking in em.
PLACE_DOT, PLACE_LINE, PLACE_GAP = 0.0032, 0.07, 0.009
PLACE_CAP, PLACE_SUB, PLACE_TRACK, PLACE_LEAD = 0.0135, 0.0095, 0.06, 0.65
FONT_K = os.path.expanduser("~/Library/Fonts/SöhneBreit-Kräftig.otf")
FONT_B = os.path.expanduser("~/Library/Fonts/SöhneBreit-Buch.otf")


# --- cadastre -----------------------------------------------------------------

def qld(layer, **params):
    url = f"{QLD}/{layer}/query?" + urllib.parse.urlencode({"f": "json", **params})
    with urllib.request.urlopen(url, timeout=30) as r:
        d = json.load(r)
    if "error" in d:
        raise SystemExit(f"QLD cadastre error: {d['error']}")
    return d["features"]


def lookup(address):
    """Address -> (address record, lot boundary ring as [lon, lat])."""
    words = re.sub(r"[^A-Z0-9 /]", "", address.upper()).split()
    where = "UPPER(address) LIKE '" + "%".join(words) + "%'"
    hits = qld(0, where=where, outFields="address,lotplan,latitude,longitude", returnGeometry="false")
    if not hits:
        raise SystemExit(f"No QLD address matches '{address}'. Try the street number, name and suburb only.")
    if len(hits) > 1:
        names = sorted({h["attributes"]["address"] for h in hits})
        if len(names) > 1:
            raise SystemExit("Several addresses match, be more specific:\n  " + "\n  ".join(names[:15]))
    rec = hits[0]["attributes"]
    parcels = qld(4, where=f"lotplan='{rec['lotplan']}'", outFields="lotplan,lot_area", outSR="4326")
    if not parcels:
        raise SystemExit(f"No parcel found for lot/plan {rec['lotplan']}")
    rings = parcels[0]["geometry"]["rings"]
    ring = max(rings, key=len)
    if ring[0] == ring[-1]:
        ring = ring[:-1]
    rec["lot_area"] = parcels[0]["attributes"].get("lot_area")
    return rec, ring


def interior_point(poly):
    """The point deepest inside the polygon (metres): where the roof is most likely."""
    lo, hi = poly.min(0), poly.max(0)
    s = 0.25
    w, h = int((hi[0] - lo[0]) / s) + 3, int((hi[1] - lo[1]) / s) + 3
    mask = np.zeros((h, w), np.uint8)
    cv2.fillPoly(mask, [np.round((poly - lo) / s + 1).astype(np.int32)], 1)
    dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
    y, x = np.unravel_index(dist.argmax(), dist.shape)
    return lo + (np.array([x, y]) - 1) * s


# --- photo metadata + camera model ---------------------------------------------

def meta(path):
    b = path.read_bytes()
    dji = {k.decode(): v.decode() for k, v in re.findall(rb'drone-dji:([A-Za-z]+)="([^"]*)"', b)}
    crs = {k.decode(): v.decode() for k, v in re.findall(rb'crs:(Crop[A-Za-z]+|HasCrop)="([^"]*)"', b)}
    im = Image.open(path)
    W, H = im.size
    f35 = im.getexif().get_ifd(0x8769).get(0xA405)
    m = {"file": path.name, "w": W, "h": H, "f35": f35}
    need = ["GpsLatitude", "GpsLongitude", "RelativeAltitude", "GimbalYawDegree", "GimbalPitchDegree"]
    if not f35 or any(k not in dji for k in need):
        m["error"] = "no drone position data (export with All Metadata, or use the original file)"
        return m
    # Heading: the aircraft's FlightYawDegree. On the Mavic 4 Pro and Air 3S files
    # tested, GimbalYawDegree sits 40-55 degrees off true north while FlightYaw lands
    # the lot on the house (Somerset Dr, 7 photos, 2026-10-27).
    m.update(lat=float(dji["GpsLatitude"]), lon=float(dji["GpsLongitude"]), alt=float(dji["RelativeAltitude"]),
             yaw=float(dji.get("FlightYawDegree", dji["GimbalYawDegree"])), pitch=float(dji["GimbalPitchDegree"]),
             roll=float(dji.get("GimbalRollDegree", 0)), drone=dji.get("ProductName", ""))
    crop = [float(crs.get(k, d)) for k, d in (("CropLeft", 0), ("CropTop", 0), ("CropRight", 1), ("CropBottom", 1))]
    m["crop"] = crop if crs.get("HasCrop", "False") == "True" else [0, 0, 1, 1]
    m["crop_angle"] = float(crs.get("CropAngle", 0)) if crs.get("HasCrop") == "True" else 0.0
    return m


def enu(lat, lon, lat0, lon0):
    R = 6378137.0
    return np.array([math.radians(lon - lon0) * R * math.cos(math.radians(lat0)),
                     math.radians(lat - lat0) * R])


def project(m, pts, dyaw=0.0, dpitch=0.0, droll=0.0):
    """World points (E, N, U metres, origin under the takeoff point's datum but
    E/N relative to the drone) -> exported-photo pixels. Returns (uv, in_front)."""
    yaw, pitch, roll = (math.radians(m["yaw"] + dyaw), math.radians(m["pitch"] + dpitch), math.radians(m["roll"] + droll))
    fwd = np.array([math.sin(yaw) * math.cos(pitch), math.cos(yaw) * math.cos(pitch), math.sin(pitch)])
    right = np.array([math.cos(yaw), -math.sin(yaw), 0.0])
    down = np.cross(fwd, right)
    right, down = right * math.cos(roll) + down * math.sin(roll), down * math.cos(roll) - right * math.sin(roll)
    v = np.asarray(pts, float) - np.array([0, 0, m["alt"]])
    x, y, z = v @ right, v @ down, v @ fwd
    L, T, Rr, B = m["crop"]
    W0, H0 = m["w"] / (Rr - L), m["h"] / (B - T)        # original frame in export-pixel units
    f = m["f35"] / DIAG35 * math.hypot(W0, H0)
    zs = np.where(z > 1e-6, z, 1e-6)
    u, vv = W0 / 2 + f * x / zs, H0 / 2 + f * y / zs
    cx, cy = (L + Rr) / 2 * W0, (T + B) / 2 * H0          # crop centre in the original
    a = math.radians(m["crop_angle"])
    du, dv = u - cx, vv - cy
    ue = m["w"] / 2 + du * math.cos(a) + dv * math.sin(a)
    ve = m["h"] / 2 - du * math.sin(a) + dv * math.cos(a)
    return np.stack([ue, ve], 1), z > 0


def unproject(m, uv, z, dyaw=0.0, dpitch=0.0, droll=0.0):
    """Exported-photo pixel -> the ground point (E, N) where its ray hits height z."""
    yaw, pitch, roll = (math.radians(m["yaw"] + dyaw), math.radians(m["pitch"] + dpitch), math.radians(m["roll"] + droll))
    fwd = np.array([math.sin(yaw) * math.cos(pitch), math.cos(yaw) * math.cos(pitch), math.sin(pitch)])
    right = np.array([math.cos(yaw), -math.sin(yaw), 0.0])
    down = np.cross(fwd, right)
    right, down = right * math.cos(roll) + down * math.sin(roll), down * math.cos(roll) - right * math.sin(roll)
    L, T, Rr, B = m["crop"]
    W0, H0 = m["w"] / (Rr - L), m["h"] / (B - T)
    f = m["f35"] / DIAG35 * math.hypot(W0, H0)
    a = math.radians(m["crop_angle"])
    du, dv = uv[0] - m["w"] / 2, uv[1] - m["h"] / 2
    u = (L + Rr) / 2 * W0 + du * math.cos(a) - dv * math.sin(a)
    v = (T + B) / 2 * H0 + du * math.sin(a) + dv * math.cos(a)
    ray = fwd + right * (u - W0 / 2) / f + down * (v - H0 / 2) / f
    t = (z - m["alt"]) / ray[2]
    return ray[:2] * t


def set_target(m, site, uv):
    """Move the pin target to where this pixel's ray meets roof height."""
    e, n = unproject(m, uv, m.get("dz", 0.0) + site.get("roof_h", ROOF_H), m.get("dyaw", 0.0), m.get("dpitch", 0.0), m.get("droll", 0.0))
    site["tip"] = [m["lon"] + math.degrees(e / (6378137.0 * math.cos(math.radians(m["lat"])))),
                   m["lat"] + math.degrees(n / 6378137.0)]
    site["tip_from"] = m["file"]


def world(m, site, dz=0.0):
    """Site geometry in this photo's drone-centred ENU frame. dz = the lot's ground
    height above the takeoff point (hilly sites; solved from the photos you fix)."""
    lot = np.array([np.r_[enu(lat, lon, m["lat"], m["lon"]), dz] for lon, lat in site["ring"]])
    tip = np.r_[enu(site["tip"][1], site["tip"][0], m["lat"], m["lon"]), dz + site.get("roof_h", ROOF_H)]
    return tip, lot


def propose(m, site, dyaw=0.0, dpitch=0.0, droll=0.0, dz=None):
    """Re-project the site through this photo's (corrected) camera. A hand-edited
    outline and hand-placed location pins are kept as they are."""
    dz = m.get("dz", 0.0) if dz is None else dz
    tip_w, lot_w = world(m, site, dz)
    tip, tip_ok = project(m, [tip_w], dyaw, dpitch, droll)
    lot, lot_ok = project(m, lot_w, dyaw, dpitch, droll)
    inside = lambda p: 0 <= p[0] < m["w"] and 0 <= p[1] < m["h"]
    places = dict(m.get("places", {}))
    for pl in site.get("places", []):
        key = str(pl["id"])
        old = places.get(key, {})
        if old.get("manual"):
            continue
        w = np.r_[enu(pl["lat"], pl["lon"], m["lat"], m["lon"]), dz]
        uv, ok = project(m, [w], dyaw, dpitch, droll)
        seen = bool(ok[0] and inside(uv[0]))
        places[key] = {"xy": uv[0].round(1).tolist(), "on": old.get("on", seen) and seen, "manual": False}
    return {"tip": tip[0].round(1).tolist(), "tip_visible": bool(tip_ok[0] and inside(tip[0])),
            "lot": m["lot"] if m.get("manual") else lot.round(1).tolist(),
            "lot_visible": bool(lot_ok.all() and all(inside(p) for p in lot)),
            "places": places, "dyaw": dyaw, "dpitch": dpitch, "droll": droll, "dz": dz}


def place_distance(site, pl):
    d = float(np.linalg.norm(enu(pl["lat"], pl["lon"], site["tip"][1], site["tip"][0])))
    return f"{d / 1000:.1f} KM" if d >= 1000 else f"{round(d / 10) * 10:.0f} M"


def add_place(m, site, uv, label):
    """A location clicked on this photo: its ray meets the ground, and that spot
    becomes a place every photo can show."""
    e, n = unproject(m, uv, m.get("dz", 0.0), m.get("dyaw", 0.0), m.get("dpitch", 0.0), m.get("droll", 0.0))
    if not math.isfinite(e) or np.hypot(e, n) > 50000:
        raise ValueError("that point is at or above the horizon; click the ground under the place")
    pl = {"id": max([p["id"] for p in site.get("places", [])], default=0) + 1,
          "label": label.strip().upper(), "dist": True,
          "lon": m["lon"] + math.degrees(e / (6378137.0 * math.cos(math.radians(m["lat"])))),
          "lat": m["lat"] + math.degrees(n / 6378137.0), "from": m["file"]}
    site.setdefault("places", []).append(pl)
    return pl


def solve(m, site, anchors):
    """Yaw/pitch/roll correction that puts the dragged handles where the user put
    them. anchors: {"tip": [x, y], "0": [x, y], ...} (lot corners by index).
    One handle pins two of the three angles; a weak prior keeps the third near zero."""
    if not anchors:
        return [0.0, 0.0, 0.0]
    tip_w, lot_w = world(m, site, m.get("dz", 0.0))
    pts = [tip_w if k == "tip" else lot_w[int(k)] for k in anchors]
    tgt = np.array(list(anchors.values()), float)
    scale = math.hypot(m["w"], m["h"])

    def resid(d):
        uv, _ = project(m, pts, *d)
        return np.r_[((uv - tgt) / scale).ravel(), 0.002 * d]
    x = least_squares(resid, [m.get("dyaw", 0.0), m.get("dpitch", 0.0), m.get("droll", 0.0)]).x
    return [float(v) for v in x]


def flight_fix(done, site):
    """One compass offset + the lot's ground height, fitted to every handle you
    placed on approved photos. These two errors are shared by the whole flight;
    per-photo tilt and roll are not, so they don't carry."""
    def resid(x):
        r = []
        for m in done:
            tip_w, lot_w = world(m, site, x[1])
            pts = [tip_w if k == "tip" else lot_w[int(k)] for k in m["anchors"]]
            uv, _ = project(m, pts, x[0])
            r.append(((uv - np.array(list(m["anchors"].values()))) / math.hypot(m["w"], m["h"])).ravel())
        return np.r_[np.concatenate(r), 0.002 * x[0], 0.0002 * x[1]]
    # Ground height is only separable from tilt with photos at clearly different
    # ranges; otherwise fix it at the takeoff height and fit the compass alone.
    ranges = [np.linalg.norm(enu(site["tip"][1], site["tip"][0], m["lat"], m["lon"])) for m in done]
    if len(done) < 2 or max(ranges) < 2 * max(min(ranges), 1.0):
        x = least_squares(lambda v: resid([v[0], 0.0]), [0.0]).x
        return float(x[0]), 0.0
    x = least_squares(resid, [0.0, 0.0]).x
    return float(x[0]), float(x[1])


def default_mode(m):
    return "outline" if m["pitch"] <= -70 else "pin"


# --- job files -------------------------------------------------------------------

def load(job, name):
    return json.loads((job / name).read_text())


def save(job, name, data):
    (job / name).write_text(json.dumps(data, indent=1))


def cmd_init(a):
    job, photos = Path(a.job), Path(a.photos)
    (job / "previews").mkdir(parents=True, exist_ok=True)
    rec, ring = lookup(a.address)
    lat0, lon0 = rec["latitude"], rec["longitude"]
    poly = np.array([enu(lat, lon, lat0, lon0) for lon, lat in ring])
    ip = interior_point(poly)
    tip = [lon0 + math.degrees(ip[0] / (6378137.0 * math.cos(math.radians(lat0)))),
           lat0 + math.degrees(ip[1] / 6378137.0)]
    site = {"address": rec["address"], "lotplan": rec["lotplan"], "lot_area": rec["lot_area"],
            "ring": ring, "tip": tip, "roof_h": a.roof_height, "photos": str(photos.resolve())}
    save(job, "site.json", site)
    print(f"{rec['address']}  lot {rec['lotplan']}  {rec['lot_area']} m²  {len(ring)} corners")

    marks = {}
    for p in sorted(photos.iterdir()):
        if p.suffix.lower() not in EXTS:
            continue
        m = meta(p)
        if "error" not in m:
            m.update(propose(m, site))
            m["mode"] = default_mode(m)
            dist = np.linalg.norm(enu(tip[1], tip[0], m["lat"], m["lon"]))
            m["note"] = f"{dist:.0f} m from the lot, {m['alt']:.0f} m up, pitch {m['pitch']:.0f}°"
            if m["mode"] == "pin" and not m["tip_visible"]:
                m["mode"] = "none"
                m["note"] += ", lot not in frame"
        else:
            m["mode"] = "none"
            m["tip"] = [m["w"] / 2, m["h"] * 0.6]
            m["lot"] = []
        m["reviewed"] = False
        marks[p.name] = m
        make_preview(p, job)
        print(f"  {p.name}: {m['mode']:7s} {m.get('note', m.get('error'))}")
    save(job, "marks.json", marks)
    k_glyph().save(job / "previews" / "_k.png")


# --- review server --------------------------------------------------------------

def make_preview(p, job):
    im = Image.open(p)
    im.thumbnail((PREVIEW, PREVIEW))
    im.convert("RGB").save(job / "previews" / (p.stem + ".jpg"), quality=88)


def cmd_review(a):
    job = Path(a.job)
    site = load(job, "site.json")
    for name in load(job, "marks.json"):
        # Rebuild previews made before PREVIEW grew (older jobs).
        pv, src = job / "previews" / (Path(name).stem + ".jpg"), Path(site["photos"]) / name
        if src.exists() and (not pv.exists() or max(Image.open(pv).size) < PREVIEW):
            make_preview(src, job)
    lock = threading.Lock()

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *x):
            pass

        def send(self, body, ctype="application/json", code=200):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = urllib.parse.unquote(self.path.split("?")[0])
            if path == "/":
                html = (HERE / "review.html").read_text()
                return self.send(html.replace("__SIZES__", json.dumps(
                    {"BADGE": BADGE, "BADGE_K": BADGE_K, "BADGE_BORDER": BADGE_BORDER, "PIN_LINE": PIN_LINE,
                     "BADGE_FILL": "#%02x%02x%02x" % BADGE_FILL, "LINE_W": LINE_W, "LINE_LEN": LINE_LEN,
                     "TOP_MARGIN": TOP_MARGIN, "OUTLINE_W": OUTLINE_W, "BLACKOUT_FEATHER": BLACKOUT_FEATHER,
                     "SHADOW_OFFSET": SHADOW_OFFSET, "SHADOW_BLUR": SHADOW_BLUR, "SHADOW_OPACITY": SHADOW_OPACITY,
                     "PLACE_DOT": PLACE_DOT, "PLACE_LINE": PLACE_LINE, "PLACE_GAP": PLACE_GAP,
                     "PLACE_CAP": PLACE_CAP, "PLACE_SUB": PLACE_SUB, "PLACE_TRACK": PLACE_TRACK,
                     "PLACE_LEAD": PLACE_LEAD})).encode(), "text/html")
            if path == "/marks":
                return self.send(json.dumps({"site": site, "marks": load(job, "marks.json")}).encode())
            if path.startswith("/preview/"):
                f = job / "previews" / Path(path).name
                if f.exists():
                    return self.send(f.read_bytes(), "image/png" if f.suffix == ".png" else "image/jpeg")
            if path.startswith("/mask/"):
                f = job / "masks" / Path(path).name
                if f.exists():
                    return self.send(f.read_bytes(), "image/png")
            if path in ("/font/kraftig", "/font/buch"):
                return self.send(Path(FONT_K if path.endswith("kraftig") else FONT_B).read_bytes(), "font/otf")
            self.send(b"not found", "text/plain", 404)

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
            if self.path == "/choose_folder":
                # Native macOS folder picker (the browser can't hand us a real path).
                start = body.get("start") or site["photos"]
                while start and not Path(start).exists():
                    start = str(Path(start).parent)
                script = f'POSIX path of (choose folder with prompt "Export to" default location (POSIX file "{start}"))'
                r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
                return self.send(json.dumps({"folder": r.stdout.strip().rstrip("/") or None}).encode())
            if self.path == "/export":
                try:
                    done = export(job, site, load(job, "marks.json"), body)
                except Exception as e:
                    return self.send(json.dumps({"error": str(e)}).encode())
                return self.send(json.dumps({"done": done}).encode())
            with lock:
                marks = load(job, "marks.json")
                if self.path == "/save":
                    marks.update(body)
                    save(job, "marks.json", marks)
                    return self.send(b"{}")
                if self.path == "/solve":
                    # Handles dragged: solve this photo's correction, re-project everything.
                    m = marks[body["file"]]
                    anchors = dict(body["anchors"])
                    rng = np.linalg.norm(enu(site["tip"][1], site["tip"][0], m["lat"], m["lon"]))
                    close = m["pitch"] <= -60 or rng <= TARGET_MAX_RANGE
                    if "tip" in anchors and close and (not site.get("tip_from") or body.get("target")):
                        # First pin drag (or "set house here"): this pixel IS the house.
                        # Move the target for every photo instead of bending this camera.
                        set_target(m, site, anchors.pop("tip"))
                        save(job, "site.json", site)
                        for o in marks.values():
                            if "error" not in o and (o is m or not o.get("reviewed")):
                                o.update(propose(o, site, o.get("dyaw", 0.0), o.get("dpitch", 0.0), o.get("droll", 0.0)))
                        save(job, "marks.json", marks)
                    m["anchors"] = anchors
                    if anchors:
                        m.update(propose(m, site, *solve(m, site, anchors)))
                    elif not body.get("target") and "tip" not in body["anchors"]:
                        m.update(propose(m, site))
                    save(job, "marks.json", marks)   # without this, solves and resets were lost on reload
                    return self.send(json.dumps({"m": m, "site": site, "marks": marks}).encode())
                if self.path == "/mask":
                    # "Behind" brush: where buildings stand in front of the outline.
                    (job / "masks").mkdir(exist_ok=True)
                    png = base64.b64decode(body["data"].split(",", 1)[1])
                    (job / "masks" / (Path(body["file"]).stem + ".png")).write_bytes(png)
                    return self.send(b"{}")
                if self.path == "/place":
                    m = marks[body["file"]]
                    try:
                        add_place(m, site, body["xy"], body["label"])
                    except ValueError as e:
                        return self.send(json.dumps({"error": str(e)}).encode())
                    save(job, "site.json", site)
                    for o in marks.values():
                        if "error" not in o:
                            o.update(propose(o, site, o.get("dyaw", 0.0), o.get("dpitch", 0.0), o.get("droll", 0.0)))
                    save(job, "marks.json", marks)
                    return self.send(json.dumps({"site": site, "marks": marks}).encode())
                if self.path == "/place_edit":
                    pl = next(p for p in site["places"] if p["id"] == body["id"])
                    if body.get("delete"):
                        site["places"].remove(pl)
                        for o in marks.values():
                            o.get("places", {}).pop(str(pl["id"]), None)
                    for k in ("label", "dist"):
                        if k in body:
                            pl[k] = body[k].strip().upper() if k == "label" else bool(body[k])
                    save(job, "site.json", site)
                    save(job, "marks.json", marks)
                    return self.send(json.dumps({"site": site, "marks": marks}).encode())
                if self.path == "/apply":
                    # Median correction of the reviewed photos, applied to the rest of the flight.
                    done = [m for m in marks.values() if m.get("reviewed") and m.get("anchors") and "error" not in m]
                    if not done:
                        return self.send(json.dumps({"error": "drag and approve at least one photo first"}).encode())
                    dyaw, dz = flight_fix(done, site)
                    for m in marks.values():
                        if not m.get("reviewed") and "error" not in m:
                            m.update(propose(m, site, dyaw, 0.0, 0.0, dz))
                    save(job, "marks.json", marks)
                    return self.send(json.dumps({"dyaw": dyaw, "dz": dz, "marks": marks}).encode())
            self.send(b"{}", code=404)

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", a.port), H)
    url = f"http://127.0.0.1:{a.port}/"
    print("review page:", url, "(Ctrl+C to stop)")
    if not a.no_open:
        webbrowser.open(url)
    srv.serve_forever()


# --- render ------------------------------------------------------------------------

def k_glyph():
    """The K from the white Kollosche wordmark (first two shapes of the lockup)."""
    src = Image.open(ROOT / "raw/kollosche/team-logos/HayleyKidson/HK Kollosche_2white.png").convert("RGBA")
    band = src.crop((0, 232, src.width, 621))
    lab, _ = ndimage.label(np.array(band.getchannel("A")) > 8)
    objs = ndimage.find_objects(lab)
    first = sorted(range(len(objs)), key=lambda i: objs[i][1].start)[:2]
    a = np.where(np.isin(lab, [i + 1 for i in first]), np.array(band.getchannel("A")), 0).astype(np.uint8)
    k = Image.new("RGBA", band.size, (255, 255, 255, 0))
    k.putalpha(Image.fromarray(a))
    return k.crop(k.getchannel("A").getbbox())


def pin_layout(m):
    """Badge side and line length; per-photo pin_len (dragged in review) wins,
    and the line shortens so the badge stays in frame."""
    H = m["h"]
    side = BADGE * H
    want = m.get("pin_len", LINE_LEN) * H
    room = m["tip"][1] - TOP_MARGIN * H - side
    return side, max(0.0, min(want, room))


def badge(side, k):
    """Navy square, thin white border, white K centred."""
    side = round(side)
    b = Image.new("RGBA", (side, side), BADGE_FILL + (255,))
    bw = max(1, round(BADGE_BORDER * side))
    a = np.zeros((side, side), np.uint8)
    a[:bw], a[-bw:], a[:, :bw], a[:, -bw:] = 255, 255, 255, 255
    border = Image.new("RGBA", (side, side), (255, 255, 255, 0))
    border.putalpha(Image.fromarray(a))
    b.alpha_composite(border)
    kw = round(BADGE_K * side)
    kk = k.resize((kw, round(k.height * kw / k.width)), Image.LANCZOS)
    b.alpha_composite(kk, ((side - kk.width) // 2, (side - kk.height) // 2))
    return b


def text_image(text, font_path, cap_px, track_em):
    """White kerned caps (HarfBuzz) whose cap height is cap_px; tight RGBA."""
    import uharfbuzz as hb
    from PIL import ImageDraw, ImageFont
    probe = ImageFont.truetype(font_path, 1000)
    hbox = probe.getbbox("H")
    size = cap_px / ((hbox[3] - hbox[1]) / 1000)
    font = ImageFont.truetype(font_path, max(1, round(size)))
    face = hb.Font(hb.Face(hb.Blob.from_file_path(font_path)))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(face, buf, {"kern": True})
    adv = [g.x_advance / face.face.upem * font.size for g in buf.glyph_positions]
    track = track_em * font.size
    width = sum(adv) + track * max(0, len(text) - 1)
    ink = font.getbbox("H")
    pad = round(cap_px)
    layer = Image.new("L", (int(width) + 2 * pad, int(cap_px) + 2 * pad), 0)
    d = ImageDraw.Draw(layer)
    x = pad
    for c, w in zip(text, adv):
        d.text((x, pad - ink[1]), c, font=font, fill=255)
        x += w + track
    im = Image.new("RGBA", layer.size, (255, 255, 255, 0))
    im.putalpha(layer)
    return im, pad   # pad: offset of the cap top / left edge inside the image


def shadowed(alpha, lw):
    """The outline's subtle drop shadow, for any white alpha layer."""
    off = round(SHADOW_OFFSET * lw)
    sh = np.roll(alpha, off, axis=0).astype(np.float32)
    sh = cv2.GaussianBlur(sh, (0, 0), SHADOW_BLUR * lw) * SHADOW_OPACITY
    shadow = Image.new("RGBA", (alpha.shape[1], alpha.shape[0]), (0, 0, 0, 0))
    shadow.putalpha(Image.fromarray(np.clip(sh, 0, 255).astype(np.uint8)))
    line = Image.new("RGBA", shadow.size, (255, 255, 255, 0))
    line.putalpha(Image.fromarray(alpha))
    shadow.alpha_composite(line)
    return shadow


def draw_places(m, site, W, H):
    """Location pins: dot, thin line up, label over distance, centred on the spot."""
    layer = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    a = np.zeros((H, W), np.uint8)
    lw = max(2, round(LINE_W * H))
    for pl in site.get("places", []):
        st = m.get("places", {}).get(str(pl["id"]))
        if not st or not st.get("on"):
            continue
        x, y = st["xy"]
        r = PLACE_DOT * H
        cv2.circle(a, (round(x * 16), round(y * 16)), round(r * 16), 255, -1, cv2.LINE_AA, shift=4)
        top = y - PLACE_LINE * H
        a[max(0, round(top)):max(0, round(y)), max(0, round(x - lw / 2)):max(0, round(x - lw / 2) + lw)] = 255
        lines = [(pl["label"], FONT_K, PLACE_CAP * H)]
        if pl.get("dist", True):
            lines.append((place_distance(site, pl), FONT_B, PLACE_SUB * H))
        imgs = [text_image(t, f, c, PLACE_TRACK) + (c,) for t, f, c in lines]
        lead = PLACE_LEAD * PLACE_CAP * H
        block = sum(c for _, _, c in imgs) + lead * (len(imgs) - 1)
        cy = top - PLACE_GAP * H - block
        for im, pad, c in imgs:
            tw = im.width - 2 * pad
            tx = min(max(x - tw / 2, 0.02 * W), W - 0.02 * W - tw)
            ta = np.array(im.getchannel("A"))
            x0, y0 = round(tx - pad), round(cy - pad)
            xs, ys = max(0, x0), max(0, y0)
            xe, ye = min(W, x0 + ta.shape[1]), min(H, y0 + ta.shape[0])
            if xe > xs and ye > ys:
                a[ys:ye, xs:xe] = np.maximum(a[ys:ye, xs:xe], ta[ys - y0:ye - y0, xs - x0:xe - x0])
            cy += c + lead
    if a.any():
        layer.alpha_composite(shadowed(a, lw))
    return layer


def lit_area(lot, lift):
    """Polygons whose union is the lot swept straight up by `lift` px, so the building rising
    above a ground-level outline stays bright under the blackout."""
    polys = [lot]
    if lift > 0:
        up = [[x, y - lift] for x, y in lot]
        polys.append(up)
        polys += [[lot[j], lot[(j + 1) % len(lot)], up[(j + 1) % len(lot)], up[j]] for j in range(len(lot))]
    return polys


def draw_overlay(m, k, site=None, mask=None):
    W, H = m["w"], m["h"]
    ss = 2
    a = np.zeros((H * ss, W * ss), np.uint8)
    if m["mode"] in ("outline", "both") and m["lot"]:
        lw = max(2, round(OUTLINE_W * m.get("outline_w", 1) * W)) * ss
        p = np.round(np.array(m["lot"]) * ss * 16).astype(np.int32)
        gaps = set(m.get("gaps", []))   # razor-removed edges, by start corner
        for j in range(len(p)):
            if j in gaps:
                continue
            seg = np.array([p[j], p[(j + 1) % len(p)]])
            cv2.polylines(a, [seg], False, 255, lw, cv2.LINE_AA, shift=4)
            for x, y in seg:
                cv2.circle(a, (int(x), int(y)), lw // 2 * 16, 255, -1, cv2.LINE_AA, shift=4)
    alpha = cv2.resize(a, (W, H), interpolation=cv2.INTER_AREA)
    im = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    if m.get("blackout") and (m.get("lit") or m["lot"]):
        # ZED look: darken everything outside the bright area, soft edge. The bright area is the
        # hand-drawn Bright lasso shapes (added/cut in order) if any, else the outline (+ lift).
        inside = np.zeros((H, W), np.uint8)
        shapes = [(sh["pts"], 0 if sh.get("cut") else 255) for sh in m["lit"]] if m.get("lit") \
            else [(poly, 255) for poly in lit_area(m["lot"], m.get("lift", 0) * H)]
        for poly, val in shapes:
            cv2.fillPoly(inside, [np.round(np.array(poly) * 16).astype(np.int32)], val, cv2.LINE_AA, shift=4)
        inside = cv2.GaussianBlur(inside.astype(np.float32), (0, 0), BLACKOUT_FEATHER * W)
        dark = (m["blackout"] * (255 - inside)).clip(0, 255).astype(np.uint8)
        im = Image.merge("RGBA", (*[Image.new("L", (W, H), 0)] * 3, Image.fromarray(dark)))
    if alpha.any():
        lw = max(2, round(OUTLINE_W * m.get("outline_w", 1) * W))
        if mask is not None:
            # "Behind" brush: hide the line (and so its shadow) where buildings stand in front.
            mk = cv2.resize(np.array(mask.convert("L")), (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)
            mk = cv2.GaussianBlur(mk, (0, 0), 0.15 * lw)
            alpha = (alpha * (1 - mk / 255)).astype(np.uint8)
        im.alpha_composite(shadowed(alpha, lw))
    if site is not None:
        im.alpha_composite(draw_places(m, site, W, H))
    if m["mode"] in ("pin", "both"):
        tx, ty = m["tip"]
        side, length = pin_layout(m)
        lw = max(2, round(PIN_LINE * side))
        line = Image.new("RGBA", (lw, max(1, round(length))), (255, 255, 255, 255))
        im.alpha_composite(line, (round(tx - lw / 2), round(ty - length)))
        bd = badge(side, k)
        im.alpha_composite(bd, (round(tx - bd.width / 2), round(ty - length - bd.height)))
    return im


def finished(job, site, name, m, k):
    """The photo with its pin/outline burned in, plus the source's EXIF/ICC and the overlay layer."""
    src = Image.open(Path(site["photos"]) / name)
    mf = job / "masks" / (Path(name).stem + ".png")
    mask = Image.open(mf).getchannel("A") if mf.exists() else None
    ov = draw_overlay(m, k, site, mask)
    final = src.convert("RGBA")
    final.alpha_composite(ov)
    extra = {k2: src.info[k2] for k2 in ("exif", "icc_profile") if k2 in src.info}
    if "exif" in extra:
        # Re-serialise: drops Lightroom's embedded thumbnail of the CLEAN photo, which Finder and
        # Quick Look show instead of the real pixels (looked like "print has no pin").
        extra["exif"] = src.getexif().tobytes()
    return final.convert("RGB"), extra, ov


# Export presets. Print: the clean original photo (or, if asked, full resolution with graphics, max quality, 300 dpi).
# Web: 2048 px long edge, lighter file, no EXIF (drops the drone GPS), colour profile kept.
WEB_EDGE = 2048


def safe_name(n):
    n = re.sub(r'[/\\:*?"<>|]+', "-", n).strip().strip(".")
    return re.sub(r"\.jpe?g$", "", n, flags=re.I) or "photo"


def export(job, site, marks, body):
    folder = Path(body["folder"]).expanduser()
    if not folder.is_absolute():
        raise ValueError("pick a folder first")
    kinds = [x for x in ("print", "web") if body.get(x)]
    if not kinds or not body.get("items"):
        raise ValueError("nothing to export")
    names = [safe_name(it["name"]) for it in body["items"]]
    if len(set(n.lower() for n in names)) < len(names):
        raise ValueError("two photos have the same name")
    k, done = k_glyph(), []
    for it, nm in zip(body["items"], names):
        img, extra, _ = finished(job, site, it["file"], marks[it["file"]], k)
        for kind in kinds:
            d = folder / kind.capitalize()
            d.mkdir(parents=True, exist_ok=True)
            if kind == "print" and not body.get("print_graphics"):
                # Kollosche: print copies are the clean photo (no pin, no outline), byte-for-byte.
                shutil.copyfile(Path(site["photos"]) / it["file"], d / f"{nm}.jpg")
            elif kind == "print":
                img.save(d / f"{nm}.jpg", quality=100, subsampling=0, dpi=(300, 300), **extra)
            else:
                w = img.copy()
                w.thumbnail((WEB_EDGE, WEB_EDGE), Image.LANCZOS)
                w.save(d / f"{nm}.jpg", quality=85, optimize=True, progressive=True,
                       **({"icc_profile": extra["icc_profile"]} if "icc_profile" in extra else {}))
            done.append(str(d / f"{nm}.jpg"))
    return done


def cmd_render(a):
    job = Path(a.job)
    site, marks = load(job, "site.json"), load(job, "marks.json")
    out = job / "out"
    out.mkdir(exist_ok=True)
    k = k_glyph()
    for name, m in marks.items():
        if m["mode"] == "none" and not m.get("blackout") and not any(p.get("on") for p in m.get("places", {}).values()):
            continue
        if not m.get("reviewed") and not a.all:
            print(f"  skip {name}: not approved in review (use --all to render anyway)")
            continue
        final, extra, ov = finished(job, site, name, m, k)
        ov.save(out / f"{Path(name).stem}_overlay.png")
        for old in out.glob(f"{Path(name).stem}_*.jpg"):
            old.unlink()   # one finished JPG per photo, whatever its mode was last time
        final.save(out / f"{Path(name).stem}_{m['mode']}.jpg", quality=95, **extra)
        print(f"  {name}: {m['mode']}")
    print("done", out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("job")
    p.add_argument("photos")
    p.add_argument("--address", required=True)
    p.add_argument("--roof-height", type=float, default=ROOF_H, help="pin tip height in metres (single storey ~6, three storey ~10)")
    p = sub.add_parser("review")
    p.add_argument("job")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--no-open", action="store_true")
    p = sub.add_parser("render")
    p.add_argument("job")
    p.add_argument("--all", action="store_true", help="render photos not yet approved too")
    a = ap.parse_args()
    {"init": cmd_init, "review": cmd_review, "render": cmd_render}[a.cmd](a)


if __name__ == "__main__":
    main()
