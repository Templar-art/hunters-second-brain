import bpy, numpy as np
sc=bpy.context.scene; clip=bpy.data.movieclips[0]; tr=clip.tracking
print("objs",[ (o.name,o.type) for o in bpy.data.objects])
cam=sc.camera; print("cam",cam.name,[c.type for c in cam.constraints], cam.data.lens, cam.data.sensor_width)
P=[]
for f in (1,12,23,34,46):
    sc.frame_set(f); m=cam.matrix_world; P.append(np.array(m.translation)); print(f, [round(x,3) for x in m.translation], [round(x,2) for x in m.to_euler()])
print("travel", np.linalg.norm(P[-1]-P[0]))
B=np.array([t.bundle for t in tr.tracks if t.has_bundle]); print("bundles",len(B)); print("min",B.min(0).round(2),"max",B.max(0).round(2),"median",np.median(B,0).round(2))
sc.frame_set(1); c=np.array(cam.matrix_world.translation); d=np.linalg.norm(B-c,axis=1); print("dist from cam min/med/max",d.min().round(2),np.median(d).round(2),d.max().round(2))
# fit plane to bundles
cen=B.mean(0); u,s,vt=np.linalg.svd(B-cen); n=vt[2]; print("plane normal",n.round(3),"sv",s.round(2)); print("cam height above plane", abs(np.dot(c-cen,n)).round(3))
