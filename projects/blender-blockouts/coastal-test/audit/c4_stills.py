# C4 ground-gimbal push-in: start/end framing stills on a throwaway copy (markers removed, temp camera, never saved).
import bpy, math, sys
out = sys.argv[sys.argv.index("--") + 1]
sc = bpy.context.scene
for m in list(sc.timeline_markers):
    sc.timeline_markers.remove(m)
cd = bpy.data.cameras.new("C4_tmp"); cd.lens = 28.0; cd.clip_start = 0.1; cd.clip_end = 1000
cam = bpy.data.objects.new("C4_tmp", cd); sc.collection.objects.link(cam)
sc.camera = cam
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 100
sc.render.image_settings.file_format = "PNG"
for tag, loc, pitch, yaw in [("start", (5.5, -20, 1.34), 1, 186), ("end", (6.0, -13, 1.52), 1, 190)]:
    cam.location = loc
    cam.rotation_euler = (math.radians(90 + pitch), 0, math.radians(180 + yaw))
    sc.render.filepath = f"{out}/c4-{tag}.png"
    bpy.ops.render.render(write_still=True)
