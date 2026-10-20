"""site: lot, street, beach terrain + ocean, boardwalk, neighbour houses.

scene.json "site": {
  "lot":    {"size": [24, 50], "center": [0, 14], "lawn": "leafy_grass",
             "boundary_walls": {"x": 12, "height": 1.2, "length": 52, "y": 16},
             "hedges": {"x": 11.4, "height": 1.8, "length": 50, "y": 16},
             "driveway": {"x": 6, "y": 30, "size": [5.5, 22]}, "letterbox": [-6.8, 24.5]},
  "street": {"y": 46, "width": 10, "length": 300, "footpath": {"y": 41, "width": 2.4},
             "lights": {"y": 42.6, "from": -60, "to": 60, "spacing": 30, "height": 7}},
  "beach":  {"x": [-150, 150], "y": [-80, 45], "step": 1.5,
             "profile": [[y, z], …], "dune_noise": {"band": [-30, -12], "amp": 0.35},
             "wet_sand_y": -71, "ocean": {"y": -260, "z": -3.5, "size": 360},
             "surf_y": [-76, -85, -94, -103, -112],
             "boardwalk": {"x": 1, "from_y": -11, "count": 16, "step": 1.3, "size": [1.6, 1.2]},
             "dune_posts": {"x": [-0.2, 2.2], "from_y": -12, "to_y": -30, "step": 2, "height": 0.9}},
  "neighbours": {"depth": 20, "houses": [{"x": -30, "width": 17.4, "storeys": 3,
                 "cladding": "NB_RenderWarm", "accent": "NB_TimberLight", "pool": true}, …]}
}
"""
import math
from . import core
from .core import box, cyl


def _interp(profile, y):
    pts = sorted(profile)
    if y <= pts[0][0]:
        return pts[0][1]
    for (y0, z0), (y1, z1) in zip(pts, pts[1:]):
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            t = t * t * (3 - 2 * t)                     # smooth step between profile points
            return z0 + (z1 - z0) * t
    return pts[-1][1]


def _noise_fn(rng, amp):
    waves = [(rng.uniform(0.05, 0.35), rng.uniform(0.08, 0.4), rng.uniform(0, 6.28), rng.uniform(0.5, 1)) for _ in range(6)]
    def n(x, y):
        return amp * sum(w * math.sin(fx * x + fy * y + ph) for fx, fy, ph, w in waves) / sum(w for *_, w in waves)
    return n


def beach(spec, ctx, col):
    prof = spec["profile"]
    dn = spec.get("dune_noise")
    noise = _noise_fn(ctx.rng, dn["amp"]) if dn else (lambda x, y: 0)

    def z(x, y):
        base = _interp(prof, y)
        if dn and dn["band"][0] <= y <= dn["band"][1]:
            lo, hi = dn["band"]
            fade = math.sin(math.pi * (y - lo) / (hi - lo))    # 0 at band edges, 1 in the middle
            base += noise(x, y) * fade
        return base

    ctx.terrain = z
    (x0, x1), (y0, y1) = spec["x"], spec["y"]
    core.grid("Beach", x0, x1, y0, y1, spec.get("step", 1.5), z, spec.get("material", "Sand"), col)

    if "wet_sand_y" in spec:
        wy = spec["wet_sand_y"]
        box("WetSand_Strip", (400, 6, 0.05), (0, wy, z(0, wy)), "WetSand", col)
    if "ocean" in spec:
        oc = spec["ocean"]
        o = box("Ocean", (oc.get("size", 360), oc.get("size", 360), 0.1), (0, oc["y"], oc["z"]), "Ocean", col)
        m = o.modifiers.new("Ocean", "OCEAN")
        m.geometry_mode = "DISPLACE"
        m.spatial_size = 50
        m.wave_scale = oc.get("wave_scale", 0.25)
    for i, sy in enumerate(spec.get("surf_y", [])):
        box(f"Surf_{i}", (400, 1.0 + 0.3 * i, 0.06), (0, sy, spec.get("ocean", {}).get("z", -3.5) + 0.3), "Surf", col)

    bw = spec.get("boardwalk")
    if bw:
        for i in range(bw["count"]):
            y = bw["from_y"] - i * bw["step"]
            box(f"Boardwalk_{i}", (*bw["size"], 0.08), (bw["x"], y, z(bw["x"], y) + 0.2), "Timber", col)
    dp = spec.get("dune_posts")
    if dp:
        i, y = 0, dp["from_y"]
        while y >= dp["to_y"]:
            for x in dp["x"]:
                box(f"DunePost_{i}_{x}", (0.1, 0.1, dp["height"]), (x, y, z(x, y) + dp["height"] / 2 + 0.2), "Timber", col)
            i += 1
            y -= dp["step"]


def lot(spec, ctx, col):
    (w, d), (cx, cy) = spec["size"], spec["center"]
    box("Lot_Lawn", (w, d, 0.04), (cx, cy, 0.0), spec.get("lawn", "leafy_grass"), col)
    bw = spec.get("boundary_walls")
    if bw:
        for s in (-1, 1):
            box(f"BoundaryWall_{s * bw['x']:g}", (0.25, bw["length"], bw["height"]), (s * bw["x"], bw["y"], bw["height"] / 2), "Render", col, bevel=0.02)
    hd = spec.get("hedges")
    if hd:
        for s in (-1, 1):
            box(f"Hedge_{s * hd['x']:g}", (0.7, hd["length"], hd["height"]), (s * hd["x"], hd["y"], hd["height"] / 2), "Hedge", col)
    dw = spec.get("driveway")
    if dw:
        box("Driveway", (*dw["size"], 0.06), (dw["x"], dw["y"], 0.0), "Footpath", col)
    if "letterbox" in spec:
        x, y = spec["letterbox"]
        box("Letterbox", (0.45, 0.35, 1.2), (x, y, 0.6), "concrete_wall_009", col, bevel=0.02)


def street(spec, ctx, col):
    box("Street", (spec["length"], spec["width"], 0.04), (0, spec["y"], 0.0), "Street", col)
    fp = spec.get("footpath")
    if fp:
        box("Footpath", (spec["length"], fp["width"], 0.08), (0, fp["y"], 0.0), "Footpath", col)
    lt = spec.get("lights")
    if lt:
        h, i, x = lt.get("height", 7), 0, lt["from"]
        while x <= lt["to"]:
            cyl(f"StreetLight_{i}", 0.07, h, (x, lt["y"], h / 2), "Bronze", col, verts=8)
            box(f"StreetLight_Head_{i}", (0.3, 1.2, 0.12), (x, lt["y"] - 0.6, h), "Bronze", col)
            i += 1
            x += lt["spacing"]


def neighbour(i, h, depth, col, rng):
    """A modern 1–4 storey beach house block: slabs, side/back walls, front piers + glazing,
    balconies on upper floors, roof, front fence, lawn, hedge, optional pool, driveway."""
    x, w, n = h["x"], h["width"], h.get("storeys", 2)
    clad, accent = h.get("cladding", "NB_RenderWarm"), h.get("accent", "NB_TimberLight")
    cy = depth / 2 - 1                                   # house spans y = -1 … depth-1
    fh = h.get("floor_height", 3.2)
    p = f"Neighbour_{i}"
    for s in range(n):
        z0 = 0.2 + s * fh
        set_back = 0 if s == 0 else rng.choice([0.4, 0.8, 1.1])
        d = depth - set_back
        sy = cy + set_back / 2
        front = sy - d / 2
        box(f"{p}_Slab_{s}", (w, d, 0.3), (x, sy, z0), "concrete_wall_009", col, bevel=0.02)
        box(f"{p}_Back_{s}", (w, 0.3, fh - 0.3), (x, depth - 1.1, z0 + fh / 2), clad, col)
        for side in (-1, 1):
            box(f"{p}_Side_{s}_{side}", (0.3, d, fh - 0.3), (x + side * (w / 2 - 0.2), sy, z0 + fh / 2), clad, col, bevel=0.02)
        piers = 4 + (s > 0) * rng.choice([1, 2])
        for k in range(piers):
            px = x - w / 2 + 0.5 + k * (w - 1) / (piers - 1)
            box(f"{p}_Pier_{s}_{k}", (0.6, 0.3, fh - 0.3), (px, front + 0.1, z0 + fh / 2), clad if k in (0, piers - 1) else accent, col)
        box(f"{p}_Glass_{s}", (w - 0.8, 0.05, fh - 0.5), (x, front + 0.2, z0 + fh / 2), "Glass", col)
        box(f"{p}_Int_{s}", (w - 0.6, d - 0.6, 0.06), (x, sy, z0 + fh - 0.2), "Render", col)
        if s > 0:
            bw = w * 0.85
            box(f"{p}_Balc_{s}", (bw, 1.8, 0.25), (x, front - 0.9, z0), "concrete_wall_009", col, bevel=0.02)
            box(f"{p}_BalcGlass_{s}", (bw, 0.03, 1.0), (x, front - 1.8, z0 + 0.65), "Glass", col)
    box(f"{p}_Roof", (w + 1.5, depth + 2, 0.35), (x, cy + 0.5, 0.2 + n * fh), "concrete_wall_009", col, bevel=0.03)
    box(f"{p}_Fence", (w, 0.04, 1.2), (x, -6, 0.6), "Glass", col)
    box(f"{p}_Lawn", (w + 4, 6, 0.04), (x, -6.5, 0.0), "leafy_grass", col)
    box(f"{p}_Hedge", (w + 2, 0.7, 1.0), (x, -9.6, 0.5), "Hedge", col)
    if h.get("pool"):
        box(f"{p}_PoolWater", (10, 3.6, 0.1), (x - 2, -4, 0.1), "PoolWater", col)
        box(f"{p}_PoolEdge", (10.6, 4.2, 0.08), (x - 2, -4, 0.0), "Tile", col)
    box(f"{p}_Drive", (5, 20, 0.06), (x + w / 2 - 2.5, depth + 12, 0.0), "Footpath", col)


def build(spec, ctx):
    col = core.coll("Site")
    if "beach" in spec:
        beach(spec["beach"], ctx, core.coll("Site_Beach", col))
    if "lot" in spec:
        lot(spec["lot"], ctx, core.coll("Site_Lot", col))
    if "street" in spec:
        street(spec["street"], ctx, core.coll("Site_Street", col))
    nb = spec.get("neighbours")
    if nb:
        ncol = core.coll("Site_Neighbours", col)
        for i, h in enumerate(nb["houses"]):
            neighbour(i, h, nb.get("depth", 20), ncol, ctx.rng)
