# Usage: blender -b file.blend -P rekey_camera.py -- CAMERA "x,y,z;tx,ty,tz" "x,y,z;tx,ty,tz"
# Re-keys a shot camera (and its Tgt_ empty) between start and end of its 192-frame slot, then saves.
import bpy, sys
a=sys.argv[sys.argv.index("--")+1:]; name=a[0]; L=192
sc=bpy.context.scene; cam=bpy.data.objects[name]; t=bpy.data.objects["Tgt_"+name]
f0=next(m.frame for m in sc.timeline_markers if m.name==name)
cam.animation_data_clear(); t.animation_data_clear()
for u,spec in zip((0,1),a[1:3]):
    c,tg=[tuple(map(float,p.split(","))) for p in spec.split(";")]
    fr=round(f0+u*(L-1)); cam.location=c; t.location=tg
    cam.keyframe_insert("location",frame=fr); t.keyframe_insert("location",frame=fr)
bpy.ops.wm.save_mainfile(); print("REKEYED",name)
