import bpy, sys
a = sys.argv[sys.argv.index("--") + 1:]
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.eevee.taa_render_samples = 8
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1280, 720, 100
sc.render.image_settings.file_format = "JPEG"
sc.frame_start, sc.frame_end = int(a[1]), int(a[2])
sc.render.filepath = a[0]
bpy.ops.render.render(animation=True)
