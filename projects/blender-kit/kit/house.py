"""house: parametric multi-level house from a plan-derived spec (Job Framework v2, phase 4).

scene.json "house": {
  "name": "Lot48", "ceiling": 3.0, "slab": 0.3, "wall": {"thickness": 0.3, "material": "Render"},
  "levels": [{"name": "Lower", "z": 3.3, "rect": [x0, y0, x1, y1], "ceiling": 3.0,
              "openings": [{"side": "N", "offset": 0.6, "width": 16.8, "height": 2.7, "sill": 0,
                            "type": "stacker|window|bifold|door|garage_door|void", "panels": 6}]}],
  "alfresco":  {"level": "Lower", "rect": [...]},
  "balconies": [{"level": "Upper", "side": "N", "depth": 3.45, "balustrade": "glass"}],
  "core":      {"name": "Lift", "rect": [...], "levels": ["Garage", "Lower", "Upper"]},
  "roof":      {"type": "flat", "pitch_deg": 3, "overhang": 0.9, "fascia": 0.3, "material": "RoofDark"},
  "observatory": {"rect": [...], "height": 2.7},
  "pool":      {"rect": [...], "z": 0},
  "materials": {"slab": …, "glass": …, "frame": …, "garage_door": …, "floor": …}
}
Sides: S = y0 (front/street), N = y1 (rear), W = x0, E = x1. An opening's offset runs along
its side from the x0 (S/N) or y0 (W/E) end. Walls are built as segments around the openings
(piers, sills, lintels, glazing, mullions), with no booleans, so builds stay fast and exact.
Plan-to-spec: read the plan PDF's dimensions into this block; mark guesses with "_assumed".
"""
import math
from . import core
from .core import box

FRAME = 0.06  # glazing frame / mullion size


def _side_geom(rect, side):
    """(start point, unit direction along the wall, inward normal, length) for a side."""
    x0, y0, x1, y1 = rect
    return {
        "S": ((x0, y0), (1, 0), (0, 1), x1 - x0),
        "N": ((x0, y1), (1, 0), (0, -1), x1 - x0),
        "W": ((x0, y0), (0, 1), (1, 0), y1 - y0),
        "E": ((x1, y0), (0, 1), (-1, 0), y1 - y0),
    }[side]


def _piece(name, side, along0, along1, z0, z1, depth, inset, rect, material, col):
    """Box spanning [along0, along1] along a side, z0..z1, `depth` thick, centred `inset` in from the edge."""
    (sx, sy), (dx, dy), (nx, ny), _ = _side_geom(rect, side)
    if along1 - along0 < 0.01 or z1 - z0 < 0.01:
        return None
    mid = (along0 + along1) / 2
    cx, cy = sx + dx * mid + nx * inset, sy + dy * mid + ny * inset
    size = (along1 - along0, depth, z1 - z0) if dx else (depth, along1 - along0, z1 - z0)
    return box(name, size, (cx, cy, (z0 + z1) / 2), material, col)


def _glazing(p, side, a0, a1, z0, z1, kind, panels, t, rect, M, col):
    """Glass + frame + mullions inside an opening."""
    inset = t / 2
    if kind == "void":
        return
    if kind == "garage_door":
        _piece(f"{p}_GarageDoor", side, a0, a1, z0, z1, 0.08, inset + 0.1, rect, M["garage_door"], col)
        return
    if kind == "door":
        _piece(f"{p}_Door", side, a0, a1, z0, z1, 0.06, inset, rect, M["door"], col)
        return
    _piece(f"{p}_Glass", side, a0 + FRAME, a1 - FRAME, z0 + FRAME, z1 - FRAME, 0.03, inset, rect, M["glass"], col)
    for k, (b0, b1) in enumerate(((a0, a0 + FRAME), (a1 - FRAME, a1))):
        _piece(f"{p}_Jamb{k}", side, b0, b1, z0, z1, FRAME * 1.5, inset, rect, M["frame"], col)
    _piece(f"{p}_Head", side, a0, a1, z1 - FRAME, z1, FRAME * 1.5, inset, rect, M["frame"], col)
    _piece(f"{p}_Sill", side, a0, a1, z0, z0 + FRAME, FRAME * 1.5, inset, rect, M["frame"], col)
    n = panels or {"stacker": max(2, round((a1 - a0) / 2.8)), "bifold": max(2, round((a1 - a0) / 0.9)), "window": max(1, round((a1 - a0) / 1.8))}[kind]
    for k in range(1, n):
        m = a0 + (a1 - a0) * k / n
        _piece(f"{p}_Mullion{k}", side, m - FRAME / 2, m + FRAME / 2, z0, z1, FRAME * 1.2, inset, rect, M["frame"], col)


def _walls(L, H, t, M, col, skip_sides=()):
    rect, zf = L["rect"], L["z"] + H["slab"]
    ceil = L.get("ceiling", H["ceiling"])
    zt = zf + ceil
    p = f"{H['name']}_{L['name']}"
    for side in "SNWE":
        if side in skip_sides:
            continue
        _, _, _, length = _side_geom(rect, side)
        ops = sorted([o for o in L.get("openings", []) if o["side"] == side], key=lambda o: o["offset"])
        cur, k = 0.0, 0
        for o in ops:
            a0, a1 = o["offset"], min(length, o["offset"] + o["width"])
            if a0 < cur - 1e-6:
                raise ValueError(f"{p}: openings overlap on side {side} at {a0}")
            _piece(f"{p}_Wall_{side}_{k}", side, cur, a0, zf, zt, t, t / 2, rect, M["wall"], col)
            s0 = zf + o.get("sill", 0)
            s1 = min(zt, s0 + o["height"])
            _piece(f"{p}_Sill_{side}_{k}", side, a0, a1, zf, s0, t, t / 2, rect, M["wall"], col)
            _piece(f"{p}_Lintel_{side}_{k}", side, a0, a1, s1, zt, t, t / 2, rect, M["wall"], col)
            _glazing(f"{p}_Op_{side}_{k}", side, a0, a1, s0, s1, o["type"], o.get("panels"), t, rect, M, col)
            cur, k = a1, k + 1
        _piece(f"{p}_Wall_{side}_{k}", side, cur, length, zf, zt, t, t / 2, rect, M["wall"], col)


def _rect_box(name, rect, z0, z1, material, col, grow=0.0, bevel=0.0):
    x0, y0, x1, y1 = rect
    return box(name, (x1 - x0 + 2 * grow, y1 - y0 + 2 * grow, z1 - z0), ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), material, col, bevel=bevel)


def _balustrade(name, rect, z, sides, M, col, h=1.0):
    x0, y0, x1, y1 = rect
    for s in sides:
        if s in "SN":
            y = y0 if s == "S" else y1
            box(f"{name}_{s}", (x1 - x0, 0.03, h), ((x0 + x1) / 2, y, z + h / 2), M["glass"], col)
        else:
            x = x0 if s == "W" else x1
            box(f"{name}_{s}", (0.03, y1 - y0, h), (x, (y0 + y1) / 2, z + h / 2), M["glass"], col)
        box(f"{name}_{s}_Rail", (x1 - x0, 0.05, 0.05) if s in "SN" else (0.05, y1 - y0, 0.05),
            ((x0 + x1) / 2 if s in "SN" else (x0 if s == "W" else x1), (y0 + y1) / 2 if s in "WE" else (y0 if s == "S" else y1), z + h),
            M["frame"], col)


def build(H, ctx):
    col = core.coll("House")
    M = {"wall": H.get("wall", {}).get("material", "Render"), "slab": "concrete_wall_009", "glass": "Glass",
         "frame": "Bronze", "garage_door": "Timber", "door": "Timber", "floor": "wood_floor", "deck": "Timber",
         "roof": "RoofDark", "water": "PoolWater", "coping": "StoneTile", **H.get("materials", {})}
    t = H.get("wall", {}).get("thickness", 0.3)
    H.setdefault("ceiling", 3.0)
    H.setdefault("slab", 0.3)
    levels = {L["name"]: L for L in H["levels"]}
    n = H["name"]

    for i, L in enumerate(H["levels"]):
        z = L["z"]
        _rect_box(f"{n}_{L['name']}_Slab", L["rect"], z, z + H["slab"], M["slab"], col, bevel=0.02)
        if i > 0:
            _rect_box(f"{n}_{L['name']}_Floor", L["rect"], z + H["slab"], z + H["slab"] + 0.02, M["floor"], col, grow=-t)
        _walls(L, H, t, M, col)

    top = H["levels"][-1]
    roof_z = top["z"] + H["slab"] + top.get("ceiling", H["ceiling"])
    r = H.get("roof", {})
    if r:
        ov, x0, y0, x1, y1 = r.get("overhang", 0.6), *top["rect"]
        rr = (x0 - ov, y0 - ov, x1 + ov, y1 + ov)
        roof = _rect_box(f"{n}_Roof", rr, roof_z, roof_z + 0.25, M["roof"], col)
        roof.rotation_euler.x = math.radians(r.get("pitch_deg", 0))       # falls to the rear
        f = r.get("fascia", 0.3)
        for s, (dims, loc) in {
            "S": ((rr[2] - rr[0], 0.05, f), ((rr[0] + rr[2]) / 2, rr[1], roof_z + 0.1)),
            "N": ((rr[2] - rr[0], 0.05, f), ((rr[0] + rr[2]) / 2, rr[3], roof_z + 0.1)),
            "W": ((0.05, rr[3] - rr[1], f), (rr[0], (rr[1] + rr[3]) / 2, roof_z + 0.1)),
            "E": ((0.05, rr[3] - rr[1], f), (rr[2], (rr[1] + rr[3]) / 2, roof_z + 0.1)),
        }.items():
            box(f"{n}_Fascia_{s}", dims, loc, r.get("fascia_material", M["frame"]), col)

    a = H.get("alfresco")
    if a:
        L = levels[a["level"]]
        z = L["z"]
        _rect_box(f"{n}_Alfresco_Slab", a["rect"], z, z + H["slab"], M["slab"], col)
        _rect_box(f"{n}_Alfresco_Deck", a["rect"], z + H["slab"], z + H["slab"] + 0.03, M["deck"], col, grow=-0.05)
        x0, y0, x1, y1 = a["rect"]
        for k, (px, py) in enumerate(((x0 + 0.2, y1 - 0.2), (x1 - 0.2, y1 - 0.2))):
            box(f"{n}_Alfresco_Post{k}", (0.25, 0.25, z), (px, py, z / 2), M["wall"], col)   # down to ground
        _balustrade(f"{n}_Alfresco_Bal", a["rect"], z + H["slab"], "N", M, col)

    for b in H.get("balconies", []):
        L = levels[b["level"]]
        x0, y0, x1, y1 = L["rect"]
        d = b["depth"]
        rect = {"N": (x0, y1, x1, y1 + d), "S": (x0, y0 - d, x1, y0), "E": (x1, y0, x1 + d, y1), "W": (x0 - d, y0, x0, y1)}[b["side"]]
        _rect_box(f"{n}_Balcony_{b['level']}", rect, L["z"], L["z"] + H["slab"], M["slab"], col, bevel=0.02)
        outer = {"N": "NWE", "S": "SWE", "E": "ENS", "W": "WNS"}[b["side"]]
        _balustrade(f"{n}_Balcony_{b['level']}_Bal", rect, L["z"] + H["slab"], outer, M, col)

    c = H.get("core")
    if c:
        zs = [levels[l]["z"] for l in c["levels"]]
        z1 = max(levels[l]["z"] + H["slab"] + levels[l].get("ceiling", H["ceiling"]) for l in c["levels"])
        _rect_box(f"{n}_{c.get('name', 'Core')}", c["rect"], min(zs), z1 + 0.3, M["wall"], col)

    ob = H.get("observatory")
    if ob:
        h = ob.get("height", 2.7)
        z0 = roof_z + 0.25
        _rect_box(f"{n}_Obs_Slab", ob["rect"], z0, z0 + 0.15, M["slab"], col)
        ol = {"name": "Obs", "z": z0 - H["slab"] + 0.15, "rect": ob["rect"], "ceiling": h,
              "openings": [{"side": s, "offset": 0.3, "width": (ob["rect"][2] - ob["rect"][0] if s in "SN" else ob["rect"][3] - ob["rect"][1]) - 0.6,
                            "height": h - 0.3, "type": "window"} for s in "SNWE"]}
        _walls(ol, H, 0.2, M, col)
        x0, y0, x1, y1 = ob["rect"]
        _rect_box(f"{n}_Obs_Roof", (x0 - 0.4, y0 - 0.4, x1 + 0.4, y1 + 0.4), z0 + 0.15 + h, z0 + 0.4 + h, M["roof"], col)

    pl = H.get("pool")
    if pl:
        z = pl.get("z", 0.0)
        _rect_box(f"{n}_Pool_Coping", pl["rect"], z - 0.02, z + 0.06, M["coping"], col, grow=0.4)
        _rect_box(f"{n}_Pool_Water", pl["rect"], z, z + 0.08, M["water"], col)

    ctx.report["house_objects"] = len(col.all_objects)
