import bpy, math
from mathutils import Vector
sc=bpy.context.scene; sc.render.use_motion_blur=False
cd=bpy.data.cameras.new("c"); cd.lens=50; c=bpy.data.objects.new("c",cd); sc.collection.objects.link(c); sc.camera=c
sc.render.film_transparent=False; sc.render.resolution_x=400; sc.render.resolution_y=300
r=bpy.data.objects["Gull_hero"]
for f in range(1,10):
    sc.frame_set(f); p=r.matrix_world.translation; fw=r.matrix_world.to_3x3()@Vector((0,1,0)); side=fw.cross(Vector((0,0,1))).normalized()
    c.location=p+side*2.0+Vector((0,0,0.9)); c.rotation_euler=(p-c.location).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=f"//render/beat_{f:02d}.png"; bpy.ops.render.render(write_still=True)
