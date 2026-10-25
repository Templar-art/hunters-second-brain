"""Low-poly version of a scan:  blender -b -P lowpoly.py -- <in.usdz|.blend> <out.glb> [faces 20000] [tex 2048]
Decimates every mesh (collapse) to the face budget overall and downsizes textures; exports GLB."""
import bpy, sys, os
a = sys.argv[sys.argv.index("--") + 1:]
src, out = a[0], a[1]; BUDGET = int(a[2]) if len(a) > 2 else 20000; TEX = int(a[3]) if len(a) > 3 else 2048
if src.endswith(".blend"):
    bpy.ops.wm.open_mainfile(filepath=src)
else:
    bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.wm.usd_import(filepath=src)
ms = [o for o in bpy.data.objects if o.type == "MESH"]
total = sum(len(o.data.polygons) for o in ms)
for o in ms:
    m = o.modifiers.new("dec", "DECIMATE"); m.ratio = min(1.0, BUDGET / max(total, 1))
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    with bpy.context.temp_override(object=o, active_object=o):
        bpy.ops.object.modifier_apply(modifier=m.name)
for im in bpy.data.images:
    if im.size[0] > TEX:
        im.scale(TEX, int(im.size[1] * TEX / im.size[0]))
bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_image_format="JPEG", export_jpeg_quality=85)
print("LOWPOLY_OK", total, "->", sum(len(o.data.polygons) for o in ms), "faces;", round(os.path.getsize(out) / 1e6, 1), "MB")
