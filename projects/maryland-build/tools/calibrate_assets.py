"""Import every assets/<id>/<id>.gltf in a row and render it from -Y (front view) plus top-down, to read each
asset's native front direction. blender -b --factory-startup -P tools/calibrate_assets.py"""
import bpy, os, math
from mathutils import Vector
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
ids = sorted(os.listdir(os.path.join(HERE, "assets")))
x = 0.0; dims = {}
for i in ids:
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(HERE, "assets", i, i + ".gltf"))
    new = [o for o in bpy.data.objects if o not in before]
    pts = [o.matrix_world @ Vector(c) for o in new if o.type == "MESH" for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    root = [o for o in new if o.parent is None]
    for o in root:
        o.location.x += x - lo.x
    dims[i] = [round(v, 2) for v in (hi - lo)]
    cu = bpy.data.curves.new(i, "FONT"); cu.body = i[:14]; cu.size = 0.12
    t = bpy.data.objects.new("lbl_" + i, cu); sc.collection.objects.link(t); t.location = (x, lo.y - 0.4, 0)
    x += (hi.x - lo.x) + 0.5
print("DIMS", dims)
bpy.ops.mesh.primitive_plane_add(size=200); 
w = bpy.data.worlds.new("w"); sc.world = w; w.color = (0.6, 0.6, 0.6)
s = bpy.data.objects.new("s", bpy.data.lights.new("s", "SUN")); sc.collection.objects.link(s); s.rotation_euler = (0.6, 0.2, 0.3); s.data.energy = 3
sc.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE_NEXT"
for name, loc, rot, ortho in (("front", (x / 2, -12, 1.0), (math.radians(88), 0, 0), x / 2 + 1),
                              ("top", (x / 2, 0, 20), (0, 0, 0), x / 2 + 1)):
    cd = bpy.data.cameras.new(name); cd.type = "ORTHO"; cd.ortho_scale = x + 1
    c = bpy.data.objects.new(name, cd); sc.collection.objects.link(c); c.location = loc; c.rotation_euler = rot
    sc.camera = c; sc.render.resolution_x, sc.render.resolution_y = 3000, 500 if name == "front" else 700
    sc.render.filepath = os.path.join(HERE, "qc", "calib_" + name + ".png"); bpy.ops.render.render(write_still=True)
