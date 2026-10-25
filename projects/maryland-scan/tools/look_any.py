"""Level a scan: fit the ground plane (PCA, smallest-variance axis = up), rotate it to Z-up, sit it on z=0,
then render obliques around the densest part (the house):
  blender -b -P level.py -- <in.usdz> <out prefix> [save.blend]"""
import bpy, sys, math
import numpy as np
from mathutils import Vector, Matrix
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
(bpy.ops.import_scene.gltf(filepath=a[0]) if a[0].endswith(".glb") else bpy.ops.wm.usd_import(filepath=a[0]))
ms = [o for o in bpy.data.objects if o.type == "MESH"]
for m in bpy.data.materials:
    if not m.use_nodes: continue
    nt = m.node_tree; b = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    o = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
    if b and o and b.inputs["Base Color"].links:
        e = nt.nodes.new("ShaderNodeEmission"); nt.links.new(b.inputs["Base Color"].links[0].from_socket, e.inputs[0]); nt.links.new(e.outputs[0], o.inputs[0])
P = np.concatenate([np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) for o in ms])
c = P.mean(0); U, S, Vt = np.linalg.svd(P - c, full_matrices=False)
up = Vt[2]
# up should point away from the side the drone saw from: most normals face the cameras (above)
N = np.concatenate([np.array([(o.matrix_world.to_3x3() @ p.normal)[:] for p in o.data.polygons]) for o in ms])
if (N @ up).mean() < 0: up = -up
R = Vector(up).rotation_difference(Vector((0, 0, 1))).to_matrix().to_4x4()
root = bpy.data.objects.new("scan_root", None); bpy.context.scene.collection.objects.link(root)
for o in list(bpy.data.objects):
    if o.parent is None and o is not root: o.parent = root
root.matrix_world = R @ Matrix.Translation(Vector(-c))
bpy.context.view_layer.update()
Q = np.concatenate([np.array([(o.matrix_world @ v.co)[:] for v in o.data.vertices]) for o in ms])
z0 = np.percentile(Q[:, 2], 5); root.location.z -= z0; Q[:, 2] -= z0
span = Q.max(0) - Q.min(0)
# house = tallest dense stuff: centre on points above the 90th height percentile
hi = Q[Q[:, 2] > np.percentile(Q[:, 2], 90)]
hc = Vector(np.median(hi, 0)); hc.z = np.percentile(Q[:, 2], 70)
print("LEVEL span", np.round(span, 3), "house centre", np.round(hc[:], 3))
sc = bpy.context.scene; sc.view_settings.view_transform = "Standard"
sc.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE_NEXT"
sc.render.resolution_x, sc.render.resolution_y = 960, 600
w = bpy.data.worlds.new("w"); sc.world = w
cd = bpy.data.cameras.new("c"); cd.lens = 35; cd.clip_start = 0.001; cam = bpy.data.objects.new("c", cd); sc.collection.objects.link(cam); sc.camera = cam
r = float(max(span[0], span[1])) * 0.45
for k, (az, el) in enumerate([(0, 30), (90, 30), (180, 30), (270, 30), (45, 75), (225, 15)]):
    d = Vector((math.cos(math.radians(el)) * math.cos(math.radians(az)), math.cos(math.radians(el)) * math.sin(math.radians(az)), math.sin(math.radians(el))))
    cam.location = hc + d * r
    cam.rotation_euler = (hc - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = a[1] + f".{k}.png"; bpy.ops.render.render(write_still=True)
if len(a) > 2:
    bpy.ops.wm.save_as_mainfile(filepath=a[2])
