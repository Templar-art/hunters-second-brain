import bpy, numpy as np
clip=bpy.data.movieclips[0]; tr=clip.tracking; rec=tr.objects.active.reconstruction
cams=rec.cameras; print("ncams",len(cams), "err", rec.average_error)
for c in cams:
    m=c.matrix; 
    if c.frame in (1,2,10,20,30,40,44,45,46): print(c.frame, [round(x,3) for x in m.translation], [round(x,4) for x in m.to_euler()], round(c.average_error,3))
B=np.array([t.bundle for t in tr.tracks if t.has_bundle]); d=np.linalg.norm(B,axis=1); print("bundle dist pct", np.percentile(d,[5,25,50,75,95]).round(1))
cam=bpy.context.scene.camera; print(cam.constraints[0].use_active_clip, cam.matrix_basis.translation)
