# Render guide frames for chosen frames only (camera from the timeline marker), never saves.
#   blender -b build/coastal-test.blend -P audit/render_guides.py -- <out_dir> <frame> [<frame> ...]
import bpy, os, sys
a = sys.argv[sys.argv.index("--") + 1:]
out, frames = a[0], [int(f) for f in a[1:]]
sc = bpy.context.scene
sc.render.image_settings.file_format = "PNG"
m = sorted(sc.timeline_markers, key=lambda m: m.frame)
for f in frames:
    sc.frame_set(f)
    sc.camera = [mm for mm in m if mm.frame <= f][-1].camera
    sc.render.filepath = os.path.join(out, f"shot_{f:04d}.png")
    bpy.ops.render.render(write_still=True)
