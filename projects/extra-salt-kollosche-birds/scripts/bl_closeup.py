import bpy, math
from mathutils import Vector
sc=bpy.context.scene; sc.render.use_motion_blur=False; sc.frame_set(30)
r=bpy.data.objects["Gull_hero"]; p=r.matrix_world.translation
cd=bpy.data.cameras.new("c"); cd.lens=50; c=bpy.data.objects.new("c",cd); sc.collection.objects.link(c)
c.location=p+Vector((0.0,-1.6,1.2)); d=p-c.location; c.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); sc.camera=c
sc.render.film_transparent=False; sc.render.resolution_x=800; sc.render.resolution_y=500
sc.render.filepath="//render/closeup.png"; bpy.ops.render.render(write_still=True)
