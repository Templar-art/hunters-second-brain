"""passes: density report, camera clearance check, guide frames, material-ID frames.

scene.json "passes": {"density": {"min_total": 1500, "min": {"Landscape": 800}},
                      "clearance": {"radius": 0.35, "every": 4},
                      "guides": true, "id": true, "resolution": [1920, 1080], "percent": 100}
"""
import json, os
import bpy
from mathutils import Vector
from . import core

# ---------- density ----------

def density(spec, ctx):
    counts = {}
    for c in bpy.context.scene.collection.children:
        if c.name == core.ASSET_COL:
            continue
        counts[c.name] = len([o for o in c.all_objects if o.type == "MESH"])
    total = sum(counts.values())
    fails = []
    if spec.get("min_total") and total < spec["min_total"]:
        fails.append(f"total {total} < {spec['min_total']}")
    for k, v in spec.get("min", {}).items():
        if counts.get(k, 0) < v:
            fails.append(f"{k} {counts.get(k, 0)} < {v}")
    ctx.report["density"] = {"total": total, "by_collection": counts, "fails": fails}
    return fails


# ---------- clearance ----------

DIRS = [Vector(d) for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]


def clearance(spec, ctx):
    sc = bpy.context.scene
    r, every = spec.get("radius", 0.35), spec.get("every", 4)
    hits = []
    cams = [m for m in sc.timeline_markers if m.camera]
    cams.sort(key=lambda m: m.frame)
    for i, m in enumerate(cams):
        end = cams[i + 1].frame if i + 1 < len(cams) else sc.frame_end + 1
        for f in range(m.frame, end, every):
            sc.frame_set(f)
            dg = bpy.context.evaluated_depsgraph_get()
            p = m.camera.matrix_world.translation
            for d in DIRS:
                ok, loc, _, _, obj, _ = sc.ray_cast(dg, p, d, distance=r)
                if ok:
                    hits.append({"shot": m.name, "frame": f, "object": obj.name, "dist": round((loc - p).length, 2)})
                    break
    ctx.report["clearance"] = hits
    return hits


# ---------- renders ----------

def _render(out_dir, prefix, frames, res, pct):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = pct
    sc.render.image_settings.file_format = "PNG"
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for name, f in frames:
        sc.frame_set(f)
        m = next(mm for mm in sc.timeline_markers if mm.name == name)
        sc.camera = m.camera
        sc.render.filepath = os.path.join(out_dir, f"{prefix}_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        paths.append(sc.render.filepath)
    return paths


# Category -> flat colour. Key colours that look like real paint (magenta, lavender) leak into
# image-model output, so neighbours share the house white and people are purple (16 Oct shootout).
CAT = {
    "timber": (1, 0, 0), "glass": (0, 1, 1), "concrete": (0.6, 0.6, 0.6), "render": (1, 1, 1),
    "metal": (0, 0, 0), "water": (0, 0.2, 1), "ocean": (0, 0, 0.45), "surf": (0.85, 0.85, 1),
    "sand": (1, 0.85, 0), "wetsand": (0.6, 0.45, 0), "grass": (0, 0.8, 0), "plant": (0, 0.35, 0),
    "trunk": (0.45, 0.2, 0.05), "fabric": (1, 0, 1), "stone": (1, 0.5, 0), "road": (0.25, 0.25, 0.25),
    "neighbour": (1, 1, 1), "person": (0.5, 0, 0.5), "hedge": (0.0, 0.5, 0.25), "screen": (0.05, 0.05, 0.05),
}
RULES = (("mannequin", "person"), ("person_", "person"), ("hedge", "hedge"), ("tvblack", "screen"), ("boucle", "fabric"),
         ("linen", "fabric"), ("wool", "fabric"), ("oak", "timber"), ("porcelain", "stone"), ("stonetile", "stone"),
         ("pool_water", "water"), ("poolwater", "water"), ("ocean", "ocean"), ("surf", "surf"), ("wetsand", "wetsand"),
         ("sand", "sand"), ("beach", "sand"), ("glass", "glass"), ("timber", "timber"), ("deck", "timber"),
         ("batten", "timber"), ("garage", "timber"), ("wood_floor", "timber"), ("path", "timber"), ("bronze", "metal"),
         ("post", "metal"), ("fascia", "metal"), ("carpaint", "metal"), ("concrete", "concrete"), ("slab", "concrete"),
         ("roof", "concrete"), ("pool_", "concrete"), ("render", "render"), ("wall", "render"), ("ceiling", "render"),
         ("neighbour", "neighbour"), ("nb_", "neighbour"), ("grass", "grass"), ("lawn", "grass"), ("dunegrass", "grass"), ("leaf", "plant"),
         ("leaves", "plant"), ("palmleaf", "plant"), ("anthurium", "plant"), ("calathea", "plant"), ("fern", "plant"),
         ("trunk", "trunk"), ("bark", "trunk"), ("street", "road"), ("footpath", "road"), ("marble", "stone"),
         ("coping", "stone"), ("tyre", "metal"), ("cargrey", "metal"), ("carwhite", "metal"), ("dirt", "trunk"), ("_pot", "stone"), ("island", "stone"), ("tile", "stone"), ("fabric", "fabric"), ("sofa", "fabric"), ("rug", "fabric"),
         ("lounger", "fabric"), ("chair", "fabric"), ("table", "stone"), ("lamp", "metal"))


def category(obj_name, mat_name):
    """Material name decides first (a "Garage" wall in Render is still render); the object
    name is the fallback for generic materials."""
    for n in (mat_name.lower(), obj_name.lower()):
        c = next((c for k, c in RULES if k in n), None)
        if c:
            return c
    return None


def material_id(ctx):
    """Swap every material slot (object-linked) to its flat ID colour; lights off; exact colours."""
    sc = bpy.context.scene
    mats, unknown = {}, set()

    def idmat(c):
        if c not in mats:
            m = bpy.data.materials.new("ID_" + c)
            m.use_nodes = True
            nt = m.node_tree
            nt.nodes.clear()
            e = nt.nodes.new("ShaderNodeEmission")
            e.inputs[0].default_value = (*CAT[c], 1)
            o = nt.nodes.new("ShaderNodeOutputMaterial")
            nt.links.new(e.outputs[0], o.inputs[0])
            mats[c] = m
        return mats[c]

    for o in sc.objects:
        if o.type != "MESH":
            continue
        for sl in o.material_slots:
            c = category(o.name, sl.material.name if sl.material else "")
            if c is None:
                unknown.add(f"{o.name}:{sl.material.name if sl.material else '-'}")
                c = "render"
            sl.link = "OBJECT"
            sl.material = idmat(c)
    w = bpy.data.worlds.new("ID_Sky")
    w.use_nodes = True
    next(n for n in w.node_tree.nodes if n.type == "BACKGROUND").inputs[0].default_value = (0.55, 0.8, 1, 1)
    sc.world = w
    for o in sc.objects:
        if o.type == "LIGHT":
            o.hide_render = True
        if any(k in o.name for k in ("Fence", "Balustrade")):
            o.hide_render = True
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.eevee.taa_render_samples = 1
    sc.render.filter_size = 0.0
    ctx.report["id_unknown"] = sorted(unknown)[:50]


def build(spec, ctx, out_dir, blend_path):
    res, pct = spec.get("resolution", [1920, 1080]), spec.get("percent", 100)
    frames = ctx.report.get("guide_frames", [])
    if "density" in spec:
        density(spec["density"], ctx)
    if "clearance" in spec:
        clearance(spec["clearance"], ctx)
    if spec.get("guides", True) and frames:
        ctx.report["guides"] = _render(os.path.join(out_dir, "guides"), "shot", frames, res, pct)
    if spec.get("id", True) and frames:
        material_id(ctx)                                   # destructive: runs last, file not re-saved
        ctx.report["id"] = _render(os.path.join(out_dir, "id"), "id", frames, res, pct)
