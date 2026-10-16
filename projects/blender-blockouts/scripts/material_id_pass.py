import bpy
s=bpy.context.scene
# category -> flat colour (sRGB-ish, Standard view so colours stay exact)
CAT={
 "timber":(1,0,0),        # red
 "glass":(0,1,1),         # cyan
 "concrete":(0.6,0.6,0.6),# mid grey
 "render":(1,1,1),        # white
 "metal":(0,0,0.0),       # black
 "water":(0,0.2,1),       # blue (pool)
 "ocean":(0,0,0.45),      # navy
 "surf":(0.85,0.85,1),    # pale lilac
 "sand":(1,0.85,0),       # yellow
 "wetsand":(0.6,0.45,0),  # ochre
 "grass":(0,0.8,0),       # green
 "plant":(0,0.35,0),      # dark green
 "trunk":(0.45,0.2,0.05), # brown
 "fabric":(1,0,1),        # magenta
 "stone":(1,0.5,0),       # orange
 "road":(0.25,0.25,0.25), # dark grey
 "neighbour":(0.8,0.7,1), # lavender
 "person":(1,0.6,0.75),   # pink = a real person goes here
 "hedge":(0.0,0.5,0.25),  # teal-green clipped hedge
 "screen":(0.05,0.05,0.05),
}
def cat(o,m):
    n=((m.name if m else "")+" "+o.name).lower()
    for k,c in (("mannequin","person"),("person_","person"),("hedge","hedge"),("tvblack","screen"),("boucle","fabric"),("linen","fabric"),("wool","fabric"),("oak","timber"),("porcelain","stone"),("stonetile","stone"),("pool_water","water"),("poolwater","water"),("ocean","ocean"),("surf","surf"),("wetsand","wetsand"),("sand","sand"),("beach","sand"),
                ("glass","glass"),("timber","timber"),("deck","timber"),("batten","timber"),("garage","timber"),("wood_floor","timber"),("path","timber"),
                ("bronze","metal"),("post","metal"),("fascia","metal"),("carpaint","metal"),
                ("concrete","concrete"),("slab","concrete"),("roof","concrete"),("pool_","concrete"),
                ("render","render"),("wall","render"),("ceiling","render"),("neighbour","neighbour"),
                ("grass","grass"),("lawn","grass"),("dunegrass","grass"),("leaf","plant"),("leaves","plant"),("palmleaf","plant"),
                ("trunk","trunk"),("bark","trunk"),("street","road"),("marble","stone"),("coping","stone"),("island","stone"),
                ("fabric","fabric"),("sofa","fabric"),("rug","fabric"),("lounger","fabric"),("chair","fabric"),("table","stone"),("lamp","metal")):
        if k in n: return c
    return None
mats={}
def idmat(c):
    if c in mats: return mats[c]
    m=bpy.data.materials.new("ID_"+c); m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
    e=nt.nodes.new("ShaderNodeEmission"); e.inputs[0].default_value=(*CAT[c],1); e.inputs[1].default_value=1
    o=nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0],o.inputs[0]); mats[c]=m; return m
unknown=set()
for o in s.objects:
    if o.type!='MESH': continue
    slots=o.material_slots
    if not slots: unknown.add(o.name); continue
    for sl in slots:
        c=cat(o,sl.material) or cat(o,None)
        if c is None: unknown.add(o.name+":"+(sl.material.name if sl.material else "-")); c="render"
        sl.link='OBJECT'; sl.material=idmat(c)
# Poly Haven trees: leaves/bark by material name already handled via original names lost after OBJECT link? handled above before swap
w=bpy.data.worlds.new("ID_Sky"); w.use_nodes=True; bg=next(n for n in w.node_tree.nodes if n.type=="BACKGROUND"); bg.inputs[0].default_value=(0.55,0.8,1,1); s.world=w
for o in s.objects:
    if o.type=='LIGHT': o.hide_render=True
s.view_settings.view_transform='Standard'; s.view_settings.look='None'
s.render.resolution_percentage=100; s.eevee.taa_render_samples=1; s.render.filter_size=0.0
s.render.image_settings.file_format='PNG'
print("UNKNOWN",sorted(unknown)[:30])
for o in s.objects:
    if any(k in o.name for k in ("Fence","Balustrade")): o.hide_render=True
