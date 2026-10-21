"""Dump the car's world position per frame from maryland.blend -> track.json (for follow.py)."""
import json, os, bpy
sc = bpy.context.scene; car = bpy.data.objects["Sketchfab_model"]; out = []
for f in range(sc.frame_start, sc.frame_end + 1):
    sc.frame_set(f); p = car.matrix_world.translation
    out.append([f, p.x, p.y, p.z])
json.dump(out, open(os.path.join(os.path.dirname(bpy.data.filepath), "track.json"), "w"))
print("TRACK_OK", len(out))
