# Beach house: the deck slab sat over the pool. Replace it with deck pieces around the pool cut-out.
import bpy, bmesh
O=bpy.data.objects; col=bpy.context.scene.collection
d=O["Deck"]; m=d.data.materials[0]; O.remove(d,do_unlink=True)
def box(n,c,dim):
    bm=bmesh.new(); bmesh.ops.create_cube(bm,size=1); bmesh.ops.scale(bm,vec=dim,verts=bm.verts)
    me=bpy.data.meshes.new(n); bm.to_mesh(me); bm.free(); me.materials.append(m); o=O.new(n,me); o.location=c; col.objects.link(o)
# pool shell x -8.2..4.2, y -8.2..-3.8
box("Deck_Back",(0,-1.9,0.12),(22,3.8,0.24))
box("Deck_East",(7.6,-6,0.12),(6.8,4.4,0.24))
box("Deck_West",(-9.6,-6,0.12),(2.8,4.4,0.24))
bpy.ops.wm.save_mainfile(); print("DECK FIXED")
