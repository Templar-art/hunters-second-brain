"""Shared helpers for the 10x Blender kit: collections, materials, primitives, assets, terrain."""
import math, random
import bmesh, bpy
from bpy_extras import anim_utils
from mathutils import Vector

ASSET_COL = "_KitAssets"


class Ctx:
    """Build context passed to every module."""
    def __init__(self, spec, base_dir):
        self.spec = spec
        self.base = base_dir
        self.rng = random.Random(spec.get("seed", 1))
        self.terrain = lambda x, y: 0.0       # replaced by site.beach when a beach exists
        self.report = {}

    def path(self, p):
        import os
        return p if os.path.isabs(p) else os.path.normpath(os.path.join(self.base, p))


# ---------- collections ----------

def coll(name, parent=None):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


# ---------- materials ----------

FALLBACK_COLOURS = {
    "render": (0.92, 0.91, 0.88), "concrete": (0.6, 0.6, 0.58), "glass": (0.6, 0.75, 0.8),
    "timber": (0.45, 0.3, 0.18), "sand": (0.86, 0.78, 0.6), "water": (0.1, 0.4, 0.6),
    "grass": (0.25, 0.45, 0.15), "metal": (0.3, 0.25, 0.2), "hedge": (0.15, 0.35, 0.12),
}


def mat(name):
    """Return the material by name (asset library materials are loaded with the assets);
    otherwise create a plain principled material so a build never fails on a missing name."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    col = next((c for k, c in FALLBACK_COLOURS.items() if k in name.lower()), (0.7, 0.7, 0.7))
    bsdf.inputs["Base Color"].default_value = (*col, 1)
    return m


# ---------- primitives ----------

def _obj(name, me, col, loc, rot=(0, 0, 0)):
    o = bpy.data.objects.new(name, me)
    o.location = loc
    o.rotation_euler = rot
    col.objects.link(o)
    return o


def box(name, dims, loc, material, col, bevel=0.0, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.scale(bm, vec=dims, verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat(material))
    o = _obj(name, me, col, loc, rot)
    if bevel:
        b = o.modifiers.new("Bevel", "BEVEL")
        b.width = bevel
        b.segments = 2
    return o


def cyl(name, r, h, loc, material, col, verts=16, r_top=None, rot=(0, 0, 0)):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r, radius2=r if r_top is None else r_top, depth=h)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat(material))
    return _obj(name, me, col, loc, rot)


def grid(name, x0, x1, y0, y1, step, zfn, material, col):
    """Ground mesh with z = zfn(x, y)."""
    nx, ny = max(2, int((x1 - x0) / step) + 1), max(2, int((y1 - y0) / step) + 1)
    bm = bmesh.new()
    verts = [[bm.verts.new((x0 + (x1 - x0) * i / (nx - 1), y0 + (y1 - y0) * j / (ny - 1), 0)) for i in range(nx)] for j in range(ny)]
    for row in verts:
        for v in row:
            v.co.z = zfn(v.co.x, v.co.y)
    for j in range(ny - 1):
        for i in range(nx - 1):
            bm.faces.new((verts[j][i], verts[j][i + 1], verts[j + 1][i + 1], verts[j + 1][i]))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    me.materials.append(mat(material))
    return _obj(name, me, col, (0, 0, 0))


# ---------- assets ----------

def load_assets(path):
    """Append every A_* collection from the kit asset library into a hidden collection."""
    holder = coll(ASSET_COL)
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.collections = [c for c in src.collections if c.startswith("A_")]
        dst.worlds = list(src.worlds)
    for c in dst.collections:
        holder.children.link(c)
        for o in c.objects:                 # free the clean names for the copies
            o.name = "KIT_" + o.name
    vl = bpy.context.view_layer.layer_collection.children[ASSET_COL]
    vl.exclude = True
    holder.hide_render = True
    return {c.name[2:]: list(c.objects) for c in dst.collections}


def assets(key):
    c = bpy.data.collections.get("A_" + key)
    if c is None:
        raise KeyError(f"asset '{key}' not in the kit library")
    return list(c.objects)


def copy_obj(src, name, col, loc=None, rot_z=None, scale=None):
    """Linked duplicate: shares mesh data, so thousands of copies stay cheap."""
    o = src.copy()
    o.name = name
    col.objects.link(o)
    if loc is not None:
        o.location = loc
    if rot_z is not None:
        o.rotation_euler.z = rot_z
    if scale is not None:
        o.scale = (scale, scale, scale)
    return o


def copy_hierarchy(root, new_name, col):
    """Copy an object tree (e.g. rig empty > armature > body), re-pointing parents,
    armature modifiers and actions at the copies."""
    mapping = {}
    for o in [root] + list(root.children_recursive):
        c = o.copy()
        if o.type == "ARMATURE":
            c.data = o.data.copy()
        if o.animation_data and o.animation_data.action:
            c.animation_data.action = o.animation_data.action.copy()
        old_id = root.name.removeprefix("KIT_").removeprefix("Rig_")
        c.name = o.name.removeprefix("KIT_").replace(old_id, new_name)
        col.objects.link(c)
        mapping[o] = c
    for o, c in mapping.items():
        if o.parent in mapping:
            c.parent = mapping[o.parent]
        for m in c.modifiers:
            if m.type == "ARMATURE" and m.object in mapping:
                m.object = mapping[m.object]
    return mapping[root]


# ---------- animation ----------

def fcurves(o):
    ad = o.animation_data
    if not ad or not ad.action:
        return []
    cb = anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot)
    return list(cb.fcurves) if cb else []


def key_path(o, frames_points, data_path="location"):
    """frames_points: [(frame, (x, y, z)), …]"""
    for f, p in frames_points:
        setattr(o, data_path, p)
        o.keyframe_insert(data_path, frame=f)


def scatter_points(rng, zone, count, exclude=(), min_dist=0.0):
    """Random points in zone [x0, x1, y0, y1], avoiding exclude rects."""
    x0, x1, y0, y1 = zone
    pts, tries = [], 0
    while len(pts) < count and tries < count * 50:
        tries += 1
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if any(a <= x <= b and c <= y <= d for a, b, c, d in exclude):
            continue
        if min_dist and any((x - px) ** 2 + (y - py) ** 2 < min_dist ** 2 for px, py in pts):
            continue
        pts.append((x, y))
    return pts
