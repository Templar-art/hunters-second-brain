"""Render 4 orbit views + top of a scanned usdz:  blender -b -P look.py -- <in.usdz> <out.jpg>"""
import bpy, sys, math
from mathutils import Vector
a = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.usd_import(filepath=a[0])
ms = [o for o in bpy.data.objects if o.type == "MESH"]
pts = [o.matrix_world @ Vector(c) for o in ms for c in o.bound_box]
lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)])
c = (lo + hi) / 2; r = (hi - lo).length / 2
print("BOUNDS", [round(v, 2) for v in lo], [round(v, 2) for v in hi], "faces", sum(len(o.data.polygons) for o in ms))
for m in bpy.data.materials:                 # unlit: show the scan's own texture as captured
    if not m.use_nodes: continue
    nt = m.node_tree; b = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    o = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
    if b and o and b.inputs["Base Color"].links:
        e = nt.nodes.new("ShaderNodeEmission"); nt.links.new(b.inputs["Base Color"].links[0].from_socket, e.inputs[0])
        nt.links.new(e.outputs[0], o.inputs[0])
sc = bpy.context.scene; sc.view_settings.view_transform = "Standard"; sc.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items] else "BLENDER_EEVEE_NEXT"
sc.render.resolution_x, sc.render.resolution_y = 800, 500
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
cd = bpy.data.cameras.new("c"); cd.lens = 35; cam = bpy.data.objects.new("c", cd); sc.collection.objects.link(cam); sc.camera = cam
import os; outs = []
up = 2  # usdz from Object Capture is Y-up; Blender importer converts to Z-up
for k, (az, el) in enumerate([(0, 35), (90, 35), (180, 35), (270, 35), (0, 85)]):
    d = Vector((math.cos(math.radians(el)) * math.cos(math.radians(az)), math.cos(math.radians(el)) * math.sin(math.radians(az)), math.sin(math.radians(el))))
    cam.location = c + d * r * 2.0
    cam.rotation_euler = (c - cam.location).to_track_quat("-Z", "Y").to_euler()
    p = a[1] + f".{k}.png"; sc.render.filepath = p; bpy.ops.render.render(write_still=True); outs.append(p)
