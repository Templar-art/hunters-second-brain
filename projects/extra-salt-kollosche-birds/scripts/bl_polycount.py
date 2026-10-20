import bpy
dg=bpy.context.evaluated_depsgraph_get(); t=0
for o in bpy.data.objects:
    if o.type=='MESH': t+=len(o.evaluated_get(dg).data.polygons)
print("POLYS", t, "per gull", t//4)
