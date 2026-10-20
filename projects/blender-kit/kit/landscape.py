"""landscape: dune grass, palms, planted beds, pots, trees — all from the kit asset library.

scene.json "landscape": {
  "dune_grass": {"zone": [x0, x1, y0, y1], "count": 680, "exclude": [[x0, x1, y0, y1]],
                 "variants": 24, "pieces": [4, 12], "spread": 0.6, "scale": [5, 9]},
  "palms":  {"at": [[x, y], …], "height": [8, 9.5], "fronds": 11, "lean": 0.12},
  "beds":   [{"name": "GardenBed", "zone": [...], "count": 40, "assets": ["calathea", "anthurium", "fern"],
              "scale": [0.8, 1.6], "z": 0}],
  "pots":   [{"name": "Pot", "at": [[x, y, z], …], "scale": 1.0}],
  "trees":  [{"name": "StreetTree", "asset": "island_tree", "at": [[x, y], …]}]
}
Counts are what the density report checks — a bare scene has to be asked for explicitly.
"""
import math
import bmesh, bpy
from mathutils import Matrix
from . import core


def _clump_meshes(ctx, spec):
    """Build a few dune-grass clump meshes by merging random grass pieces; instances share them."""
    pieces = [o for o in core.assets("grass") if o.type == "MESH"]
    lo, hi = spec.get("pieces", [4, 12])
    spread = spec.get("spread", 0.6)
    meshes = []
    for v in range(spec.get("variants", 24)):
        bm = bmesh.new()
        for _ in range(ctx.rng.randint(lo, hi)):
            src = ctx.rng.choice(pieces)
            m = Matrix.Translation((ctx.rng.uniform(-spread, spread) / 6, ctx.rng.uniform(-spread, spread) / 6, 0)) @ \
                Matrix.Rotation(ctx.rng.uniform(0, 6.28), 4, "Z")
            tmp = src.data.copy()
            tmp.transform(m)
            bm.from_mesh(tmp)
            bpy.data.meshes.remove(tmp)
        me = bpy.data.meshes.new(f"DuneClump_{v}")
        bm.to_mesh(me)
        bm.free()
        me.materials.append(core.mat("grass_medium_01"))
        meshes.append(me)
    return meshes


def dune_grass(spec, ctx, col):
    meshes = _clump_meshes(ctx, spec)
    s0, s1 = spec.get("scale", [5, 9])
    pts = core.scatter_points(ctx.rng, spec["zone"], spec["count"], spec.get("exclude", []))
    for i, (x, y) in enumerate(pts):
        o = bpy.data.objects.new(f"DuneGrass_{i}", ctx.rng.choice(meshes))
        o.location = (x, y, ctx.terrain(x, y))
        o.rotation_euler.z = ctx.rng.uniform(0, 6.28)
        s = ctx.rng.uniform(s0, s1)
        o.scale = (s, s, s * ctx.rng.uniform(0.8, 1.3))
        col.objects.link(o)


def palm(i, x, y, spec, ctx, col):
    h = ctx.rng.uniform(*spec.get("height", [8, 9.5]))
    segs = 8
    lean = spec.get("lean", 0.12)
    lean_dir = ctx.rng.uniform(0, 6.28)
    z0 = ctx.terrain(x, y)
    seg_h = h / segs
    for s in range(segs):
        t = s / segs
        off = lean * h * t * t
        core.cyl(f"Palm{i}_t{s}", 0.24 - 0.08 * t, seg_h * 1.02,
                 (x + off * math.cos(lean_dir), y + off * math.sin(lean_dir), z0 + seg_h * (s + 0.5)), "PalmTrunk", col, verts=10, r_top=0.23 - 0.08 * t)
    top = (x + lean * h * math.cos(lean_dir), y + lean * h * math.sin(lean_dir), z0 + h)
    n = spec.get("fronds", 11)
    for f in range(n):
        a = 2 * math.pi * f / n + ctx.rng.uniform(-0.1, 0.1)
        L = ctx.rng.uniform(3.0, 3.6)
        droop = ctx.rng.uniform(0.3, 0.5)
        cx, cy = top[0] + math.cos(a) * L / 2 * math.cos(droop), top[1] + math.sin(a) * L / 2 * math.cos(droop)
        core.box(f"Palm{i}_f{f}", (L, 0.55, 0.04), (cx, cy, top[2] - math.sin(droop) * L / 2 + 0.1), "PalmLeaf", col, rot=(0, droop, a))


def beds(spec, ctx, col):
    pool = [o for k in spec["assets"] for o in core.assets(k) if o.type == "MESH"]
    s0, s1 = spec.get("scale", [0.8, 1.6])
    for i, (x, y) in enumerate(core.scatter_points(ctx.rng, spec["zone"], spec["count"], spec.get("exclude", []))):
        z = spec.get("z", ctx.terrain(x, y) if "z" not in spec else spec["z"])
        core.copy_obj(ctx.rng.choice(pool), f"{spec['name']}_{i}", col, (x, y, z), ctx.rng.uniform(0, 6.28), ctx.rng.uniform(s0, s1))


def pots(spec, ctx, col):
    parts = core.assets("potted_plant")
    anchor = next(p for p in parts if p.name.endswith("_pot"))     # "at" = where the pot itself sits
    for i, (x, y, z) in enumerate(spec["at"]):
        rz = ctx.rng.uniform(0, 6.28)
        for p in parts:
            o = core.copy_obj(p, f"{spec['name']}_{i}_{p.name.removeprefix('KIT_potted_plant_02')}", col)
            d = p.location - anchor.location
            o.location = (x + d.x, y + d.y, z + d.z)
            o.rotation_euler.z = rz
            o.scale = [v * spec.get("scale", 1.0) for v in p.scale]


def trees(spec, ctx, col):
    src = core.assets(spec["asset"])[0]
    for i, (x, y) in enumerate(spec["at"]):
        core.copy_obj(src, f"{spec['name']}_{i}", col, (x, y, ctx.terrain(x, y)), ctx.rng.uniform(0, 6.28))


def build(spec, ctx):
    col = core.coll("Landscape")
    if "dune_grass" in spec:
        dune_grass(spec["dune_grass"], ctx, core.coll("Land_DuneGrass", col))
    if "palms" in spec:
        pc = core.coll("Land_Palms", col)
        for i, (x, y) in enumerate(spec["palms"]["at"]):
            palm(i, x, y, spec["palms"], ctx, pc)
    for b in spec.get("beds", []):
        beds(b, ctx, core.coll("Land_Beds", col))
    for p in spec.get("pots", []):
        pots(p, ctx, core.coll("Land_Pots", col))
    for t in spec.get("trees", []):
        trees(t, ctx, core.coll("Land_Trees", col))
