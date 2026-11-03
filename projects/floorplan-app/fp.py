#!/usr/bin/env python3
"""10x floor-plan app, milestone 1: import a CubiCasa export, review its labels, write a 10x copy.

    fp.py import <cubicasa folder> [--final <supplier pdf/jpg>] [--client SLUG] [--address "…"]
    fp.py import-all            # every folder in raw/floorplans/cubicasa (finals matched by name)
    fp.py serve [--port 8790]   # review UI for every job

Rules this code holds to:
  * the source folder is copied into jobs/<slug>/source and made read-only; nothing writes to it
  * the SVG is untrusted: DOCTYPE/entities are refused, and anything outside a whitelist of
    plain drawing elements and attributes is stripped (and listed in the job's sanitise report)
  * only <text> content changes; every other element must come out byte-identical (geometry check)
  * labels are proposed from house-style.json; anything ambiguous is left for a human
  * nothing is inferred: north, land area, beds/baths/cars stay empty or 'derived, confirm'
"""
import argparse
import http.server
import json
import re
import shutil
import stat
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # render/sitedraw sit beside this file (the server runs with -I)
ROOT = HERE.parent.parent
JOBS = HERE / "jobs"
RAW = ROOT / "raw" / "floorplans"
STYLE = json.loads((HERE / "house-style.json").read_text())

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)

SAFE_TAGS = {"svg", "g", "defs", "pattern", "clipPath", "mask", "linearGradient", "radialGradient",
             "stop", "polygon", "polyline", "path", "line", "rect", "circle", "ellipse", "text",
             "tspan", "title", "desc", "style", "marker"}
SAFE_ATTRS = {"id", "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry", "width", "height",
              "points", "d", "transform", "fill", "stroke", "stroke-width", "stroke-dasharray",
              "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "fill-opacity",
              "fill-rule", "opacity", "style", "viewBox", "version", "patternUnits", "patternTransform",
              "clip-path", "mask", "offset", "stop-color", "stop-opacity", "gradientUnits",
              "gradientTransform", "font-family", "font-size", "font-weight", "font-style",
              "text-anchor", "dominant-baseline", "letter-spacing", "dy", "dx", "display",
              "visibility", "preserveAspectRatio", "data-automation-id", "class", "xml:space",
              "markerWidth", "markerHeight", "refX", "refY", "orient", "markerUnits", "marker-start",
              "marker-mid", "marker-end", "type"}
DIM = re.compile(r"^\s*([\d.]+)\s*m\s*x\s*([\d.]+)\s*m\s*$", re.I)


def local(tag):
    return tag.rsplit("}", 1)[-1]


# ---------- sanitise ----------

def bad_css(s):
    """True when CSS can reach outside the file: @import, or url() that isn't data: or #id."""
    if "@import" in s.lower() or "expression(" in s.lower():
        return True
    for u in re.findall(r"url\(\s*['\"]?([^'\")]*)", s, re.I):
        if not (u.startswith("#") or u.startswith("data:font/") or u.startswith("data:application/font")
                or u.startswith("data:application/x-font") or u.startswith("data:image/png")):
            return True
    return False


def sanitise(raw):
    """Parse untrusted SVG text and strip anything that isn't plain drawing. Returns (root, report)."""
    if re.search(r"<!DOCTYPE|<!ENTITY", raw, re.I):
        raise ValueError("SVG has a DOCTYPE/ENTITY declaration; refused (entity attacks)")
    root = ET.fromstring(raw)
    if local(root.tag) != "svg":
        raise ValueError("not an SVG")
    report = []

    def walk(el):
        for child in list(el):
            t = local(child.tag)
            if child.tag.split("}")[0].strip("{") not in (SVG,) or t not in SAFE_TAGS:
                report.append(f"removed <{t}>")
                el.remove(child)
                continue
            if t == "style" and bad_css(child.text or ""):
                report.append("removed <style> with external url/@import")
                el.remove(child)
                continue
            walk(child)
        for k in list(el.attrib):
            name = local(k) if k.startswith("{") and not k.startswith("{http://www.w3.org/XML") else k
            if k.startswith("{http://www.w3.org/XML"):
                name = "xml:" + local(k)
            v = el.attrib[k]
            if name.lower().startswith("on") or name not in SAFE_ATTRS:
                report.append(f"removed attribute {name} on <{local(el.tag)}>")
                del el.attrib[k]
            elif name == "style" and bad_css(v):
                report.append(f"removed style on <{local(el.tag)}> (external url)")
                del el.attrib[k]
            elif re.match(r"\s*url\(", v) and not re.match(r"\s*url\(\s*['\"]?#", v):
                report.append(f"removed {name}={v[:40]} on <{local(el.tag)}>")
                del el.attrib[k]

    walk(root)
    return root, report


# ---------- labels ----------

def texts(root):
    return [e for e in root.iter(f"{{{SVG}}}text")]


def text_of(e):
    return "".join(e.itertext()).strip()


def set_text(e, s):
    kids = list(e)
    if kids:  # keep the first tspan (its x/y), clear the rest
        for k in kids[1:]:
            e.remove(k)
        e.text = None
        kids[0].text = s
        for k in kids[0]:
            kids[0].remove(k)
    else:
        e.text = s


def fmt_num(s, rnd):
    if rnd:
        return f"{float(s):.1f}"
    return s


def title(s):
    return " ".join(w[:1].upper() + w[1:] for w in s.strip().lower().split())


FLOORS = {"1st floor": ("Ground Floor", "auto", "CubiCasa counts storeys US-style: 1st = ground"),
          "2nd floor": ("Upper Floor", "needs-you", "Upper Floor or First Floor?"),
          "3rd floor": ("Second Floor", "needs-you", "Which storey name?"),
          "basement": ("Basement", "auto", "storey title")}


def propose(src, kind, rnd):
    """Deterministic proposal for one label. Returns (text, status, note)."""
    if kind == "footer":
        return "", "auto", "CubiCasa footer; the 10x template prints the areas instead"
    if kind == "storey":
        return FLOORS.get(src.strip().lower(), (title(src), "needs-you", "storey title"))
    if kind == "dim":
        m = DIM.match(src)
        w, h = fmt_num(m[1], rnd), fmt_num(m[2], rnd)
        out = STYLE["dims"]["format"].format(w=w, h=h)
        changed = (w, h) != (m[1], m[2])
        return out, "needs-you" if changed else "auto", ("rounded from " + src) if changed else "format only, numbers untouched"
    key = src.strip().lower()
    if key in STYLE["ask"]:
        return title(src), "needs-you", STYLE["ask"][key]
    if key in STYLE["rename"]:
        return STYLE["rename"][key], "auto", "house-style rename"
    return title(src), "auto", "title case"


def classify(all_texts):
    out = []
    for i, e in enumerate(all_texts):
        s = text_of(e)
        low = s.lower()
        if DIM.match(s):
            kind = "dim"
        elif re.fullmatch(r"basement|\d+(st|nd|rd|th) floor", low):
            kind = "storey"
        elif any(p in low for p in STYLE["footer_patterns"]):
            kind = "footer"
        else:
            kind = "room"
        out.append({"i": i, "src": s, "kind": kind})
    # a dimension belongs to the room label just before it
    last = None
    for t in out:
        if t["kind"] == "room":
            last = t["i"]
        elif t["kind"] == "dim":
            t["room"] = last
    return out


# Where each CubiCasa "excluded" component goes by default. Taken from the Oct 2026 finals
# (Ormeau 203 + 11 walls = 214 internal; Parkwood 179 + 16 walls + 28 garage = 223 internal).
# A default only: the review page shows every component and the person decides.
AREA_DEFAULT = {"walls": "internal", "garage": "internal", "open to below": "none"}


def areas(items):
    """Area components exactly as CubiCasa printed them (no pixel maths)."""
    lines = [t["src"] for t in items if t["kind"] == "footer"]
    floors, excluded, gla = {}, {}, None
    for ln in lines:
        low = ln.lower()
        if "created by cubicasa" in low:
            continue
        m = re.search(r"total gla:\s*([\d.]+)", low)
        if m:  # older style: "Total GLA: 126 m2 | Total: 193 m2"
            gla = float(m[1])
            continue
        m = re.search(r"\(excluded areas\s*([\d.]+)", low)
        if m:  # older style: "1st floor: 126 m2 (Excluded areas 67 m2)"
            excluded["excluded areas"] = float(m[1])
            ln = ln[:m.start()]
            low = ln.lower()
        pairs = [(k.strip().lower(), float(v)) for k, v in re.findall(r"([A-Za-z0-9][A-Za-z0-9 ]*?):\s*([\d.]+)\s*m", ln, re.I)]
        if low.startswith("excluded areas"):
            excluded.update((k, v) for k, v in pairs if k != "excluded areas")
        elif low.startswith("total"):
            gla = pairs[-1][1] if pairs else gla
        else:
            floors.update(pairs)
    if gla is None and floors:
        gla = sum(floors.values())
    assign = {k: AREA_DEFAULT.get(k, "external") for k in excluded}
    return {"floors": floors, "gla": gla, "excluded": excluded, "assign": assign, "source": " / ".join(lines)}


def derived_counts(items):
    rooms = [t["src"].lower() for t in items if t["kind"] == "room"]
    return {"beds": sum("bedroom" in r for r in rooms),
            "baths": sum(r in ("bath", "primary bath") for r in rooms),
            "cars": None, "note": "counted from CubiCasa labels; confirm (WCs, PDRs and garages are your call)"}


# ---------- jobs ----------

def slug_of(folder):
    return re.sub(r"_gold_coast$", "", Path(folder).name.replace(" ", "_").lower())


def pick_svg(src):
    c = sorted((src / "svg-with-dim").glob("all_floors*.svg")) or sorted(src.rglob("*.svg"))
    if not c:
        raise SystemExit(f"no SVG in {src}")
    return c[0]


def lock(path):
    for p in [path, *path.rglob("*")]:
        mode = p.stat().st_mode
        p.chmod(mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def cmd_import(folder, final=None, client=None, address=None):
    folder = Path(folder).resolve()
    slug = slug_of(folder)
    job = JOBS / slug
    if (job / "job.json").exists():
        print(f"{slug}: already imported")
        return
    (job / "work").mkdir(parents=True, exist_ok=True)
    shutil.copytree(folder, job / "source")
    lock(job / "source")
    svg = pick_svg(job / "source")
    root, report = sanitise(svg.read_text(encoding="utf-8"))
    ET.ElementTree(root).write(job / "work" / "plan.svg", encoding="unicode")
    items = classify(texts(root))
    rnd = STYLE["dims"]["round_default"]
    for t in items:
        t["text"], t["status"], t["note"] = propose(t["src"], t["kind"], rnd)
        t["hidden"] = t["kind"] == "footer"
        t["approved"] = t["status"] == "auto"
    ref = None
    if final:
        final = Path(final)
        if final.suffix.lower() == ".pdf":
            subprocess.run(["pdftoppm", "-r", "110", "-png", "-singlefile", str(final), str(job / "work" / "final")], check=True)
            ref = "final.png"
        else:
            ref = "final" + final.suffix.lower()
            shutil.copy(final, job / "work" / ref)
    a = areas(items)
    data = {"slug": slug, "source_svg": str(svg.relative_to(job)), "client": client, "address": address,
            "round_dims": rnd, "north": None, "land_area": None, "areas": a,
            "counts": derived_counts(items), "labels": items, "sanitise": report, "final": ref,
            "checks": None}
    (job / "job.json").write_text(json.dumps(data, indent=1))
    print(f"{slug}: {len(items)} labels, {sum(t['status'] == 'needs-you' for t in items)} need you, "
          f"{len(report)} things stripped")


def cmd_import_all():
    for folder in sorted((RAW / "cubicasa").iterdir()):
        if not folder.is_dir():
            continue
        s = slug_of(folder)
        finals = sorted((RAW / "finals").glob(s + ".*"))
        cmd_import(folder, finals[0] if finals else None)


# ---------- write + checks ----------

def client_profile(name):
    """clients/<slug>.json whose name or aliases match the job's client text."""
    if not name:
        return None
    key = re.sub(r"[^a-z0-9]", "", name.lower())
    for f in sorted((HERE / "clients").glob("*.json")):
        prof = json.loads(f.read_text())
        names = [prof["name"], *prof.get("aliases", [])]
        if any(re.sub(r"[^a-z0-9]", "", n.lower()) == key for n in names):
            return prof
    return None


def write_out(job):
    import render
    data = json.loads((job / "job.json").read_text())
    root = ET.parse(job / "work" / "plan.svg").getroot()
    ts = texts(root)
    for t in data["labels"]:
        e = ts[t["i"]]
        if t["hidden"]:
            render.hide(e)
        elif t["approved"]:
            set_text(e, t["text"])
    (job / "out").mkdir(exist_ok=True)
    out = job / "out" / f"{data['slug']}-10x.svg"
    ET.ElementTree(root).write(out, encoding="unicode")
    # 10x skin (presentation only) + the A4 page
    rep = render.skin(root)
    data["skin"] = rep
    data["scale"] = rep["scale"]
    styled = job / "out" / f"{data['slug']}-10x-plan.svg"
    ET.ElementTree(root).write(styled, encoding="unicode")
    pg = render.page(data, styled.read_text(), client_profile(data.get("client")))
    data["exports"] = [p.name for p in render.export(pg, job / "out" / f"{data['slug']}-10x-page")]
    data["checks"] = checks(job, data, styled)
    (job / "job.json").write_text(json.dumps(data, indent=1))
    return data["checks"]


GEOM = {"points", "d", "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "rx", "ry", "width", "height",
        "transform", "viewBox", "patternTransform", "refX", "refY", "orient", "markerWidth", "markerHeight"}


def drawing(root):
    """Drawing elements in order, skipping <defs> (patterns/filters the skin adds) and text."""
    out, skip = [], set()
    for e in root.iter():
        if local(e.tag) == "defs":
            skip.update(e.iter())
        if e in skip or local(e.tag) in ("text", "tspan"):
            continue
        out.append(e)
    return out


def geometry_same(a, b):
    """Every drawing element keeps its tag and every geometry attribute exactly as CubiCasa drew it.
    Colours, line weights and fonts may change; positions and shapes may not."""
    A, B = drawing(a), drawing(b)
    if len(A) != len(B):
        return False, f"element count {len(A)} → {len(B)}"
    for x, y in zip(A, B):
        gx = {k: v for k, v in x.attrib.items() if k in GEOM}
        gy = {k: v for k, v in y.attrib.items() if k in GEOM}
        if x.tag != y.tag or gx != gy:
            return False, f"<{local(x.tag)}> geometry changed"
    return True, f"{len(A)} drawing elements, every coordinate identical"


def checks(job, data, out):
    src = ET.parse(job / "work" / "plan.svg").getroot()
    new = ET.parse(out).getroot()
    res = []
    ok, msg = geometry_same(src, new)
    res.append({"name": "Geometry unchanged", "ok": ok, "msg": msg})
    pend = [t["src"] for t in data["labels"] if not t["hidden"] and not t["approved"]]
    res.append({"name": "Every label approved", "ok": not pend, "msg": ", ".join(pend) or "all approved"})
    shown = [t for t in data["labels"] if not t["hidden"] and t["approved"]]
    bad_dim = [t["text"] for t in shown if t["kind"] == "dim" and not re.fullmatch(r"[\d.]+m x [\d.]+m", t["text"])]
    res.append({"name": "Dimension format 0.0m x 0.0m", "ok": not bad_dim, "msg": ", ".join(bad_dim) or "ok"})
    names = [t["text"] for t in shown if t["kind"] == "room"]
    dup = sorted({n for n in names if names.count(n) > 1 and n.lower().startswith("bedroom")})
    res.append({"name": "Bedrooms numbered uniquely", "ok": not dup, "msg": ", ".join(dup) or "ok"})
    bad_num = [t["text"] for t in shown if re.search(r"\d\.\d{3}", t["text"])]
    res.append({"name": "No 1.061-style separators", "ok": not bad_num, "msg": ", ".join(bad_num) or "ok"})
    res.append({"name": "North set by a person", "ok": data["north"] is not None,
                "msg": "never inferred; set it" if data["north"] is None else f"{data['north']}°"})
    res.append({"name": "Land area supplied", "ok": bool(data["land_area"]),
                "msg": "needs the title/listing figure" if not data["land_area"] else f"{data['land_area']} m²"})
    sc = data.get("scale")
    res.append({"name": "Scale verified against printed sizes", "ok": bool(sc and sc["ok"]),
                "msg": f"{sc['rooms_checked']} rooms, worst {sc['worst_cm']} cm" if sc else "no sized rooms; scale bar left off"})
    sk = data.get("skin") or {}
    res.append({"name": "Floor finishes", "ok": True,
                "msg": f"{len(sk.get('rooms', []))} floors textured, {sk.get('unlabelled', 0)} unlabelled spaces got a default (check them)"})
    res.append({"name": "Client profile found", "ok": client_profile(data.get("client")) is not None,
                "msg": data.get("client") or "no client set"})
    res.append({"name": "Source untouched (read-only copy)", "ok": not any(
        p.stat().st_mode & stat.S_IWUSR for p in (job / "source").rglob("*") if p.is_file()), "msg": "jobs/…/source"})
    return res


# ---------- review server ----------

CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'")


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, body, ctype="application/json", code=200):
        if isinstance(body, str):
            body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def job(self, slug):
        j = (JOBS / slug).resolve()
        if j.parent != JOBS.resolve() or not (j / "job.json").exists():
            raise FileNotFoundError(slug)
        return j

    def do_GET(self):
        p = self.path.split("?")[0]
        try:
            if p == "/":
                return self.send((HERE / "review.html").read_text(), "text/html; charset=utf-8")
            m = re.fullmatch(r"/trace/([\w-]+)", p)
            if m:
                self.job(m[1])
                return self.send((HERE / "trace.html").read_text(), "text/html; charset=utf-8")
            if p == "/api/jobs":
                js = [json.loads((d / "job.json").read_text()) for d in sorted(JOBS.iterdir()) if (d / "job.json").exists()]
                return self.send(json.dumps([{"slug": x["slug"], "address": x["address"], "client": x["client"],
                                              "final": bool(x["final"]),
                                              "todo": sum(1 for t in x["labels"] if not t["hidden"] and not t["approved"])} for x in js]))
            m = re.fullmatch(r"/api/job/([\w-]+)", p)
            if m:
                return self.send((self.job(m[1]) / "job.json").read_text())
            m = re.fullmatch(r"/job/([\w-]+)/(plan\.svg|final\.(?:png|jpg|jpeg)|out\.svg|page\.png|page\.pdf|site\.png|site-raw\.png|site-drawn\.png)", p)
            if m:
                j = self.job(m[1])
                f = {"out.svg": j / "out" / f"{m[1]}-10x.svg",
                     "page.png": j / "out" / f"{m[1]}-10x-page.png",
                     "page.pdf": j / "out" / f"{m[1]}-10x-page.pdf"}.get(m[2], j / "work" / m[2])
                ctype = {".svg": "image/svg+xml", ".png": "image/png", ".pdf": "application/pdf"}.get(f.suffix, "image/jpeg")
                return self.send(f.read_bytes(), ctype)
        except FileNotFoundError:
            pass
        self.send('{"error":"not found"}', code=404)

    def do_POST(self):
        m = re.fullmatch(r"/api/job/([\w-]+)/site", self.path)
        if m:  # site plan image: decoded and re-encoded as PNG, so nothing but pixels survives
            from PIL import Image
            import io
            j = self.job(m[1])
            raw = self.rfile.read(min(int(self.headers["Content-Length"] or 0), 40_000_000))
            try:
                im = Image.open(io.BytesIO(raw))
                im.load()
            except Exception:
                return self.send('{"error":"not an image"}', code=400)
            im = im.convert("RGB")
            im.thumbnail((2400, 2400))
            im.save(j / "work" / "site.png")
            data = json.loads((j / "job.json").read_text())
            data["site_plan"] = str(j / "work" / "site.png")
            (j / "job.json").write_text(json.dumps(data, indent=1))
            return self.send(json.dumps(data))
        m = re.fullmatch(r"/api/job/([\w-]+)/trace", self.path)
        if m:  # roof traced on the aerial + markers -> drawn site plan -> page
            j = self.job(m[1])
            body = json.loads(self.rfile.read(min(int(self.headers["Content-Length"] or 0), 2_000_000)) or b"{}")
            data = json.loads((j / "job.json").read_text())
            try:
                trace = [{"kind": "flat" if t.get("kind") == "flat" else "hip",
                          "points": [[float(x), float(y)] for x, y in t["points"]][:200]} for t in body["site_trace"]][:40]
                marks = [{"label": str(mk["label"])[:40], "x": None if mk.get("x") is None else float(mk["x"]),
                          "y": None if mk.get("y") is None else float(mk["y"]), "traced": True} for mk in body.get("site_markers", [])][:12]
            except (KeyError, TypeError, ValueError):
                return self.send('{"error":"bad trace"}', code=400)
            data["site_trace"], data["site_markers"] = trace, marks
            try:
                import sitedraw
                png = sitedraw.main_traced(j, data)
                data["site_plan"] = str(sitedraw.faded(png))
                data["site_plan_kind"] = "drawn by code from a roof traced on the QLD aerial (no AI)"
                (j / "job.json").write_text(json.dumps(data, indent=1))
                write_out(j)
            except Exception as e:
                return self.send(json.dumps({"error": f"{type(e).__name__}: {e}"}), code=500)
            return self.send((j / "job.json").read_text())
        m = re.fullmatch(r"/api/job/([\w-]+)/(save|write)", self.path)
        if not m:
            return self.send('{"error":"not found"}', code=404)
        j = self.job(m[1])
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"] or 0)) or b"{}")
        data = json.loads((j / "job.json").read_text())
        for k in ("client", "address", "north", "land_area", "round_dims", "counts", "areas", "floor_title", "legend"):
            if k in body:
                data[k] = body[k]
        if "labels" in body:
            by = {t["i"]: t for t in body["labels"]}
            for t in data["labels"]:
                u = by.get(t["i"])
                if u:
                    t["text"], t["hidden"], t["approved"] = str(u["text"])[:80], bool(u["hidden"]), bool(u["approved"])
        if "round_dims" in body:  # re-propose dims that haven't been hand-edited
            for t in data["labels"]:
                if t["kind"] == "dim":
                    txt, st, note = propose(t["src"], "dim", data["round_dims"])
                    t["text"], t["status"], t["note"] = txt, st, note
                    t["approved"] = st == "auto"
        (j / "job.json").write_text(json.dumps(data, indent=1))
        if body.get("clear_site"):
            data["site_plan"] = None
            (j / "job.json").write_text(json.dumps(data, indent=1))
        if m[2] == "write":
            try:
                write_out(j)
            except Exception as e:  # report, don't crash the server
                return self.send(json.dumps({"error": f"{type(e).__name__}: {e}"}), code=500)
            data = json.loads((j / "job.json").read_text())
        self.send(json.dumps(data))


def cmd_serve(port):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), H)
    print(f"http://127.0.0.1:{port}/")
    srv.serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("import")
    a.add_argument("folder")
    a.add_argument("--final")
    a.add_argument("--client")
    a.add_argument("--address")
    sub.add_parser("import-all")
    s = sub.add_parser("serve")
    s.add_argument("--port", type=int, default=8790)
    o = ap.parse_args()
    if o.cmd == "import":
        cmd_import(o.folder, o.final, o.client, o.address)
    elif o.cmd == "import-all":
        cmd_import_all()
    else:
        cmd_serve(o.port)
