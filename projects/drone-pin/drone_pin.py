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

Usage (system python3):
  python3 -I drone_pin.py init   <job_dir> <photos_dir> --address "47 Somerset Drive Mudgeeraba"
  python3 -I drone_pin.py review <job_dir>          # opens the review page
  python3 -I drone_pin.py render <job_dir>          # finished JPGs + transparent PNG overlays
"""
import argparse
import http.server
import io
import json
import math
import re
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
QLD = "https://spatial-gis.information.qld.gov.au/arcgis/rest/services/PlanningCadastre/LandParcelPropertyFramework/MapServer"
DIAG35 = math.hypot(36, 24)
ROOF_H = 6.0          # metres above ground for the pin tip
PREVIEW = 1600        # long edge of review previews (px)
EXTS = {".jpg", ".jpeg", ".tif", ".tiff", ".png"}

# Pin and outline sizes, as fractions of the photo (same ratios as the video pin).
K_W, LINE_W, LINE_LEN, GAP, TOP_MARGIN = 0.079, 0.0037, 0.42, 0.015, 0.05
OUTLINE_W = 0.0055


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
    e, n = unproject(m, uv, m.get("dz", 0.0) + ROOF_H, m.get("dyaw", 0.0), m.get("dpitch", 0.0), m.get("droll", 0.0))
    site["tip"] = [m["lon"] + math.degrees(e / (6378137.0 * math.cos(math.radians(m["lat"])))),
                   m["lat"] + math.degrees(n / 6378137.0)]
    site["tip_from"] = m["file"]


def world(m, site, dz=0.0):
    """Site geometry in this photo's drone-centred ENU frame. dz = the lot's ground
    height above the takeoff point (hilly sites; solved from the photos you fix)."""
    lot = np.array([np.r_[enu(lat, lon, m["lat"], m["lon"]), dz] for lon, lat in site["ring"]])
    tip = np.r_[enu(site["tip"][1], site["tip"][0], m["lat"], m["lon"]), dz + ROOF_H]
    return tip, lot


def propose(m, site, dyaw=0.0, dpitch=0.0, droll=0.0, dz=None):
    dz = m.get("dz", 0.0) if dz is None else dz
    tip_w, lot_w = world(m, site, dz)
    tip, tip_ok = project(m, [tip_w], dyaw, dpitch, droll)
    lot, lot_ok = project(m, lot_w, dyaw, dpitch, droll)
    inside = lambda p: 0 <= p[0] < m["w"] and 0 <= p[1] < m["h"]
    return {"tip": tip[0].round(1).tolist(), "tip_visible": bool(tip_ok[0] and inside(tip[0])),
            "lot": lot.round(1).tolist(), "lot_visible": bool(lot_ok.all() and all(inside(p) for p in lot)),
            "dyaw": dyaw, "dpitch": dpitch, "droll": droll, "dz": dz}


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
            "ring": ring, "tip": tip, "photos": str(photos.resolve())}
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
        im = Image.open(p)
        im.thumbnail((PREVIEW, PREVIEW))
        im.convert("RGB").save(job / "previews" / (p.stem + ".jpg"), quality=85)
        print(f"  {p.name}: {m['mode']:7s} {m.get('note', m.get('error'))}")
    save(job, "marks.json", marks)
    k_glyph().save(job / "previews" / "_k.png")


# --- review server --------------------------------------------------------------

def cmd_review(a):
    job = Path(a.job)
    site = load(job, "site.json")
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
                    {"K_W": K_W, "LINE_W": LINE_W, "LINE_LEN": LINE_LEN, "GAP": GAP,
                     "TOP_MARGIN": TOP_MARGIN, "OUTLINE_W": OUTLINE_W})).encode(), "text/html")
            if path == "/marks":
                return self.send(json.dumps({"site": site, "marks": load(job, "marks.json")}).encode())
            if path.startswith("/preview/"):
                f = job / "previews" / Path(path).name
                if f.exists():
                    return self.send(f.read_bytes(), "image/png" if f.suffix == ".png" else "image/jpeg")
            self.send(b"not found", "text/plain", 404)

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])) or b"{}")
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
                    if "tip" in anchors and (not site.get("tip_from") or body.get("target")):
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
                    return self.send(json.dumps({"m": m, "site": site, "marks": marks}).encode())
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


def pin_layout(W, H, tip, k_aspect):
    """K size and line length for a tip; the line shortens so the K stays in frame."""
    kw = K_W * H
    kh = kw * k_aspect
    room = tip[1] - TOP_MARGIN * H - kh - GAP * H
    return kw, kh, max(0.0, min(LINE_LEN * H, room))


def draw_overlay(m, k):
    W, H = m["w"], m["h"]
    ss = 2
    a = np.zeros((H * ss, W * ss), np.uint8)
    if m["mode"] in ("outline", "both") and m["lot"]:
        lw = max(2, round(OUTLINE_W * W)) * ss
        p = np.round(np.array(m["lot"]) * ss * 16).astype(np.int32)
        cv2.polylines(a, [p], True, 255, lw, cv2.LINE_AA, shift=4)
        for x, y in p:
            cv2.circle(a, (int(x), int(y)), lw // 2 * 16, 255, -1, cv2.LINE_AA, shift=4)
    alpha = cv2.resize(a, (W, H), interpolation=cv2.INTER_AREA)
    im = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    im.putalpha(Image.fromarray(alpha))
    if m["mode"] in ("pin", "both"):
        tx, ty = m["tip"]
        kw, kh, length = pin_layout(W, H, m["tip"], k.height / k.width)
        lw = max(2, round(LINE_W * H))
        line = Image.new("RGBA", (lw, max(1, round(length))), (255, 255, 255, 255))
        im.alpha_composite(line, (round(tx - lw / 2), round(ty - length)))
        kk = k.resize((round(kw), round(kh)), Image.LANCZOS)
        im.alpha_composite(kk, (round(tx - kw / 2), round(ty - length - GAP * H - kh)))
    return im


def cmd_render(a):
    job = Path(a.job)
    site, marks = load(job, "site.json"), load(job, "marks.json")
    out = job / "out"
    out.mkdir(exist_ok=True)
    k = k_glyph()
    for name, m in marks.items():
        if m["mode"] == "none":
            continue
        if not m.get("reviewed") and not a.all:
            print(f"  skip {name}: not approved in review (use --all to render anyway)")
            continue
        src = Image.open(Path(site["photos"]) / name)
        ov = draw_overlay(m, k)
        ov.save(out / f"{Path(name).stem}_overlay.png")
        final = src.convert("RGBA")
        final.alpha_composite(ov)
        extra = {k2: src.info[k2] for k2 in ("exif", "icc_profile") if k2 in src.info}
        final.convert("RGB").save(out / f"{Path(name).stem}_{m['mode']}.jpg", quality=95, **extra)
        print(f"  {name}: {m['mode']}")
    print("done", out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init")
    p.add_argument("job")
    p.add_argument("photos")
    p.add_argument("--address", required=True)
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
