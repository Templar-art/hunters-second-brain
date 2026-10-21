"""Dump per-subframe wing elevation, distance to camera and screen x for each gull (for SFX sync)."""
import bpy, json, math, os
from bpy_extras.object_utils import world_to_camera_view
sc = bpy.context.scene; cam = sc.camera
out = {}
steps = 8
for root in [o for o in bpy.data.objects if o.name.startswith("Gull_")]:
    tag = root.name[5:]
    inner = bpy.data.objects[f"{tag}_wingIn_1"]
    rows = []
    for f in range(sc.frame_start, sc.frame_end + 1):
        for s in range(steps):
            sc.frame_set(f, subframe=s / steps)
            p = root.matrix_world.translation
            v = world_to_camera_view(sc, cam, p)
            rows.append([f + s / steps, -math.degrees(inner.rotation_euler[1]), (p - cam.matrix_world.translation).length, v.x, v.y])
    out[tag] = rows
fps = sc.render.fps / sc.render.fps_base
json.dump({"fps": fps, "birds": out}, open(os.path.join(os.path.dirname(bpy.data.filepath), "wings.json"), "w"))
print("DUMPED", list(out))
