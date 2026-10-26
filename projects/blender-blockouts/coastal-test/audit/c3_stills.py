import bpy, math, sys
out = sys.argv[sys.argv.index("--") + 1]
sc = bpy.context.scene
for m in list(sc.timeline_markers):
    sc.timeline_markers.remove(m)
src = bpy.data.objects["C2_RiseReveal"].data
cd = src.copy(); cd.lens = 28.0
cam = bpy.data.objects.new("C3_tmp", cd); sc.collection.objects.link(cam)
sc.camera = cam
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1920, 1080, 100
sc.render.image_settings.file_format = "PNG"
for tag, loc, pitch in [("start", (1.5, -32, 2.5), 2), ("end", (1.5, -22, 7), -12)]:
    cam.location = loc
    cam.rotation_euler = (math.radians(90 + pitch), 0, math.radians(180 + 184))
    sc.render.filepath = f"{out}/c3-{tag}.png"
    bpy.ops.render.render(write_still=True)
